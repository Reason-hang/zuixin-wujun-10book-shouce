#!/usr/bin/env python3
"""Export 112 must-check topics from spec/pillars.yaml to handbook coverage skeleton."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

OUT_DEFAULT = Path("out/D1_手册草稿/必检议题覆盖表_骨架.md")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--pillars", default="spec/pillars.yaml")
    p.add_argument("--out", default=str(OUT_DEFAULT))
    p.add_argument(
        "--outcome",
        default="待P5",
        help="Default outcome column when no mapping file",
    )
    args = p.parse_args()
    data = yaml.safe_load(Path(args.pillars).read_text(encoding="utf-8"))
    lines = [
        "# 必检议题覆盖表（骨架）\n",
        "> v2 §15.5.6 步 4 / AC-5.8。共 **112** 项，自 `spec/pillars.yaml` 导出。\n",
        "> 结局枚举：成卡｜并入｜本包原著未涉及｜待P5\n\n",
        "| # | 柱 | L2 | 议题 | 结局 | 指向 |\n",
        "|---:|---|---|---|---|---|\n",
    ]
    n = 0
    for pillar in data["pillars"]:
        pid = pillar["id"]
        for sub in pillar.get("subs", []):
            sid = sub["id"]
            for topic in sub.get("must_check_topics", []):
                n += 1
                lines.append(f"| {n} | {pid} | {sid} | {topic} | {args.outcome} | |\n")
    lines.append(f"\n生成项：**{n}**（须为 112）\n")
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    print(f"wrote {args.out} rows={n}")


if __name__ == "__main__":
    main()
