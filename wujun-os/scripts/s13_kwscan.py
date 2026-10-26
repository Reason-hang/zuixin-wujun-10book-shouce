#!/usr/bin/env python3
"""S13 / G10①：概念关键词全文反查，登记段落去向（v2 §6.1 G10）。

用法:
  python3 scripts/s13_kwscan.py --src src_frozen --watchlist data/concept_watchlist.csv --out logs/g10_kw.md
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from bisect import bisect_right
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 与 s01_probe.BOOKS 一致（文件名子串匹配）
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


def book_paths(src: Path) -> dict[str, Path]:
    files = list(src.glob("*.md"))
    out: dict[str, Path] = {}
    for key, code in BOOKS:
        for f in files:
            if key in f.name:
                out[code] = f
                break
    return out


def load_units() -> dict[str, list[tuple[int, int, str, str]]]:
    """book -> sorted (start, end, unit_id, disposal)."""
    by_book: dict[str, list[tuple[int, int, str, str]]] = defaultdict(list)
    disp: dict[str, str] = {}
    for p in (ROOT / "data/unitcards").glob("uc_*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            u = json.loads(line)
            disp[u["unit_id"]] = u.get("disposal") or ""
    with (ROOT / "data/units/units_index.csv").open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            by_book[row["book_code"]].append(
                (
                    int(row["start_line"]),
                    int(row["end_line"]),
                    row["unit_id"],
                    disp.get(row["unit_id"], ""),
                )
            )
    for code in by_book:
        by_book[code].sort(key=lambda x: x[0])
    return by_book


def load_anchors() -> dict[str, list[tuple[int, int, str, str]]]:
    """book -> (start, end, claim_id, unit_id)."""
    by_book: dict[str, list[tuple[int, int, str, str]]] = defaultdict(list)
    for p in (ROOT / "data/cards").rglob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for c in d.get("cards", []):
            a = c.get("anchor") or {}
            bc = a.get("book_code")
            if not bc:
                continue
            by_book[bc].append(
                (
                    int(a.get("start_line", 0)),
                    int(a.get("end_line", 0)),
                    c.get("claim_id", ""),
                    c.get("unit_id", d.get("unit_id", "")),
                )
            )
    for code in by_book:
        by_book[code].sort(key=lambda x: x[0])
    return by_book


def unit_at(
    intervals: list[tuple[int, int, str, str]], line: int
) -> tuple[str, str] | None:
    starts = [x[0] for x in intervals]
    i = bisect_right(starts, line) - 1
    if i < 0:
        return None
    s, e, uid, disp = intervals[i]
    if s <= line <= e:
        return uid, disp
    return None


def claim_at(
    anchors: list[tuple[int, int, str, str]], line: int
) -> str | None:
    for s, e, cid, _ in anchors:
        if s <= line <= e:
            return cid
    return None


def paragraphs(lines: list[str]) -> list[tuple[int, str]]:
    """(start_line_1based, text)."""
    out: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 1
    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            if buf:
                out.append((start, "\n".join(buf)))
                buf = []
            continue
        if not buf:
            start = i
        buf.append(line)
    if buf:
        out.append((start, "\n".join(buf)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="src_frozen")
    ap.add_argument("--watchlist", default="data/concept_watchlist.csv")
    ap.add_argument("--out", default="logs/g10_kw.md")
    ap.add_argument("--strict", action="store_true", help="无去向段落则退出码 1")
    ap.add_argument("--min-para-len", type=int, default=20, help="忽略过短段落（字）")
    args = ap.parse_args()
    src = ROOT / args.src
    keywords: list[str] = []
    with (ROOT / args.watchlist).open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kw = (row.get("keyword") or "").strip()
            if kw:
                keywords.append(kw)

    paths = book_paths(src)
    units = load_units()
    anchors = load_anchors()
    hits = 0
    resolved = 0
    unresolved: list[str] = []
    by_kw: dict[str, int] = defaultdict(int)

    for code, path in sorted(paths.items()):
        lines = path.read_text(encoding="utf-8").splitlines()
        iv = units.get(code, [])
        av = anchors.get(code, [])
        for start_line, para in paragraphs(lines):
            if len(re.sub(r"\s+", "", para)) < args.min_para_len:
                continue
            for kw in keywords:
                if kw not in para:
                    continue
                hits += 1
                by_kw[kw] += 1
                uid_disp = unit_at(iv, start_line)
                dest = ""
                if uid_disp:
                    uid, disp = uid_disp
                    dest = f"unit={uid} disposal={disp or '?'}"
                    cid = claim_at(av, start_line)
                    if cid:
                        dest += f" claim={cid}"
                    elif disp in ("K", "C", "M"):
                        dest += " (K层无行级锚点)"
                    resolved += 1
                else:
                    unresolved.append(
                        f"{code} L{start_line} 「{kw}」 {para[:40].replace(chr(10), ' ')}…"
                    )

    lines_out = [
        "# G10① 关键词反查（S13）\n",
        f"\n生成: {datetime.now().isoformat(timespec='seconds')}\n",
        f"词表: `{args.watchlist}`（{len(keywords)} 词）\n",
        f"书目: {len(paths)}/10\n\n",
        "## 汇总\n\n",
        f"| 指标 | 值 |\n|---|---|\n",
        f"| 段落命中次数 | {hits} |\n",
        f"| 已登记去向 | {resolved} |\n",
        f"| 无单元映射 | {len(unresolved)} |\n",
        f"| 去向率 | {resolved / hits * 100:.1f}% |\n" if hits else "| 去向率 | — |\n",
        "\n## 分词命中（次数）\n\n",
    ]
    for kw in keywords:
        if by_kw[kw]:
            lines_out.append(f"- {kw}: {by_kw[kw]}\n")

    if unresolved:
        lines_out.append("\n## 无单元映射样例（前 40）\n\n")
        for u in unresolved[:40]:
            lines_out.append(f"- {u}\n")

    verdict = "PASS" if not unresolved else f"WARN（{len(unresolved)} 段无单元）"
    if args.strict and unresolved:
        verdict = "FAIL"
    lines_out.append(f"\n**结论**: {verdict}\n")

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(lines_out), encoding="utf-8")
    print(f"hits={hits} unresolved={len(unresolved)} out={out_path}")
    if args.strict and unresolved:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
