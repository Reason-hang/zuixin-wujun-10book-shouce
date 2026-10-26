#!/usr/bin/env python3
"""导出 AC-3.6 启发式建议列（独立文件，**不写入**正式召回表，非人工签收）。"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEUR = ROOT / "logs/ac36_semantic_heuristic_latest.md"
OUT = ROOT / "logs/ac36_recall_agent_draft_column_20261026.md"
AC36 = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"


def main() -> int:
    subprocess.run([sys.executable, "scripts/s13_ac36_semantic_heuristic.py"], cwd=ROOT, check=True)
    rates: dict[str, tuple[float, str]] = {}
    if HEUR.is_file():
        for ln in HEUR.read_text(encoding="utf-8").splitlines():
            if not ln.startswith("| C-"):
                continue
            parts = [p.strip() for p in ln.strip().strip("|").split("|")]
            if len(parts) < 3:
                continue
            cid, rate_s, tag = parts[0], parts[1], parts[2]
            try:
                rate = float(rate_s)
            except ValueError:
                rate = -1.0
            rates[cid] = (rate, tag)
    lines = [
        "# AC-3.6 回读召回 · Agent 启发式草稿列\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`s13_ac36_agent_draft_column.py`\n",
        "> **不得**替代 `AC36_抽检召回表_草稿.md` 的「回读召回」列；你签收前 P6 步 3 **未过关**。\n\n",
        "| claim_id | ngram 重合 | Agent 草稿建议 | 你确认 |\n",
        "|---|---:|---|---|\n",
    ]
    n = 0
    for ln in AC36.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or "C-" not in ln:
            continue
        m = re.search(r"(C-[A-Z0-9]+-U\d+-\d+)", ln)
        if not m:
            continue
        cid = m.group(1)
        rate, tag = rates.get(cid, (-1.0, "无数据"))
        draft = "Y（启发式）" if tag == "启发式OK" else "待你回读"
        rate_col = f"{rate:.2f}" if rate >= 0 else "—"
        lines.append(f"| `{cid}` | {rate_col} | {draft} | |\n")
        n += 1
    lines.append(f"\n共 **{n}** 条；正式表仍须人工填「回读召回」。\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    ok_n = sum(1 for _, t in rates.values() if t == "启发式OK")
    print(f"rows={n} heuristic_ok={ok_n} out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
