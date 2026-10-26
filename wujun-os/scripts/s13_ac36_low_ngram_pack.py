#!/usr/bin/env python3
"""AC-3.6：导出 ngram 低于阈值的卡 — 转述 vs 锚点段对照包（供人工/Agent 深读）。"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEUR = ROOT / "logs/ac36_semantic_heuristic_latest.md"
OUT = ROOT / "logs/ac36_low_ngram_review_pack_20261026.md"
THRESH_LINE = "待人工"
BOOKS = [
    ("来信1", "SG1"),
    ("吴军来信2", "WJ2"),
    ("硅谷来信3", "SG3"),
    ("谷歌方法论", "GG"),
    ("见识", "JS"),
    ("数学通识", "SX"),
    ("格局", "GJ"),
    ("境界", "JJ"),
    ("富足", "FZ"),
    ("态度", "TD"),
]
CJK = re.compile(r"[\u4e00-\u9fff]")


def book_files() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted((ROOT / "src_frozen").glob("*.md")):
        for key, code in BOOKS:
            if key in p.name:
                out[code] = p.read_text(encoding="utf-8")
                break
    return out


def line_span(text: str, ls: int, le: int) -> str:
    lines = text.split("\n")
    starts = []
    pos = 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    cs = starts[ls - 1]
    ce = starts[le - 1] + len(lines[le - 1])
    return text[cs:ce]


def load_cards() -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    for p in (ROOT / "data/cards").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            cid = c.get("claim_id")
            if cid:
                by_id[cid] = c
    return by_id


def main() -> None:
    flag_ids: list[str] = []
    rates: dict[str, str] = {}
    for ln in HEUR.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("| C-") or THRESH_LINE not in ln:
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) >= 3:
            flag_ids.append(parts[0])
            rates[parts[0]] = parts[1]
    books = book_files()
    cards = load_cards()
    lines = [
        "# AC-3.6 低 ngram 对照包（24 条 · 优先人工回读）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
    ]
    for i, cid in enumerate(flag_ids, 1):
        c = cards.get(cid, {})
        claim = c.get("claim_text", "（无卡）")
        a = c.get("anchor") or {}
        bc = a.get("book_code") or re.match(r"^C-([A-Z0-9]+)-U", cid).group(1)
        ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
        seg = ""
        try:
            seg = line_span(books.get(bc, ""), ls, le)
        except (ValueError, IndexError, AttributeError):
            seg = "（锚点读取失败）"
        seg_short = "".join(CJK.findall(seg))[:280]
        lines.append(f"## {i}. `{cid}`（ngram {rates.get(cid, '?')}）\n\n")
        lines.append(f"- 行号: L{ls}–L{le}\n")
        lines.append(f"- **转述**: {claim}\n")
        lines.append(f"- **锚点摘录**: {seg_short}{'…' if len(''.join(CJK.findall(seg))) > 280 else ''}\n")
        lines.append("- **Agent 草稿判定**: \n")
        lines.append("- **你确认（Y/N/改卡）**: \n\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"n={len(flag_ids)} out={OUT}")


if __name__ == "__main__":
    main()
