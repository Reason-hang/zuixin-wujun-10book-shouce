#!/usr/bin/env python3
"""P6 步 2：十书 K 卡 ↔ 单元 ↔ 手册锚点引用 粗矩阵（可复算草稿）。"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/覆盖与质检报告/P6_核心论点覆盖矩阵_草稿.md"
BOOK_ORDER = ("SG1", "WJ2", "SG3", "GG", "JS", "SX", "GJ", "JJ", "FZ", "TD")


def cards_per_book() -> tuple[Counter[str], set[str]]:
    c: Counter[str] = Counter()
    units_with: set[str] = set()
    for p in (ROOT / "data/cards").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        bc = d.get("book_code") or p.name.split("-")[0]
        n = len(d.get("cards", []))
        if n:
            c[bc] += n
            units_with.add(d.get("unit_id", ""))
    return c, units_with


def content_units() -> Counter[str]:
    c: Counter[str] = Counter()
    with (ROOT / "data/units/units_index.csv").open(encoding="utf-8") as fp:
        for row in csv.DictReader(fp):
            if row["type"] == "C":
                c[row["book_code"]] += 1
    return c


def manual_anchor_refs() -> Counter[str]:
    merge = ROOT / "out/D1_手册草稿/D1_主手册合并稿_v1.md"
    if not merge.is_file():
        return Counter()
    text = merge.read_text(encoding="utf-8")
    c: Counter[str] = Counter()
    for m in re.finditer(r"C-([A-Z0-9]+)-U", text):
        c[m.group(1)] += 1
    return c


def book_coverage_verdict(code: str) -> str:
    p = ROOT / f"out/覆盖与质检报告/book_coverage_{code}.md"
    if not p.is_file():
        return "缺报告"
    t = p.read_text(encoding="utf-8")
    if "结论: PASS" in t or "→ PASS" in t:
        return "PASS"
    if "FAIL" in t:
        return "FAIL"
    return "?"


def main() -> None:
    cards, units_with_cards = cards_per_book()
    content = content_units()
    hb = manual_anchor_refs()
    lines = [
        "# P6 核心论点覆盖矩阵（草稿）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`scripts/s16_p6_coverage_matrix.py`\n",
        "> **粗矩阵**：K 卡计数 + 书级处置 PASS + 手册 `C-书码-` 引用次数；**非** AC-3.6 抽检召回证明。\n\n",
        "| 书码 | 内容单元 C | K 卡数 | 卡/内容单元 | 书级处置 | 手册锚点引用次 |\n",
        "|---|---:|---:|---:|---|---:|\n",
    ]
    for code in BOOK_ORDER:
        cu = content.get(code, 0)
        k = cards.get(code, 0)
        ratio = f"{k / cu:.2f}" if cu else "—"
        lines.append(
            f"| {code} | {cu} | {k} | {ratio} | {book_coverage_verdict(code)} | {hb.get(code, 0)} |\n"
        )
    total_k = sum(cards.values())
    lines.append(f"\n**合计 K 卡**: {total_k}（`verify_cards` 应为 9019）\n")
    lines.append(
        "\n## 说明\n\n"
        "- 双向语义矩阵（单元↔划重点↔M 卡）仍待 P6 全量与抽检；SG3 划重点见 `g10_sg3_highlight_recall.md`。\n"
        "- 再生：`python3 scripts/s16_p6_coverage_matrix.py`\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT} k_total={total_k}")


if __name__ == "__main__":
    main()
