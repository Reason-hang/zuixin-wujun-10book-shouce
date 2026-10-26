#!/usr/bin/env python3
"""P6 人工签收进度条（只读统计，不冒充过关）。"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/p6_step_status_latest.md"


def count_empty_recall() -> tuple[int, int]:
    p = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"
    if not p.is_file():
        return 0, 0
    total = filled = 0
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or "C-" not in ln:
            continue
        parts = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(parts) >= 6 and parts[0].isdigit():
            total += 1
            if parts[5]:
                filled += 1
    return filled, total


def count_g10_empty() -> tuple[int, int]:
    p = ROOT / "out/覆盖与质检报告/G10②_盲抽单元表_草稿.md"
    if not p.is_file():
        return 0, 0
    total = filled = 0
    uid_re = re.compile(r"\|\s*([A-Z0-9]+)\s*\|\s*([A-Z0-9]+-U\d+)\s*\|")
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or "---" in ln or "单元 ID" in ln:
            continue
        m = uid_re.match(ln)
        if not m:
            continue
        total += 1
        tail = ln.rstrip()
        if re.search(r"\|\s*\|\s*$", tail):
            pass
        else:
            filled += 1
    return filled, total


def count_spot_empty() -> tuple[int, int]:
    p = ROOT / "out/覆盖与质检报告/P6_用户抽查20张_草稿.md"
    if not p.is_file():
        return 0, 0
    total = filled = 0
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("| V-"):
            parts = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(parts) >= 6:
                total += 1
                if parts[5]:
                    filled += 1
    return filled, total


def m3_done() -> bool:
    return (ROOT / "logs/m3_user_signoff_record.md").is_file()


def main() -> None:
    ac_f, ac_t = count_empty_recall()
    g_f, g_t = count_g10_empty()
    s_f, s_t = count_spot_empty()
    lines = [
        "# P6 签收进度（只读）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`make p6-step-status`\n\n",
        "| 项 | 已填 | 总数 | 过关？ |\n",
        "|---|---:|---:|---|\n",
        f"| P5 M3 记录 | {1 if m3_done() else 0} | 1 | {'✅' if m3_done() else '🔄'} |\n",
        f"| AC-3.6 回读召回 | {ac_f} | {ac_t} | {'✅' if ac_t and ac_f == ac_t else '🔄'} |\n",
        f"| G10② 漏收 | {g_f} | {g_t} | {'✅' if g_t and g_f == g_t else '🔄'} |\n",
        f"| 用户 20 张 | {s_f} | {s_t} | {'✅' if s_t and s_f == s_t else '🔄'} |\n",
        "\n代签：`make user-signoff-apply`（须 `user_signoff_authorization.txt`）。\n",
    ]
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT} m3={m3_done()} ac36={ac_f}/{ac_t} g10={g_f}/{g_t} spot={s_f}/{s_t}")


if __name__ == "__main__":
    main()
