#!/usr/bin/env python3
"""s11_readlevel.py — P2 读法层 A/B/C 标注（T-P2-04/05）

规则来源：v2 §7.2（quiz Q10、CHG-006、行 172/642）+ HC-15 + CHG-025（P2A 审计修正①②）：
  A 精读 = 六本成书正文；周末互动、回信精选；来信里的骨架单元；领域直连单元
  B 标准 = 问答（答读者问、周末问答）；高信号来信（GG 全书、SG3 有划重点的信）
  C 快处置 = 其余来信（WJ2、SG1、SG3 无划重点的信）
  S/N 结构与非内容单元：不读，disposal 预置 N
领域直连判据（v2 行 172，CHG-025 修订）：正文关键词 跨境|电商|物流|供应链|出海|定价|库存|仓储|运费 命中 ≥3 次；
  "关税"单独提阈（自身命中 ≥5 次才计入）；标题含 日记|之旅|摄影|彩蛋 的单元（游记/生活文体）不参与领域直连判定
骨架正则（CHG-025 修订）：总览|目录|作者目录|发刊词（去"系列"——系列单元由 series_group 同组处置，非骨架）
断言闸门（规格记录值，T-P2-05 强制核对，CHG-025 同步规格）：领域直连 27（原 33）、问答 170、周末互动 24
内容单元每次运行全量重算 read_level/domain_direct/tag_rules（幂等；disposal/batch_id 等回写字段不动）

用法: python3 scripts/s11_readlevel.py  （在 wujun-os/ 执行）
输出: 更新 data/unitcards/uc_*.jsonl（read_level、disposal、domain_direct、tag_rules）
      logs/p2_triage.md（分诊表）
"""
import glob, json, os, re, sys

BOOKS_A = {'TD', 'FZ', 'JJ', 'GJ', 'SX', 'JS'}          # 六本成书
KW_DOMAIN = ['跨境', '电商', '物流', '供应链', '出海', '定价', '库存', '仓储', '运费']
KW_GUANSHUI, KW_GUANSHUI_MIN = '关税', 5               # CHG-025：关税单独提阈
RE_EXCLUDE = re.compile(r'日记|之旅|摄影|彩蛋')           # CHG-025：文体排除，不参与领域直连
RE_QA = re.compile(r'答读者问|周末问答|回用户|回同学')          # 与 s01_probe.QA 同源（170 断言）
RE_INTERACT = re.compile(r'周末互动|周末放送|回信精选|精选')     # 与 s01_probe.INTERACT 同源（24 断言）
RE_SKELETON = re.compile(r'总览|目录|作者目录|发刊词')           # CHG-025：去"系列"

def unit_path(uid):
    book, num = uid.split('-U')
    return f'data/units/{book}/unit_{num}.md'

def main():
    rows = []
    for jl in sorted(glob.glob('data/unitcards/uc_*.jsonl')):
        out = []
        for line in open(jl, encoding='utf-8'):
            c = json.loads(line)
            uid, book, typ = c['unit_id'], c['book_code'], c['type']
            rules = []
            if typ in ('S', 'N'):
                c['disposal'] = 'N'
                rules.append('S/N→不读')
            else:
                # CHG-025：内容单元全量重算（幂等）；disposal/batch_id 等回写字段不动
                text = open(unit_path(uid), encoding='utf-8').read()
                m = re.search(r'^## (.+)$', text, re.M)
                title = m.group(1) if m else ''
                kw_hits = sum(text.count(k) for k in KW_DOMAIN)
                if text.count(KW_GUANSHUI) >= KW_GUANSHUI_MIN:
                    kw_hits += text.count(KW_GUANSHUI)
                domain = kw_hits >= 3 and not RE_EXCLUDE.search(title)
                c['domain_direct'] = domain
                if book in BOOKS_A:
                    lvl = 'A'; rules.append('成书→A')
                elif RE_QA.search(title):
                    lvl = 'B'; rules.append('问答→B(HC-15)')
                elif RE_INTERACT.search(title):
                    lvl = 'A'; rules.append('互动/回信精选→A')
                elif RE_SKELETON.search(title):
                    lvl = 'A'; rules.append('骨架单元→A')
                elif domain:
                    lvl = 'A'; rules.append('领域直连→A')
                elif book == 'GG':
                    lvl = 'B'; rules.append('谷歌来信→B(作者目录骨架)')
                elif book == 'SG3':
                    lvl = 'B' if '划重点' in text else 'C'
                    rules.append('SG3划重点→B' if lvl == 'B' else 'SG3无划重点→C')
                else:
                    lvl = 'C'; rules.append('其余来信→C')
                c['read_level'] = lvl
            c['tag_rules'] = rules
            out.append(c)
            rows.append(c)
        with open(jl, 'w', encoding='utf-8') as f:
            for c in out:
                f.write(json.dumps(c, ensure_ascii=False) + '\n')

    # 断言闸门（T-P2-05）
    n_dom = sum(1 for c in rows if c.get('domain_direct'))
    n_qa = sum(1 for c in rows if any('问答' in r for r in c.get('tag_rules', [])))
    n_int = sum(1 for c in rows if any('互动' in r for r in c.get('tag_rules', [])))
    checks = [('领域直连=27', n_dom, 27), ('问答=170', n_qa, 170), ('周末互动=24', n_int, 24)]  # CHG-025：33→27
    ok = True
    msgs = []
    for name, got, want in checks:
        s = 'PASS' if got == want else 'FAIL'
        if got != want: ok = False
        msgs.append(f'{name}: 实测 {got} {s}')
        print(msgs[-1])

    # 汇总
    from collections import Counter
    lv = Counter(c.get('read_level') or 'N/A' for c in rows)
    chars = Counter()
    for c in rows:
        chars[c.get('read_level') or 'N/A'] += c.get('char_count', 0)
    L = ['# P2 分诊表（T-P2-09/10，脚本产出勿手改）', '', f'- 单元总数 {len(rows)}（=1,742 断言：{"PASS" if len(rows)==1742 else "FAIL"}）', '',
         '| 读法层 | 单元数 | 汉字数 | 说明 |', '|---|---|---|---|']
    for k in ('A', 'B', 'C', 'N/A'):
        L.append(f"| {k} | {lv.get(k,0)} | {chars.get(k,0):,} | {'精读' if k=='A' else '标准' if k=='B' else '快处置' if k=='C' else 'S/N 不读'} |")
    L += ['', '## 逐书读法层分布', '', '| 书 | A | B | C | S/N |', '|---|---|---|---|---|']
    for book in ['SG1','WJ2','SG3','GG','JS','SX','GJ','JJ','FZ','TD']:
        sub = [c for c in rows if c['book_code'] == book]
        cc = Counter(c.get('read_level') or 'N/A' for c in sub)
        L.append(f"| {book} | {cc.get('A',0)} | {cc.get('B',0)} | {cc.get('C',0)} | {cc.get('N/A',0)} |")
    L += ['', '## 断言闸门（T-P2-05）'] + [f'- {m}' for m in msgs]
    open('logs/p2_triage.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f"分诊表 -> logs/p2_triage.md；读法层分布 {dict(lv)}")
    sys.exit(0 if ok and len(rows) == 1742 else 1)

if __name__ == '__main__':
    main()
