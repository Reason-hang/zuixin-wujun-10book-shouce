#!/usr/bin/env python3
"""P6 步 8：D1 草稿 24 字滑窗重复（仅字段6–7正文，跨卡）。"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

BLOCK_RE = re.compile(r"^#### (M-D\d+-\d+[^\n]+)", re.MULTILINE)
CLAIM_RE = re.compile(r"C-[A-Z0-9]+-[A-Za-z0-9]+-?\d*")
FIELD67_RE = re.compile(
    r"6\.\s+\*\*行动方法\*\*.*?(?=8\.\s+\*\*出处\*\*)",
    re.DOTALL,
)


def substance(block: str) -> str:
    m = FIELD67_RE.search(block)
    if not m:
        return ""
    t = CLAIM_RE.sub("", m.group(0))
    t = re.sub(r"\s+", "", t)
    t = re.sub(r"[`*#|>\-\d\.「」]", "", t)
    return t


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="out/D1_手册草稿")
    ap.add_argument("--win", type=int, default=24)
    ap.add_argument("--max-report", type=int, default=20)
    ap.add_argument("--out", default="logs/s17_manual_dup_slide_latest.md")
    args = ap.parse_args()
    root = Path(args.dir)
    pairs: list[tuple[str, str]] = []
    for md in sorted(root.glob("*.md")):
        if md.name.startswith("00_") or md.name.startswith("D1_主手册合并稿"):
            continue
        text = md.read_text(encoding="utf-8")
        heads = list(BLOCK_RE.finditer(text))
        for i, m in enumerate(heads):
            if "[核心卡]" not in m.group(1):
                continue
            start = m.start()
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            body = substance(text[start:end])
            if len(body) >= args.win * 2:
                pairs.append((m.group(1).strip(), body))

    index: dict[str, list[str]] = defaultdict(list)
    for title, body in pairs:
        for i in range(len(body) - args.win + 1):
            index[body[i : i + args.win]].append(title)

    issues = [
        f"「{frag[:18]}…」: {uniq[0]} ↔ {uniq[1]}"
        for frag, titles in index.items()
        for uniq in [sorted(set(titles))]
        if len(uniq) > 1
    ]

    lines = [
        "# P6 步 8 · 24 字滑窗重复（字段6–7）\n\n",
        f"核心卡块: {len(pairs)}；窗口: {args.win}\n\n",
    ]
    if not issues:
        lines.append("**PASS**\n")
        status = 0
    else:
        lines.append(f"**FAIL**：{len(issues)} 组\n\n")
        for i in issues[: args.max_report]:
            lines.append(f"- {i}\n")
        status = 1
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    print(f"cards={len(pairs)} dups={len(issues)} report={args.out}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
