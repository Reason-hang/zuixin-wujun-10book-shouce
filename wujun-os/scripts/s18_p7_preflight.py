#!/usr/bin/env python3
"""P7 工程预检（AC-7.2/7.3 子集；≠ M4 终版过关）。退出码 0=预检绿，1=有 FAIL。"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/p7_preflight_latest.md"

REQUIRED = [
    "out/D1_手册草稿/D1_主手册合并稿_v1.md",
    "out/D2_行动工具集_草稿.md",
    "out/D5_内容盘点与单元清单.md",
    "out/覆盖与质检报告/D4_覆盖与质检报告_草稿.md",
    "out/覆盖与质检报告/P7_交付清单_草稿.md",
    "out/P7_交付说明_草稿.md",
    "out/覆盖与质检报告/s15_check_all_snapshot.md",
    "state/p4_freeze.json",
]


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    for rel in REQUIRED:
        p = ROOT / rel
        checks.append((rel, p.is_file(), "存在" if p.is_file() else "缺失"))

    r = subprocess.run(
        [sys.executable, "scripts/s18_render_check.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    s18 = (ROOT / "logs/s18_render_check_latest.md").read_text(encoding="utf-8")
    s18_ok = r.returncode == 0 and "**PASS**" in s18
    checks.append(("S18 out/ 渲染", s18_ok, f"exit={r.returncode}"))

    fact = ROOT / "out/事实源与冻结哈希_草稿.md"
    checks.append(("事实源哈希草稿", fact.is_file(), str(fact.name)))

    m4 = ROOT / "out/P7_交付说明_v1.0.md"
    checks.append(("P7 终版文件名", m4.is_file(), "待 P6 后定稿" if not m4.is_file() else "已有"))

    fail = sum(1 for _, ok, _ in checks if not ok)
    lines = [
        "# P7 工程预检\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`make p7-preflight`\n\n",
        "| 项 | 结果 | 说明 |\n|---|---|---|\n",
    ]
    for label, ok, msg in checks:
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} | {msg} |\n")
    lines.append(f"\n**fail={fail}**（终版命名 FAIL 在 P6 前为预期）\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    # 终版缺失不算工程预检失败
    eng_fail = sum(1 for label, ok, _ in checks if not ok and "终版" not in label)
    print(f"out={OUT} eng_fail={eng_fail}")
    return 0 if eng_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
