#!/usr/bin/env python3
"""AC-3.6：成书每本 15 条、来信每本 10 条 K 卡抽检表（确定性抽样，待回读填列）。"""
from __future__ import annotations

import json
import random
import re
from datetime import datetime
from pathlib import Path

CID_RE = re.compile(r"^C-[A-Z0-9]+-U\d+-\d+$")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"

LETTER = ("SG1", "WJ2", "SG3")
BOOK = ("GG", "JS", "SX", "GJ", "JJ", "FZ", "TD")
N_LETTER = 10
N_BOOK = 15
SEED = 20261026

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


def book_file(code: str) -> str:
    for key, bc in BOOKS:
        if bc == code:
            for p in (ROOT / "src_frozen").glob("*.md"):
                if key in p.name:
                    return p.name
    return ""


def load_pool() -> dict[str, list[dict]]:
    pool: dict[str, list[dict]] = {c: [] for c in LETTER + BOOK}
    seen: set[str] = set()
    for p in (ROOT / "data/cards").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        bc = d.get("book_code", "")
        if bc not in pool:
            continue
        for c in d.get("cards", []):
            a = c.get("anchor") or {}
            if c.get("disposal") == "X":
                continue
            cid = c.get("claim_id", "")
            if not cid or cid in seen or not CID_RE.fullmatch(cid):
                continue
            seen.add(cid)
            pool[bc].append(
                {
                    "claim_id": cid,
                    "unit_id": c.get("unit_id", d.get("unit_id", "")),
                    "text": (c.get("claim_text") or "")[:80],
                    "lines": f"{a.get('start_line', '')}–{a.get('end_line', '')}",
                }
            )
    return pool


def main() -> None:
    pool = load_pool()
    rng = random.Random(SEED)
    lines = [
        "# AC-3.6 抽检召回表（草稿）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；种子 {SEED}。\n",
        "> **未回读前不得标 PASS**；有漏须补抽补写直至样本 100%。\n\n",
    ]
    total = 0
    for code in LETTER + BOOK:
        n = N_LETTER if code in LETTER else N_BOOK
        items = pool.get(code, [])
        rng.shuffle(items)
        pick = items[:n]
        if len(pick) < n:
            lines.append(f"\n## {code} ⚠️ 仅 {len(pick)}/{n} 张可抽\n\n")
        else:
            lines.append(f"\n## {code}（{n} 条）\n\n")
        lines.append("| # | 卡 ID | 单元 | 行号 | 转述摘录 | 回读召回 |\n")
        lines.append("|---|---|---|---|---|---|\n")
        for i, row in enumerate(pick, 1):
            total += 1
            lines.append(
                f"| {i} | {row['claim_id']} | {row['unit_id']} | {row['lines']} | {row['text']} | |\n"
            )
        fn = book_file(code)
        if fn:
            lines.append(f"\n文件: `{fn}`\n")
    lines.append(f"\n**合计样本**: {total}（目标 {len(LETTER)*N_LETTER + len(BOOK)*N_BOOK}）\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"rows={total} out={OUT}")


if __name__ == "__main__":
    main()
