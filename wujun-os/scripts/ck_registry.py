#!/usr/bin/env python3
"""ck_registry.py — 概念键全局注册表（P4 前置欠账②）

扫描全部论点卡目录，归一 concept_key（去空格；同键名合并），分配全局 CK 编号，
输出 data/rules/concept_keys.csv：global_ck, name, cards, books, sources
用法: python3 scripts/ck_registry.py
"""
import csv, glob, json, os, re
from collections import defaultdict

DIRS = ['data/pilot/cards_first', 'data/pilot/cards_second', 'data/pilot/batch2/N1',
        'data/pilot/batch2/N2', 'data/pilot/batch2/N3', 'data/pilot/batch2_recheck/N4',
        'data/gold/gate_c_20261024'] + sorted(glob.glob('data/cards/T-P3*'))

def norm(k):
    return re.sub(r'\s+', '', k or '').strip('，。；')

def main():
    stats = defaultdict(lambda: {'cards': 0, 'books': set(), 'units': set()})
    for d in DIRS:
        for p in glob.glob(os.path.join(d, '*.json')):
            try:
                data = json.load(open(p, encoding='utf-8'))
            except Exception:
                continue
            cards = data['cards'] if isinstance(data, dict) and 'cards' in data else (data if isinstance(data, list) else [])
            uid = data.get('unit_id') if isinstance(data, dict) else None
            book = (uid or p).split('-')[0].split('/')[-1]
            if isinstance(data, dict) and data.get('book_code'):
                book = data['book_code']
            for c in cards:
                raw = c.get('concept_key', '')
                # 代理批内编号（CK-xxxx）不透明：有 concept_name 时用命名，否则保留原值
                k = norm(c.get('concept_name') if re.fullmatch(r'CK-\d{3,4}', raw or '') and c.get('concept_name') else raw)
                if not k:
                    continue
                stats[k]['cards'] += 1
                stats[k]['books'].add(book)
                stats[k]['units'].add(uid or '?')

    rows = sorted(stats.items(), key=lambda x: (-x[1]['cards'], x[0]))
    out = 'data/rules/concept_keys.csv'
    os.makedirs('data/rules', exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['global_ck', 'name', 'cards', 'books', 'units', 'cross_book'])
        for i, (k, s) in enumerate(rows, 1):
            w.writerow([f'CK-{i:04d}', k, s['cards'], '|'.join(sorted(s['books'])), len(s['units']), 'Y' if len(s['books']) > 1 else ''])
    multi = sum(1 for k, s in stats.items() if len(s['books']) > 1)
    print(f'概念键归一: {len(stats)} 个唯一键（跨书复用 {multi} 个）-> {out}')
    print('高频前 10:', [(k, s['cards']) for k, s in rows[:10]])

if __name__ == '__main__':
    main()
