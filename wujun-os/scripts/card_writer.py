#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
card_writer.py — 论点卡断言前置写盘器（J-117 提速工具 2）

消除三类高频错误源：①SHA1 手抄错（工具从原书重算）②Python 字典字面量的
quote=/notes= 漏等号 SyntaxError（卡片改为 JSON 管道传入）③指纹词凭记忆
书写（工具逐字校验锚内子串）。只前移校验，不替代官方 verify_cards（GATE-B）。

用法（在 wujun-os/ 执行）：
  python3 scripts/card_writer.py <unit_id> <batch_dir> <book_path> <w0> <w1> \
      --extractor EXT-XX --batch-id T-P3b-B-XXX --disposal K \
      --reason "..." --x-disposals-file /tmp/xd.json [--dry-run] \
      < cards.json

cards.json（stdin，UTF-8 JSON 数组）：每卡含 speaker/claim_text/quote/
anchor{book_code,start_line,end_line,fingerprint}/evidence_level/
pillar_candidates/concept_key/ability_tags/notes；sha1/claim_id/unit_id/status
由本工具生成，传入即忽略。anchor.book_code 可省略（默认取 unit_id 前缀）。
"""
import json, hashlib, os, re, sys, argparse

SPEAKERS = ("吴军本人", "转述·", "史实·", "读者·", "编校转录", "嘉宾", "待核")
EVID = ("E1", "E2", "E3", "E4")
TAGS = ("思", "学", "沟", "做")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("unit_id")
    ap.add_argument("batch_dir")
    ap.add_argument("book_path")
    ap.add_argument("w0", type=int)
    ap.add_argument("w1", type=int)
    ap.add_argument("--extractor", default="R-ORCH-inline")
    ap.add_argument("--batch-id", required=True)
    ap.add_argument("--disposal", default="K")
    ap.add_argument("--reason", default="")
    ap.add_argument("--x-disposals-file")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.w1 < a.w0:
        sys.exit("行窗非法")
    cards = json.load(sys.stdin)
    if not isinstance(cards, list) or not cards:
        sys.exit("stdin 须为非空 JSON 数组")
    lines = open(a.book_path, encoding="utf-8").read().split("\n")
    num = int(a.unit_id.split("-U")[1])
    book_code = a.unit_id.split("-U")[0]
    errs = []
    for i, c in enumerate(cards, 1):
        cid = f"C-{book_code}-U{num:04d}-{i:02d}"
        sp = c.get("speaker", "吴军本人")
        if not sp.startswith(SPEAKERS):
            errs.append(f"{cid} speaker 非法: {sp!r}")
        if c.get("evidence_level") not in EVID:
            errs.append(f"{cid} E级非法: {c.get('evidence_level')}");
        if len(c.get("claim_text", "")) > 60 or not c.get("claim_text"):
            errs.append(f"{cid} claim 超长或为空"); continue
        tags = c.get("ability_tags", [])
        if not tags or len(tags) > 2 or any(t not in TAGS for t in tags):
            errs.append(f"{cid} 标签非法: {tags}"); continue
        for p in c.get("pillar_candidates", []):
            if not re.fullmatch(r"D\d{2}-\d", p):
                errs.append(f"{cid} 柱码非法 {p}")
        anch = c.get("anchor", {})
        s, e = anch.get("start_line"), anch.get("end_line")
        if not (isinstance(s, int) and isinstance(e, int) and a.w0 <= s <= e <= a.w1):
            errs.append(f"{cid} 行窗越界 {s}-{e} ∉ {a.w0}-{a.w1}"); continue
        span = "\n".join(lines[s - 1:e])
        if len(span) > 800:
            errs.append(f"{cid} 锚超800（{len(span)}）")
        q = c.get("quote", "")
        if not (0 < len(q) <= 15) or q not in span:
            errs.append(f"{cid} quote 非法: {q!r}")
        fps = anch.get("fingerprint", [])
        if not (1 <= len(fps) <= 3) or any(f not in span for f in fps):
            errs.append(f"{cid} 指纹词非法: {fps}")
        if not c.get("concept_key"):
            errs.append(f"{cid} 缺 concept_key")
        c.setdefault("status", "已生成")
        if c["status"] != "已生成":
            errs.append(f"{cid} status 非法")
        # 就地补全（断言全过后）
        anch["book_code"] = anch.get("book_code", book_code)
        anch["sha1"] = hashlib.sha1(span.encode("utf-8")).hexdigest()
        c["claim_id"], c["unit_id"] = cid, a.unit_id
    if errs:
        print("\n".join(errs))
        sys.exit(f"FAIL {len(errs)} 项，未写盘")
    out_dir = a.batch_dir if os.path.isabs(a.batch_dir) else a.batch_dir
    path = os.path.join(out_dir, f"{a.unit_id}.json")
    doc = {
        "unit_id": a.unit_id, "book_code": book_code, "extractor": a.extractor,
        "batch_id": a.batch_id, "cards": cards,
        "x_disposals": (json.load(open(a.x_disposals_file)) if a.x_disposals_file else []),
        "unit_disposal": a.disposal, "unit_disposal_reason": a.reason,
    }
    if a.dry_run:
        print(f"DRY-RUN PASS {a.unit_id}: {len(cards)} 卡（断言全过，未写盘）")
        return
    if os.path.exists(path):
        sys.exit(f"防覆盖拦截：{path} 已存在")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"OK {a.unit_id}: {len(cards)} 卡 -> {path}")


if __name__ == "__main__":
    main()
