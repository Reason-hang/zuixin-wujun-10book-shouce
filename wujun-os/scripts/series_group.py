#!/usr/bin/env python3
"""series_group.py — 系列单元成组（P2 遗留 T-P2-06）

标题与探测器同源：import s01_probe 的 load/split_units 取标题，SERIES 同源正则识别，
同书同主干归组，写回 unitcards 的 series_group。断言：系列单元总数 == 91（基线）。
用法: python3 scripts/series_group.py
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import s01_probe

SERIES = s01_probe.SERIES
STAMP = re.compile(r'[（(](?:上|下|中|一|二|三|四|五)[）)]|[上下]篇|之[一二三四]')

def main():
    src = 'src_frozen'
    allu = s01_probe.load(src)
    series_titles = {}   # unit 序号(1-based per book) -> title
    counts = {}
    for kw, disp, code, lvl in s01_probe.BOOKS:
        units = s01_probe.split_units(allu[code]['text'], lvl)
        for i, u in enumerate(units, 1):
            if SERIES.search(u['title']):
                series_titles.setdefault(code, {})[i] = u['title']
        counts[code] = sum(1 for u in units if SERIES.search(u['title']))
    total = sum(counts.values())
    print('逐书系列单元:', counts, '合计', total)

    n_tagged = 0
    for jl in sorted(glob.glob('data/unitcards/uc_*.jsonl')):
        out, groups = [], {}
        for line in open(jl, encoding='utf-8'):
            c = json.loads(line)
            c.pop('series_group', None)
            out.append(c)
        code = out[0]['book_code']
        for c in out:
            n = int(c['unit_id'].split('U')[1])
            t = series_titles.get(code, {}).get(n)
            if t:
                stem = STAMP.sub('', t).strip()
                key = (code, stem)
                gid = groups.setdefault(key, f"SG-{code}-{len(groups)+1:03d}")
                c['series_group'] = gid
                n_tagged += 1
        with open(jl, 'w', encoding='utf-8') as f:
            for c in out:
                f.write(json.dumps(c, ensure_ascii=False) + '\n')
    ok = (total == 91) and (n_tagged == total)
    print(f'成组写入 {n_tagged} 个（基线 91 → {"PASS" if ok else "FAIL"}）')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
