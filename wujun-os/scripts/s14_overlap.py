#!/usr/bin/env python3
"""s14_overlap.py — S14 双盲重抽重合率计算（T-P1-06 / GATE-C 漂移回归同口径）

用法（在 wujun-os/ 执行）:
  python3 scripts/s14_overlap.py --first data/pilot/cards_first --second data/pilot/cards_second --out logs/p1_overlap.md --mode attr

匹配模式（rules_v0.9.md R2 双档）:
  strict  严口径: 主归属 pillar_candidates[0] 相等（漂移监控报告用）
  attr    归属口径: 候选集有交集即算归属匹配（放行判定用，v0.9 起默认）
满足归属匹配后，任一即算卡匹配: a) 锚点行区间交集（同书） b) 概念键相同 c) 指纹词交集 ≥1
重合率 = 2×匹配对数 / (|首抽|+|重抽|)   （双边加权，惩罚两边数量失衡）
通过线: ≥0.7（v2 §15.12 / 稳定性方案 M8）
"""
import argparse, glob, json, os

def load(d):
    cards = []
    for p in sorted(glob.glob(os.path.join(d, '*.json'))):
        data = json.load(open(p, encoding='utf-8'))
        if isinstance(data, dict) and 'cards' in data:   # {unit_id, cards:[...]} 包装格式
            data = data['cards']
        if isinstance(data, list):
            cards += [c for c in data if isinstance(c, dict)]
        elif isinstance(data, dict):
            cards.append(data)
    # 无锚点的卡（如读者上下文卡）不参与锚点匹配，补空锚点避免崩溃
    for c in cards:
        if not c.get('anchor') or 'start_line' not in (c.get('anchor') or {}):
            c['anchor'] = {'book_code': c.get('unit_id', '?').split('-')[0], 'start_line': 0, 'end_line': -1, 'fingerprint': []}
            c['_no_anchor'] = True
    return cards

def spans_overlap(a, b):
    return a['book_code'] == b['book_code'] and not (a['end_line'] < b['start_line'] or b['end_line'] < a['start_line'])

def match(c1, c2, mode='attr'):
    p1, p2 = c1.get('pillar_candidates') or ['?'], c2.get('pillar_candidates') or ['?']
    if mode == 'strict':
        if p1[0] != p2[0]:
            return False
    else:  # attr: 候选集交集（DT-待判 视为不匹配任何具体柱）
        if not (set(p1) & set(p2)) - {'DT-待判'}:
            return False
    if spans_overlap(c1['anchor'], c2['anchor']):
        return True
    if c1.get('concept_key', '').strip() and c1.get('concept_key', '').strip() == c2.get('concept_key', '').strip():
        return True
    fp1, fp2 = set(c1['anchor'].get('fingerprint', [])), set(c2['anchor'].get('fingerprint', []))
    return bool(fp1 & fp2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--first', required=True)
    ap.add_argument('--second', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--mode', choices=['strict', 'attr'], default='attr')
    args = ap.parse_args()

    A, B = load(args.first), load(args.second)
    used_b = set()
    pairs = []
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            if j in used_b:
                continue
            if match(a, b, args.mode):
                used_b.add(j)
                pairs.append((a, b))
                break
    overlap = 2 * len(pairs) / (len(A) + len(B)) if (A and B) else 0.0
    verdict = 'PASS' if overlap >= 0.7 else 'FAIL'

    L = [f'# S14 双盲重抽重合率（脚本产出，勿手改；模式={args.mode}）', '',
         f'- 首抽卡数: {len(A)}　重抽卡数: {len(B)}　匹配对: {len(pairs)}　模式: {args.mode}',
         f'- 重合率: {overlap:.3f}（通过线 ≥0.7）→ **{verdict}**', '',
         '| 首抽卡 | 重抽卡 | 主归属 | 匹配依据 |', '|---|---|---|---|']
    for a, b in pairs:
        basis = []
        if spans_overlap(a['anchor'], b['anchor']):
            basis.append('锚点交叠')
        if a.get('concept_key', '') == b.get('concept_key', ''):
            basis.append('概念键相同')
        elif set(a['anchor'].get('fingerprint', [])) & set(b['anchor'].get('fingerprint', [])):
            basis.append('指纹词交集')
        L.append(f"| {a['claim_id']} | {b['claim_id']} | {(a.get('pillar_candidates') or ['?'])[0]} | {'+'.join(basis)} |")
    L += ['', '## 未匹配卡', '']
    for i, a in enumerate(A):
        if not any(a['claim_id'] == pa['claim_id'] for pa, _ in pairs):
            L.append(f"- 首抽 {a['claim_id']}（{a.get('claim_text', '')[:30]}… 主归属 {(a.get('pillar_candidates') or ['?'])[0]}）")
    for j, b in enumerate(B):
        if j not in used_b:
            L.append(f"- 重抽 {b['claim_id']}（{b.get('claim_text', '')[:30]}… 主归属 {(b.get('pillar_candidates') or ['?'])[0]}）")

    open(args.out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'S14 重合率: {overlap:.3f}（{len(A)} vs {len(B)} 卡，匹配 {len(pairs)} 对）→ {verdict}；报告 {args.out}')
    raise SystemExit(0 if verdict == 'PASS' else 1)

if __name__ == '__main__':
    main()
