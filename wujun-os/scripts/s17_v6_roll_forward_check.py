#!/usr/bin/env python3
"""写入 V6 工程绿链 + 签收缺口快照（供交接/审计，不冒充 V6 complete）。"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/v6_roll_forward_check_latest.md"


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout or r.stderr or "").strip().splitlines()
    return r.returncode, tail[-1] if tail else ""


def main() -> int:
    ts = datetime.now().isoformat(timespec="seconds")
    eng_rc, eng_tail = run(["make", "v6-engineering"])
    audit_rc, audit_tail = run([sys.executable, "scripts/s17_v6_completion_audit.py"])
    status = (ROOT / "logs/p6_step_status_latest.md").read_text(encoding="utf-8")
    audit_body = (ROOT / "logs/v6_completion_audit_latest.md").read_text(encoding="utf-8")
    lines = [
        f"# V6 roll-forward 检查\n\n",
        f"> 生成: {ts}；`make v6-roll-forward`\n\n",
        f"| 步骤 | exit | 末行摘要 |\n|---|---|---|\n",
        f"| v6-engineering | {eng_rc} | `{eng_tail[:120]}` |\n",
        f"| v6-audit | {audit_rc} | `{audit_tail[:120]}` |\n\n",
        "## P6 签收进度\n\n",
        status,
        "\n## V6 审计摘要\n\n",
        audit_body.split("**V6 整体**")[-1] if "**V6 整体**" in audit_body else audit_body[-800:],
        "\n",
    ]
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"out={OUT} eng={eng_rc} audit={audit_rc}")
    # audit_rc=1 expected until user signoff; snapshot always written
    return 0 if eng_rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
