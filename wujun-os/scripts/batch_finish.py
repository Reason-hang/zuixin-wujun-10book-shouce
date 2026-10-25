#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_finish.py — 批次收尾器（J-117 提速工具 3）

一条命令完成批次三件收尾事：①官方 verify（0 FAIL 才继续，否则退出码 1）；
②uc 回写（disposal+batch_id，幂等）；③统计输出（卡数/E 分布/说话人/批内
同名键），并附 journal 素材行。不做 state 刷新、journal、git——留给主智能体。

用法（在 wujun-os/ 执行）：
  python3 scripts/batch_finish.py <batch_id> <batch_dir> <uc_path> [--out 报告路径]
例：
  python3 scripts/batch_finish.py T-P3b-B-047 data/cards/T-P3b-B-047 data/unitcards/uc_SG3.jsonl
"""
import json, glob, sys, subprocess, os
from collections import Counter

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    batch_id, batch_dir, uc_path = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    # ① 官方 verify（GATE-B 闸门不跳过）
    rep = out or f"logs/cards_verify_{batch_id}_finish.md"
    r = subprocess.run(["python3", "scripts/verify_cards.py", "--dirs", batch_dir, "--out", rep],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if "FAIL 0" not in (r.stdout + r.stderr):
        sys.exit("verify 未过 0 FAIL，中止回写")
    # ② uc 回写（幂等）
    cards_by_unit = {}
    for f in sorted(glob.glob(os.path.join(batch_dir, "*.json"))):
        d = json.load(open(f))
        cards_by_unit[d["unit_id"]] = d
    rows = [json.loads(l) for l in open(uc_path)]
    n = 0
    for row in rows:
        if row["unit_id"] in cards_by_unit:
            row["disposal"] = cards_by_unit[row["unit_id"]]["unit_disposal"]
            row["batch_id"] = batch_id
            n += 1
    covered = len(cards_by_unit)
    if n != covered:
        sys.exit(f"覆盖不足：uc 命中 {n} != 批内 {covered} 单元，中止")
    with open(uc_path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    # ③ 统计
    ev, sp, ck, tot = Counter(), Counter(), Counter(), 0
    for d in cards_by_unit.values():
        for c in d["cards"]:
            tot += 1; ev[c["evidence_level"]] += 1; sp[c["speaker"]] += 1
            ck[c["concept_key"]] += 1
    dup = [k for k, v in ck.items() if v > 1]
    k_units = sum(1 for d in cards_by_unit.values() if d["unit_disposal"] == "K")
    print(f"回写 {n} 行；覆盖 {covered}/{covered}")
    print(f"卡 {tot} | {dict(ev)} | {dict(sp)} | 唯一键 {len(ck)} | 批内同名键 {dup if dup else '无'}")
    print(f"JOURNAL素材: {batch_id} 完成：{covered} 单元 {tot} 卡（K{k_units}），"
          f"E1×{ev.get('E1',0)}/E2×{ev.get('E2',0)}/E3×{ev.get('E3',0)}，"
          f"X 处置 {sum(len(d['x_disposals']) for d in cards_by_unit.values())} 条，"
          f"verify 0 FAIL、覆盖 {covered}/{covered}、uc 回写。批内同名键{'：'+'、'.join(dup) if dup else ' 0'}")

if __name__ == "__main__":
    main()
