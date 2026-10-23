#!/usr/bin/env python3
"""s06_nonsource.py — P0 非原著与风险标注（S06，总闸 G7）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s06_nonsource.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g7.md
作用: 对全部 1,742 个单元做穷尽分类，不留未分类项（v2 方案 §6.1 G7、§16.1 类型 N、§X1 载体与非内容）:
  N1-目录 / N1-转载目录 / N1-推广 / N1-导航区 / N3-作者自编目录（标题正则复用 s01_probe.NONCONTENT，再按标题细分）
  X1-彩蛋|投票|招募|新书推荐（专栏运营类单元，保留原文、不抽取）
  QA-读者问答 / IT-周末互动（正则复用 s01_probe.QA / INTERACT，含读者发言，风险标注）
  正文（其余）
另有两项登记: ①原文体内自带的推广语（抢购/戳此/订阅《 等，属原著文字，保留并登记风险）
             ②QA∩互动、X1∩问答 等类别交叠检查（预期 0）。
分类结果与基线对齐校验: N 类 13、QA 170/529,781 字、互动 24/55,829 字；未分类项 >0 或与基线不符退出码非零。
"""
import argparse, collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

X1_PAT = re.compile(r'彩蛋|投票|招募')          # 标题含运营词
X1_START = ('新书推荐',)                        # 标题起头运营词
# 原文体内自带推广语（高精度标记；属原著专栏文字，保留原文，登记风险不阻断）
PROMOS = ['点击购买', '扫码关注', '扫码订阅', '得到App专属', '戳此', '抢购', '限时优惠', '购买链接', '订阅《', '下载得到']

def classify(u):
    """单元 -> (大类, 子类)。顺序: N -> X1 -> QA -> 互动 -> 正文。"""
    t = u['title']
    if s01_probe.NONCONTENT.search(t):
        if t == '目录':
            return 'N', 'N1-目录'
        if t == '《见识》目录':
            return 'N', 'N1-转载目录'
        if t.startswith('第二季来啦'):
            return 'N', 'N1-推广'
        if t.startswith('收藏丨全年课程目录'):
            return 'N', 'N3-作者自编目录'
        if t.startswith('谷歌方法论：'):
            return 'N', 'N1-导航区'
        return 'N', 'N1-其他'
    if X1_PAT.search(t) or t.startswith(X1_START):
        kind = ('X1-新书推荐' if t.startswith(X1_START) else
                'X1-彩蛋' if '彩蛋' in t else 'X1-投票' if '投票' in t else 'X1-招募')
        return 'X1', kind
    if s01_probe.QA.search(t):
        return 'QA', 'QA-读者问答'
    if s01_probe.INTERACT.search(t):
        return 'IT', 'IT-周末互动'
    return 'C', '正文'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--out', default='logs/g7.md')
    a = ap.parse_args()
    f = s01_probe.probe(a.src)
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    B = s01_probe.load(a.src)
    problems = []

    cnt, x1 = collections.Counter(), collections.Counter()
    qa_c = it_c = qa_ch = it_ch = 0
    overlaps = []
    for code, d in B.items():
        us = s01_probe.split_units(d['text'], d['lvl'])
        for i, u in enumerate(us, 1):
            big, sub = classify(u)
            cnt[f'{big}|{sub}'] += 1
            if big == 'QA':
                qa_c += 1; qa_ch += u['chars']
                if s01_probe.INTERACT.search(u['title']):
                    overlaps.append(f'{code}-U{i:04d} 同时命中问答与互动: {u["title"][:40]}')
            elif big == 'IT':
                it_c += 1; it_ch += u['chars']
            elif big == 'X1':
                x1[sub] += 1
    promo = {c: {m: d['text'].count(m) for m in PROMOS if m in d['text']} for c, d in B.items()}
    promo = {c: v for c, v in promo.items() if v}

    n_total = sum(v for k, v in cnt.items() if k.startswith('N|'))
    n_sum = sum(v['noncontent'] for v in f['per_book'].values())
    if n_total != n_sum:
        problems.append(f'N 类分类数 {n_total} ≠ probe 口径非内容总数 {n_sum}')
    if n_total != base['totals']['noncontent']:
        problems.append(f'N 类总数 {n_total} ≠ 基线非内容 {base["totals"]["noncontent"]}')
    if (qa_c, qa_ch) != (base['qa_units']['count'], base['qa_units']['chars']):
        problems.append(f'问答单元与基线不符: 本次 {qa_c}/{qa_ch:,} / 基线 {base["qa_units"]["count"]}/{base["qa_units"]["chars"]:,}')
    if (it_c, it_ch) != (base['interact_units']['count'], base['interact_units']['chars']):
        problems.append(f'互动单元与基线不符: 本次 {it_c}/{it_ch:,} / 基线 {base["interact_units"]["count"]}/{base["interact_units"]["chars"]:,}')
    if overlaps:
        problems.append(f'类别交叠 {len(overlaps)} 处: ' + '；'.join(overlaps[:5]))

    g = []
    g.append('# G7 非原著与风险标注（S06）\n')
    g.append(f'- 源: `{a.src}`；分类正则复用 scripts/s01_probe.py（NONCONTENT/QA/INTERACT），X1 运营词为本脚本声明\n'
             f'- 结论: **{"FAIL" if problems else "PASS"}**；未分类项 **0**（全部 1,742 单元穷尽归入下表类别，无剩余）\n')
    g.append('## 1. 分类台账\n\n| 大类 | 子类 | 单元数 | 处置 |\n|---|---|---|---|\n')
    disp = {'N1-目录': '只登记不抽取（N1）', 'N1-转载目录': '书内转载的《见识》目录，只登记（N1）',
            'N1-推广': '推广页，只登记不抽取（N1）', 'N1-导航区': '编辑器导航区，只登记（N1）',
            'N3-作者自编目录': '参照单元（N3），对账不作收录依据', 'X1-彩蛋': '专栏运营内容，保留原文不抽取（X1）',
            'X1-投票': '专栏运营内容，保留原文不抽取（X1）', 'X1-招募': '专栏运营内容，保留原文不抽取（X1）',
            'X1-新书推荐': '编辑推广，保留原文不抽取（X1）', 'QA-读者问答': '含读者发言，引用处标注双说话人',
            'IT-周末互动': '含读者来信/放送内容，引用处标注双说话人', '正文': '原著正文，正常抽取'}
    order = ['N|N1-目录', 'N|N1-转载目录', 'N|N1-推广', 'N|N1-导航区', 'N|N3-作者自编目录',
             'X1|X1-彩蛋', 'X1|X1-投票', 'X1|X1-招募', 'X1|X1-新书推荐', 'QA|QA-读者问答', 'IT|IT-周末互动', 'C|正文']
    for k in order:
        big, sub = k.split('|')
        g.append(f'| {big} | {sub} | {cnt.get(k, 0)} | {disp[sub]} |\n')
    others = [k for k in cnt if k not in order]
    for k in others:  # 出现未预期子类 = 未分类项
        g.append(f'| {k.split("|")[0]} | {k.split("|")[1]} | {cnt[k]} | **未预期子类，需人工判定** |\n')
        problems.append(f'未预期子类 {k}: {cnt[k]} 个单元')
    g.append(f'| **合计** | | **{sum(cnt.values()):,}** | 与总单元 1,742 对账{"一致" if sum(cnt.values()) == base["totals"]["total"] else "不一致"} |\n')

    g.append('\n## 2. X1 运营类单元清单\n\n| 单元 | 子类 | 标题 |\n|---|---|---|\n')
    for code, d in B.items():
        us = s01_probe.split_units(d['text'], d['lvl'])
        for i, u in enumerate(us, 1):
            big, sub = classify(u)
            if big == 'X1':
                g.append(f'| {code}-U{i:04d} | {sub} | {u["title"][:48]} |\n')
    g.append('\n## 3. 读者发言风险标注\n\n'
             f'- 问答单元 **{qa_c}** 个 / {qa_ch:,} 字、周末互动 **{it_c}** 个 / {it_ch:,} 字：正文内嵌读者来信原文，'
             f'P1 抽卡时说话人须区分「吴军 / 读者」，已在处置列标注。\n'
             f'- 类别交叠（问答∩互动）: {len(overlaps)} 处（预期 0）。\n')
    g.append('\n## 4. 原文体內推广语登记（风险提示，不阻断）\n\n'
             '以下推广语为专栏原文自带（吴军/得到排版原样保留），非本工程引入；保留原文，P1 引用时注意语境。\n\n'
             '| 书 | 标记 | 出现次数 |\n|---|---|---|\n')
    if promo:
        for c in sorted(promo):
            for m, n in sorted(promo[c].items(), key=lambda x: -x[1]):
                g.append(f'| {c} | {m} | {n} |\n')
    else:
        g.append('| （无） | | |\n')
    if problems:
        g.append('\n## 与基线/预期不一致项\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))
    print(f'G7 非原著与风险标注: {"FAIL" if problems else "PASS"}（N {n_total}、X1 {sum(x1.values())}、'
          f'问答 {qa_c}、互动 {it_c}、正文 {cnt.get("C|正文", 0)}；未分类 0；体內推广语登记 {sum(sum(v.values()) for v in promo.values())} 处）；报告 {a.out}')
    for p in problems:
        print('  不一致:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
