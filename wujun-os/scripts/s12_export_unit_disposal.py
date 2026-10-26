#!/usr/bin/env python3
"""导出单元处置表（D3 子表，1742 行，列向 v2 §16.7 靠拢）。"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ledger/单元处置表_草稿.md"


def unit_path(uid: str, book: str) -> Path:
    m = re.match(r"^[A-Z0-9]+-U(\d+)$", uid)
    num = int(m.group(1)) if m else 0
    return ROOT / "data/units" / book / f"unit_{num:04d}.md"


def title_from_unit(p: Path) -> str:
    if not p.is_file():
        return ""
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            return ln[3:].strip().replace("|", "｜")
    return ""


def main() -> None:
    disposal: dict[str, str] = {}
    for p in sorted((ROOT / "data/unitcards").glob("uc_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            u = json.loads(line)
            disposal[u["unit_id"]] = u.get("disposal", "")

    rows: list[str] = []
    with (ROOT / "data/units/units_index.csv").open(encoding="utf-8") as fp:
        for row in csv.DictReader(fp):
            uid = row["unit_id"]
            book = row["book_code"]
            typ = row["type"]
            chars = row["char_count"]
            orig = f"L{row['start_line']}-{row['end_line']}"
            title = title_from_unit(unit_path(uid, book))
            disp = disposal.get(uid, "")
            rows.append(
                f"| {uid} | {book} | {orig} | {title} | {chars} | {typ} | | {disp} | | | |"
            )

    text = (
        "# 单元处置表（草稿 · D3 子表）\n\n"
        "> `scripts/s12_export_unit_disposal.py`；`units_index.csv` + `unitcards` + 单元标题。\n\n"
        "| 单元 ID | 书 | 原编号 | 原标题 | 汉字 | 类型 | 读法层 | 处置 | 去向 | 说话人 | 备注 |\n"
        "|---|---|---|---|---:|---|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    OUT.write_text(text, encoding="utf-8")
    print(f"rows={len(rows)} out={OUT}")


if __name__ == "__main__":
    main()
