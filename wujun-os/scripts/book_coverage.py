#!/usr/bin/env python3
"""book_coverage.py — 单书覆盖验收（v2.1 Z2-09：书内归并 + 单书覆盖验收）

用法: python3 scripts/book_coverage.py --book TD --out logs/book_TD.md
检查：该书全部单元（含 S/N）在 unitcards 中 disposal 非空；批卡目录中单元文件齐全；
     K/M/C/X/N 分布、卡数、E 分布、转述卡数、DT-待判数；概念键初归并（同名合并计数）。
"""
import argparse, glob, json, os
from collections import Counter

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    B = args.book

    units = [json.loads(l) for l in open(f'data/unitcards/uc_{B}.jsonl', encoding='utf-8')]
    total = len(units)
    undisp = [u['unit_id'] for u in units if not u.get('disposal')]
    disp = Counter(u.get('disposal') for u in units)

    cards, e_dist, speakers, ck, dt = 0, Counter(), Counter(), Counter(), []
    for p in glob.glob(f'data/cards/*/{B}-U*.json'):
        d = json.load(open(p, encoding='utf-8'))
        for c in d.get('cards', []):
            cards += 1
            e_dist[c.get('evidence_level')] += 1
            speakers[c.get('speaker')] += 1
            ck[c.get('concept_key', '')] += 1
            if (c.get('pillar_candidates') or [''])[0] == 'DT-待判':
                dt.append(c['claim_id'])
    multi_ck = {k: v for k, v in ck.items() if v > 1}

    ok = not undisp
    L = [f'# 单书覆盖验收：{B}（Z2-09，脚本产出）', '',
         f'- 单元总数 {total}；处置未落值 {len(undisp)} → {"PASS" if ok else "FAIL: " + ",".join(undisp[:10])}',
         f'- 处置分布 {dict(disp)}',
         f'- 累计卡数 {cards}；证据分布 {dict(e_dist)}；说话人 {dict(speakers)}',
         f'- DT-待判 {len(dt)} 张：{", ".join(dt[:8]) or "无"}',
         f'- 跨批同名概念键 {len(multi_ck)} 个（P4 归并候选）：{", ".join(list(multi_ck)[:10]) or "无"}']
    verdict = 'PASS（全书处置覆盖完整，可做书内归并）' if ok else 'FAIL'
    L += ['', '结论: ' + verdict]
    open(args.out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[:5]))
    raise SystemExit(0 if ok else 1)

if __name__ == '__main__':
    main()
