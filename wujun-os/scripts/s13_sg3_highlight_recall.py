#!/usr/bin/env python3
"""G10③：来信3「划重点」要点对手册/K 卡召回（启发式，v2 AC-3.7 / P6 步 5）。

用法:
  python3 scripts/s13_sg3_highlight_recall.py --out logs/g10_sg3_highlight_recall.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u4e00-\u9fff]")
BULLET_RE = re.compile(r"^\s*\d+[、\.．)\）]\s*(.+)")
HEAD_RE = re.compile(r"^#{1,6}\s+")


def cjk_len(s: str) -> int:
    return len(CJK.findall(s))


def ngrams(s: str, n: int = 4) -> set[str]:
    t = "".join(CJK.findall(s))
    if len(t) < n:
        return {t} if t else set()
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def load_sg3_cards() -> tuple[dict[str, list[str]], str]:
    by_unit: dict[str, list[str]] = {}
    global_parts: list[str] = []
    for p in (ROOT / "data/cards").rglob("SG3-U*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        uid = d.get("unit_id", "")
        for c in d.get("cards", []):
            blob = " ".join(
                filter(
                    None,
                    [
                        c.get("claim_text", ""),
                        c.get("quote", ""),
                        c.get("notes", ""),
                        c.get("concept_key", ""),
                    ],
                )
            )
            if uid:
                by_unit.setdefault(uid, []).append(blob)
            global_parts.append(blob)
    d1 = ROOT / "out/D1_手册草稿"
    carry = d1 / "SG3_划重点承接表_草稿.md"
    hb_main: list[str] = []
    if d1.is_dir():
        for md in d1.glob("*.md"):
            if md.name.startswith("00_") or md.name == carry.name:
                continue
            hb_main.append(md.read_text(encoding="utf-8"))
    cards_blob = "\n".join(global_parts)
    hb_blob = "\n".join(hb_main)
    carry_blob = carry.read_text(encoding="utf-8") if carry.is_file() else ""
    full = "\n".join(x for x in (cards_blob, hb_blob, carry_blob) if x)
    no_carry = "\n".join(x for x in (cards_blob, hb_blob) if x)
    return by_unit, full, no_carry


def unit_letter_body(path: Path) -> tuple[str, str]:
    """unit_id, prose before「划重点」节（不含元数据头）。"""
    text = path.read_text(encoding="utf-8")
    uid = ""
    for line in text.splitlines()[:12]:
        if line.startswith("unit_id:"):
            uid = line.split(":", 1)[1].strip()
    body_lines: list[str] = []
    past_meta = False
    for line in text.splitlines():
        if line.strip() == "---" and not past_meta:
            past_meta = True
            continue
        if not past_meta:
            continue
        if "划重点" in line and HEAD_RE.match(line) and line.strip().endswith("划重点"):
            break
        body_lines.append(line)
    return uid, "\n".join(body_lines)


def extract_bullets(path: Path) -> list[tuple[str, str]]:
    """(unit_id, bullet_text)."""
    text = path.read_text(encoding="utf-8")
    uid = ""
    for line in text.splitlines()[:12]:
        if line.startswith("unit_id:"):
            uid = line.split(":", 1)[1].strip()
    bullets: list[tuple[str, str]] = []
    in_hz = False
    for line in text.splitlines():
        if "划重点" in line and HEAD_RE.match(line) and line.strip().endswith("划重点"):
            in_hz = True
            continue
        if in_hz and (HEAD_RE.match(line) or line.strip().startswith("![")):
            in_hz = False
        if in_hz and line.strip() in ("* * *", "---"):
            in_hz = False
        if not in_hz:
            continue
        m = BULLET_RE.match(line)
        if m and cjk_len(m.group(1)) >= 8:
            bullets.append((uid, m.group(1).strip()))
    return bullets


def overlap_bullet_blob(bullet: str, blob: str) -> bool:
    if not blob:
        return False
    bt = "".join(CJK.findall(bullet))
    if len(bt) >= 6 and bt[:6] in "".join(CJK.findall(blob)):
        return True
    for n in (3, 4):
        ng = ngrams(bullet, n)
        bg = ngrams(blob, n)
        if not ng or not bg:
            continue
        inter = len(ng & bg)
        if inter >= max(2, len(ng) // 6):
            return True
    return False


def matched(
    bullet: str,
    unit_id: str,
    by_unit: dict[str, list[str]],
    unit_body: dict[str, str],
    global_blob: str,
    disposal: str,
    *,
    allow_letter: bool,
) -> bool:
    if not allow_letter and disposal == "X":
        return True
    if allow_letter and overlap_bullet_blob(bullet, unit_body.get(unit_id, "")):
        return True
    for blob in by_unit.get(unit_id, []):
        if overlap_bullet_blob(bullet, blob):
            return True
    if bullet[:12] in global_blob:
        return True
    ng4 = ngrams(bullet, 4)
    if ng4:
        hit = sum(1 for g in ng4 if g in global_blob)
        if hit >= max(3, len(ng4) // 3):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units-dir", default="data/units/SG3")
    ap.add_argument("--out", default="logs/g10_sg3_highlight_recall.md")
    ap.add_argument("--threshold", type=float, default=0.95)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="仅对 K 卡+手册召回（不含同单元正文，用于 P6 门槛）",
    )
    args = ap.parse_args()
    by_unit, global_blob, global_no_carry = load_sg3_cards()
    disposal_map: dict[str, str] = {}
    uc = ROOT / "data/unitcards/uc_SG3.jsonl"
    if uc.is_file():
        for line in uc.read_text(encoding="utf-8").splitlines():
            if line.strip():
                u = json.loads(line)
                disposal_map[u["unit_id"]] = u.get("disposal") or ""
    unit_body: dict[str, str] = {}
    all_bullets: list[tuple[str, str]] = []
    for md in sorted((ROOT / args.units_dir).glob("unit_*.md")):
        uid, body = unit_letter_body(md)
        if uid:
            unit_body[uid] = body
        all_bullets.extend(extract_bullets(md))

    def score(allow_letter: bool, blob: str) -> tuple[int, list[str]]:
        ok_n = 0
        miss_l: list[str] = []
        for uid, b in all_bullets:
            if matched(
                b,
                uid,
                by_unit,
                unit_body,
                blob,
                disposal_map.get(uid, ""),
                allow_letter=allow_letter,
            ):
                ok_n += 1
            else:
                miss_l.append(f"{uid}: {b[:60]}…")
        return ok_n, miss_l

    ok_loose, _ = score(True, global_blob)
    ok_strict, miss_strict = score(False, global_blob)
    ok_core, miss_core = score(False, global_no_carry)

    total = len(all_bullets)
    rate_loose = ok_loose / total if total else 0.0
    rate_strict = ok_strict / total if total else 0.0
    rate_core = ok_core / total if total else 0.0
    lines = [
        "# G10③ 来信3 划重点召回\n",
        f"\n生成: {datetime.now().isoformat(timespec='seconds')}\n\n",
        f"| 指标 | 值 |\n|---|---|\n",
        f"| 划重点条目 | {total} |\n",
        f"| 召回（含同单元正文，健全性） | {rate_loose * 100:.1f}% |\n",
        f"| strict（K卡+手册+承接表） | {rate_strict * 100:.1f}% |\n",
        f"| strict（仅 K卡+手册章，无承接表） | {rate_core * 100:.1f}% |\n",
        f"| 门槛（strict 含承接表） | ≥{args.threshold * 100:.0f}% |\n\n",
    ]
    miss = miss_strict
    if args.strict:
        if rate_strict >= args.threshold:
            lines.append("**PASS**（strict 启发式；未命中须人工 M/X）\n\n")
            status = 0
        else:
            lines.append(
                f"**FAIL**（strict {rate_strict*100:.1f}% < 门槛，{len(miss)} 条）\n\n"
            )
            status = 1
    else:
        lines.append(
            "**INFO**：默认不判 FAIL；P6 以 `--strict` 为准（当前 strict 见上表）。\n\n"
        )
        status = 0
    if miss and (args.strict or rate_strict < args.threshold):
        lines.append("## 未命中样例（前 30）\n\n")
        for m in miss[:30]:
            lines.append(f"- {m}\n")
    backlog = ROOT / "logs/g10_sg3_highlight_miss_backlog.md"
    miss_for_carry = miss_core if miss_core else miss_strict
    if miss_for_carry:
        bl = [
            "# G10③ strict 未命中 backlog（P6 补卡/手册或标 M/X）\n\n",
            f"共 {len(miss_for_carry)} 条（来源：无承接表 strict）。X 层已计合规。\n\n",
        ]
        for m in miss_for_carry:
            bl.append(f"- {m}\n")
        backlog.write_text("".join(bl), encoding="utf-8")
    else:
        backlog.write_text(
            "# G10③ backlog\n\n当前无未命中（含承接表 strict 已过）。\n",
            encoding="utf-8",
        )
    out = ROOT / args.out
    out.write_text("".join(lines), encoding="utf-8")
    print(f"bullets={total} strict={rate_strict:.3f} out={out}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
