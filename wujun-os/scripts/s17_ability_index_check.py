#!/usr/bin/env python3
"""AC-5.6：能力速查四表须覆盖草稿中每张核心卡（按能力标签分表，可多表重复）。"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "out/D1_手册草稿"
CARD_RE = re.compile(r"^#### (M-D\d{2}-\d{2})\s")
TAG_RE = re.compile(r"能力标签：(.+?)(?:\||\｜)")
ABILITY_FILES = {
    "思": DRAFT / "能力速查_思.md",
    "做": DRAFT / "能力速查_做.md",
    "沟": DRAFT / "能力速查_沟.md",
    "学": DRAFT / "能力速查_学.md",
}
ABILITY_MAP = {"思": "思", "做": "做", "沟": "沟", "学": "学"}


def parse_cards() -> dict[str, set[str]]:
    """card_id -> set of ability keys"""
    cards: dict[str, set[str]] = {}
    for md in sorted(DRAFT.glob("[0-9][0-9]_*.md")):
        text = md.read_text(encoding="utf-8")
        blocks = re.split(r"(?=#### M-D)", text)
        for block in blocks:
            m = CARD_RE.match(block)
            if not m:
                continue
            cid = m.group(1)
            tm = TAG_RE.search(block)
            if not tm:
                cards[cid] = {"思"}
                continue
            raw = tm.group(1)
            tags: set[str] = set()
            for key in ABILITY_MAP:
                if key in raw:
                    tags.add(key)
            cards[cid] = tags or {"思"}
    return cards


def index_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return set(re.findall(r"M-D\d{2}-\d{2}", path.read_text(encoding="utf-8")))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="logs/s17_ability_index_latest.md")
    args = ap.parse_args()
    cards = parse_cards()
    table_ids = {k: index_ids(p) for k, p in ABILITY_FILES.items()}
    missing: list[str] = []
    for cid, tags in sorted(cards.items()):
        for t in tags:
            if cid not in table_ids.get(t, set()):
                missing.append(f"{cid} 缺于「{t}」表")
    lines = [
        "# AC-5.6 能力速查覆盖\n\n",
        f"核心卡数：**{len(cards)}**\n\n",
    ]
    if missing:
        lines.append(f"**FAIL**：{len(missing)} 项\n\n")
        for x in missing[:60]:
            lines.append(f"- {x}\n")
        status = 1
    else:
        lines.append("**PASS**：每张核心卡在其能力标签对应表中均有条目。\n")
        status = 0
    out = ROOT / args.out
    out.write_text("".join(lines), encoding="utf-8")
    print(f"cards={len(cards)} missing={len(missing)} -> {out}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
