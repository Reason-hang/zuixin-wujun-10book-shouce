#!/usr/bin/env python3
"""P6 步 11：生成用户 20 张抽查表（v2 §16.10），确定性抽样。"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/覆盖与质检报告/P6_用户抽查20张_草稿.md"

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


def book_files() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted((ROOT / "src_frozen").glob("*.md")):
        for key, code in BOOKS:
            if key in p.name:
                out[code] = p.name
                break
    return out


def claim_text_60(s: str) -> str:
    s = re.sub(r"\s+", "", s)
    return (s[:60] + "…") if len(s) > 60 else s


def main() -> None:
    books = book_files()
    pool: list[dict] = []
    for path in sorted((ROOT / "data/cards").rglob("*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            a = c.get("anchor") or {}
            bc = a.get("book_code")
            ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
            cid = c.get("claim_id", "")
            if not cid or not bc or bc not in books or ls <= 0:
                continue
            pool.append(
                {
                    "claim_id": cid,
                    "book": books[bc],
                    "lines": f"{ls}–{le}",
                    "text": claim_text_60(c.get("claim_text", "")),
                    "book_code": bc,
                }
            )
    rng = random.Random(20261026)
    by_book: dict[str, list[dict]] = {}
    for item in pool:
        by_book.setdefault(item["book_code"], []).append(item)
    for items in by_book.values():
        rng.shuffle(items)
    picked: list[dict] = []
    codes = sorted(by_book.keys())
    idx = 0
    while len(picked) < 20 and codes:
        code = codes[idx % len(codes)]
        if by_book[code]:
            picked.append(by_book[code].pop())
        else:
            codes.remove(code)
            if not codes:
                break
            idx -= 1
        idx += 1
    if len(picked) < 20:
        rest = [x for items in by_book.values() for x in items]
        rng.shuffle(rest)
        picked.extend(rest[: 20 - len(picked)])

    lines = [
        "# P6 用户抽查 20 张（草稿）\n\n",
        "> `scripts/s12_export_p6_spotcheck_v20.py`；种子 **20261026**；**「你的判断」列由用户填写**。\n\n",
        "| V 编号 | 卡 ID | 书与文件 | 行号 | 转述（≤60字） | 你的判断 |\n",
        "|---|---|---|---|---|---|\n",
    ]
    for i, row in enumerate(picked[:20], 1):
        lines.append(
            f"| V-{i:02d} | {row['claim_id']} | {row['book']} | {row['lines']} | {row['text']} | |\n"
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"cards={len(picked[:20])} out={OUT}")


if __name__ == "__main__":
    main()
