#!/usr/bin/env python3
"""s01_split.py — P0 单元切分（S01）
用法（在仓库根目录 wujun-os/ 执行）:
  python3 scripts/s01_split.py --src src_frozen --rules data/split_rules --out data/units
作用: 读 data/split_rules/split_<书码>.yaml（书码、文件名关键词、标题层级），import s01_probe 复用
      split_units()（与 1,742 基线同一切分逻辑），把已配置规则的书切成单元文件：
      <out>/<书码>/unit_0001.md …（含元数据头）+ <out>/units_index.csv 全量索引。
      unit_id 按 spec/v2_方案.md §16.1：<书码>-U<4位序号>，序号=文件内位置序号，从 0001 起。
      char_count = 单元行区间内全部汉字数（含标题行），因此 Σchar_count == 原文汉字总数，
      G3 汉字守恒可精确对账（s01_probe 的 per-unit chars 不含标题行，仅用于 C/S 分类，二者口径不同、用途不同）。
      只读 src_frozen，全部输出写 <out>/；规则参数与 s01_probe.BOOKS 不一致、源文件不唯一等异常返回非零。
"""
import argparse, csv, glob, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_probe

def parse_rule(path):
    """解析极简 YAML（key: value，# 起为注释；值不含 #，不引第三方库）。"""
    r = {}
    for ln in open(path, encoding='utf-8'):
        ln = ln.split('#', 1)[0].strip()
        if not ln or ':' not in ln:
            continue
        k, v = ln.split(':', 1)
        k, v = k.strip(), v.strip()
        r[k] = int(v) if re.fullmatch(r'-?\d+', v) else v
    return r

def find_src(src, key):
    hits = [p for p in sorted(glob.glob(os.path.join(src, '*.md'))) if key in os.path.basename(p)]
    if len(hits) != 1:
        raise SystemExit(f'关键词「{key}」在 {src} 匹配到 {len(hits)} 个文件，必须恰好 1 个')
    return hits[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='src_frozen')
    ap.add_argument('--rules', default='data/split_rules')
    ap.add_argument('--out', default='data/units')
    a = ap.parse_args()
    paths = sorted(glob.glob(os.path.join(a.rules, 'split_*.yaml')))
    if not paths:
        raise SystemExit(f'{a.rules} 里没有 split_*.yaml 规则文件')
    rules = []
    for rp in paths:
        r = parse_rule(rp)
        code, key, lvl = r.get('book_code'), r.get('book_key'), r.get('title_level')
        if not code or not key or lvl is None:
            raise SystemExit(f'{rp} 缺少 book_code / book_key / title_level')
        lvl_by_code = {c: l for _, _, c, l in s01_probe.BOOKS}
        if code not in lvl_by_code:
            raise SystemExit(f'{rp}: 书码 {code} 不在 s01_probe.BOOKS 十书之内')
        if lvl_by_code[code] != lvl:
            raise SystemExit(f'{rp}: title_level={lvl} 与 s01_probe.BOOKS 里 {code} 的层级 {lvl_by_code[code]} 不一致，会破坏 1,742 对账')
        rules.append((code, key, lvl))
    if len({c for c, _, _ in rules}) != len(rules):
        raise SystemExit('规则文件里有重复的 book_code')
    os.makedirs(a.out, exist_ok=True)
    rows = []
    for code, key, lvl in rules:
        path = find_src(a.src, key)
        text = open(path, 'rb').read().decode('utf-8')  # 与 s01_probe.load 完全一致的读取方式
        units = s01_probe.split_units(text, lvl)
        bdir = os.path.join(a.out, code)
        os.makedirs(bdir, exist_ok=True)
        for old in glob.glob(os.path.join(bdir, 'unit_*.md')):  # 清旧产物，保证目录与本次切分一致
            os.remove(old)
        cnt = {'C': 0, 'S': 0, 'N': 0}
        for i, u in enumerate(units, 1):
            uid, n = f'{code}-U{i:04d}', s01_probe.cjk(u['text'])
            cnt[u['cls']] += 1
            body = '\n'.join(['---', f'unit_id: {uid}', f'book_code: {code}', f'type: {u["cls"]}',
                              f'char_count: {n}', f'start_line: {u["start"] + 1}', f'end_line: {u["end"]}',
                              '---', u['text']]) + '\n'
            open(os.path.join(bdir, f'unit_{i:04d}.md'), 'w', encoding='utf-8').write(body)
            rows.append(dict(unit_id=uid, book_code=code, type=u['cls'], char_count=n,
                             start_line=u['start'] + 1, end_line=u['end']))
        print(f'{code}: {os.path.basename(path)} -> {len(units)} 单元（内容 {cnt["C"]}，容器 {cnt["S"]}，非内容 {cnt["N"]}）')
    for d in glob.glob(os.path.join(a.out, '*')):  # 清掉已无规则的书目录，防止 S02 对账到陈旧产物
        if os.path.isdir(d) and os.path.basename(d) not in {c for c, _, _ in rules}:
            shutil.rmtree(d)
            print(f'已清理无规则的书目录: {d}')
    csv_path = os.path.join(a.out, 'units_index.csv')
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['unit_id', 'book_code', 'type', 'char_count', 'start_line', 'end_line'])
        w.writeheader()
        w.writerows(rows)
    print(f'索引 {len(rows)} 行 -> {csv_path}')

if __name__ == '__main__':
    main()
