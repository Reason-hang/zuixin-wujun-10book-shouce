#!/usr/bin/env python3
"""从 D1 草稿核心卡同步四张能力速查表（AC-5.6）。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "out/D1_手册草稿"
TITLE_RE = re.compile(r"^#### (M-D\d{2}-\d{2})\s+(.+?)\s+[［\[]核心卡[］\]]", re.M)
TAG_RE = re.compile(r"能力标签：(.+?)(?:\||\｜)")
CH_RE = re.compile(r"所属：D(\d{2})")


def collect() -> list[tuple[str, str, str, set[str]]]:
    rows: list[tuple[str, str, str, set[str]]] = []
    for md in sorted(DRAFT.glob("[0-9][0-9]_*.md")):
        text = md.read_text(encoding="utf-8")
        for m in TITLE_RE.finditer(text):
            cid, title = m.group(1), m.group(2).strip()
            start = m.start()
            block = text[start : start + 1200]
            tm = TAG_RE.search(block)
            raw = tm.group(1) if tm else "思"
            tags = {k for k in ("思", "做", "沟", "学") if k in raw}
            if not tags:
                tags = {"思"}
            cm = CH_RE.search(block)
            ch = f"D{cm.group(1)}" if cm else md.name[3:6]
            rows.append((cid, title[:24], ch, tags))
    return sorted(rows, key=lambda r: r[0])


def render_table(rows: list[tuple[str, str, str]]) -> str:
    lines = ["| 模型 | 标题 | 章 |\n", "|---|---|---|\n"]
    for cid, title, ch in rows:
        lines.append(f"| {cid} | {title} | {ch} |\n")
    return "".join(lines)


def main() -> None:
    all_rows = collect()
    by_ability: dict[str, list[tuple[str, str, str]]] = {k: [] for k in ("思", "做", "沟", "学")}
    for cid, title, ch, tags in all_rows:
        for t in tags:
            by_ability[t].append((cid, title, ch))
    headers = {
        "思": "# 能力速查表：思\n\n> 由 `s17_sync_ability_tables.py` 同步；AC-5.6。\n\n",
        "做": "# 能力速查表：做\n\n> 由 `s17_sync_ability_tables.py` 同步；工具见 `out/D2_行动工具集_草稿.md`。\n\n",
        "沟": "# 能力速查表：沟\n\n> 由 `s17_sync_ability_tables.py` 同步。\n\n",
        "学": "# 能力速查表：学\n\n> 由 `s17_sync_ability_tables.py` 同步。\n\n",
    }
    for key, path in [
        ("思", DRAFT / "能力速查_思.md"),
        ("做", DRAFT / "能力速查_做.md"),
        ("沟", DRAFT / "能力速查_沟.md"),
        ("学", DRAFT / "能力速查_学.md"),
    ]:
        body = headers[key] + render_table(by_ability[key])
        if key == "沟":
            body += "\n| 工具 | 说明 | 章 |\n|---|---|---|\n| T-D07-01 | 复述确认四步 | D07 |\n| T-D06-02 | 三句话周一报 | D06 |\n"
        if key == "做":
            body += "\n| 工具 | 说明 | 章 |\n|---|---|---|\n| T-D05-01 | 决策记录三条 | D05 |\n| T-D06-01 | 伪工作自检 | D06 |\n"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path.name} rows={len(by_ability[key])}")


if __name__ == "__main__":
    main()
