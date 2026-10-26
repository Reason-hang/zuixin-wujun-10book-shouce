#!/usr/bin/env python3
"""D07 沟通专题阶段 1：从 K 卡筛「沟」能力标签，生成簇索引草稿（人读出处）。"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out/D1_手册草稿/D07_沟通簇索引_草稿.md"
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
CID_RE = re.compile(r"^C-[A-Z0-9]+-U\d+-\d+$")
LIMIT = 40


def unit_title(uid: str) -> str:
    m = re.match(r"^([A-Z0-9]+)-U(\d+)$", uid)
    if not m:
        return uid
    p = ROOT / f"data/units/{m.group(1)}/unit_{int(m.group(2)):04d}.md"
    if not p.is_file():
        return uid
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            return ln[3:].strip()[:70]
    return uid


def main() -> None:
    rows: list[dict] = []
    for p in sorted((ROOT / "data/cards").rglob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            if c.get("disposal") == "X":
                continue
            tags = c.get("ability_tags") or []
            if "沟" not in tags:
                continue
            cid = c.get("claim_id", "")
            if not CID_RE.fullmatch(cid):
                continue
            uid = c.get("unit_id", d.get("unit_id", ""))
            bc = uid.split("-")[0] if uid else ""
            rows.append(
                {
                    "cid": cid,
                    "uid": uid,
                    "book": BOOK.get(bc, bc),
                    "title": unit_title(uid),
                    "claim": (c.get("claim_text") or "")[:70],
                    "key": c.get("concept_key", "") or "(无键)",
                }
            )
    by_key: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_key[r["key"]].append(r)
    keys = sorted(by_key.keys(), key=lambda k: (-len(by_key[k]), k))[:LIMIT]
    lines = [
        "# D07 沟通簇索引（草稿 · K 卡「沟」标签）\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}；`s17_d07_comm_cluster_index.py`\n",
        f"> 共扫描 **{len(rows)}** 张「沟」卡；本表取 **{len(keys)}** 个概念键代表条。**非** M3 过关证明，供 Q2 整合阅读。\n\n",
        "| 概念键 | 条数 | 代表论点（人读） | claim_id |\n",
        "|---|---:|---|---|\n",
    ]
    for k in keys:
        rep = by_key[k][0]
        human = f"{rep['book']} · {rep['title']} — {rep['claim']}"
        lines.append(f"| {k} | {len(by_key[k])} | {human} | `{rep['cid']}` |\n")
    lines.append(
        "\n**手册已覆盖（核心）**：M-D07-01/02/04/05、T-D07-01；路线图见 `D07_沟通专题_路线图_草稿.md`。\n"
    )
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"tags沟={len(rows)} keys={len(keys)} out={OUT}")


if __name__ == "__main__":
    main()
