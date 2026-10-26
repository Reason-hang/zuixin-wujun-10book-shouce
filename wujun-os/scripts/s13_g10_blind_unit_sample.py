#!/usr/bin/env python3
"""G10②：盲抽已排除/非内容单元（不看原处置重读）— 确定性样本表。"""
from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/覆盖与质检报告/G10②_盲抽单元表_草稿.md"
SEED = 20261026
PER_BOOK = 2  # 草稿子集；全量 P6 可加大


def unit_body_text(raw: str) -> str:
    import re

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        raw = parts[2] if len(parts) >= 3 else raw
    lines: list[str] = []
    for ln in raw.splitlines():
        s = ln.strip()
        if not s or ln.startswith("#") or ln.startswith(">") or s == "---":
            continue
        lines.append(s)
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def unit_excerpt(uid: str, book: str, limit: int = 100) -> str:
    import re

    m = re.match(r"^[A-Z0-9]+-U(\d+)$", uid)
    if not m:
        return ""
    p = ROOT / "data/units" / book / f"unit_{int(m.group(1)):04d}.md"
    if not p.is_file():
        return ""
    text = unit_body_text(p.read_text(encoding="utf-8"))
    return text[:limit] + ("…" if len(text) > limit else "")


def unit_title(uid: str, book: str) -> str:
    import re

    m = re.match(r"^[A-Z0-9]+-U(\d+)$", uid)
    if not m:
        return ""
    p = ROOT / "data/units" / book / f"unit_{int(m.group(1)):04d}.md"
    if not p.is_file():
        return ""
    raw = p.read_text(encoding="utf-8")
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        raw = parts[2] if len(parts) >= 3 else raw
    for ln in raw.splitlines():
        if ln.startswith("## "):
            return ln[3:].strip()[:60]
    return ""


def main() -> None:
    by_book: dict[str, list[dict]] = {}
    for p in sorted((ROOT / "data/unitcards").glob("uc_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            u = json.loads(line)
            disp = u.get("disposal", "")
            typ = u.get("type", "")
            if disp not in ("X", "N") and typ not in ("N", "S"):
                continue
            bc = u.get("book_code", "")
            uid = u["unit_id"]
            by_book.setdefault(bc, []).append(
                {
                    "unit_id": uid,
                    "disposal": disp,
                    "type": typ,
                    "title": unit_title(uid, bc),
                    "lines": f"L{u.get('start_line','')}-{u.get('end_line','')}",
                }
            )
    rng = random.Random(SEED)
    lines = [
        "# G10② 盲抽单元表（草稿 · 子集）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；每书 {PER_BOOK} 个 X/N/S 单元；种子 {SEED}。\n",
        "> 审查员**不看**台账处置，重读单元正文后填：是否漏收核心论点。\n\n",
        "| 书 | 单元 ID | 登记处置 | 类型 | 行号 | 标题 | 摘录（审阅用·前 100 字） | 漏收核心论点？ |\n",
        "|---|---|---|---|---|---|---|---|\n",
    ]
    n = 0
    for bc in sorted(by_book.keys()):
        items = by_book[bc]
        rng.shuffle(items)
        for row in items[:PER_BOOK]:
            n += 1
            ex = unit_excerpt(row["unit_id"], bc).replace("|", "｜")
            lines.append(
                f"| {bc} | {row['unit_id']} | {row['disposal']} | {row['type']} | {row['lines']} | {row['title']} | {ex} | |\n"
            )
    text = "".join(lines)
    if "book_code:" in text or "char_count:" in text:
        raise SystemExit("G10 excerpt regression: YAML leaked into table")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"rows={n} out={OUT}")


if __name__ == "__main__":
    main()
