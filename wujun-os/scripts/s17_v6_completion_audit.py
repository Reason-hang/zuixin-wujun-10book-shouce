#!/usr/bin/env python3
"""V6 目标链完成度审计（只读汇总；不冒充过关）。退出码：0=全绿，1=仍有缺口。"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/v6_completion_audit_latest.md"


def row(ok: bool, label: str, evidence: str) -> tuple[str, bool]:
    mark = "✅" if ok else "🔄"
    return f"| {label} | {mark} | {evidence} |", ok


def main() -> int:
    subprocess.run([sys.executable, "scripts/s17_p6_step_status.py"], cwd=ROOT, check=False)
    status = (ROOT / "logs/p6_step_status_latest.md").read_text(encoding="utf-8")

    checks: list[tuple[str, bool, str]] = []

    def exists(rel: str) -> bool:
        return (ROOT / rel).is_file()

    checks.append(("SG1 B-017~020 + 单书验收", exists("logs/book_coverage_SG1_20261026.md"), "book_coverage_SG1_20261026.md"))
    checks.append(("GATE-D 9019 0 FAIL", exists("logs/gate_d_summary_20261026.md"), "gate_d_summary_20261026.md"))
    checks.append(("P4 冻结 manifest", exists("state/p4_freeze.json"), "state/p4_freeze.json"))
    s15 = (ROOT / "logs/s15_check_all_latest.md").read_text(encoding="utf-8") if exists("logs/s15_check_all_latest.md") else ""
    p6_subset_ok = bool(s15) and "| FAIL |" not in s15 and "| PASS |" in s15
    checks.append(
        ("P5 脚本 AC-5.1~5.8", p6_subset_ok, "s15_check_all_latest.md fail=0"),
    )
    m3 = exists("logs/m3_user_signoff_record.md")
    checks.append(("P5 M3 用户签收", m3, "m3_user_signoff_record.md 或 M3-确认+apply"))
    checks.append(("P6 步 3 AC36 正式列满", "AC-3.6 回读召回 | 135 | 135 | ✅" in status, "p6_step_status_latest.md"))
    checks.append(("P6 G10② 漏收列满", "G10② 漏收 | 20 | 20 | ✅" in status, "p6_step_status_latest.md"))
    checks.append(("P6 步 11 抽查满", "用户 20 张 | 20 | 20 | ✅" in status, "p6_step_status_latest.md"))
    checks.append(("P7 D4 快照", exists("out/覆盖与质检报告/D4_覆盖与质检报告_草稿.md"), "D4_覆盖与质检报告_草稿.md"))
    checks.append(("P7 交付清单草稿", exists("out/覆盖与质检报告/P7_交付清单_草稿.md"), "P7_交付清单_草稿.md"))
    checks.append(("P7 终版命名 M4", exists("out/P7_交付说明_v1.0.md"), "无 v1.0 终版文件名 — 待 P6 后定稿"))
    drill = (ROOT / "logs/p6_scene_drill_log_20261026.md").read_text(encoding="utf-8")
    checks.append(
        ("P6 步 7 演练签收", "🔄 Agent草稿" not in drill and "✅" in drill, "p6_scene_drill_log 表内 ✅"),
    )
    pre = (ROOT / "logs/p6_adversarial_preflight_latest.md").read_text(encoding="utf-8") if exists(
        "logs/p6_adversarial_preflight_latest.md"
    ) else ""
    checks.append(("P6 对抗预检", "fail=0" in pre or "**FAIL**：0" in pre, "p6_adversarial_preflight_latest.md"))
    p7pre = (ROOT / "logs/p7_preflight_latest.md").read_text(encoding="utf-8") if exists(
        "logs/p7_preflight_latest.md"
    ) else ""
    checks.append(("P7 工程预检", "eng_fail=0" in p7pre, "p7_preflight_latest.md"))

    lines = [
        "# V6 完成度审计（自动汇总）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`make v6-audit`\n\n",
        "| 项 | 状态 | 证据 |\n",
        "|---|---|---|\n",
    ]
    all_ok = True
    for label, ok, ev in checks:
        ln, ok2 = row(ok, label, ev)
        lines.append(ln + "\n")
        all_ok = all_ok and ok2

    lines.append("\n```bash\nmake test && make p6-subset && make p6-adversarial-preflight && make d4-snapshot\n```\n")
    lines.append(f"\n**V6 整体**: {'✅ 可标 complete' if all_ok else '🔄 未完成（勿 UpdateGoal complete）'}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT} v6_complete={all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
