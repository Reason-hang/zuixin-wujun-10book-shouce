#!/usr/bin/env python3
"""P6 步 6 子集：45 张核心卡「数理工程表达」字段统计（非全库数理映射率）。"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/s17_math_mapping_audit_latest.md"
CARD_RE = re.compile(r"^#### (M-D\d{2}-\d{2})")


def field5(block: str) -> str:
    m = re.search(r"5\.\s*\*\*数理工程表达\*\*[：:](.+?)(?=\n6\.\s*\*\*)", block, re.DOTALL)
    return (m.group(1).strip() if m else "").replace("\n", " ")


def main() -> None:
    chapters = sorted((ROOT / "out/D1_手册草稿").glob("[0-9][0-9]_D*.md"))
    rows: list[tuple[str, str, str]] = []
    for ch in chapters:
        if ch.name.startswith("00_"):
            continue
        text = ch.read_text(encoding="utf-8")
        parts = re.split(r"(?=^#### M-D)", text, flags=re.MULTILINE)
        for part in parts:
            m = CARD_RE.match(part.strip())
            if not m:
                continue
            mid = m.group(1)
            f5 = field5(part)
            if "不映射" in f5 or f5.startswith("不映射"):
                tag = "不映射"
            elif "可检验" in f5 or "可观测" in f5 or "映射——" in f5:
                tag = "可检验/可观测"
            elif f5:
                tag = "其他表述"
            else:
                tag = "缺字段"
            rows.append((mid, tag, f5[:80]))
    counts: dict[str, int] = {}
    for _, tag, _ in rows:
        counts[tag] = counts.get(tag, 0) + 1
    lines = [
        "# 核心卡数理工程表达审计（P6 步 6 子集）\n\n",
        f"生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
        f"核心卡数: **{len(rows)}**\n\n",
        "| 分类 | 数量 |\n|---|---:|\n",
    ]
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |\n")
    lines.append("\n## 明细\n\n| 卡 ID | 分类 | 摘录 |\n|---|---|---|\n")
    for mid, tag, ex in rows:
        lines.append(f"| {mid} | {tag} | {ex} |\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"cards={len(rows)} out={OUT}")


if __name__ == "__main__":
    main()
