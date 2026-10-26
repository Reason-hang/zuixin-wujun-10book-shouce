#!/usr/bin/env python3
"""从 K 卡 JSON 导出 D3 锚点表草稿 → ledger/溯源与处置台账.md（供 anchor_tool verify）。"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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


def book_files(src: Path) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for p in sorted(src.glob("*.md")):
        name = p.name
        for key, code in BOOKS:
            if key in name:
                out[code] = (name, p.read_text(encoding="utf-8"))
                break
    return out


def line_span(text: str, ls: int, le: int) -> tuple[int, int, str]:
    lines = text.split("\n")
    if ls < 1 or le > len(lines):
        raise ValueError(f"line range {ls}-{le} out of {len(lines)}")
    starts = []
    pos = 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    cs = starts[ls - 1]
    ce = starts[le - 1] + len(lines[le - 1])
    return cs, ce, text[cs:ce]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src_frozen")
    ap.add_argument("--out", default="ledger/溯源与处置台账.md")
    ap.add_argument("--limit", type=int, default=0, help="0=全部")
    args = ap.parse_args()
    books = book_files(ROOT / args.src)
    rows: list[str] = []
    drift = 0
    n = 0
    for path in sorted(glob.glob(str(ROOT / "data/cards/**/*.json"), recursive=True)):
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            a = c.get("anchor") or {}
            bc = a.get("book_code")
            if not bc or bc not in books:
                continue
            book_name, text = books[bc]
            ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
            if ls <= 0 or le < ls:
                continue
            try:
                cs, ce, seg = line_span(text, ls, le)
            except ValueError:
                drift += 1
                continue
            sha = hashlib.sha1(seg.encode("utf-8")).hexdigest()
            card_sha = a.get("sha1", "")
            if card_sha and sha != card_sha:
                drift += 1
            fp = a.get("fingerprint") or []
            words = ",".join(fp) if isinstance(fp, list) else str(fp)
            cid = c.get("claim_id", "")
            rows.append(f"| {cid} | {book_name} | {ls} | {le} | {cs} | {ce} | {sha} | {words} |")
            n += 1
            if args.limit and n >= args.limit:
                break
        if args.limit and n >= args.limit:
            break

    header = [
        "# 溯源与处置台账（锚点表 · 自动生成草稿）\n\n",
        "> `scripts/s12_export_anchor_ledger.py`；单元/论点分表待 P6 补全。\n\n",
        "| claim_id | book | ls | le | cs | ce | sha1 | fingerprint |\n",
        "|---|---|---:|---:|---:|---:|---|---|\n",
    ]
    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(header) + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"rows={n} sha_drift={drift} out={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
