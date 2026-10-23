#!/usr/bin/env python3
"""test_split.py — S01/S02 自测（独立运行，不影响 make test 的 7 项计数）
用法（在仓库根目录 wujun-os/ 执行）:  python3 tests/test_split.py
场景: ① 8 行 3 单元微型假书（复用真实书码 TD 的规则形态）经 S01 切分，S02 对账应通过
         （行覆盖缺口 0、重叠 0，汉字守恒差 0）；
      ② 故意删掉某单元正文一行，S02 必须检出（退出码非零，报告出现 FAIL）。
"""
import os, subprocess, sys, tempfile

PY = sys.executable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S1 = os.path.join(ROOT, 'scripts', 's01_split.py')
S2 = os.path.join(ROOT, 'scripts', 's02_consistency.py')
FAKE = ('## 甲单元\n第一行：知止而后有定。\n第二行：定而后能静。\n'
        '## 乙单元\n第三行：静而后能安。\n'
        '## 丙单元\n第四行：安而后能虑。\n第五行：虑而后能得。\n')

def run(args, cwd):
    r = subprocess.run([PY] + args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        src, rules, units = (os.path.join(tmp, x) for x in ('src', 'rules', 'units'))
        os.makedirs(src); os.makedirs(rules)
        open(os.path.join(src, '《态度》测试微型假书.md'), 'w', encoding='utf-8').write(FAKE)
        open(os.path.join(rules, 'split_TD.yaml'), 'w', encoding='utf-8').write(
            'book_code: TD\nbook_key: 态度\ntitle_level: 2\n')
        rep = os.path.join(tmp, 'g2g3.md')
        rc, out = run([S1, '--src', src, '--rules', rules, '--out', units], cwd=ROOT)
        files = sorted(os.listdir(os.path.join(units, 'TD'))) if os.path.isdir(os.path.join(units, 'TD')) else []
        results.append(('S01：微型假书切分成功（3 个单元文件）', rc == 0 and
                        files == ['unit_0001.md', 'unit_0002.md', 'unit_0003.md'],
                        out.splitlines()[-1] if out else ''))
        idx = open(os.path.join(units, 'units_index.csv'), encoding='utf-8').read() if os.path.exists(os.path.join(units, 'units_index.csv')) else ''
        results.append(('S01：units_index.csv 含表头与 3 行索引', idx.startswith('unit_id,book_code,type,char_count,start_line,end_line') and idx.count('\n') == 4,
                        f'行数 {idx.count(chr(10))}'))
        rc, out = run([S2, '--src', src, '--units', units, '--report', rep], cwd=ROOT)
        t = open(rep, encoding='utf-8').read() if os.path.exists(rep) else ''
        results.append(('S02：覆盖无缺口/重叠、汉字守恒差 0，应通过', rc == 0 and 'PASS' in t and '缺口 0，重叠 0' in t and '/ 0 | PASS |' in t,
                        out.splitlines()[0] if out else ''))
        p2 = os.path.join(units, 'TD', 'unit_0002.md')  # 篡改：删掉乙单元正文一行
        ls = open(p2, encoding='utf-8').read().split('\n')
        k = next(i for i, l in enumerate(ls) if l.startswith('第三行'))
        del ls[k]
        open(p2, 'w', encoding='utf-8').write('\n'.join(ls))
        rc, out = run([S2, '--src', src, '--units', units, '--report', rep], cwd=ROOT)
        t = open(rep, encoding='utf-8').read()
        results.append(('S02：单元被删一行必须检出（退出码非零）', rc != 0 and 'FAIL' in t,
                        out.splitlines()[1] if rc != 0 and len(out.splitlines()) > 1 else out.splitlines()[0] if out else ''))
    print('| 测试 | 结果 | 说明 |\n|---|---|---|')
    for n, ok, note in results:
        print(f"| {n} | {'PASS' if ok else 'FAIL'} | {note} |")
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)

if __name__ == '__main__':
    main()
