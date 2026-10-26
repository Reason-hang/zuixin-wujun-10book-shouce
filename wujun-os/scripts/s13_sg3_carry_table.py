#!/usr/bin/env python3
"""由 G10③ miss backlog 生成 SG3 划重点承接表（P6 可追溯，供 strict 召回语料）。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u4e00-\u9fff]")
OUT = ROOT / "out/D1_手册草稿/SG3_划重点承接表_草稿.md"


def cjk(s: str) -> str:
    return "".join(CJK.findall(s))


def ngrams(s: str, n: int = 3) -> set[str]:
    t = cjk(s)
    if len(t) < n:
        return {t} if t else set()
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def load_unit_cards() -> dict[str, list[dict]]:
    by_u: dict[str, list[dict]] = {}
    for p in (ROOT / "data/cards").rglob("SG3-U*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        uid = d.get("unit_id", "")
        by_u.setdefault(uid, []).extend(d.get("cards", []))
    return by_u


def best_claim(bullet: str, cards: list[dict]) -> dict | None:
    if not cards:
        return None
    best = None
    best_score = 0
    ng = ngrams(bullet, 3)
    for c in cards:
        blob = " ".join(
            filter(
                None,
                [c.get("claim_text", ""), c.get("quote", ""), c.get("concept_key", "")],
            )
        )
        score = len(ng & ngrams(blob, 3)) if ng else 0
        if score > best_score:
            best_score = score
            best = c
    return best or cards[0]


def parse_backlog() -> list[tuple[str, str]]:
    p = ROOT / "logs/g10_sg3_highlight_miss_backlog.md"
    if not p.is_file():
        return []
    rows: list[tuple[str, str]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("- SG3-U"):
            continue
        body = line[2:].strip()
        uid, rest = body.split(":", 1)
        bullet = rest.strip().rstrip("…").strip()
        rows.append((uid.strip(), bullet))
    return rows


def main() -> None:
    by_u = load_unit_cards()
    misses = parse_backlog()
    lines = [
        "# SG3 划重点承接表（草稿 · P6 G10③）\n\n",
        "> 由 `s13_sg3_carry_table.py` 自 strict miss backlog 生成；"
        "承接句摘自同单元 K 卡 `claim_text`（非新观点）。\n\n",
        "| 单元 | 划重点摘要 | claim_id | 承接句（K 卡） |\n",
        "|---|---|---|---|\n",
    ]
    for uid, bullet in misses:
        cards = by_u.get(uid, [])
        c = best_claim(bullet, cards)
        if c:
            cid = c.get("claim_id", "")
            carry = (c.get("claim_text") or "")[:120].replace("|", "｜")
            summ = bullet[:48].replace("|", "｜") + ("…" if len(bullet) > 48 else "")
            lines.append(f"| {uid} | {summ} | {cid} | {carry} |\n")
        else:
            summ = bullet[:48].replace("|", "｜")
            lines.append(f"| {uid} | {summ} | — | （X/无卡，待 P6 标 M/X） |\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"rows={len(misses)} out={OUT}")


if __name__ == "__main__":
    main()
