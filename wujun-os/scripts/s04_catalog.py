#!/usr/bin/env python3
"""s04_catalog.py — P0 自动目录一致性 + 谷歌作者目录比对（S04，总闸 G5）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s04_catalog.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g5.md
作用（v2 方案 §6.1 G5a/G5b、§7 决策 D-09: 自动目录是弱证据，只作对账不作收录依据）:
  (a) 自动目录一致性——逐书提取目录单元（GG 为导航区单元 U0001）中的 `- [标题](#锚点)` 条目，做两个口径比对:
        a1 目录条目 vs 单元标题集（切分口径）;
        a2 目录条目 vs 文内全部标题行集（v2 方案 §145 口径: 来信2/态度/数学通识/格局/见识/谷歌 6 本差集 0）。
      差集逐条定性；与下方 EXPECTED（2026-10-24 在冻结源上实测核对，含 v2 §145/§170 已声明事实）不符即 FAIL。
  (b) 谷歌作者目录——复用 s01_probe.probe 的 gg_author_catalog，与基线比对（预期 219/223，缺 021–024）。
目录定位: 除 GG 外各书取标题为「目录」的非内容单元；GG 无目录单元，自动目录在导航区单元（标题以「谷歌方法论：」起）。
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

LINK = re.compile(r'^\s*[-*]\s*\[(.+?)\]\(\s*#')
HEAD = re.compile(r'^(#{1,6})\s+(.*)')

# 与已核对事实的差异预期（2026-10-24 冻结源实测；空集/缺书码表示差集应为空）。
# 依据: v2 方案 §145（6 本差集 0、富足差 4 个本章小结、境界 3–5 项差异、来信1 分块、来信3 无目录块→实测有、见报告定性）
EXP_A1_TOC_ONLY = {  # a1: 目录有而单元标题没有
    'WJ2': ['白话译文'],
    'JS': ['招人', '确立公司的价值观或企业文化', '第一板斧：确立“愿景一目标一道路”',
           '第三板斧：凡事做记录，这样可以避免狗熊掰棒子', '第二板斧：即使听到不中听的话，也要试着找出其中的合理之处',
           '误区一：工作和职业分不清', '误区一：简单重复', '误区三：林黛玉式的困境',
           '误区三：被语言暴力激怒后就乱了章法', '误区二：习惯性失败',
           '误区二：把自己仅仅当作一个单位的过客，而不是主人', '误区四：狗熊掰棒子', '误区四：疏于沟通',
           '起到刹车的作用，而不是引擎的作用', '钱是上帝存在你那里的，不是给你的，回头你要还给他'],
    'JJ': ['“上帝死了”，人该怎么办', '伊壁鸠鲁学派宣扬的是纸醉金迷的享乐吗'],
}
EXP_A1_UNIT_ONLY = {  # a1: 单元标题有而目录没有
    'SG1': ['吴军的硅谷来信', '目录'],
    'SG3': ['吴军·硅谷来信3', '目录'],
    'FZ': ['本章小结'],
    'JJ': ['“上帝死了”,人该怎么办', '伊壁鸠魯学派宣扬的是纸醉金迷的享乐吗',
           '境界：提升认知与人生维度的底层逻辑', '目录'],
}
EXP_A2_TOC_ONLY = {  # a2: 目录有而文内标题行没有（v2 §145: 其余 6 本必须为空）
    'JJ': ['“上帝死了”，人该怎么办', '伊壁鸠鲁学派宣扬的是纸醉金迷的享乐吗'],
}
EXP_A2_HEAD_ONLY = {  # a2: 文内标题行有而目录没有
    'FZ': ['本章小结'],
    'JJ': ['“上帝死了”,人该怎么办', '伊壁鸠魯学派宣扬的是纸醉金迷的享乐吗',
           '境界：提升认知与人生维度的底层逻辑', '目录', '科学知识、技能知识和道德知识'],
}
A2_REPORT_ONLY = ('SG1', 'SG3')  # 信内小节标题不进目录（目录为单元级），数量级大，只报告不设卡

def toc_of(code, us):
    """返回 (目录单元, 定位说明)。"""
    t = next((u for u in us if u['title'] == '目录'), None)
    if t:
        return t, '「目录」单元'
    t = next((u for u in us if u['title'].startswith('谷歌方法论：')), None)
    if t:
        return t, '导航区单元（无目录单元，v2 §155: 谷歌 365 条自动目录在此）'
    return None, ''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--out', default='logs/g5.md')
    a = ap.parse_args()
    f = s01_probe.probe(a.src)
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    B = s01_probe.load(a.src)
    problems = []

    cat = f['gg_author_catalog']
    if cat != base['gg_author_catalog']:
        problems.append(f'谷歌作者目录与基线不符: 本次 {cat} / 基线 {base["gg_author_catalog"]}')

    rows = []
    for _, _, code, _ in s01_probe.BOOKS:
        us = s01_probe.split_units(B[code]['text'], B[code]['lvl'])
        toc, where = toc_of(code, us)
        if toc is None:
            problems.append(f'{code}: 找不到目录单元或导航区目录')
            continue
        links = [m.group(1).strip() for l in toc['text'].split('\n') for m in [LINK.match(l)] if m]
        lset, ut = set(links), {u['title'] for u in us}
        heads = {m.group(2).strip() for l in B[code]['text'].split('\n') for m in [HEAD.match(l)] if m}
        a1_t, a1_u = sorted(lset - ut), sorted(ut - lset)
        a2_t, a2_u = sorted(lset - heads), sorted(heads - lset)
        for kind, got, exp in (('a1仅目录', a1_t, EXP_A1_TOC_ONLY.get(code, [])),
                               ('a1仅单元', a1_u, EXP_A1_UNIT_ONLY.get(code, [])),
                               ('a2仅目录', a2_t, EXP_A2_TOC_ONLY.get(code, [])),
                               ('a2仅标题', a2_u if code not in A2_REPORT_ONLY else None,
                                None if code in A2_REPORT_ONLY else EXP_A2_HEAD_ONLY.get(code, []))):
            if exp is None:
                continue
            if got != exp:
                problems.append(f'{code} {kind} 与预期不符: 本次 {got} / 预期 {exp}')
        rows.append((code, where, len(links), a1_t, a1_u, a2_t, a2_u))

    g = []
    g.append('# G5 自动目录一致性 + 谷歌作者目录（S04）\n')
    g.append(f'- 源: `{a.src}`；目录条目提取自目录单元（GG 为导航区单元）的 `- [标题](#锚点)` 行\n'
             f'- 结论: **{"FAIL" if problems else "PASS"}**（G5b 与基线比对 + G5a 与已核对预期比对，不一致 {len(problems)} 项）\n')
    g.append('## 1. 逐书目录比对总表\n\n'
             '| 书 | 目录定位 | 条目数 | a1差集(目录↔单元) | a2差集(目录↔文内标题行) |\n|---|---|---|---|---|\n')
    for code, where, n, a1_t, a1_u, a2_t, a2_u in rows:
        fmt = lambda x: (f'{len(x)} 条' if x else '0')
        detail = lambda x: ('' if not x else '（见下）')
        g.append(f'| {code} | {where} | {n:,} | {fmt(a1_t)+detail(a1_t)}+{fmt(a1_u)+detail(a1_u)} | '
                 f'{fmt(a2_t)+detail(a2_t)}+{fmt(a2_u)+detail(a2_u)} |\n')
    g.append('\n## 2. 差集逐条定性\n')
    quals = {
        'a1': '目录条目未对应到任何单元标题',
        'a2': '目录条目未对应到文内任何标题行',
    }
    for code, where, n, a1_t, a1_u, a2_t, a2_u in rows:
        items = []
        if a1_t:
            items.append(f'- a1 仅目录有（{quals["a1"]}）: ' + '；'.join(f'「{x[:36]}」' for x in a1_t[:6])
                         + ('…' if len(a1_t) > 6 else ''))
        if a1_u:
            items.append(f'- a1 仅单元有（目录未收录的单元标题）: ' + '；'.join(f'「{x[:36]}」' for x in a1_u[:6])
                         + ('…' if len(a1_u) > 6 else ''))
        if code in A2_REPORT_ONLY and (a2_t or a2_u):
            items.append(f'- a2 仅文内标题行有 {len(a2_u)} 条: 信内小节标题（如 #信后思考#、问答小问），层级低于目录收录粒度，属结构差异，不设卡')
        elif a2_t:
            items.append(f'- a2 仅目录有: ' + '；'.join(f'「{x[:36]}」' for x in a2_t[:6]))
        elif a2_u:
            items.append(f'- a2 仅文内标题行有: ' + '；'.join(f'「{x[:36]}」' for x in a2_u[:6]))
        if not items:
            items.append('- a1/a2 差集均为 0（目录与单元/标题行逐项一致）')
        note = ''
        if code == 'FZ':
            note = '。定性: 「本章小结」×4 为编辑附写的提炼层单元，目录未收录（v2 方案 §170: 骨架优先读），非内容缺失'
        elif code == 'JJ':
            note = '。定性: 目录与正文标题存在 2 处编校差异——全角逗号「，」vs 半角「,」、「鲁」vs 繁体「魯」；另目录未收书名/目录自身及 1 条文内小节，非内容缺失'
        elif code == 'WJ2' and a1_t:
            note = '。定性: 「白话译文」目录条目指向信内「### 白话译文」小节（a2 口径可对上），目录含小节级条目所致'
        elif code == 'JS' and a1_t:
            note = f'。定性: {len(a1_t)} 条均为信内「###」小节级条目（a2 口径全部可对上），目录含小节级条目所致'
        elif code in ('SG1', 'SG3') and a1_u:
            note = '。定性: 仅书名容器与「目录」单元自身不在目录条目中，属正常；' + (
            '来信1 目录为单元级全收录（SG1 a2 仅文内小节 %d 条不设卡）' % len(a2_u) if code == 'SG1'
            else '来信3 实测有目录块（317 条），与 v2 方案 §145「来信3 无自动目录块」表述不符，以本包冻结源实测为准')
        g.append(f'### {code}（条目 {n:,}）\n\n' + '\n'.join(items) + note + '\n')
    g.append('## 3. 谷歌作者目录（G5b）\n\n'
             f'- 作者自编「收藏丨全年课程目录一键直达」覆盖 **{cat["covered"]}/223** 封信，'
             f'缺号: {"、".join(f"{x:03d}" for x in cat["missing"]) or "无"}\n'
             f'- 定性: 作者目录是接近独立的参照来源（v2 方案 §6.1 G5b），缺 021–024 与基线一致；'
             f'其中第 023 封标题含「减法」，与回归概念相关，**只作对账、不作收录依据**（v2 方案 §7 D-09）\n')
    if problems:
        g.append('## 与预期不一致项\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))
    print(f'G5 目录对账: {"FAIL" if problems else "PASS"}（谷歌作者目录 {cat["covered"]}/223 缺 {cat["missing"]}；'
          f'10 书 a1/a2 差集逐条定性完成）；报告 {a.out}')
    for p in problems:
        print('  不一致:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
