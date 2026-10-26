#!/usr/bin/env python3
"""AC-5.5: D1 T1 工具数量与要素检查（v2 §9.6 / §15.5.6 步 6）。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOL_HEAD = re.compile(r"^#### (T-D\d+-\d+)", re.MULTILINE)
CLAIM_RE = re.compile(r"C-[A-Z0-9]+-[A-Za-z0-9]+-?\d*")
REQUIRED = ("触发条件", "输入", "步骤", "输出", "复查")


def scan_dir(d1: Path) -> tuple[dict[str, str], list[str]]:
    tools: dict[str, str] = {}
    issues: list[str] = []
    for md in sorted(d1.glob("*.md")):
        if md.name.startswith("00_") or md.name.startswith("D1_主手册合并稿"):
            continue
        text = md.read_text(encoding="utf-8")
        for m in TOOL_HEAD.finditer(text):
            tid = m.group(1)
            start = m.start()
            nxt = text.find("\n#### ", start + 1)
            block = text[start : nxt if nxt != -1 else len(text)]
            if tid in tools:
                issues.append(f"重复工具 ID {tid}: {md.name} 与已有定义冲突")
            tools[tid] = block
            if "[T1" not in block.split("\n", 1)[0]:
                issues.append(f"{tid}: 标题未标 [T1 …]")
            for key in REQUIRED:
                if f"- {key}" not in block and f"- **{key}**" not in block:
                    issues.append(f"{tid}: 缺字段「{key}」")
            steps = ""
            for line in block.splitlines():
                if line.strip().startswith("- 步骤"):
                    steps = line
                    break
            if "[T1" in block and steps and not CLAIM_RE.search(steps):
                issues.append(f"{tid}: T1 步骤行无 C- 锚点（须在步骤中标注出处）")
    return tools, issues


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="out/D1_手册草稿")
    ap.add_argument("--min", type=int, default=12)
    ap.add_argument("--max", type=int, default=18)
    ap.add_argument("--out", default="logs/s17_tools_check_latest.md")
    args = ap.parse_args()
    tools, issues = scan_dir(Path(args.dir))
    n = len(tools)
    if n < args.min or n > args.max:
        issues.append(f"工具数量 {n} 不在 [{args.min},{args.max}]")
    lines = [
        "# AC-5.5 行动工具检查\n\n",
        f"扫描: `{args.dir}`\n\n",
        f"工具数: **{n}**（ID: {', '.join(sorted(tools))})\n\n",
    ]
    if not issues:
        lines.append("**PASS**\n")
        status = 0
    else:
        lines.append(f"**FAIL**：{len(issues)} 项\n\n")
        for i in issues[:60]:
            lines.append(f"- {i}\n")
        status = 1
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    print(f"tools={n} issues={len(issues)} report={args.out}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
