#!/usr/bin/env python3
"""S17: Lint D1 handbook drafts (v2 §15.5.6 step 10 / S17 registry)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CORE_MARK = "[核心卡]"
FIELD_RE = re.compile(r"^\s*\d+\.\s+\*\*", re.MULTILINE)
CLAIM_RE = re.compile(r"C-[A-Z0-9]+-[A-Za-z0-9]+-?\d*")
LONG_QUOTE_RE = re.compile(r"[「""][^」""]{16,}[」""]")


def lint_file(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    if CORE_MARK not in text:
        return issues
    blocks = re.split(r"(?=#### M-D)", text)
    for block in blocks:
        if CORE_MARK not in block:
            continue
        title = block.split("\n", 1)[0]
        fields = FIELD_RE.findall(block)
        if len(fields) < 9:
            issues.append(f"{path.name}: {title.strip()} 仅 {len(fields)}/9 编号字段")
        if "出处" in block and not CLAIM_RE.search(block):
            issues.append(f"{path.name}: {title.strip()} 出处区无 C- claim_id")
    for m in LONG_QUOTE_RE.finditer(text):
        issues.append(f"{path.name}: 疑似长引文 ({len(m.group())} 字): …{m.group()[:20]}…")
    return issues


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="out/D1_手册草稿")
    p.add_argument("--out", default="logs/s17_manual_lint_report.md")
    args = p.parse_args()
    root = Path(args.dir)
    all_issues: list[str] = []
    for md in sorted(root.glob("*.md")):
        if md.name.startswith("00_"):
            continue
        all_issues.extend(lint_file(md))
    lines = ["# S17 manual lint 报告\n\n", f"扫描目录: `{args.dir}`\n\n"]
    if not all_issues:
        lines.append("**PASS**：未发现结构性问题（启发式）。\n")
        status = 0
    else:
        lines.append(f"**FAIL**：{len(all_issues)} 项\n\n")
        for i in all_issues[:80]:
            lines.append(f"- {i}\n")
        if len(all_issues) > 80:
            lines.append(f"\n… 另有 {len(all_issues)-80} 项\n")
        status = 1
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    print(f"issues={len(all_issues)} report={args.out}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
