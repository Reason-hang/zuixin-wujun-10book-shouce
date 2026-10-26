#!/usr/bin/env python3
"""AC-3.6 子步骤：对抽检表内 claim_id 做锚点 SHA1 复验（位置真实，非语义召回）。"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AC36 = ROOT / "out/覆盖与质检报告/AC36_抽检召回表_草稿.md"
OUT = ROOT / "logs/ac36_anchor_ping_latest.md"

BOOKS = [
    ("来信1", "SG1"),
    ("吴军来信2", "WJ2"),
    ("硅谷来信3", "SG3"),
    ("谷歌方法论", "GG"),
    ("见识", "JS"),
    ("数学通识", "SX"),
    ("格局", "GJ"),
    ("境界", "JJ"),
    ("富足", "FZ"),
    ("态度", "TD"),
]


def book_files() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for p in sorted((ROOT / "src_frozen").glob("*.md")):
        for key, code in BOOKS:
            if key in p.name:
                out[code] = (p.name, p.read_text(encoding="utf-8"))
                break
    return out


def line_span(text: str, ls: int, le: int) -> str:
    lines = text.split("\n")
    starts = []
    pos = 0
    for line in lines:
        starts.append(pos)
        pos += len(line) + 1
    cs = starts[ls - 1]
    ce = starts[le - 1] + len(lines[le - 1])
    return text[cs:ce]


def load_cards() -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    for p in (ROOT / "data/cards").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            cid = c.get("claim_id")
            if cid:
                by_id[cid] = c
    return by_id


def claim_ids_from_ac36() -> list[str]:
    if not AC36.is_file():
        return []
    ids: list[str] = []
    for ln in AC36.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|"):
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 2 or not parts[0].isdigit():
            continue
        cid = parts[1]
        if re.fullmatch(r"C-[A-Z0-9]+-U\d+-\d+", cid):
            ids.append(cid)
    return ids


def main() -> int:
    books = book_files()
    cards = load_cards()
    ids = claim_ids_from_ac36()
    ok = fail = miss = 0
    fails: list[str] = []
    for cid in ids:
        c = cards.get(cid)
        if not c:
            miss += 1
            fails.append(f"{cid}: 无卡")
            continue
        a = c.get("anchor") or {}
        bc = a.get("book_code", "")
        if not bc:
            m = re.match(r"^C-([A-Z0-9]+)-U", cid)
            if m:
                bc = m.group(1)
        if bc not in books:
            fail += 1
            fails.append(f"{cid}: 无书文件 {bc}")
            continue
        _, text = books[bc]
        ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
        try:
            seg = line_span(text, ls, le)
        except (ValueError, IndexError):
            fail += 1
            fails.append(f"{cid}: 行号越界")
            continue
        sha = hashlib.sha1(seg.encode("utf-8")).hexdigest()
        expect = a.get("sha1", "")
        if expect and sha != expect:
            fail += 1
            fails.append(f"{cid}: sha 漂移")
        else:
            ok += 1
    lines = [
        "# AC-3.6 锚点位置复验（子集）\n\n",
        f"生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
        f"| 样本 | {len(ids)} |\n|---|---|\n",
        f"| PASS | {ok} |\n| FAIL | {fail} |\n| 无卡 | {miss} |\n\n",
    ]
    if fails:
        lines.append("## 失败样例（前 20）\n\n")
        for f in fails[:20]:
            lines.append(f"- {f}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"ids={len(ids)} ok={ok} fail={fail} miss={miss} out={OUT}")
    return 1 if fail or miss else 0


if __name__ == "__main__":
    raise SystemExit(main())
