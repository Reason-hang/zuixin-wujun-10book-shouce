#!/usr/bin/env python3
"""从 logs/g7.md 导出 X1 运营类排除清单（D3 子表草稿）。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G7 = ROOT / "logs/g7.md"
OUT = ROOT / "ledger/X排除清单_草稿.md"


def main() -> None:
    text = G7.read_text(encoding="utf-8")
    block = text.split("## 2. X1 运营类单元清单", 1)
    if len(block) < 2:
        raise SystemExit("g7.md section 2 not found")
    section = block[1].split("## 3.", 1)[0]
    rows: list[str] = []
    uid_re = re.compile(r"^[A-Z0-9]+-U\d+$")
    for ln in section.splitlines():
        if not ln.strip().startswith("|") or ln.startswith("| 单元"):
            continue
        if re.match(r"^\|[-:\s|]+\|$", ln.strip()):
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 3:
            continue
        uid, sub = parts[0], parts[1]
        if not uid_re.match(uid):
            continue
        rows.append(
            f"| {uid} | {sub} | 专栏运营内容，保留原文不抽取 | 否 | 待 P6 抽检 |"
        )
    body = (
        "# X 排除清单（草稿 · D3 子表）\n\n"
        "> `scripts/s12_export_x_exclusion.py`；来源 `logs/g7.md` §2。\n\n"
        "| 单元 ID | 子类 | 理由 | 可迁移方法论 | 抽样复核 |\n"
        "|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    OUT.write_text(body, encoding="utf-8")
    print(f"rows={len(rows)} out={OUT}")


if __name__ == "__main__":
    main()
