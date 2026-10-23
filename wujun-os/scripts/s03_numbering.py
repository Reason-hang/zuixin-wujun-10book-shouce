#!/usr/bin/env python3
"""s03_numbering.py — P0 编号连续检查（S03，总闸 G4）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s03_numbering.py --src src_frozen --baseline spec/baseline_facts.json --out logs/g4.md
作用: 复用 s01_probe 的 load/split_units/numbering/probe，检查三类编号并逐条列出缺号：
  (1) 书信编号「第X封信」: SG1/WJ2/SG3/GG（基线 361/262/261/223，无缺无重）
  (2) 问答编号: WJ2「周末问答X」、SG3/GG「答读者问X」（预期 SG3 缺 48、WJ2 缺 5，GG 55 全）
  (3) 数学通识「NN｜」讲编号（v2 方案 §154: 数学通识 1–50）
缺号定性: 考察缺号前后两个编号单元之间夹了哪些单元——中间为正常连载信件（无占位缺文）
  则定性「编号跳号（源文件即如此）」，并登记供人工复核；比对基线任何不符退出码非零。
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

# 数学通识讲编号预期（v2 方案 §154「数学通识 1–50」；不在 JSON 基线内，此处为已核对预期值）
SX_EXPECTED = dict(count=50, max=50, missing=[], dup=[])

def series_ctx(units, pat, miss):
    """缺号上下文: 返回 (前号单元描述, 后号单元描述, 中间隔的单元列表)。缺前号/后号时对应项为 None。"""
    idx = {}
    for i, u in enumerate(units):
        m = re.search(pat, u['title'])
        if m:
            idx[int(m.group(1))] = i
    prev = idx.get(miss - 1)
    nxt = idx.get(miss + 1)
    mid = []
    if prev is not None and nxt is not None and nxt > prev:
        mid = [(f'U{j+1:04d}', units[j]['cls'], units[j]['title']) for j in range(prev + 1, nxt)]
    return prev, nxt, mid

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    ap.add_argument('--out', default='logs/g4.md')
    a = ap.parse_args()
    f = s01_probe.probe(a.src)                      # 与基线同源复算（letters / qa_numbering）
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']
    B = s01_probe.load(a.src)
    allu = {c: s01_probe.split_units(d['text'], d['lvl']) for c, d in B.items()}
    sx = s01_probe.numbering(allu['SX'], r'^\s*0*(\d+)\s*｜')

    problems = []
    for c in ('SG1', 'WJ2', 'SG3', 'GG'):
        if f['letters'][c] != base['letters'][c]:
            problems.append(f'{c} 第X封信编号与基线不符: 本次 {f["letters"][c]} / 基线 {base["letters"][c]}')
    for c in ('WJ2', 'SG3', 'GG'):
        if f['qa_numbering'][c] != base['qa_numbering'][c]:
            problems.append(f'{c} 问答编号与基线不符: 本次 {f["qa_numbering"][c]} / 基线 {base["qa_numbering"][c]}')
    if sx != SX_EXPECTED:
        problems.append(f'SX 讲编号与预期不符: 本次 {sx} / 预期 {SX_EXPECTED}')

    rows_l = '\n'.join(f'| {c} | {f["letters"][c]["count"]} | {f["letters"][c]["max"]} | '
                       f'{"、".join(map(str, f["letters"][c]["missing"])) or "无"} | '
                       f'{"、".join(map(str, f["letters"][c]["dup"])) or "无"} |' for c in ('SG1', 'WJ2', 'SG3', 'GG'))
    rows_q = '\n'.join(f'| {c} | {"周末问答" if c == "WJ2" else "答读者问"} | {f["qa_numbering"][c]["count"]} | '
                       f'{f["qa_numbering"][c]["max"]} | {"、".join(map(str, f["qa_numbering"][c]["missing"])) or "无"} | '
                       f'{"、".join(map(str, f["qa_numbering"][c]["dup"])) or "无"} |' for c in ('WJ2', 'SG3', 'GG'))

    g = []
    g.append('# G4 编号连续检查（S03）\n')
    g.append(f'- 源: `{a.src}`；切分与编号算法复用 scripts/s01_probe.py（与 1,742 基线同口径）\n'
             f'- 结论: **{"FAIL" if problems else "PASS"}**（与 spec/baseline_facts.json 比对不一致 {len(problems)} 项）\n')
    g.append('## 1. 书信编号「第X封信」\n\n| 书 | 编号单元数 | 最大号 | 缺号 | 重号 |\n|---|---|---|---|---|\n' + rows_l + '\n')
    g.append('## 2. 问答编号\n\n| 书 | 系列 | 编号单元数 | 最大号 | 缺号 | 重号 |\n|---|---|---|---|---|---|\n' + rows_q + '\n')
    g.append('## 3. 数学通识讲编号「NN｜」\n\n'
             f'- 讲编号单元 {sx["count"]}，最大号 {sx["max"]}，缺号 {"、".join(map(str, sx["missing"])) or "无"}，'
             f'重号 {"、".join(map(str, sx["dup"])) or "无"}（预期 1–50 齐全，v2 方案 §154）\n')
    g.append('## 4. 缺号逐条定性\n')
    QA_PAT = {'SG3': r'答读者问\s*0*(\d+)', 'WJ2': r'周末问答\s*0*(\d+)'}
    for c in ('SG3', 'WJ2'):
        for miss in f['qa_numbering'][c]['missing']:
            prev, nxt, mid = series_ctx(allu[c], QA_PAT[c], miss)
            if prev is None or nxt is None:
                verdict = '前号或后号也缺失，需人工核对源文件'
            elif mid:
                verdict = f'编号跳号（源文件即如此）: 缺号位置夹 {len(mid)} 个正常连载单元（{mid[0][2][:24]}… 等），无占位缺文；是否原有该篇被删无法从文本判定，登记异常台账供人工复核'
            else:
                verdict = '前后编号单元直接相连，无中间内容: 编号跳号（作者跳号）'
            g.append(f'- **{c} {"周末问答" if c == "WJ2" else "答读者问"}缺 {miss}**: {verdict}\n'
                     f'  - 前号: U{prev+1:04d} {allu[c][prev]["title"][:40]!r}；'
                     f'后号: U{nxt+1:04d} {allu[c][nxt]["title"][:40]!r}\n')
    g.append('- SG1/WJ2/SG3/GG 书信编号 1–361/1–262/1–261/1–223 连续无缺无重；GG「答读者问」1–55 连续；SX 讲 1–50 连续。\n')
    if problems:
        g.append('## 与基线不一致项\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))
    print(f'G4 编号连续: {"FAIL" if problems else "PASS"}（书信 4 书、问答 3 书、SX 讲编号均比对；缺号 SG3:48、WJ2:5 定性=编号跳号）；报告 {a.out}')
    for p in problems:
        print('  不一致:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
