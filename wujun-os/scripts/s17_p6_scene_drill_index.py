#!/usr/bin/env python3
"""P6 步 7 子集：v2 §9 五类应用验证场景 → 手册场景 ID 映射（可复算索引）。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/p6_scene_drill_index_latest.md"

# v2 列举的五类 P6 演练场景（编辑新增，非原著标题）
DRILLS = [
    (
        "需求优先级",
        "S-032 / S-127",
        "M-D03-02",
        "需求池过多、评审不敢删条目",
    ),
    (
        "库存与履约数据判断",
        "S-102 / S-128",
        "M-D01-01 / M-D04-01",
        "相关≠因果；指数增长备货线性",
    ),
    (
        "B 端方案评审",
        "S-103 / S-071",
        "M-D01-02 / M-D07-01",
        "只有优点无边界；评审否定方案",
    ),
    (
        "跨部门协作",
        "S-129 / S-130 / S-063",
        "M-D07-02 / M-D06-02",
        "运营↔技术、多仓口径、无效周会",
    ),
    (
        "专业成长与职业迁移",
        "S-105 / S-061",
        "M-D06-01",
        "转岗；晋升答辩自评",
    ),
]


def main() -> None:
    lines = [
        "# P6 步 7｜五类应用验证场景索引（子集）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`s17_p6_scene_drill_index.py`\n",
        "> **演练记录**（走通/异常）仍须人工填写；本表仅证明手册内**有对应场景入口**。\n\n",
        "| 验证类 | 场景 ID | 模型 | 情境摘要 |\n",
        "|---|---|---|---|\n",
    ]
    for kind, scenes, models, note in DRILLS:
        lines.append(f"| {kind} | {scenes} | {models} | {note} |\n")
    lines.append(
        "\n**演练记录模板**：`logs/p6_scene_drill_log_20261026.md`（每类 1 段：输入→用卡→输出→异常）。\n"
    )
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"drills={len(DRILLS)} out={OUT}")


if __name__ == "__main__":
    main()
