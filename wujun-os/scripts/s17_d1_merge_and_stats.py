#!/usr/bin/env python3
"""S17: 合并 D1 十章正文 + AC-5.3 三柱篇幅比（汉字计，v2 §14.3 / AC-5.3）。"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "out/D1_手册草稿"

# §14.7 阅读顺序（不含附录）
CHAPTER_ORDER = [
    "00_使用说明与全景.md",
    "06_D06_职业与职场.md",
    "01_D01_认知格局与境界哲学.md",
    "02_D02_个人成长与世界观.md",
    "03_D03_判断决策与取舍.md",
    "05_D05_做事方法与执行力.md",
    "07_D07_为人处世与组织协同.md",
    "04_D04_数理与工程思维.md",
    "08_D08_商业与创业.md",
    "09_D09_财富与投资.md",
    "10_D10_创新与产品方法.md",
]
PILLAR_PREFIXES = ("01_D01", "02_D02", "06_D06")
TEN_CHAPTER_PREFIXES = tuple(f"{i:02d}_" for i in range(1, 11))  # 01..10 by glob prefix


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def chapter_path(name: str) -> Path:
    p = DRAFT / name
    if not p.is_file():
        raise FileNotFoundError(p)
    return p


def ten_chapter_files() -> list[Path]:
    out: list[Path] = []
    for pref in (
        "01_D01",
        "02_D02",
        "03_D03",
        "04_D04",
        "05_D05",
        "06_D06",
        "07_D07",
        "08_D08",
        "09_D09",
        "10_D10",
    ):
        out.append(next(DRAFT.glob(f"{pref}*.md")))
    return out


def merge(out_path: Path) -> None:
    parts = [
        "# 吴军十书·个人手册（D1 合并稿 v1）\n\n",
        f"> 由 `scripts/s17_d1_merge_and_stats.py` 生成 @ {datetime.now().isoformat(timespec='seconds')}\n",
        "> 十章按 v2 §14.7 顺序拼接；锚点与声明以分章源文件为准。\n\n",
        "---\n\n",
    ]
    for name in CHAPTER_ORDER:
        text = chapter_path(name).read_text(encoding="utf-8")
        parts.append(f"\n\n<!-- source: {name} -->\n\n")
        parts.append(text.strip())
        parts.append("\n\n---\n\n")
    out_path.write_text("".join(parts), encoding="utf-8")


def stats_report(report_path: Path) -> tuple[float, bool]:
    files = ten_chapter_files()
    by_name: dict[str, int] = {}
    total = 0
    pillar = 0
    for f in files:
        n = cjk_count(f.read_text(encoding="utf-8"))
        by_name[f.name[:6]] = n
        total += n
        if f.name.startswith(PILLAR_PREFIXES):
            pillar += n
    ratio = pillar / total if total else 0.0
    ok = 0.45 <= ratio <= 0.55
    lines = [
        "# D1 篇幅统计（AC-5.3）\n\n",
        f"生成时间：{datetime.now().isoformat(timespec='seconds')}\n\n",
        "| 章 | 汉字数 |\n|---|---:|\n",
    ]
    for f in files:
        lines.append(f"| {f.name} | {by_name[f.name[:6]]} |\n")
    lines.append(f"| **十章合计** | **{total}** |\n")
    lines.append(f"| **重点三柱 D01+D02+D06** | **{pillar}** |\n")
    lines.append(f"| **占比** | **{ratio*100:.1f}%** |\n\n")
    lines.append("门槛：45%–55%（v2 AC-5.3）。\n\n")
    lines.append(f"**判定**：{'PASS' if ok else 'FAIL'}\n")
    report_path.write_text("".join(lines), encoding="utf-8")
    return ratio, ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--merge-out", default="out/D1_手册草稿/D1_主手册合并稿_v1.md")
    ap.add_argument("--stats-out", default="logs/s17_d1_pillar_ratio_latest.md")
    ap.add_argument("--no-merge", action="store_true")
    args = ap.parse_args()
    if not args.no_merge:
        merge(ROOT / args.merge_out)
        print(f"merged -> {args.merge_out}")
    ratio, ok = stats_report(ROOT / args.stats_out)
    print(f"pillar_ratio={ratio*100:.1f}% ac53={'PASS' if ok else 'FAIL'} report={args.stats_out}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
