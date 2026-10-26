#!/usr/bin/env python3
"""AC-3.6 辅助：转述与锚点段 4 字 ngram 重合率（启发式，非语义判定）。"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/ac36_semantic_heuristic_latest.md"
THRESH = 0.12

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


def ngrams(s: str, n: int = 4) -> set[str]:
    t = "".join(CJK.findall(s))
    if len(t) < n:
        return {t} if t else set()
    return {t[i : i + n] for i in range(len(t) - n + 1)}


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


def main() -> int:
    ac36 = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"
    ids: list[str] = []
    if ac36.is_file():
        for ln in ac36.read_text(encoding="utf-8").splitlines():
            if not ln.startswith("|"):
                continue
            parts = [p.strip() for p in ln.strip().strip("|").split("|")]
            if len(parts) < 2 or not parts[0].isdigit():
                continue
            cid = parts[1]
            if re.fullmatch(r"C-[A-Z0-9]+-U\d+-\d+", cid):
                ids.append(cid)
    books = book_files()
    cards = load_cards()
    flag = 0
    lines = [
        "# AC-3.6 语义启发式（ngram 重合，非过关）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；阈值 {THRESH}；低于标 **待人工**。\n\n",
        "| claim_id | 重合率 | 建议 |\n|---|---:|---|\n",
    ]
    for cid in ids:
        c = cards.get(cid)
        if not c:
            lines.append(f"| {cid} | — | 无卡 |\n")
            flag += 1
            continue
        a = c.get("anchor") or {}
        bc = a.get("book_code") or re.match(r"^C-([A-Z0-9]+)-U", cid).group(1)
        text = books.get(bc, "")
        ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
        try:
            seg = line_span(text, ls, le)
        except (ValueError, IndexError, AttributeError):
            lines.append(f"| {cid} | — | 锚点失败 |\n")
            flag += 1
            continue
        g1, g2 = ngrams(c.get("claim_text", "")), ngrams(seg)
        if not g1 or not g2:
            rate = 0.0
        else:
            rate = len(g1 & g2) / len(g1)
        tag = "待人工" if rate < THRESH else "启发式OK"
        if rate < THRESH:
            flag += 1
        lines.append(f"| {cid} | {rate:.2f} | {tag} |\n")
    lines.append(f"\n**待人工/异常**: {flag} / {len(ids)}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"n={len(ids)} flag={flag} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
