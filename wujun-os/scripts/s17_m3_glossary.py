#!/usr/bin/env python3
"""为 M3 题面中的 C- claim_id 生成「人读版」附录（书名·单元标题·转述）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = {
    "SG1": "硅谷来信1",
    "WJ2": "吴军来信2",
    "SG3": "硅谷来信3",
    "GG": "谷歌方法论",
    "JS": "见识",
    "TD": "态度",
    "GJ": "格局",
    "FZ": "富足",
    "JJ": "境界",
    "SX": "数学通识50讲",
}


def unit_title(uid: str) -> str:
    m = re.match(r"^([A-Z0-9]+)-U(\d+)$", uid)
    if not m:
        return uid
    p = ROOT / f"data/units/{m.group(1)}/unit_{int(m.group(2)):04d}.md"
    if not p.is_file():
        return uid
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            return ln[3:].strip()
    return uid


def claim_text(cid: str) -> str:
    prefix = cid.rstrip("-")
    for p in ROOT.glob("data/cards/**/*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            x = c.get("claim_id", "")
            if x == cid or x.startswith(prefix):
                return (c.get("claim_text") or "")[:60]
    return ""


def gloss(cid: str) -> str:
    m = re.match(r"^C-([A-Z0-9]+)-U(\d+)", cid)
    if not m:
        return cid
    bc, num = m.group(1), int(m.group(2))
    uid = f"{bc}-U{num:04d}"
    title = BOOK.get(bc, bc) + " · " + unit_title(uid)
    return f"- **{title}** — {claim_text(cid)}（`{cid}`）"


def main() -> None:
    ids = sys.argv[1:] or []
    if not ids:
        print("usage: s17_m3_glossary.py C-SG1-U0004-02 ...")
        raise SystemExit(1)
    for i in ids:
        print(gloss(i))


if __name__ == "__main__":
    main()
