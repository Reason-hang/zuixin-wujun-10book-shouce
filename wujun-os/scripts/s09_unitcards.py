#!/usr/bin/env python3
"""s09_unitcards.py — P2 单元卡生成（T-P2-01 脚本部分，对应 v2 §16.2 单元记录的 P2 落地子集）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s09_unitcards.py --units data/units --out data/unitcards
作用: 读 data/units/units_index.csv 与各单元文件元数据头（交叉断言一致，防索引与产物漂移），
      按 PK（P2 分诊）前占位口径生成 data/unitcards/uc_<书码>.jsonl——每行一张单元卡：
      unit_id、book_code、type(C/S/N)、char_count（含标题行汉字，G3 守恒口径）、start_line、end_line、
      read_level=null（待 P2 标注）、disposal=null（待 §15.7.1）、batch_id=null（待 S10 回填）。
      1,742 个单元全部登记；类型计数与 spec/baseline_facts.json 的 1,742=1,697+32+13 断言一致。
"""
import argparse, csv, glob, json, os, sys

BOOK_ORDER = ['SG1', 'WJ2', 'SG3', 'GG', 'JS', 'SX', 'GJ', 'JJ', 'FZ', 'TD']  # s01_probe.BOOKS 顺序

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--units', default='data/units')
    ap.add_argument('--out', default='data/unitcards')
    ap.add_argument('--baseline', default='spec/baseline_facts.json')
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(a.units, 'units_index.csv'), encoding='utf-8')))
    if len(rows) != 1742:
        print(f'索引行数 {len(rows)} ≠ 1742'); return 1
    errs, cards = [], []
    for r in rows:
        i = int(r['unit_id'].split('-U')[1])
        p = os.path.join(a.units, r['book_code'], f'unit_{i:04d}.md')
        ls = open(p, encoding='utf-8').read().split('\n')
        meta = {}
        for ln in ls[1:ls.index('---', 1)]:
            k, v = ln.split(':', 1)
            meta[k.strip()] = v.strip()
        # 交叉断言：索引行 vs 单元文件元数据头
        for k in ('unit_id', 'book_code', 'type', 'char_count', 'start_line', 'end_line'):
            if meta.get(k) != r[k]:
                errs.append(f'{r["unit_id"]}: 索引 {k}={r[k]} ≠ 文件头 {k}={meta.get(k)}')
        cards.append(dict(unit_id=r['unit_id'], book_code=r['book_code'], type=r['type'],
                          char_count=int(r['char_count']), start_line=int(r['start_line']),
                          end_line=int(r['end_line']), read_level=None, disposal=None, batch_id=None))
    cnt = {t: sum(1 for c in cards if c['type'] == t) for t in ('C', 'S', 'N')}
    base = json.load(open(a.baseline, encoding='utf-8'))['probe']['totals']
    if (cnt['C'], cnt['S'], cnt['N']) != (base['content'], base['container'], base['noncontent']):
        errs.append(f'类型计数 {cnt} ≠ 基线 {{content:{base["content"]}, container:{base["container"]}, noncontent:{base["noncontent"]}}}')
    if errs:
        print('S09 校验失败：'); [print(' -', e) for e in errs[:10]]; return 1
    os.makedirs(a.out, exist_ok=True)
    for old in glob.glob(os.path.join(a.out, 'uc_*.jsonl')):
        os.remove(old)
    for code in BOOK_ORDER:
        cs = [c for c in cards if c['book_code'] == code]
        if not cs:
            continue
        with open(os.path.join(a.out, f'uc_{code}.jsonl'), 'w', encoding='utf-8') as f:
            for c in cs:
                f.write(json.dumps(c, ensure_ascii=False) + '\n')
    total = len(cards)
    print(f'单元卡 {total} 张（C {cnt["C"]} / S {cnt["S"]} / N {cnt["N"]}，与基线 1,742=1,697+32+13 一致）'
          f'-> {a.out}/uc_<书码>.jsonl 共 {len(BOOK_ORDER)} 个文件')
    return 0

if __name__ == '__main__':
    sys.exit(main())
