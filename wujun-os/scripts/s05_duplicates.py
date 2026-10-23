#!/usr/bin/env python3
"""s05_duplicates.py — P0 书内 + 跨书重复扫描（S05，总闸 G6）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s05_duplicates.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g6.md
作用: 复用 s01_probe 的 paras()/probe() 口径（≥40 汉字、非列表/图片/引用/标题行的整段），扫描
  (1) 书内重复: 同书出现 >1 次的段落数（预期 GG 28、GJ 1、SG3 2、WJ2 5，共 36 处）
  (2) 跨书精确重复: 两书段落集合交集（预期 118 段 / 8,884 字，其中 GG↔SG1 107 段 / 8,023 字）
并把每条重复段落登记到所在单元（双出处登记），供 P1 抽卡时两处来源并记。
数字与 spec/baseline_facts.json probe.dup_inbook / probe.dup_cross 逐项比对，任何不符退出码非零。
"""
import argparse, collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

def para_unit_index(units):
    """书内 段落全文 -> 出现它的单元序号列表（1 起）。段落口径与 s01_probe.paras 完全一致。"""
    idx = {}
    for i, u in enumerate(units, 1):
        for l in u['text'].split('\n'):
            s = l.strip()
            if s01_probe.cjk(s) >= 40 and not re.match(r'^([-*]\s*\[|!\[|>|#)', s):
                idx.setdefault(s, []).append(i)
    return idx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--out', default='logs/g6.md')
    a = ap.parse_args()
    f = s01_probe.probe(a.src)
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    B = s01_probe.load(a.src)
    allu = {c: s01_probe.split_units(d['text'], d['lvl']) for c, d in B.items()}
    pidx = {c: para_unit_index(allu[c]) for c in B}
    P = {c: s01_probe.paras(B[c]['text']) for c in B}
    problems = []

    ib = {c: n for c, n in f['dup_inbook'].items()}
    if ib != base['dup_inbook']:
        problems.append(f'书内重复与基线不符: 本次 {ib} / 基线 {base["dup_inbook"]}')
    dc = f['dup_cross']
    if (dc['paragraphs'], dc['chars'], dc['pairs']) != (base['dup_cross']['paragraphs'], base['dup_cross']['chars'], base['dup_cross']['pairs']):
        problems.append(f'跨书重复与基线不符: 本次 {dc["paragraphs"]} 段/{dc["chars"]} 字 {dc["pairs"]} / '
                        f'基线 {base["dup_cross"]["paragraphs"]} 段/{base["dup_cross"]["chars"]} 字 {base["dup_cross"]["pairs"]}')

    g = []
    g.append('# G6 重复扫描（S05）\n')
    g.append(f'- 源: `{a.src}`；口径复用 scripts/s01_probe.paras（≥40 汉字整段、排除列表/图片/引用/标题行）\n'
             f'- 结论: **{"FAIL" if problems else "PASS"}**（与基线比对不一致 {len(problems)} 项）\n')
    g.append('## 1. 跨书精确重复（重复簇表）\n\n| 书对 | 段落数 | 汉字数 | 与基线 |\n|---|---|---|---|\n')
    for k in sorted(base['dup_cross']['pairs']):
        v, b = dc['pairs'].get(k, {}), base['dup_cross']['pairs'][k]
        ok = '一致' if v == b else '不一致'
        g.append(f'| {k} | {v.get("paragraphs", 0)} | {v.get("chars", 0):,} | {ok} |\n')
    g.append(f'| **合计** | **{dc["paragraphs"]}** | **{dc["chars"]:,}** | {"一致" if not problems else "见不一致项"} |\n')
    g.append('\n## 2. 书内重复\n\n| 书 | 重复段落数（出现>1次的段落） | 与基线 |\n|---|---|---|\n')
    for c in sorted(base['dup_inbook']):
        g.append(f'| {c} | {ib.get(c, 0)} | {"一致" if ib.get(c) == base["dup_inbook"][c] else "不一致"} |\n')
    g.append(f'| **合计** | **{sum(ib.values())}** | |\n')

    g.append('\n## 3. 双出处登记（跨书重复段落到单元）\n')
    for k in sorted(dc['pairs']):
        x, y = k.split('<->')
        inter = sorted(set(P[x]) & set(P[y]))
        g.append(f'\n### {k}（{len(inter)} 段 / {dc["pairs"][k]["chars"]:,} 字）\n\n'
                 f'定性: 两书同载相同段落，**双出处登记**——P1 抽卡命中以下段历时，两个单元都要登记来源，收敛为一张卡（v2 方案 §15 同义重复处置）。\n\n'
                 f'| # | {x} 单元 | {y} 单元 | 段落（前 28 字） |\n|---|---|---|---|\n')
        for i, p in enumerate(inter, 1):
            ux = f'{x}-U{pidx[x][p][0]:04d}' if p in pidx[x] else '-'
            uy = f'{y}-U{pidx[y][p][0]:04d}' if p in pidx[y] else '-'
            g.append(f'| {i} | {ux} | {uy} | {p[:28]}… |\n')
    g.append('\n## 4. 书内重复明细\n')
    any_ib = False
    for c in sorted(ib):
        clus = [(p, us) for p, us in pidx[c].items() if len(us) > 1]
        if not clus:
            continue
        any_ib = True
        g.append(f'\n### {c}（{len(clus)} 处）\n\n| # | 所在单元 | 段落（前 32 字） |\n|---|---|---|\n')
        for i, (p, us) in enumerate(sorted(clus, key=lambda x: x[1][0]), 1):
            locs = '、'.join(f'{c}-U{j:04d}' for j in us)
            g.append(f'| {i} | {locs} | {p[:32]}… |\n')
    if not any_ib:
        g.append('\n（无）\n')
    if problems:
        g.append('\n## 与基线不一致项\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))
    print(f'G6 重复扫描: {"FAIL" if problems else "PASS"}（跨书 {dc["paragraphs"]} 段/{dc["chars"]:,} 字，'
          f'GG↔SG1 {dc["pairs"].get("GG<->SG1", {}).get("paragraphs", 0)} 段双出处登记；书内 {sum(ib.values())} 处）；报告 {a.out}')
    for p in problems:
        print('  不一致:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
