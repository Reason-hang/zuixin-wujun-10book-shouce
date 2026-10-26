#!/usr/bin/env python3
"""P6 步 10：对抗审查自动化预检（汇总闸门，非「全文审查过关」）。"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/p6_adversarial_preflight_latest.md"
TEMPLATE = ROOT / "logs/p6_adversarial_review_template_20261026.md"


def run(cmd: list[str]) -> tuple[bool, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout or r.stderr or "").strip().splitlines()
    return r.returncode == 0, tail[-1] if tail else "ok"


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    for name, script in [
        ("P0 G2–G8", "s15_p0_gate_check.py"),
        ("P4 冻结", None),
        ("AC-5.2 映射分栏", "s17_mapping_split_check.py"),
        ("AC-5.5 工具", "s17_tools_check.py"),
        ("G9 子集", "s12_g9_subset_check.py"),
    ]:
        if script:
            ok, msg = run([sys.executable, f"scripts/{script}"])
            checks.append((name, ok, msg))
    ok, msg = run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0,'scripts'); "
            "from s15_check_all import check_p4_freeze; "
            "ok,m=check_p4_freeze(); print(m); raise SystemExit(0 if ok else 2)",
        ]
    )
    checks.append(("P4 freeze manifest", ok, msg))

    spot = ROOT / "logs/p6_spotcheck_agent_draft_20261026.md"
    spot_msg = "未生成；make p6-spotcheck-agent"
    if spot.is_file():
        t = spot.read_text(encoding="utf-8")
        if "anchor_fail=0" in t or "锚点 FAIL: **0**" in t:
            spot_msg = "20 张锚点 PASS（草稿列未签收）"
        else:
            spot_msg = "见 p6_spotcheck_agent_draft"
    checks.append(("步11 抽查锚点", spot.is_file(), spot_msg))

    g10 = ROOT / "out/覆盖与质检报告/G10②_盲抽单元表_草稿.md"
    g10_ok = g10.is_file() and "book_code:" not in g10.read_text(encoding="utf-8")
    checks.append(("G10② 摘录正文", g10_ok, "无 YAML 泄漏（D-WJ-018）"))

    fail = sum(1 for _, ok, _ in checks if not ok)
    lines = [
        "# P6 对抗审查预检（自动）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}\n",
        f"> 人工角度 #1/#3 与手册深读仍见 `{TEMPLATE.name}`。\n\n",
        "| 检查 | 结果 | 说明 |\n|---|---|---|\n",
    ]
    for name, ok, msg in checks:
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {msg} |\n")
    lines.append(f"\n**fail={fail}**（0 仅表示脚本子集；≠ 步 10 终签）\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"fail={fail} out={OUT}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
