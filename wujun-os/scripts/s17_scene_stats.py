#!/usr/bin/env python3
"""AC-5.4：场景入口 30–50 条，每条须含 M-D 模型 ID。"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "out/D1_手册草稿/场景入口_汇总.md"
ROW_RE = re.compile(r"^\| (S-\d+)", re.M)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="logs/s17_scene_stats_latest.md")
    args = ap.parse_args()
    text = PATH.read_text(encoding="utf-8")
    ids = [m.group(1) for m in ROW_RE.finditer(text)]
    bad = [ln for ln in text.splitlines() if ln.startswith("| S-") and "M-D" not in ln]
    ok = 30 <= len(ids) <= 50 and not bad
    body = (
        f"# AC-5.4 场景统计\n\n"
        f"条目：**{len(ids)}**（门槛 30–50）\n\n"
        f"无 M-D 指向行：**{len(bad)}**\n\n"
        f"**判定**：{'PASS' if ok else 'FAIL'}\n"
    )
    (ROOT / args.out).write_text(body, encoding="utf-8")
    print(f"scenes={len(ids)} ac54={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
