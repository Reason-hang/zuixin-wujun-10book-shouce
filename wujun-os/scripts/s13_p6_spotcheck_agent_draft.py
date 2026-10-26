#!/usr/bin/env python3
"""P6 步 11：20 张抽查 — 锚点 + 说话人 + ngram 启发式 Agent 草稿（非「你的判断」签收）。"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "out/覆盖与质检报告/P6_用户抽查20张_草稿.md"
OUT = ROOT / "logs/p6_spotcheck_agent_draft_20261026.md"
THRESH = 0.12
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
CJK = re.compile(r"[\u4e00-\u9fff]")
CID_RE = re.compile(r"^C-[A-Z0-9]+-U+\d+-\d+$")


def ngrams(s: str, n: int = 4) -> set[str]:
    t = "".join(CJK.findall(s))
    if len(t) < n:
        return {t} if t else set()
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def book_text() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted((ROOT / "src_frozen").glob("*.md")):
        for key, code in BOOKS:
            if key in p.name:
                out[code] = p.read_text(encoding="utf-8")
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


def parse_table() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for ln in TABLE.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("| V-") or "C-" not in ln:
            continue
        parts = [p.strip() for p in ln.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        vid, cid = parts[0], parts[1]
        if CID_RE.fullmatch(cid):
            rows.append((vid, cid))
    return rows


def draft_judgment(anchor_ok: bool, rate: float, speaker: str, ev: str) -> str:
    if not anchor_ok:
        return "锚点FAIL（须改卡）"
    if "转述" in speaker or ev == "E2":
        return "ok（E2·转述；手册勿当吴军原话）"
    if rate < THRESH:
        return "待你回读（ngram 低）"
    return "ok（锚点+启发式）"


def main() -> int:
    books = book_text()
    cards = load_cards()
    rows = parse_table()
    lines = [
        "# P6 用户 20 张 · Agent 草稿判断（非签收）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}\n",
        "> 正式表「你的判断」列仍空；本文件 **≠** 步 11 过关。\n\n",
        "| V | claim_id | 锚点 | speaker | E | ngram | Agent 草稿 | 你确认 |\n",
        "|---|---|---|---|---|---:|---|---|\n",
    ]
    anchor_fail = 0
    for vid, cid in rows:
        c = cards.get(cid, {})
        a = c.get("anchor") or {}
        m_bc = re.match(r"^C-([A-Z0-9]+)-U", cid)
        bc = a.get("book_code") or (m_bc.group(1) if m_bc else "")
        speaker = c.get("speaker", "?")
        ev = c.get("evidence_level", "?")
        anchor_ok = False
        rate = 0.0
        if bc in books and a:
            ls, le = int(a.get("start_line", 0)), int(a.get("end_line", 0))
            try:
                seg = line_span(books[bc], ls, le)
                sha = hashlib.sha1(seg.encode("utf-8")).hexdigest()
                expect = a.get("sha1", "")
                anchor_ok = not expect or sha == expect
                g1, g2 = ngrams(c.get("claim_text", "")), ngrams(seg)
                rate = len(g1 & g2) / len(g1) if g1 and g2 else 0.0
            except (ValueError, IndexError):
                anchor_ok = False
        if not anchor_ok:
            anchor_fail += 1
        dj = draft_judgment(anchor_ok, rate, speaker, ev)
        lines.append(
            f"| {vid} | `{cid}` | {'PASS' if anchor_ok else 'FAIL'} | {speaker} | {ev} | {rate:.2f} | {dj} | |\n"
        )
    lines.append(f"\n锚点 FAIL: **{anchor_fail}** / {len(rows)}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"n={len(rows)} anchor_fail={anchor_fail} out={OUT}")
    return 1 if anchor_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
