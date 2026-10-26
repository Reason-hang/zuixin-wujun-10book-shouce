#!/usr/bin/env python3
"""P7 步 1：out/ 草稿断链与表格启发式检查（v2 S18 子集）。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BAD_MERMAID = re.compile(r"```mermaid[\s\S]*?```", re.MULTILINE)


def check_md(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    for m in LINK_RE.finditer(text):
        target = m.group(2).split("#", 1)[0].strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.startswith("%"):
            continue
        p = (path.parent / target).resolve()
        if not p.is_file():
            issues.append(f"{path.name}: 断链 {target}")
    for block in BAD_MERMAID.findall(text):
        if "graph " not in block and "flowchart" not in block and "sequenceDiagram" not in block:
            if len(block) > 20:
                issues.append(f"{path.name}: mermaid 块疑似空/语法缺省")
    def table_cols(ln: str) -> int:
        body = ln.strip()
        if not body.startswith("|"):
            return 0
        return len([c for c in body.strip("|").split("|")])

    def is_sep(ln: str) -> bool:
        return bool(re.match(r"^\|[-:\s|]+\|$", ln.strip()))

    block: list[str] = []
    for ln in text.splitlines():
        if ln.strip().startswith("|") and "|" in ln[1:]:
            block.append(ln)
        else:
            if block:
                data = [table_cols(x) for x in block if not is_sep(x)]
                if data:
                    uniq = set(data)
                    if len(uniq) > 1:
                        issues.append(f"{path.name}: 表格列数不一致 {sorted(uniq)}")
                block = []
    if block:
        data = [table_cols(x) for x in block if not is_sep(x)]
        if data and len(set(data)) > 1:
            issues.append(f"{path.name}: 表格列数不一致 {sorted(set(data))}")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="out")
    ap.add_argument("--out", default="logs/s18_render_check_latest.md")
    args = ap.parse_args()
    base = ROOT / args.dir
    issues: list[str] = []
    for md in sorted(base.rglob("*.md")):
        if "node_modules" in md.parts:
            continue
        issues.extend(check_md(md))
    lines = ["# S18 渲染/链接检查（子集）\n\n", f"扫描: `{args.dir}`\n\n"]
    if not issues:
        lines.append("**PASS**\n")
        status = 0
    else:
        lines.append(f"**FAIL**：{len(issues)} 项\n\n")
        for i in issues[:50]:
            lines.append(f"- {i}\n")
        status = 1
    (ROOT / args.out).write_text("".join(lines), encoding="utf-8")
    print(f"issues={len(issues)} report={args.out}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
