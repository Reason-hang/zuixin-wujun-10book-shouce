#!/usr/bin/env python3
"""Count outcomes in 必检议题覆盖表 for AC-5.8 progress."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--table",
        default="out/D1_手册草稿/必检议题覆盖表_骨架.md",
    )
    p.add_argument("--out", default="logs/s17_coverage_stats_latest.md")
    args = p.parse_args()
    text = Path(args.table).read_text(encoding="utf-8")
    outcomes = Counter()
    rows = 0
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("| #"):
            continue
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 7 or not parts[1].isdigit():
            continue
        rows += 1
        oc = parts[5]
        outcomes[oc] += 1
    pending = outcomes.get("待P5", 0)
    resolved = rows - pending
    report = [
        "# 必检议题覆盖统计\n\n",
        f"- 总行数: **{rows}**\n",
        f"- 已填结局: **{resolved}**\n",
        f"- 待P5: **{pending}**\n\n",
        "| 结局 | 数量 |\n|---|---:|\n",
    ]
    for k, v in sorted(outcomes.items(), key=lambda x: -x[1]):
        report.append(f"| {k} | {v} |\n")
    Path(args.out).write_text("".join(report), encoding="utf-8")
    print(f"rows={rows} resolved={resolved} pending={pending} -> {args.out}")


if __name__ == "__main__":
    main()
