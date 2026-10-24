#!/usr/bin/env python3
"""pilot_sample.py — P1 试点选样（T-P1-01，对应 v2 §7.5 试点门 + v2.1 Z2-03 微试跑）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/pilot_sample.py --units data/units --baseline spec/baseline_facts.json --g6 logs/g6.md --out data/pilot --gold data/gold
选样: 固定种子 20261024。微试跑 3（A 层成书正文 / B 层问答双说话人 / SG3 划重点覆盖信）+ 放量 11（TD/FZ/JJ/GJ/SX/JS
      成书各 1、问答再 1、互动 1、GG↔SG1 重复簇 1、长单元 >8000、短单元 <500）= 14。
      §7.5 的具体内容条件尽量落在对应槽位（富足可重复成功+做减法+本章小结、境界经验与理性、格局沟通类、见识伪工作、
      数学通识 1 讲、谷歌回信精选、谷歌答读者问、来信3 划重点、SG1↔GG 双出处）；§7.5 有而任务槽位没有的行（第008封、
      考拉袋鼠、稀缺/超越免费、系列组、第2封划重点、认命大概率）在报告"偏差"节逐条注明并给出候选，供用户微调。
校验（内置，任一失败退出非零）:
  ① SG3 划重点逐单元重算聚合 == baseline sg3_huazhongdian；② 14 个 unit_id 唯一且都在 units_index.csv；
  ③ 各条件槽位自检（答读者问/回信精选/周末问答标题匹配、小结<500、长单元>8000、重复簇双侧在索引）；④ JSON 写盘后重新解析。
输出: data/pilot/samples.json、data/pilot/sample_list.md、data/gold/gold_v0.json（微试跑 3 单元黄金样例 v0，标准答案卡待 T-P1-02）。
"""
import argparse, csv, datetime, json, os, random, re, sys

CJK = re.compile(r'[\u4e00-\u9fff]')
SEED = 20261024

def load_units(units_dir):
    rows = list(csv.DictReader(open(os.path.join(units_dir, 'units_index.csv'), encoding='utf-8')))
    for r in rows:
        r['char_count'] = int(r['char_count'])
        r['start_line'] = int(r['start_line']); r['end_line'] = int(r['end_line'])
        i = int(r['unit_id'].split('-U')[1])
        ls = open(os.path.join(units_dir, r['book_code'], f'unit_{i:04d}.md'), encoding='utf-8').read().split('\n')
        body = ls[ls.index('---', 1) + 1:]
        if body and body[-1] == '':
            body = body[:-1]
        r['body'], r['title'] = body, (body[0].lstrip('#').strip() if body else '')
    return rows

def hz(text):
    return len(CJK.findall(text))

def huazhongdian_units(rows, code):
    """重算某书逐单元"划重点"覆盖（标题恰为 划重点 的 heading，计其后到下一 heading 的汉字），口径同 s01_probe。"""
    cov, sec_tot, ch_tot = {}, 0, 0
    for r in rows:
        if r['book_code'] != code:
            continue
        n = ch = 0; inh = False
        for l in r['body']:
            m = re.match(r'^(#{1,6})\s+(.*)', l)
            if m:
                inh = m.group(2).strip() == '划重点'; n += inh
            elif inh:
                ch += hz(l)
        if n:
            cov[r['unit_id']] = n; sec_tot += n; ch_tot += ch
    return cov, sec_tot, ch_tot

def rec(slot, r, subtype, reason, checkpoints, v75):
    return dict(slot=slot, unit_id=r['unit_id'], book_code=r['book_code'], type=r['type'], subtype=subtype,
                char_count=r['char_count'], lines=f'{r["start_line"]}-{r["end_line"]}', title=r['title'],
                reason=reason, checkpoints=checkpoints, v75_rows=v75)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--g6', default='logs/g6.md')
    ap.add_argument('--out', default='data/pilot')
    ap.add_argument('--gold', default='data/gold')
    a = ap.parse_args()
    rows = load_units(a.units)
    by_code = {}
    for r in rows:
        by_code.setdefault(r['book_code'], []).append(r)
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    rng = random.Random(SEED)
    errs = []

    # —— 校验① SG3 划重点：逐单元重算聚合必须与基线一致，否则后续"在划重点覆盖内"无从谈起
    cov, sec_tot, ch_tot = huazhongdian_units(rows, 'SG3')
    bh = base['sg3_huazhongdian']
    if dict(sections=sec_tot, chars=ch_tot) != bh:
        errs.append(f'SG3 划重点重算聚合 {{sections:{sec_tot}, chars:{ch_tot}}} ≠ 基线 {bh}')
    # —— 重复簇（G6 双出处登记表：GG 单元 | SG1 单元）
    pairs = re.findall(r'^\| \d+ \| (GG-U\d{4}) \| (SG1-U\d{4}) \|', open(a.g6, encoding='utf-8').read(), re.M)
    if len(pairs) != 107:
        errs.append(f'G6 GG<->SG1 双出处登记行 {len(pairs)} ≠ 107')

    def pick(code, flt, why, allow_empty=False):
        cand = [r for r in by_code.get(code, []) if flt(r)]
        if not cand and not allow_empty:
            errs.append(f'{why}: {code} 无候选')
        return cand

    # —— 微试跑 3（Z2-03：走完整流程后才放量）
    m1 = pick('FZ', lambda r: '可重复' in r['title'] and r['type'] == 'C', '微① 可重复的成功')
    micro1 = m1[0] if m1 else None
    m2 = pick('GG', lambda r: '答读者问' in r['title'] and 1000 <= r['char_count'] <= 6000, '微② 答读者问(中长)')
    m2 = m2 or pick('GG', lambda r: '答读者问' in r['title'], '微② 答读者问(不限长)')
    micro2 = rng.choice(m2) if m2 else None
    m3 = pick('SG3', lambda r: r['unit_id'] in cov and 1000 <= r['char_count'] <= 6000, '微③ 划重点覆盖信(中长)')
    m3 = m3 or pick('SG3', lambda r: r['unit_id'] in cov, '微③ 划重点覆盖信(不限长)')
    micro3 = rng.choice(m3) if m3 else None

    # —— 放量 11
    td_c = pick('TD', lambda r: r['type'] == 'C' and re.search(r'第\s*\d+\s*封信', r['title']), 'TD 1 封')
    s_td = rng.choice(td_c) if td_c else None
    fz_j = pick('FZ', lambda r: '减法' in r['title'] and r['type'] == 'C', 'FZ 做减法')
    s_fz = fz_j[0] if fz_j else None
    jj_c = pick('JJ', lambda r: '理性' in r['title'] and '经验' in r['title'] and r['type'] == 'C', 'JJ 经验与理性')
    s_jj = jj_c[0] if jj_c else None
    gj_c = pick('GJ', lambda r: '沟通' in r['title'] and r['type'] == 'C', 'GJ 沟通类')
    s_gj = rng.choice(gj_c) if gj_c else None
    sx_c = pick('SX', lambda r: re.match(r'^\d{2}｜', r['title']) and r['type'] == 'C', 'SX 1 讲')
    s_sx = rng.choice(sx_c) if sx_c else None
    js_c = pick('JS', lambda r: '伪工作' in r['title'] and r['type'] == 'C', 'JS 伪工作')
    s_js = max(js_c, key=lambda r: r['char_count']) if js_c else None  # 章头容器（# 第四章…）与正文小节同名命中时取实质内容单元
    wj_qa = pick('WJ2', lambda r: '周末问答' in r['title'], 'WJ2 周末问答')
    s_qa2 = rng.choice(wj_qa) if wj_qa else None
    gg_it = pick('GG', lambda r: '回信精选' in r['title'], 'GG 回信精选')
    s_it = rng.choice(gg_it) if gg_it else None
    dup_gg, dup_sg1 = rng.choice(pairs) if pairs else (None, None)
    long_c = pick('WJ2', lambda r: r['char_count'] > 8000 and r['type'] == 'C', '长单元>8000(C类)')
    long_c = long_c or [r for r in rows if r['char_count'] > 8000 and r['type'] == 'C']
    s_long = long_c[0] if long_c else None
    summ = pick('FZ', lambda r: r['title'] == '本章小结' and r['char_count'] < 500, 'FZ 本章小结<500')
    s_short = max(summ, key=lambda r: r['char_count']) if summ else None

    samples = [
        rec('微①', micro1, '成书正文', 'A 层成书正文；富足第 14 章可重复的成功，论点明确、长度中等（贴近 FZ 内容单元中位）',
            ['结论句与机制抽取（§15.7.2 步2–3）', '回归组 a', '章节-小结边界（FZ 篇级本章小结单元邻接）'], ['2']) if micro1 else None,
        rec('微②', micro2, '答读者问', 'B 层问答单元，双说话人（读者提问+吴军作答）',
            ['说话人分段（§15.6）', '读者言论不得入原著核心判断（§15.7.4-3）', '锚点唯一性'], ['9']) if micro2 else None,
        rec('微③', micro3, '划重点信', 'SG3 来信单元且内含"划重点"子节，可对照外部参照算召回',
            ['划重点召回 ≥90%（§7.5 门槛）', '稳定度待判（来信类必填）', '编号信锚点'], ['13']) if micro3 else None,
        rec('放1', s_td, '书信', '态度家书 1 封：三观与书信体',
            ['书信体转述语气（§15.7.3-9）', '收信对象语境保留'], ['5']) if s_td else None,
        rec('放2', s_fz, '成书正文', '富足第 03 章做减法比做加法重要',
            ['回归组 b', '与方法类论点的 K/M 判定'], ['2']) if s_fz else None,
        rec('放3', s_jj, '成书正文', '境界"我们该选择理性还是经验"，概念对冲单元',
            ['回归组 e', '转述不得合并相左论点（§15.7.4-2）'], ['3']) if s_jj else None,
        rec('放4', s_gj, '成书正文', '格局沟通类章节',
            ['规则⑤⑫边界', '能力标签（沟通）'], ['1']) if s_gj else None,
        rec('放5', s_sx, '成书正文（讲）', '数学通识 1 讲，正文含硬换行与公式',
            ['硬换行不影响锚点（§15.7.2 步11）', '数理映射态判定'], ['6']) if s_sx else None,
        rec('放6', s_js, '成书正文', '见识伪工作者章节',
            ['职场归属（支柱提示）', '概念键查重（伪工作）'], ['4']) if s_js else None,
        rec('放7', s_qa2, '周末问答', 'WJ2 周末问答，问答 B 层第 2 样本（问答再 1），补 WJ2 覆盖',
            ['双说话人', '多问并列时一卡一论点（§15.7.3-8）'], ['12(部分：WJ2 覆盖)']) if s_qa2 else None,
        rec('放8', s_it, '回信精选', '谷歌回信精选，互动类',
            ['说话人（编者/吴军混排）', '整理者说明标记（G7 flags）'], ['8']) if s_it else None,
        rec('放9', by_code_lookup(rows, dup_gg) if dup_gg else None, '重复簇GG侧', f'GG↔SG1 跨书精确重复簇内单元（对侧 {dup_sg1} 登记双出处）',
            ['双出处登记：两单元同段收敛为一张卡', '来源以先出版者为准', f'对侧单元：{dup_sg1}'], ['11']) if dup_gg else None,
        rec('放10', s_long, '超长单元', f'内容单元 {s_long["char_count"]:,} 字（>8000 唯一 C 类）',
            ['超长单元分段读（Z2-04），处置与锚点仍整单元口径'], ['—']) if s_long else None,
        rec('放11', s_short, '本章小结', f'本章小结 {s_short["char_count"]} 字（<500 短单元），兼覆盖富足样本"含本章小结"',
            ['极短单元的处置判定（§15.7.1）', '短单元锚点下限'], ['2']) if s_short else None,
    ]
    samples = [s for s in samples if s]
    idx_ids = {r['unit_id'] for r in rows}
    ids = [s['unit_id'] for s in samples]
    # —— 校验②③
    if len(samples) != 14:
        errs.append(f'样本数 {len(samples)} ≠ 14')
    if len(set(ids)) != len(ids):
        errs.append('样本 unit_id 有重复')
    miss = [i for i in ids if i not in idx_ids]
    if miss:
        errs.append(f'unit_id 不在索引: {miss}')
    if micro3 and micro3['unit_id'] not in cov:
        errs.append(f'微③ {micro3["unit_id"]} 不在划重点覆盖集')
    if dup_gg and dup_sg1 and not ({dup_gg, dup_sg1} <= idx_ids):
        errs.append(f'重复簇对侧 {dup_gg}/{dup_sg1} 不在索引')
    if s_short and s_short['char_count'] >= 500:
        errs.append('短单元槽位 ≥500')
    if s_long and s_long['char_count'] <= 8000:
        errs.append('长单元槽位 ≤8000')
    if errs:
        print('选样校验失败：'); [print(' -', e) for e in errs]; sys.exit(1)

    today = datetime.date.today().isoformat()
    meta = dict(ticket='T-P1-01', seed=SEED, date=today, total=len(ids),
                book_spread={c: sum(1 for i in ids if i.startswith(c + '-')) for c in sorted({i.split('-')[0] for i in ids})},
                spec_refs=['spec/v2_方案.md §7.5', 'spec/v2_1_增补.md Z2-03', '§15.7 抽卡规程'],
                validation=dict(sg3_huazhongdian_recheck=f'sections {sec_tot} / chars {ch_tot}，与基线一致',
                                dup_pairs_parsed=len(pairs), all_ids_in_index=True, distinct=True))
    data = dict(meta=meta, samples=samples)
    os.makedirs(a.out, exist_ok=True)
    jp = os.path.join(a.out, 'samples.json')
    json.dump(data, open(jp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.load(open(jp, encoding='utf-8'))  # —— 校验④：重新解析
    gold = dict(meta=dict(version='v0', date=today, ticket='T-P1-01', note='标准答案卡待 T-P1-02 首抽后回填；用于 ST-3/GATE-C 漂移控制（data/gold/README.md）'),
                gold=[dict(unit_id=s['unit_id'], book_code=s['book_code'], title=s['title'],
                           anchor=dict(unit_file=f"data/units/{s['book_code']}/unit_{s['unit_id'].split('-U')[1]}.md",
                                       start_line=next(r['start_line'] for r in rows if r['unit_id'] == s['unit_id']),
                                       end_line=next(r['end_line'] for r in rows if r['unit_id'] == s['unit_id']),
                                       scope='冻结原文行号区间（src_frozen 对应书）'),
                           checkpoints=s['checkpoints']) for s in samples[:3]])
    os.makedirs(a.gold, exist_ok=True)
    gp = os.path.join(a.gold, 'gold_v0.json')
    json.dump(gold, open(gp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.load(open(gp, encoding='utf-8'))

    v75 = [('1', '覆盖', '格局沟通类 1 篇（放4）'), ('2', '覆盖', '可重复成功（微①）+ 做减法（放2）+ 本章小结（放11）'),
           ('3', '覆盖', '境界经验与理性（放3）'), ('4', '覆盖', '见识伪工作（放6）'), ('5', '覆盖', '态度 1 封（放1）'),
           ('6', '覆盖', '数学通识 1 讲（放5，硬换行）'), ('7', '未选', '谷歌第008封（三条边）无对应任务槽位；候选 GG-U0013，可微调替换'),
           ('8', '覆盖', '谷歌回信精选（放8）'), ('9', '覆盖', '谷歌答读者问（微②）'),
           ('10', '未选', 'SG1 考拉/袋鼠（SG1-U0119，1897 字）无对应槽位；可微调'), ('11', '部分', '重复簇取 GG 侧 1 个样本，对侧 SG1 单元登记为双出处（任务定 1 个；§7.5 为"单元对"）'),
           ('12', '部分', 'WJ2 由周末问答（放7）与超长信（放10）覆盖；稀缺/超越免费与系列组未单独选样'),
           ('13', '部分', '划重点信取 1 封（微③）；§7.5 原文为 2 封'), ('14', '未选', '认命/大概率相关单元（GJ-U0010 命运章头为容器单元）未选')]
    md = [f'# P1 试点选样清单（T-P1-01）', '',
          f'- 种子 {SEED}；日期 {today}；样本 {len(ids)} 个（微试跑 3 + 放量 11）；§7.5 要求"脚本按条件选，我微调"，本表供过目',
          f'- 内置校验全过：SG3 划重点重算 sections {sec_tot} / chars {ch_tot} == 基线；重复簇登记 {len(pairs)} 对；14 id 唯一且均在 units_index.csv',
          f'- 输出：data/pilot/samples.json（机器可读）；data/gold/gold_v0.json（微试跑 3 单元黄金样例 v0）', '',
          '| # | 槽位 | unit_id | 书 | 类型 | 字数 | 行区间 | 标题 | §7.5 |', '|---|---|---|---|---|---|---|---|---|']
    for i, s in enumerate(samples, 1):
        md.append(f'| {i} | {s["slot"]} | {s["unit_id"]} | {s["book_code"]} | {s["subtype"]} | {s["char_count"]:,} | {s["lines"]} | {s["title"][:24]} | {",".join(s["v75_rows"])} |')
    md += ['', '## 选择理由与检验点', '']
    for s in samples:
        md.append(f'- **{s["unit_id"]}（{s["slot"]}）**：{s["reason"]}。检验点：{"；".join(s["checkpoints"])}')
    md += ['', '## §7.5 十四类覆盖情况与偏差', '', '| §7.5 行 | 状态 | 说明 |', '|---|---|---|']
    md += [f'| {r} | {st} | {note} |' for r, st, note in v75]
    open(os.path.join(a.out, 'sample_list.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print(f'选样完成：{len(ids)} 个样本 -> {jp}；清单 {os.path.join(a.out, "sample_list.md")}；黄金样例 {gp}')
    for s in samples:
        print(f'  {s["slot"]:<3} {s["unit_id"]:<10} {s["book_code"]:<3} {s["subtype"]:<8} {s["char_count"]:>6,}  {s["title"][:30]}')

def by_code_lookup(rows, uid):
    return next(r for r in rows if r['unit_id'] == uid)

if __name__ == '__main__':
    main()
