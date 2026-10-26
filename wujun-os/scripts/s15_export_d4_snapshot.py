#!/usr/bin/env python3
"""P7 步 2 子集：将 S15 子集闸门快照写入 D4 目录（可复算引用）。。"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "logs/s15_check_all_latest.md"
OUT = ROOT / "out/覆盖与质检报告/s15_check_all_snapshot.md"


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="先跑 s15_check_all 再复制")
    args = ap.parse_args()
    if args.refresh:
        subprocess.run([sys.executable, "scripts/s15_check_all.py"], cwd=ROOT, check=False)
    if not SRC.is_file():
        print("missing s15 report; run make p6-subset first", file=sys.stderr)
        return 2
    header = (
        f"# S15 check_all 快照（P7/D4 引用）\n\n"
        f"> 复制时间: {datetime.now().isoformat(timespec='seconds')}；"
        f"源 `logs/s15_check_all_latest.md`。**子集 ≠ P6/P7 终局过关。**\n\n"
    )
    body = SRC.read_text(encoding="utf-8")
    if body.startswith("# S15"):
        body = body.split("\n", 1)[-1]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + body.lstrip(), encoding="utf-8")
    print(f"out={OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
