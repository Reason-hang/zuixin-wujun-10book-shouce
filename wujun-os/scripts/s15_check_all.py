#!/usr/bin/env python3
"""P6 步 1 子集：可复算闸门（G0 包校验、P4 冻结、P5 lint、论点卡校验）。

全量 G0–G9 / G10 见 spec §15.5.7；本脚本不冒充 P6 过关。
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_p4_freeze() -> tuple[bool, str]:
    manifest = ROOT / "state/p4_k_card_freeze_manifest.sha256"
    meta = ROOT / "state/p4_freeze.json"
    if not manifest.is_file() or not meta.is_file():
        return False, "missing p4 freeze manifest or meta"
    drift = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        digest, rel = line.split(None, 1)
        rel = rel.strip()
        p = ROOT / rel
        if not p.is_file():
            drift.append(f"missing {rel}")
            continue
        if sha256_file(p) != digest:
            drift.append(f"changed {rel}")
    if drift:
        return False, f"freeze drift {len(drift)}: {drift[0]}" + (
            f" (+{len(drift)-1})" if len(drift) > 1 else ""
        )
    return True, "p4 freeze manifest OK"


def run(cmd: list[str], name: str) -> tuple[bool, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    ok = r.returncode == 0
    tail = (r.stdout or r.stderr or "").strip().splitlines()
    msg = tail[-1] if tail else name
    return ok, msg


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    ok, msg = check_p4_freeze()
    checks.append(("P4 freeze manifest", ok, msg))

    ok, msg = run([sys.executable, "scripts/verify_pack.py"], "verify_pack")
    checks.append(("verify_pack (G0 包)", ok, msg))

    ok, msg = run([sys.executable, "scripts/s15_p0_gate_check.py"], "p0_gate")
    checks.append(("P0 G2–G8 日志", ok, msg))

    ok, msg = run([sys.executable, "scripts/s12_g9_subset_check.py"], "g9_subset")
    checks.append(("G9 单元↔卡子集", ok, msg))

    ledger = ROOT / "ledger/溯源与处置台账.md"
    if ledger.is_file():
        ok, msg = run(
            [sys.executable, "scripts/anchor_tool.py", "verify", "--ledger", str(ledger), "--books-dir", "src_frozen"],
            "verify_anchors",
        )
        checks.append(("锚点全量 verify", ok, msg))
    else:
        checks.append(("锚点全量 verify", False, "missing ledger; run make export-anchors"))

    ok, msg = run([sys.executable, "scripts/s17_manual_lint.py"], "s17_manual_lint")
    checks.append(("S17 manual lint", ok, msg))

    ok, msg = run([sys.executable, "scripts/s17_mapping_split_check.py"], "ac52_mapping")
    checks.append(("AC-5.2 原著/映射分栏", ok, msg))

    ok, msg = run(
        [sys.executable, "scripts/s17_d1_merge_and_stats.py", "--no-merge"],
        "ac53_pillar_ratio",
    )
    checks.append(("AC-5.3 三柱占比", ok, msg))

    ok, msg = run([sys.executable, "scripts/s17_scene_stats.py"], "ac54_scenes")
    checks.append(("AC-5.4 场景 30–50", ok, msg))

    ok, msg = run([sys.executable, "scripts/s17_ability_index_check.py"], "ac56_ability")
    checks.append(("AC-5.6 能力速查", ok, msg))

    ok, msg = run([sys.executable, "scripts/s17_coverage_stats.py"], "ac58_coverage")
    checks.append(("AC-5.8 议题 112", ok, msg))

    ok, msg = run([sys.executable, "scripts/s17_tools_check.py"], "ac55_tools")
    checks.append(("AC-5.5 行动工具", ok, msg))

    ok, msg = run([sys.executable, "scripts/s18_render_check.py"], "s18_render")
    checks.append(("S18 out/ 子集", ok, msg))

    ac36 = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"
    if ac36.is_file():
        ok, msg = run([sys.executable, "scripts/s13_ac36_anchor_ping.py"], "ac36_anchor")
        checks.append(("AC-3.6 锚点复验", ok, msg))
    else:
        checks.append(("AC-3.6 锚点复验", False, "missing AC36 table; make ac36-sample"))

    ok, msg = run([sys.executable, "scripts/s17_manual_dup_slide.py"], "p6_dup24")
    checks.append(("P6 步8 24字滑窗", ok, msg))

    ok, msg = run(
        [sys.executable, "scripts/s13_kwscan.py", "--out", "logs/g10_kw.md"],
        "g10_kwscan",
    )
    checks.append(("G10① 关键词反查", ok, msg))

    run(
        [sys.executable, "scripts/s13_sg3_highlight_recall.py"],
        "g10_sg3_hz_seed",
    )
    run(
        [sys.executable, "scripts/s13_sg3_carry_table.py"],
        "g10_sg3_carry",
    )
    ok, msg = run(
        [sys.executable, "scripts/s13_sg3_highlight_recall.py", "--strict"],
        "g10_sg3_hz_strict",
    )
    checks.append(("G10③ 划重点 strict", ok, msg))

    cards = ROOT / "data/cards"
    if cards.is_dir() and (ROOT / "src_frozen").is_dir():
        out = ROOT / "logs/s15_cards_verify_latest.md"
        ok, msg = run(
            [
                sys.executable,
                "scripts/verify_cards.py",
                "--dirs",
                "data/cards",
                "--out",
                str(out),
            ],
            "verify_cards",
        )
        if "0 张" in msg:
            ok = False
            msg = "verify_cards scanned 0 cards"
        checks.append(("verify_cards (K卡)", ok, msg))
    else:
        checks.append(("verify_cards (K卡)", False, "skip: need src_frozen"))

    report = ROOT / "logs/s15_check_all_latest.md"
    lines = ["# S15 check_all（子集）\n\n", "| 检查 | 结果 | 说明 |\n", "|---|---|---|\n"]
    fail = 0
    for name, ok, msg in checks:
        if not ok:
            fail += 1
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {msg} |\n")
    report.write_text("".join(lines), encoding="utf-8")
    print(f"report={report} fail={fail}")
    for name, ok, msg in checks:
        print(f"{'OK' if ok else 'FAIL'} {name}: {msg}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
