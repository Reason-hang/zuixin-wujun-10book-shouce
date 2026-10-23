#!/usr/bin/env python3
"""s02_consistency.py — P0 行覆盖与汉字守恒对账（S02，总闸 G2/G3）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s02_consistency.py --src src_frozen --units data/units --report logs/g2g3.md
校验A 行覆盖（G2）: 每本书的单元按行区间拼回与原文比对——首单元从第 1 行起、相邻单元无缺口无重叠、
                  末单元止于总行数，且全部单元正文逐行拼回后与原文完全一致。
校验B 汉字守恒（G3）: 每个单元 char_count == 其正文汉字数，且 Σchar_count == 原文汉字总数，差为 0。
报告写 logs/g2g3.md；已切分的书任一校验失败退出码非零；十书中未配置切分的书跳过并注明「未切分」。
"""
import argparse, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe
from s01_split import find_src

FIELDS = ('unit_id', 'book_code', 'type', 'char_count', 'start_line', 'end_line')

def parse_unit(path):
    """读单元文件 -> (meta dict, 正文行 list)；格式不合法抛 ValueError。"""
    ls = open(path, encoding='utf-8').read().split('\n')
    if ls and ls[-1] == '':  # S01 写出时固定补的结尾换行
        ls = ls[:-1]
    if not ls or ls[0].strip() != '---':
        raise ValueError('缺元数据头')
    try:
        j = ls.index('---', 1)
    except ValueError:
        raise ValueError('元数据头未闭合') from None
    meta = {}
    for ln in ls[1:j]:
        if ':' not in ln:
            raise ValueError(f'元数据行不合法: {ln!r}')
        k, v = ln.split(':', 1)
        meta[k.strip()] = v.strip()
    miss = [k for k in FIELDS if k not in meta]
    if miss:
        raise ValueError(f'缺字段 {miss}')
    for k in ('char_count', 'start_line', 'end_line'):
        if not re.fullmatch(r'\d+', meta[k]):
            raise ValueError(f'{k}={meta[k]!r} 不是非负整数')
    return meta, ls[j + 1:]

def check_book(code, src_path, udir):
    """返回 (problems, stats)。stats: units, C/S/N, sum_chars, total_lines, total_cjk。"""
    text = open(src_path, 'rb').read().decode('utf-8')  # 与 s01_probe.load 一致
    lines = text.split('\n')
    stats = dict(units=0, C=0, S=0, N=0, sum_chars=0, total_lines=len(lines), total_cjk=s01_probe.cjk(text))
    files = sorted(glob.glob(os.path.join(udir, 'unit_*.md')))
    if not files:
        return [f'{udir} 里没有 unit_*.md 文件'], stats
    units = []
    for p in files:
        try:
            meta, content = parse_unit(p)
        except ValueError as e:
            return [f'{os.path.basename(p)}: {e}'], stats
        units.append((meta, content, os.path.basename(p)))
    units.sort(key=lambda x: int(x[0]['start_line']))
    stats['units'] = len(units)
    P = []
    prev_end = 0
    for i, (meta, content, name) in enumerate(units, 1):
        s, e = int(meta['start_line']), int(meta['end_line'])
        if meta['unit_id'] != f'{code}-U{i:04d}':
            P.append(f'{name}: unit_id={meta["unit_id"]} 应为 {code}-U{i:04d}（按 start_line 排序后的位置序号）')
        if meta['book_code'] != code:
            P.append(f'{name}: book_code={meta["book_code"]} ≠ 目录书码 {code}')
        if meta['type'] not in ('C', 'S', 'N'):
            P.append(f'{name}: type={meta["type"]!r} 不在 C/S/N')
        else:
            stats[meta['type']] += 1
        if e < s:
            P.append(f'{name}: end_line={e} < start_line={s}')
        elif s != prev_end + 1:
            if s > prev_end + 1:
                P.append(f'行缺口: 第 {prev_end + 1}–{s - 1} 行未被任何单元覆盖（{name} 自第 {s} 行起）')
            else:
                P.append(f'行重叠: {name} 自第 {s} 行起，与前一单元（止于第 {prev_end} 行）重叠')
        prev_end = max(prev_end, e)
        n = s01_probe.cjk('\n'.join(content))
        stats['sum_chars'] += int(meta['char_count'])
        if int(meta['char_count']) != n:
            P.append(f'{name}: char_count={meta["char_count"]} ≠ 正文实际汉字 {n}')
    if units and prev_end != len(lines):
        P.append(f'末单元止于第 {prev_end} 行 ≠ 原文总行数 {len(lines)}')
    rebuilt = [l for _, content, _ in units for l in content]
    if rebuilt != lines:
        k = next((i for i in range(min(len(rebuilt), len(lines))) if rebuilt[i] != lines[i]),
                 min(len(rebuilt), len(lines)))
        P.append(f'单元拼回与原文不一致: 共 {len(rebuilt)} 行 vs 原文 {len(lines)} 行，'
                 f'首次差异在第 {k + 1} 行（单元侧 {rebuilt[k][:40]!r} / 原文侧 {lines[k][:40]!r}）')
    if stats['sum_chars'] != stats['total_cjk']:
        P.append(f'汉字守恒破缺: Σ单元 char_count={stats["sum_chars"]:,} ≠ 原文汉字 {stats["total_cjk"]:,}，差 {stats["sum_chars"] - stats["total_cjk"]:+,}')
    return P, stats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--report', default='logs/g2g3.md')
    a = ap.parse_args()
    lvl_by_code = {c: (k, b) for k, b, c, _ in s01_probe.BOOKS}
    dirs = sorted(d for d in glob.glob(os.path.join(a.units, '*')) if os.path.isdir(d))
    if not dirs:
        raise SystemExit(f'{a.units} 下没有书目录；先 make split')
    results, problems, stat_by_code = {}, {}, {}
    for d in dirs:
        code = os.path.basename(d)
        if code not in lvl_by_code:
            results[code] = 'FAIL'
            problems[code] = [f'未知书码目录 {code}，不在 s01_probe.BOOKS 十书之内']
            continue
        try:
            src_path = find_src(a.src, lvl_by_code[code][0])
        except SystemExit as e:
            results[code] = 'FAIL'
            problems[code] = [str(e)]
            continue
        P, stats = check_book(code, src_path, d)
        results[code] = 'PASS' if not P else 'FAIL'
        stat_by_code[code] = stats
        if P:
            problems[code] = P
    rows, n_pass = [], 0
    for k, _, code, _ in s01_probe.BOOKS:  # 按十书固定顺序出报告
        if code in results:
            st = results[code]
            if st == 'PASS':
                stats = stat_by_code[code]
                n_pass += 1
                rows.append(f'| {code} | {stats["units"]} | {stats["C"]}/{stats["S"]}/{stats["N"]} | 缺口 0，重叠 0 | '
                            f'{stats["sum_chars"]:,} / {stats["total_cjk"]:,} / 0 | PASS |')
            else:
                rows.append(f'| {code} | - | - | - | - | FAIL |')
        else:
            rows.append(f'| {code} | - | - | - | - | 未切分 |')
    checked = [c for c in results]
    verdict = 'PASS' if n_pass == len(checked) else 'FAIL'
    os.makedirs(os.path.dirname(a.report) or '.', exist_ok=True)
    with open(a.report, 'w', encoding='utf-8') as g:
        g.write('# G2/G3 单元对账报告（S02）\n\n'
                f'- 源: `{a.src}`；单元目录: `{a.units}`\n'
                f'- 校验A 行覆盖（G2）与校验B 汉字守恒（G3）；结果: **{verdict}**'
                f'（已切分 {len(checked)} 本，通过 {n_pass}，未切分 {10 - len(checked)}）\n\n'
                '| 书码 | 单元数 | 内容C/容器S/非内容N | 行覆盖（缺口/重叠） | 汉字守恒（Σ单元/原文/差） | 结果 |\n'
                '|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n')
        if problems:
            g.write('\n## 失败明细\n\n')
            for code in sorted(problems):
                for m in problems[code][:20]:
                    g.write(f'- {code}: {m}\n')
    print(f'G2/G3 对账: {verdict}（已切分 {len(checked)} 本，通过 {n_pass}）；报告 {a.report}')
    for code in sorted(problems):
        for m in problems[code][:10]:
            print(f'  FAIL {code}: {m}')
    sys.exit(0 if verdict == 'PASS' else 1)

if __name__ == '__main__':
    main()
