#!/usr/bin/env python3
"""s07_reverse.py — P0 反向抽查（S07，总闸 G8）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s07_reverse.py --src src_frozen --units data/units --out logs/g8.md
作用: 不经 S02 的全量重建路径，独立做反向对账（v2 方案 §6.1 G8: 随机 ≥100 个位置反查所属单元，
      随机 ≥60 个单元核对标题、首句、尾句、字数；首中尾对读无差异）:
  (1) 位置反查: 每书随机 12 个行位置（共 120 ≥ 100），定位所属单元文件，逐行比对与原文一致；
  (2) 单元核对: 每书随机 8 个单元（共 80 ≥ 60），核对标题行、首/中/尾非空行与原文一致、char_count 与正文汉字一致。
随机种子固定（20261024），结果可复跑复现。任何差异或抽样量不足退出码非零。
"""
import argparse, bisect, csv, glob, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe
from s02_consistency import parse_unit

SEED = 20261024
POS_PER_BOOK, UNITS_PER_BOOK = 12, 8
MIN_POS, MIN_UNITS = 100, 60

def book_codes(units_dir):
    ds = sorted(d for d in glob.glob(os.path.join(units_dir, '*')) if os.path.isdir(d))
    return [os.path.basename(d) for d in ds], {os.path.basename(d): d for d in ds}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--out', default='logs/g8.md')
    a = ap.parse_args()
    B = s01_probe.load(a.src)
    codes, dirs = book_codes(a.units)
    problems, diffs = [], []
    rng = random.Random(SEED)
    n_pos = n_unit = 0
    per_book = []

    with open(os.path.join(a.units, 'units_index.csv'), encoding='utf-8') as fp:
        idx = list(csv.DictReader(fp))
    by_book = {}
    for r in idx:
        by_book.setdefault(r['book_code'], []).append(r)

    for code in codes:
        if code not in by_book:
            problems.append(f'{code}: units_index.csv 里没有该书')
            continue
        rows = sorted(by_book[code], key=lambda r: int(r['start_line']))
        starts = [int(r['start_line']) for r in rows]
        key = next(k for k, b, c, _ in s01_probe.BOOKS if c == code)
        src = next(p for p in glob.glob(os.path.join(a.src, '*.md')) if key in os.path.basename(p))
        lines = open(src, 'rb').read().decode('utf-8').split('\n')
        cache = {}

        def unit_body(r):
            path = os.path.join(dirs[code], f"unit_{int(r['unit_id'].split('U')[1]):04d}.md")
            if path not in cache:
                cache[path] = parse_unit(path)
            return cache[path]

        book_diff = 0
        # (1) 位置反查
        for _ in range(POS_PER_BOOK):
            pos = rng.randint(1, len(lines))
            i = bisect.bisect_right(starts, pos) - 1
            if i < 0 or not (int(rows[i]['start_line']) <= pos <= int(rows[i]['end_line'])):
                diffs.append(f'{code}: 第 {pos} 行不属于任何单元（行覆盖缺口）')
                book_diff += 1
                continue
            meta, body = unit_body(rows[i])
            off = pos - int(rows[i]['start_line'])
            n_pos += 1
            if meta['unit_id'] != rows[i]['unit_id'] or off >= len(body) or body[off] != lines[pos - 1]:
                diffs.append(f'{code}: 第 {pos} 行反查 {rows[i]["unit_id"]} 偏移 {off} 不符: '
                             f'单元侧 {body[off][:36]!r} / 原文侧 {lines[pos-1][:36]!r}')
                book_diff += 1
        # (2) 单元核对（标题、首/中/尾、字数）
        picks = rng.sample(rows, min(UNITS_PER_BOOK, len(rows)))
        for r in picks:
            meta, body = unit_body(r)
            s = int(meta['start_line'])
            ne = [j for j, l in enumerate(body) if l.strip()]
            n_unit += 1
            checks = [('标题', body[0] if body else '', lines[s - 1] if s - 1 < len(lines) else '')]
            if ne:
                for name, j in (('首句', ne[0]), ('中句', ne[len(ne) // 2]), ('尾句', ne[-1])):
                    checks.append((name, body[j], lines[s - 1 + j] if s - 1 + j < len(lines) else ''))
            for name, got, exp in checks:
                if got != exp:
                    diffs.append(f'{code} {r["unit_id"]} {name}不符: 单元侧 {got[:36]!r} / 原文侧 {exp[:36]!r}')
                    book_diff += 1
            n = s01_probe.cjk('\n'.join(body))
            if n != int(meta['char_count']):
                diffs.append(f'{code} {r["unit_id"]} 字数不符: char_count={meta["char_count"]} 实际 {n}')
                book_diff += 1
        per_book.append((code, POS_PER_BOOK, len(picks), book_diff))

    if n_pos < MIN_POS:
        problems.append(f'位置抽查量 {n_pos} < 要求 {MIN_POS}')
    if n_unit < MIN_UNITS:
        problems.append(f'单元抽查量 {n_unit} < 要求 {MIN_UNITS}')
    if diffs:
        problems.append(f'对读差异 {len(diffs)} 处（要求 0）')

    g = []
    g.append('# G8 反向抽查（S07）\n')
    g.append(f'- 源: `{a.src}`；单元: `{a.units}`；随机种子 {SEED}（可复跑复现）\n'
             f'- 抽查量: 位置 **{n_pos}**（要求 ≥{MIN_POS}）、单元 **{n_unit}**（要求 ≥{MIN_UNITS}，核对标题/首句/中句/尾句/字数）\n'
             f'- 结论: **{"FAIL" if problems else "PASS"}**（对读差异 {len(diffs)}，要求 0）\n\n'
             '| 书 | 位置抽查 | 单元抽查 | 差异 |\n|---|---|---|---|\n'
             + '\n'.join(f'| {c} | {p} | {u} | {d} |' for c, p, u, d in per_book) + '\n')
    if diffs:
        g.append('\n## 差异明细（前 50 条）\n\n' + '\n'.join(f'- {x}' for x in diffs[:50]) + '\n')
    if problems:
        g.append('\n## 问题\n\n' + '\n'.join(f'- {p}' for p in problems) + '\n')
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as fp:
        fp.write(''.join(g))
    print(f'G8 反向抽查: {"FAIL" if problems else "PASS"}（位置 {n_pos}、单元 {n_unit}、差异 {len(diffs)}）；报告 {a.out}')
    for p in problems[:10]:
        print('  问题:', p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
