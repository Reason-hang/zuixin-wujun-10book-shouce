#!/usr/bin/env python3
"""G10②：Agent 草稿列（独立文件；正式表「漏收」列仍须你填）。"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "out/覆盖与质检报告/G10②_盲抽单元表_草稿.md"
OUT = ROOT / "logs/g10_blind_agent_draft_column_20261026.md"

# 处置 X 且为婚恋/彩蛋/非职场核心 → 草稿倾向「否（登记合理）」
SKIP_THEMES = ("元旦彩蛋", "莎士比亚", "RNA", "火山口湖", "人生最重要的投资", "择偶", "父母相处")


def draft_verdict(title: str, disposal: str, typ: str) -> str:
    t = title or ""
    if disposal == "X" and typ == "C":
        if any(k in t for k in SKIP_THEMES):
            return "否（草稿·主题偏生活/彩蛋，X 合理）"
        if "投资" in t and "上" in t:
            return "否（草稿·婚恋投资专题，X5 边界）"
        return "待你重读（X 内容卡，可能漏 M）"
    if disposal == "N" and typ in ("S", "N"):
        if "目录" in t:
            return "否（草稿·目录单元）"
        return "待你重读（结构/非内容，核对 N 登记）"
    return "待你重读"


def main() -> None:
    lines = [
        "# G10② 漏收列 · Agent 草稿（非签收）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
        "| 单元 ID | 标题 | Agent 草稿 | 你确认 |\n",
        "|---|---|---|---|\n",
    ]
    for ln in TABLE.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or "单元 ID" in ln or ln.startswith("|---"):
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 7:
            continue
        uid, disp, typ, title = parts[1], parts[2], parts[3], parts[5]
        if not re.match(r"^[A-Z0-9]+-U\d+$", uid):
            continue
        d = draft_verdict(title, disp, typ)
        lines.append(f"| {uid} | {title[:40]} | {d} | |\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT}")


if __name__ == "__main__":
    main()
