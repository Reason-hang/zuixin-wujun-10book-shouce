#!/usr/bin/env python3
"""AC-5.2: 原著（字段8 出处）与映射（字段9 落地映射）分栏检查。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CORE_MARK = "[核心卡]"
FIELD8_RE = re.compile(r"8\.\s+\*\*出处\*\*")
FIELD9_RE = re.compile(r"9\.\s+\*\*落地映射")
MAPPING_TAG_RE = re.compile(r"映射·非原著|本包原著未涉及")
CLAIM_RE = re.compile(r"C-[A-Z0-9]+-[A-Za-z0-9]+-?\d*")
SCENE_ROW_RE = re.compile(
    r"^\|\s*S-\d+\s*\|[^|]+\|[^|]+\|\s*(原著|映射[^|]*)\s*\|",
    re.MULTILINE,
)


def check_core_cards(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?=#### M-D)", text)
    for block in blocks:
        if CORE_MARK not in block:
            continue
        title = block.split("\n", 1)[0].strip()
        if not FIELD8_RE.search(block):
            issues.append(f"{path.name}: {title} 缺字段8「出处」")
        elif not CLAIM_RE.search(block.split("8. **出处**", 1)[-1][:400]):
            issues.append(f"{path.name}: {title} 字段8 无 C- claim_id")
        if not FIELD9_RE.search(block):
            issues.append(f"{path.name}: {title} 缺字段9「落地映射」")
        else:
            f9 = block.split("9. **落地映射", 1)[-1].split("\n\n", 1)[0]
            if not MAPPING_TAG_RE.search(f9):
                issues.append(f"{path.name}: {title} 字段9 未标「映射·非原著」或「本包原著未涉及」")
    return issues


def check_scene_table(path: Path) -> list[str]:
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    if "场景入口" not in text and path.name != "场景入口_汇总.md":
        return issues
    rows = SCENE_ROW_RE.findall(text)
    if path.name == "场景入口_汇总.md" and not rows:
        issues.append("场景入口_汇总.md: 未解析到带「原著/映射」列的行")
    for block in re.findall(r"^\| S-\d+.*$", text, re.MULTILINE):
        if "原著" not in block and "映射" not in block:
            issues.append(f"场景行缺类型列: {block[:60]}…")
    return issues


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="out/D1_手册草稿")
    ap.add_argument("--out", default="logs/s17_mapping_split_latest.md")
    args = ap.parse_args()
    root = Path(args.dir)
    issues: list[str] = []
    n_core = 0
    for md in sorted(root.glob("*.md")):
        if md.name.startswith("00_") or md.name.startswith("D1_主手册合并稿"):
            continue
        for block in re.split(r"(?=#### M-D)", md.read_text(encoding="utf-8")):
            if CORE_MARK in block:
                n_core += 1
        issues.extend(check_core_cards(md))
    scene = root / "场景入口_汇总.md"
    if scene.is_file():
        issues.extend(check_scene_table(scene))
    lines = [
        "# AC-5.2 原著/映射分栏检查\n\n",
        f"扫描: `{args.dir}`（不含合并稿）\n\n",
        f"核心卡计数: **{n_core}**\n\n",
    ]
    if not issues:
        lines.append("**PASS**：每张核心卡字段8/9分栏齐全；场景表含原著/映射列。\n")
        status = 0
    else:
        lines.append(f"**FAIL**：{len(issues)} 项\n\n")
        for i in issues[:100]:
            lines.append(f"- {i}\n")
        status = 1
    Path(args.out).write_text("".join(lines), encoding="utf-8")
    print(f"core_cards={n_core} issues={len(issues)} report={args.out}")
    raise SystemExit(status)


if __name__ == "__main__":
    main()
