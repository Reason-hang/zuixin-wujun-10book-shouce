#!/usr/bin/env python3
"""s08_d5.py — P0 生成 D5 内容盘点与单元清单 + 冻结分母（S08）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s08_d5.py --src src_frozen --baseline spec/baseline_facts.json \
      --units data/units --d5 out/D5_内容盘点与单元清单.md --denominator logs/p0_denominator.md
作用: 汇总 S01–S07 口径（全部复用 s01_probe / units_index.csv），生成
  (1) out/D5_内容盘点与单元清单.md: 逐书单元数表、类型分布、缺号清单、重复登记（GG↔SG1 双出处）、
      异常台账、全量 1,742 行单元清单；
  (2) logs/p0_denominator.md: 冻结分母三数——总单元 / 内容单元 / 汉字数（1,742 / 1,697 / 5,038,558）。
任何数字与 spec/baseline_facts.json 或 units_index.csv 不符、或 g4–g8 报告缺失，退出码非零并停。
"""
import argparse, collections, csv, glob, json, os, re, sys
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--d5', default='out/D5_内容盘点与单元清单.md')
    ap.add_argument('--denominator', default='logs/p0_denominator.md')
    ap.add_argument('--logs-dir', default='logs')
    a = ap.parse_args()
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    f = s01_probe.probe(a.src)
    B = s01_probe.load(a.src)
    problems = []

    # 前置报告存在性（S03–S07 已跑过）
    for g in ('g4.md', 'g5.md', 'g6.md', 'g7.md', 'g8.md'):
        p = os.path.join(a.logs_dir, g)
        if not (os.path.exists(p) and os.path.getsize(p) > 0):
            problems.append(f'缺少前置报告 {p}（先跑 s03–s07）')

    # 分母三数与基线
    tot = f['totals']
    denom = (tot['total'], tot['content'], f['file_chars'])
    denom_base = (base['totals']['total'], base['totals']['content'], base['file_chars'])
    if denom != denom_base:
        problems.append(f'分母三数与基线不符: 本次 {denom} / 基线 {denom_base}')

    # units_index.csv 与 probe / 基线 逐书对账
    with open(os.path.join(a.units, 'units_index.csv'), encoding='utf-8') as fp:
        idx = list(csv.DictReader(fp))
    csv_by_book = collections.Counter(r['book_code'] for r in idx)
    allu = {c: s01_probe.split_units(d['text'], d['lvl']) for c, d in B.items()}
    for code in csv_by_book:
        if code not in allu:
            problems.append(f'units_index.csv 出现未知书码 {code}')
    for code, us in allu.items():
        if csv_by_book.get(code, 0) != len(us):
            problems.append(f'{code}: 索引行 {csv_by_book.get(code, 0)} ≠ 切分单元 {len(us)}')
        pb = base['per_book'][code]
        c = collections.Counter(u['cls'] for u in us)
        got = dict(total=len(us), content=c['C'], container=c['S'], noncontent=c['N'],
                   content_chars=sum(u['chars'] for u in us if u['cls'] == 'C'))
        if got != pb:
            problems.append(f'{code}: 逐书数字与基线不符: {got} / {pb}')
    if len(idx) != tot['total']:
        problems.append(f'索引总行数 {len(idx)} ≠ 总单元 {tot["total"]}')

    # 缺号与重复（同 probe 口径）
    qa = f['qa_numbering']; lt = f['letters']; dc = f['dup_cross']
    missing_rows = [(c, '第X封信', lt[c]['missing']) for c in lt if lt[c]['missing']]
    missing_rows += [(c, '答读者问' if c != 'WJ2' else '周末问答', qa[c]['missing']) for c in qa if qa[c]['missing']]

    g = []
    g.append('# D5 内容盘点与单元清单（S08 · P0 冻结版）\n')
    g.append(f'- 生成: {date.today().isoformat()}；源: `{a.src}`（冻结），索引: `{a.units}/units_index.csv`\n'
             f'- 口径: 切分/分类/编号/重复全部复用 scripts/s01_probe.py 算法，与 spec/baseline_facts.json 同源\n')
    g.append('## 1. 冻结分母\n\n')
    g.append(f'| 分母 | 数值 |\n|---|---|\n| 总单元 | **{denom[0]:,}** |\n| 内容单元 | **{denom[1]:,}** |\n'
             f'| 汉字数（十书原文全部汉字） | **{denom[2]:,}** |\n\n'
             f'- 构成: 总单元 {denom[0]:,} = 内容 {tot["content"]:,} + 结构容器 {tot["container"]} + 非内容 {tot["noncontent"]}\n'
             f'- 辅助口径: 内容单元汉字 {tot["content_chars"]:,}（不含容器/非内容），与分母汉字数口径不同、用途不同\n'
             f'- 与基线核对: {"PASS" if denom == denom_base else "FAIL"}\n')
    g.append('## 2. 逐书单元数表\n\n| 书 | 书名 | 总单元 | 内容C | 容器S | 非内容N | 内容单元汉字 | 与基线 |\n|---|---|---|---|---|---|---|---|\n')
    lvl = {c: b for _, b, c, _ in s01_probe.BOOKS}
    for code, _, _, _ in [(k, 0, 0, 0) for k in ('SG1', 'WJ2', 'SG3', 'GG', 'JS', 'SX', 'GJ', 'JJ', 'FZ', 'TD')]:
        pb, fb = base['per_book'][code], f['per_book'][code]
        g.append(f'| {code} | {lvl[code]} | {fb["total"]} | {fb["content"]} | {fb["container"]} | {fb["noncontent"]} | '
                 f'{fb["content_chars"]:,} | {"一致" if fb == pb else "不一致"} |\n')
    g.append(f'| **合计** | | **{tot["total"]:,}** | **{tot["content"]:,}** | **{tot["container"]}** | **{tot["noncontent"]}** | '
             f'**{tot["content_chars"]:,}** | {"一致" if f["per_book"] == base["per_book"] else "不一致"} |\n')
    g.append('## 3. 类型分布与专项体量\n\n'
             f'- 问答单元（答读者问/周末问答等）: {base["qa_units"]["count"]} 个 / {base["qa_units"]["chars"]:,} 字\n'
             f'- 周末互动单元（互动/放送/精选）: {base["interact_units"]["count"]} 个 / {base["interact_units"]["chars"]:,} 字\n'
             f'- 系列单元（上/下篇、之N 等）: {base["series_units"]} 个\n'
             f'- X1 运营类（彩蛋/投票/招募/新书推荐）: 12 个、N 类细分与体內推广语见 logs/g7.md\n')
    g.append('## 4. 缺号清单\n\n')
    if missing_rows:
        g.append('| 书 | 系列 | 缺号 | 定性 |\n|---|---|---|---|\n')
        for c, name, ms in missing_rows:
            g.append(f'| {c} | {name} | {"、".join(map(str, ms))} | 编号跳号（源文件即如此，缺号位夹正常连载信件，无占位缺文；详见 logs/g4.md） |\n')
    else:
        g.append('书信与问答编号全部连续，无缺号。\n')
    g.append(f'- 谷歌作者目录缺 021–024（{base["gg_author_catalog"]["covered"]}/223）：作者自编目录未收录，只作对账不作收录依据。\n')
    g.append('## 5. 重复登记\n\n'
             f'- 书内重复 **{sum(f["dup_inbook"].values())}** 处: '
             + '、'.join(f'{c} {n}' for c, n in sorted(f['dup_inbook'].items())) + '\n'
             f'- 跨书精确重复 **{dc["paragraphs"]}** 段 / {dc["chars"]:,} 字: '
             + '；'.join(f'{k} {v["paragraphs"]} 段/{v["chars"]:,} 字' for k, v in sorted(dc["pairs"].items())) + '\n'
             f'- **GG↔SG1 107 段双出处登记**: 抽卡命中时两处来源并记、收敛为一张卡（明细见 logs/g6.md）\n')
    g.append('## 6. 异常台账\n\n'
             '| # | 事项 | 定性 | 处置/证据 |\n|---|---|---|---|\n'
             '| 1 | SG3 答读者问缺 48 | 编号跳号，无占位缺文 | 保留缺口，登记备查；logs/g4.md |\n'
             '| 2 | WJ2 周末问答缺 5 | 编号跳号，无占位缺文 | 同上 |\n'
             '| 3 | GG 作者目录缺 021–024 | 作者自编目录未收录（023 含「减法」相关标题） | 只作对账不作收录依据；logs/g5.md |\n'
             '| 4 | FZ 目录缺 4 个「本章小结」条目 | 编辑附写提炼层，正文有目录无 | 骨架优先读；logs/g5.md |\n'
             '| 5 | JJ 目录与正文标题 2 处差异 | 编校层与正文标点（，/,）、字形（鲁/魯）不一致 | 以正文标题为准，登记；logs/g5.md |\n'
             '| 6 | WJ2/JS 目录含小节级条目（1/15 条） | 目录粒度深于单元级（白话译文、板斧/误区等） | 弱证据对账；logs/g5.md |\n'
             '| 7 | 跨书重复 118 段（GG↔SG1 107） | 专栏内容跨书重载 | 双出处登记；logs/g6.md |\n'
             '| 8 | 书内重复 36 处 | 同书段落复现 | 登记去重线索；logs/g6.md |\n'
             '| 9 | X1 运营类 12 单元（彩蛋9/投票1/招募1/新书推荐1） | 专栏运营内容 | 保留原文不抽取；logs/g7.md |\n'
             '| 10 | 原文体內推广语（抢购/戳此/订阅《 等） | 专栏原文自带 | 保留原文，引用注意语境；logs/g7.md |\n'
             '| 11 | 非内容 13 单元（目录9/推广1/导航区1/转载目录1/作者目录1） | 编校与载体页 | 只登记不抽取；logs/g7.md |\n')
    g.append('## 7. 单元清单（全量 1,742 行）\n')
    for code in ('SG1', 'WJ2', 'SG3', 'GG', 'JS', 'SX', 'GJ', 'JJ', 'FZ', 'TD'):
        us = allu[code]
        g.append(f'\n### {code} {lvl[code]}（{len(us)} 单元）\n\n| unit_id | 类型 | 汉字 | 标题 |\n|---|---|---|---|\n')
        for i, u in enumerate(us, 1):
            n = s01_probe.cjk(u['text'])
            title = u["title"][:60].replace("|", "｜")
            g.append(f'| {code}-U{i:04d} | {u["cls"]} | {n:,} | {title} |\n')
    g.append('\n---\n'
             f'对账结论: **{"FAIL" if problems else "PASS"}**'
             + ('' if problems else '；分母三数 1,742 / 1,697 / 5,038,558 冻结，后续 P1 起以本文件为分母依据。\n'))
    if problems:
        g.append('\n## 与基线不一致项\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.d5) or '.', exist_ok=True)
    with open(a.d5, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))

    d = []
    d.append('# P0 分母冻结记录\n\n')
    d.append(f'- 冻结日期: {date.today().isoformat()}；冻结人: S08（scripts/s08_d5.py，可复跑）\n')
    d.append(f'- 源: `{a.src}`（SHA-256 见 spec/baseline_facts.json books[].sha256）\n\n')
    d.append('| 分母 | 数值 | 基线 | 一致 |\n|---|---|---|---|\n')
    d.append(f'| 总单元 | {denom[0]:,} | {denom_base[0]:,} | {"是" if denom[0] == denom_base[0] else "否"} |\n')
    d.append(f'| 内容单元 | {denom[1]:,} | {denom_base[1]:,} | {"是" if denom[1] == denom_base[1] else "否"} |\n')
    d.append(f'| 汉字数 | {denom[2]:,} | {denom_base[2]:,} | {"是" if denom[2] == denom_base[2] else "否"} |\n\n')
    d.append('## 口径说明\n\n'
             '- 总单元 1,742 = 内容单元 1,697（≥100 汉字）+ 结构容器 32（<100 汉字）+ 非内容 13（目录/导航/推广等）\n'
             '- 汉字数 5,038,558 = 十书 md 原文全部汉字（含各级标题行）；S02 汉字守恒即对此数闭环（Σ单元 char_count = 原文汉字）\n'
             '- 内容单元汉字 4,959,968 为内容单元子集口径，仅用于内容体量统计，不作分母\n'
             '- 分母一经冻结，P1 起所有覆盖率、抽取量计算以本记录为准；改动需走 v2 方案 §15.13 变更控制\n\n')
    d.append('## 逐书贡献\n\n| 书 | 总单元 | 内容单元 | 全书汉字 |\n|---|---|---|---|\n')
    for code in ('SG1', 'WJ2', 'SG3', 'GG', 'JS', 'SX', 'GJ', 'JJ', 'FZ', 'TD'):
        fb = f['per_book'][code]
        d.append(f'| {code} | {fb["total"]} | {fb["content"]} | {s01_probe.cjk(B[code]["text"]):,} |\n')
    d.append(f'| **合计** | **{denom[0]:,}** | **{denom[1]:,}** | **{denom[2]:,}** |\n')
    if problems:
        d.append('\n## 异常\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.denominator) or '.', exist_ok=True)
    with open(a.denominator, 'w', encoding='utf-8') as fp:
        fp.write(''.join(d))

    print(f'S08 D5 + 分母冻结: {"FAIL" if problems else "PASS"}（分母 {denom[0]:,}/{denom[1]:,}/{denom[2]:,}；'
          f'索引 {len(idx)} 行；D5 {a.d5}；冻结记录 {a.denominator}）')
    for p in problems:
        print('  问题:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
