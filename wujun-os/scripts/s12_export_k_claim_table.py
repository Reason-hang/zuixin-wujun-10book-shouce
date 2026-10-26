#!/usr/bin/env python3
"""导出论点卡表（D3 子表，自冻结 K 卡 JSON）。列序对齐 v2 §16.7（可空列留空）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ledger/论点卡表_草稿.md"


def cell(v: object) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        s = ",".join(str(x) for x in v)
    else:
        s = str(v)
    return s.replace("|", "｜").replace("\n", " ").strip()


def main() -> None:
    rows: list[str] = []
    for p in sorted((ROOT / "data/cards").rglob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for c in d.get("cards", []):
            cid = c.get("claim_id", "")
            if not cid:
                continue
            pillars = c.get("pillar_final") or c.get("pillar_candidates") or []
            rows.append(
                "| "
                + " | ".join(
                    [
                        cell(cid),
                        cell(c.get("unit_id", d.get("unit_id", ""))),
                        cell(c.get("speaker", "")),
                        cell(c.get("claim_text", ""))[:120],
                        cell(c.get("evidence_level", "")),
                        cell(c.get("disposal", "K")),
                        cell(c.get("concept_key", "")),
                        cell(pillars),
                        cell(c.get("ability_tags", "")),
                        cell(c.get("aux_tags", c.get("auxiliary_tags", ""))),
                        cell(c.get("stability", "")),
                        cell(c.get("math_mapping", "")),
                    ]
                )
                + " |"
            )
    header = (
        "# 论点卡表（草稿 · D3 子表）\n\n"
        "> `scripts/s12_export_k_claim_table.py`；与 `data/cards` 冻结包一致。\n\n"
        "| 卡ID | 单元ID | 说话人 | 论点转述 | 类型 | 处置 | 概念键 | 支柱候选 | 能力标签 | 辅助标签 | 稳定度 | 数理映射 |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    OUT.write_text(header + "\n".join(sorted(rows)) + "\n", encoding="utf-8")
    print(f"rows={len(rows)} out={OUT}")


if __name__ == "__main__":
    main()
