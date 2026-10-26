#!/usr/bin/env python3
"""归档 G0–G9 既有日志索引（不重跑 p0）；供 P6 步 1 对账引用。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/覆盖与质检报告/G0_G9_日志索引.md"

LOGS = [
    ("G0 输入冻结", "logs/g0_inputs.md"),
    ("G2/G3 切分守恒", "logs/g2g3.md"),
    ("G4 编号", "logs/g4.md"),
    ("G5 目录", "logs/g5.md"),
    ("G6 重复", "logs/g6.md"),
    ("G7 非源/排除", "logs/g7.md"),
    ("G8 反向抽查", "logs/g8.md"),
    ("D5 分母", "logs/p0_denominator.md"),
]


def verdict(text: str) -> str:
    if "结论: **FAIL**" in text or "结果: **FAIL**" in text:
        return "FAIL"
    if "**PASS**" in text[:800]:
        return "PASS"
    if "PASS" in text[:1200]:
        return "PASS?"
    return "未标"


def main() -> None:
    lines = [
        "# G0–G9 / P0 日志索引（快照，非重跑）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`scripts/s15_g_logs_index.py`。\n",
        "> **全量重跑**仍须 `make p0`（见 runbook）；本表仅证明仓库内**最近一次** P0 链日志仍在。\n\n",
        "| 闸门 | 日志 | mtime | 结论（文内摘录） |\n",
        "|---|---|---|---|\n",
    ]
    for name, rel in LOGS:
        p = ROOT / rel
        if not p.is_file():
            lines.append(f"| {name} | `{rel}` | — | **缺失** |\n")
            continue
        mtime = datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
        text = p.read_text(encoding="utf-8", errors="replace")
        v = verdict(text)
        lines.append(f"| {name} | `{rel}` | {mtime} | {v} |\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT}")


if __name__ == "__main__":
    main()
