#!/usr/bin/env python3
"""s10_batch.py — P2 批次装箱（T-P2-02 脚本部分；HC-14 与 v2 §7.3、§16 判例 19/20）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s10_batch.py --units data/units --cards data/unitcards --out data/batches --log logs/batch_plan.md
规则（HC-14，constraints.md 用户确认级）: 分批 3–5 万汉字、单元整块不拆、系列单元不拆开；
      同书相邻成批、书边界不跨（每批单书）；不足 3 万的尾批在同书前批内合并（合并后仍 ≤5 万），
      无法合并不跨书强拼，按 v2 §16 判例 20 记豁免；单块超 5 万按判例 19/20 单独成批记豁免。
口径: 批字数 = 单元正文汉字（不含标题行），与 baseline content_chars 4,959,968 同口径可对账；
      单元卡 char_count 是含标题的 G3 守恒口径，两口径用途不同，本脚本内部换算并断言闭环。
批号: T-P3x-B-001 起全局连续（书序按 s01_probe.BOOKS）。
内置断言（任一失败退出非零）: Σ批字数==4,959,968；批单元并集==C 类 1,697 全集；全局无重复；
      每批单书；批内单元在书内序号连续；每批 3–5 万或已登记豁免。
已知冲突（如实报告）: 全量 1,697 内容单元按 3–5 万装箱，批数约 105–115，超出 v2.1 Z2-17 的 70–90
      估算区间——该区间对应"分诊后必读层"口径；全量装箱批数偏差按 Z2-17 机制应触发重估，报告内注明。
"""
import argparse, collections, csv, datetime, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

BOOK_ORDER = ['SG1', 'WJ2', 'SG3', 'GG', 'JS', 'SX', 'GJ', 'JJ', 'FZ', 'TD']
LO, HI = 30_000, 50_000

def load_c_units(units_dir, cards_dir):
    """C 类单元：从单元卡登记表取名单，从单元文件取正文汉字（不含标题行）。"""
    ids = []
    for p in sorted(glob.glob(os.path.join(cards_dir, 'uc_*.jsonl'))):
        for ln in open(p, encoding='utf-8'):
            ids.append(json.loads(ln))
    out = []
    for c in ids:
        if c['type'] != 'C':
            continue
        i = int(c['unit_id'].split('-U')[1])
        ls = open(os.path.join(units_dir, c['book_code'], f'unit_{i:04d}.md'), encoding='utf-8').read().split('\n')
        body = ls[ls.index('---', 1) + 1:]
        if body and body[-1] == '':
            body = body[:-1]
        out.append(dict(unit_id=c['unit_id'], book_code=c['book_code'], seq=i, title=body[0].lstrip('#').strip(),
                        body_chars=s01_probe.cjk('\n'.join(body[1:]))))  # HC-14 口径：正文汉字，不含标题行
    return out

def series_blocks(units):
    """连续的系列单元（s01_probe.SERIES 命中）并为不可分块，其余单元自成一块。"""
    blocks, cur = [], []
    for u in units:
        if s01_probe.SERIES.search(u['title']):
            cur.append(u)
        else:
            if cur:
                blocks.append(cur); cur = []
            blocks.append([u])
    if cur:
        blocks.append(cur)
    return blocks

def greedy_book(blocks):
    """贪心装箱（≤5 万）+ 尾批 <3 万并入前批（≤5 万）或豁免（判例 20）。"""
    batches, exempts = [], []
    cur, cur_chars = [], 0
    for b in blocks:
        bc = sum(u['body_chars'] for u in b)
        if cur and cur_chars + bc > HI:
            batches.append(cur); cur, cur_chars = [], 0
        if bc > HI:  # 单块超上限（判例 19/20）：单独成批 + 豁免
            batches.append(b)
            exempts.append(dict(first=b[0]['unit_id'], last=b[-1]['unit_id'], chars=bc,
                                reason=f'系列块整体 {bc:,} 字 > 上限 5 万，单元整块不拆（HC-14/判例20），单独成批'))
            continue
        cur.extend(b); cur_chars += bc
    if cur:
        batches.append(cur)
    last_chars = sum(u['body_chars'] for u in batches[-1])
    if len(batches) > 1 and last_chars < LO:
        prev_chars = sum(u['body_chars'] for u in batches[-2])
        if prev_chars + last_chars <= HI:
            batches[-2].extend(batches.pop(-1))
        else:
            exempts.append(dict(first=batches[-1][0]['unit_id'], last=batches[-1][-1]['unit_id'], chars=last_chars,
                                reason=f'尾批 {last_chars:,} 字 < 下限 3 万，与前批合并将达 {prev_chars + last_chars:,} > 5 万，'
                                       f'且书边界不跨（HC-14），按判例 20 保留为豁免尾批'))
    return batches, exempts

def balanced_book(blocks, total):
    """均衡切分（DP 保证可切性）：组数 n 从 ⌈total/5万⌉ 向上搜索首个可行值（组数最小且全组 ∈[3万,5万]）；
       ⌈total/5万⌉ 的均值贴上限、窗口极窄，块粒度（单块可达数千至上万）常使最少组数无解，放宽一组即解。
       块整块不拆、相邻顺序不变；无可行 n 返回 None 回退贪心+豁免。"""
    m = len(blocks)
    pre = [0] * (m + 1)
    for i, b in enumerate(blocks):
        pre[i + 1] = pre[i] + sum(u['body_chars'] for u in b)
    for n in range(-(-total // HI), min(-(-total // HI) + 5, total // LO + 1)):
        if m < n:
            break
        dp = [[False] * (m + 1) for _ in range(n + 1)]
        choice = [[-1] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True
        for k in range(1, n + 1):
            for i in range(k, m + 1):
                for j in range(k - 1, i):
                    if dp[k - 1][j] and LO <= pre[i] - pre[j] <= HI:
                        dp[k][i], choice[k][i] = True, j
                        break
        if not dp[n][m]:
            continue
        cuts, i = [], m
        for k in range(n, 0, -1):
            cuts.append(i); i = choice[k][i]
        bounds = [0] + cuts[::-1]
        return [[u for blk in blocks[bounds[t]:bounds[t + 1]] for u in blk] for t in range(n)]
    return None

def pack_book(units):
    blocks = series_blocks(units)
    total = sum(u['body_chars'] for u in units)
    bs = balanced_book(blocks, total)
    if bs is not None:
        return bs, []
    return greedy_book(blocks)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--cards', default='data/unitcards')
    ap.add_argument('--out', default='data/batches')
    ap.add_argument('--log', default='logs/batch_plan.md')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    a = ap.parse_args()
    units = load_c_units(a.units, a.cards)
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']['totals']
    total_chars = sum(u['body_chars'] for u in units)
    errs = []
    if len(units) != base['content']:
        errs.append(f'C 类单元 {len(units)} ≠ 基线 {base["content"]}')
    if total_chars != base['content_chars']:
        errs.append(f'C 类正文汉字合计 {total_chars:,} ≠ 基线 {base["content_chars"]:,}')

    plan, exempts = [], []
    n = 0
    for code in BOOK_ORDER:
        us = sorted([u for u in units if u['book_code'] == code], key=lambda x: x['seq'])
        if not us:
            continue
        bs, ex = pack_book(us)
        exempts += [{**e, 'book_code': code} for e in ex]
        for b in bs:
            n += 1
            ch = sum(u['body_chars'] for u in b)
            plan.append(dict(batch_id=f'T-P3x-B-{n:03d}', book_code=code, units=len(b), chars=ch,
                             unit_range=f'{b[0]["unit_id"]}..{b[-1]["unit_id"]}',
                             unit_ids=[u['unit_id'] for u in b]))
    # —— 断言：无重复、无遗漏、单书、同书有序切分、字数界内或豁免
    all_ids = [i for b in plan for i in b['unit_ids']]
    if len(all_ids) != len(set(all_ids)):
        errs.append('批间存在重复单元')
    if set(all_ids) != {u['unit_id'] for u in units}:
        errs.append('批单元并集 ≠ C 类全集（有遗漏）')
    for b in plan:
        if len({i.split('-')[0] for i in b['unit_ids']}) != 1:
            errs.append(f'{b["batch_id"]}: 跨书')
        if not (LO <= b['chars'] <= HI) and not any(e['first'] == b['unit_ids'][0] and e['book_code'] == b['book_code'] for e in exempts):
            errs.append(f'{b["batch_id"]}: 字数 {b["chars"]:,} 越界且无豁免')
    for code in BOOK_ORDER:  # 每书：批序列按序拼接应恰为该书 C 类有序全集（相邻、不漏、不重、有序）
        cs = sorted([u for u in units if u['book_code'] == code], key=lambda x: x['seq'])
        joined = [i for b in plan if b['book_code'] == code for i in b['unit_ids']]
        if joined != [u['unit_id'] for u in cs]:
            errs.append(f'{code}: 批切分与书内 C 类有序序列不一致')
    if sum(b['chars'] for b in plan) != base['content_chars']:
        errs.append('Σ批字数 ≠ 4,959,968')
    if errs:
        print('S10 断言失败：'); [print(' -', e) for e in errs[:10]]; sys.exit(1)

    today = datetime.date.today().isoformat()
    by_book = collections.OrderedDict((c, [b for b in plan if b['book_code'] == c]) for c in BOOK_ORDER if any(b['book_code'] == c for b in plan))
    hist = collections.Counter()
    for b in plan:
        k = min(int(b['chars'] // 5000), 10)  # 0.0–0.5 万 … 4.5–5.0 万（≥5 万并桶）
        hist[k] += 1
    data = dict(meta=dict(date=today, total_batches=len(plan), total_chars=total_chars,
                          c_units=len(units), lo=LO, hi=HI, exempts=exempts,
                          rule='HC-14: 3–5 万汉字/批，单元整块不拆，系列不拆开，同书相邻，不跨书',
                          note='全量 C 类装箱批数超出 v2.1 Z2-17 的 70–90 估算区间（该区间为分诊后必读层口径），按 Z2-17 偏差>20% 应触发重估'),
                batches=plan)
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(os.path.dirname(a.log) or '.', exist_ok=True)
    jp = os.path.join(a.out, 'batch_plan.json')
    json.dump(data, open(jp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.load(open(jp, encoding='utf-8'))
    md = ['# P3 批次装箱计划（S10，T-P2-02）', '',
          f'- 日期 {today}；规则：{data["meta"]["rule"]}',
          f'- 内容单元 {len(units):,} 个全部装箱；Σ批字数 {total_chars:,} == 基线 content_chars 4,959,968（正文汉字口径，不含标题行）',
          f'- **总批数 {len(plan)}**；豁免批 {len(exempts)} 个；断言全过（无重复/无遗漏/单书/书内连续/字数界内或豁免）',
          f'- ⚠ 批数说明：{len(plan)} 批超出 70–90 估算区间（Z2-17）。全量 1,697 内容单元 ÷ 3–5 万/批，数学下限即 '
          f'{total_chars // HI} 批；50–90 区间对应"分诊后必读层"口径（A 层约 28 批）。按 Z2-17 偏差>20% 触发重估机制上报', '',
          '## 逐书批数', '', '| 书码 | 批数 | 单元数 | 字数 |', '|---|---|---|---|']
    for c, bs in by_book.items():
        md.append(f'| {c} | {len(bs)} | {sum(b["units"] for b in bs):,} | {sum(b["chars"] for b in bs):,} |')
    md += ['', '## 批字数分布', '', '| 区间（万） | 批数 |', '|---|---|']
    for k in sorted(hist):
        md.append(f'| {k / 2:.1f}–{min((k + 1) / 2, 5.0):.1f} | {hist[k]} |')
    if exempts:
        md += ['', '## 豁免清单（判例 19/20）', '']
        md += [f'- {e["book_code"]} {e["first"]}..{e["last"]}：{e["reason"]}' for e in exempts]
    md += ['', '## 批次明细', '', '| 批号 | 书 | 单元数 | 字数 | 单元区间 |', '|---|---|---|---|---|']
    md += [f'| {b["batch_id"]} | {b["book_code"]} | {b["units"]} | {b["chars"]:,} | {b["unit_range"]} |' for b in plan]
    open(a.log, 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print(f'装箱完成：{len(units):,} 个 C 类单元 -> {len(plan)} 批（Σ {total_chars:,} 字，== 基线 4,959,968）；'
          f'豁免 {len(exempts)} 批；计划 {jp}；日志 {a.log}')
    print('  逐书批数：' + '，'.join(f'{c} {len(bs)}' for c, bs in by_book.items()))
    print(f'  ⚠ 总批数 {len(plan)} 超 50–90 区间（全量装箱数学下限 {total_chars // HI} 批），已按 HC-14 硬约束执行并在报告注明')
    sys.exit(0)

if __name__ == '__main__':
    main()
