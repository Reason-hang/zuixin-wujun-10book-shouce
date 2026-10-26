#!/usr/bin/env python3
"""P6 步 1：读取最近一次 `make p0` 产出的 G2–G8 / D5 分母日志，要求文内 PASS。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ("G2/G3", "logs/g2g3.md"),
    ("G4", "logs/g4.md"),
    ("G5", "logs/g5.md"),
    ("G6", "logs/g6.md"),
    ("G7", "logs/g7.md"),
    ("G8", "logs/g8.md"),
    ("D5 分母", "logs/p0_denominator.md"),
]


def verdict(text: str, rel: str) -> str:
    head = text[:2000]
    if "结论: **FAIL**" in head or "结果: **FAIL**" in head or ": FAIL" in head[:500]:
        return "FAIL"
    if rel.endswith("p0_denominator.md"):
        if "| 一致 |" in text and "否" in text.split("| 一致 |", 1)[-1][:200]:
            return "FAIL"
        if "冻结日期:" in text and "| 是 |" in text:
            return "PASS"
        return "UNKNOWN"
    if "结论: **PASS**" in head or "对账: PASS" in head or "扫描: PASS" in head:
        return "PASS"
    if "PASS" in head:
        return "PASS"
    return "UNKNOWN"


def main() -> int:
    bad = []
    for name, rel in REQUIRED:
        p = ROOT / rel
        if not p.is_file():
            bad.append(f"{name}: missing {rel}")
            continue
        v = verdict(p.read_text(encoding="utf-8", errors="replace"), rel)
        if v != "PASS":
            bad.append(f"{name}: {v}")
    if bad:
        print("p0_gate FAIL: " + "; ".join(bad))
        return 2
    print("p0_gate PASS (G2-G8 + denominator logs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
