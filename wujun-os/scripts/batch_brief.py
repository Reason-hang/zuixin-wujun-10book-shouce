#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_brief.py — 子代理派单生成器（J-126 提速工具 4）

把每批手写约 1500 字的派单工单模板化：规则清单、行窗表（现算或引用
logs/batch_windows_pending_20261025.md）、card_writer 命令模板、HC 红线、
汇报格式一次渲染——消灭行窗手抄错（B-044 事件根源）与口径漂移。

用法：
  python3 scripts/batch_brief.py <batch_id> <agent_code> > /tmp/brief_<agent>.md
输出即派单提示词全文（stdout）。
"""
import json, csv, sys, os

RULES = """## 必读规则（先读再抽，缺一不可）
1. spec/rules_v0.9.md（R1-R8）
2. spec/pillars.yaml（D01-D10）
3. spec/exclusions.yaml（X1-X8：时效X2/X6、纯读者回信X7、运营X1、游记X3只抽方法论、教育X5、婚恋家庭X5+方法论例外成卡）
4. spec/boundary_rules.md（规则①-⑫）
5. 格式样例：data/cards/{sample_batch}/{sample_unit}.json"""

HC = """## HC 红线
说话人先行（名人原话被吴军转述=E2、speaker"转述·第三方"、notes 注被转述者；读者发言不得 E1）；无锚不写；指纹词逐字从原文复制勿凭记忆；案例承载可迁移判断则抽卡（勿整体 X4），纯史实背景才 X4。"""

FLOW = """## 抽卡流程（card_writer.py 断言前置）
1. 逐单元读原文→判说话人→找结论句→构造卡片数组 JSON（不含 sha1/claim_id/unit_id，工具自动生成）
2. 写盘：python3 scripts/card_writer.py <unit_id> {batch_dir} "{book}" <w0> <w1> --extractor {agent} --batch-id {batch_id} --disposal K --reason "<一句话理由>" [--x-disposals-file /tmp/xd_<uid>.json] < cards_<uid>.json
3. 卡片字段：speaker/claim_text(≤60字)/quote(≤15字且锚内连续子串)/anchor{{start_line,end_line,fingerprint[≤3]}}/evidence_level(E1-E4)/pillar_candidates/concept_key/ability_tags(思/学/沟/做)/notes
4. 工具自动重算 SHA1、校验 quote/指纹词锚内子串、行窗、锚≤800、claim≤60、枚举、赋 claim_id、防覆盖；报错即修即重跑，报错未写盘无脏文件
5. 每单元 4~9 卡；纯史实/游记为主的信可 2~3 卡并在 reason 说明；整单元确无可抽卡可写 0 卡包装文件（disposal=X，参照 data/cards/T-P3b-B-048/SG3-U0068.json 先例）"""

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    batch_id, agent = sys.argv[1], sys.argv[2]
    bp = json.load(open('data/batches/batch_plan.json'))
    bs = bp if isinstance(bp, list) else bp.get('batches', bp)
    b = [x for x in bs if x['batch_id'] == batch_id][0]
    rows = list(csv.DictReader(open('data/units/units_index.csv')))
    us = [r for r in rows if r['unit_id'] in b['unit_ids']]
    book_code = us[0]['unit_id'].split('-U')[0]
    books = {'SG3': '《硅谷来信3》｜原著完整精排典藏版｜Codex处理_副本.md',
             'SG1': '《硅谷来信》｜原著完整精排典藏版｜Codex处理_副本.md',
             'GG': '《谷歌方法论》[吴军]-原著完整精排版_副本.md',
             'WJ2': '《吴军来信2》原著完整精排版--Codex处理_副本.md',
             'FZ': '《富足：数字时代的个人财富与认知升级》[吴军]-原著完整精排版_副本2.md'}
    if book_code not in books:
        sys.exit(f'未知书码 {book_code}')
    book = f'src_frozen/{books[book_code]}'
    batch_dir = f'data/cards/{batch_id.replace("T-P3x-", "T-P3b-")}'
    num = int(batch_id[-3:])
    sample = {'SG3': ('T-P3b-B-047', 'SG3-U0049'), 'SG1': ('T-P3a-B-101', 'SG1-U0007'),
              'GG': ('T-P3b-B-066', 'GG-U0013'), 'WJ2': ('T-P3b-B-042', 'WJ2-U0307'),
              'FZ': ('T-P3a-B-103', 'FZ-U0007')}.get(book_code, ('T-P3b-B-047', 'SG3-U0049'))
    print(f'你是 WJ-OS 项目批次抽取代理，代号 {agent}，领工单 {batch_id}（目录名 {batch_dir.split("/")[-1]}）。工作目录：/Users/lizhihang/Documents/【Zcode--project】/【最新吴军10本书手册工程化】/wujun-os。')
    print(f'\n## 文件范围（互斥红线，只能写这两个路径）\n- {batch_dir}/\n- logs/cards_verify_{batch_id}_self.md\n严禁触碰：data/unitcards/、state/、data/gold/、data/cards/ 其他目录、git——由主智能体执行。')
    print(f'\n{RULES}'.replace('{sample_batch}', sample[0]).replace('{sample_unit}', sample[1]))
    print(f'\n## 工单：原书{book.split("/")[1].split("｜")[0].split("[")[0].strip("《》")} {len(us)} 单元（{b["chars"]:,} 字）\n原书：{book}')
    for r in us:
        print(f"{r['unit_id']}|{r['start_line']}-{r['end_line']}")
    print('\n' + FLOW.format(batch_dir=batch_dir, book=book, agent=agent, batch_id=batch_id))
    print('\n' + HC)
    print(f'\n## 自检收尾\n{len(us)} 单元写盘后：python3 scripts/verify_cards.py --dirs {batch_dir} --out logs/cards_verify_{os.path.basename(batch_dir)}_self.md，须 0 FAIL。若即将中断：保留已写盘文件，最终消息说明进度到哪个单元。')
    print('\n## 汇报格式（最终消息）\n各单元卡数与处置、E1/E2 分布、转述·第三方名单、X 处置条数、verify 结果、批内同名概念键、模糊点。不要贴完整 JSON。')

if __name__ == '__main__':
    main()
