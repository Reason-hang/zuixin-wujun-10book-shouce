#!/usr/bin/env python3
"""G9 子集：单元↔处置↔K 卡文件闭环（非手册 M 卡↔论点全链）。。"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs/g9_subset_check_latest.md"


def load_units() -> set[str]:
    ids: set[str] = set()
    with (ROOT / "data/units/units_index.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ids.add(row["unit_id"])
    return ids


def load_unitcards() -> dict[str, str]:
    by_id: dict[str, str] = {}
    for p in (ROOT / "data/unitcards").glob("uc_*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            u = json.loads(line)
            by_id[u["unit_id"]] = u.get("disposal", "?")
    return by_id


def card_units() -> set[str]:
    units: set[str] = set()
    for p in (ROOT / "data/cards").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        uid = d.get("unit_id") or p.stem
        units.add(uid)
        for c in d.get("cards", []):
            if c.get("unit_id"):
                units.add(c["unit_id"])
    return units


def main() -> int:
    unit_ids = load_units()
    uc = load_unitcards()
    card_u = card_units()
    missing_uc = sorted(unit_ids - set(uc.keys()))
    extra_uc = sorted(set(uc.keys()) - unit_ids)
    k_units = {uid for uid, d in uc.items() if d == "K"}
    k_no_file = sorted(uid for uid in k_units if uid not in card_u)
    card_orphan = sorted(card_u - unit_ids)
    ok = not missing_uc and not extra_uc and not k_no_file and not card_orphan
    lines = [
        "# G9 处置闭环子集检查\n\n",
        f"> 生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
        f"| 指标 | 值 |\n|---|---:|\n",
        f"| 单元索引 | {len(unit_ids)} |\n",
        f"| unitcards 行 | {len(uc)} |\n",
        f"| 索引无处置行 | {len(missing_uc)} |\n",
        f"| 处置行无索引 | {len(extra_uc)} |\n",
        f"| disposal=K 无卡文件 | {len(k_no_file)} |\n",
        f"| 卡 unit 不在索引 | {len(card_orphan)} |\n\n",
        f"**判定**: {'PASS' if ok else 'FAIL'}\n\n",
    ]
    if missing_uc:
        lines.append("## 索引缺 unitcard（前 15）\n\n")
        for u in missing_uc[:15]:
            lines.append(f"- {u}\n")
    if k_no_file:
        lines.append("\n## K 单元无 JSON（前 15）\n\n")
        for u in k_no_file[:15]:
            lines.append(f"- {u}\n")
    if card_orphan:
        lines.append("\n## 卡孤儿 unit（前 15）\n\n")
        for u in card_orphan[:15]:
            lines.append(f"- {u}\n")
    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"ok={ok} out={OUT}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
