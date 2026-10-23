#!/usr/bin/env python3
"""selftest.py — 脚本自测（make test）
用法（在仓库根目录 wujun-os/ 执行）:  python3 scripts/selftest.py
覆盖: ① 锚点脚本（原文通过、篡改一字被检出、前插一行被检出）② s01 基线比对通过 ③ s01 在被破坏的原文上必须失败
      ④ status 能渲染 ⑤ 若有 MANIFEST 则包校验通过。需要 src_frozen/ 里已有 10 本原文（make freeze）。
"""
import glob, os, re, shutil, subprocess, sys, tempfile

PY = sys.executable
ROOT = os.getcwd()
results = []

def run(args, cwd=ROOT):
    r = subprocess.run([PY] + args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

def rec(name, ok, note=''):
    results.append((name, ok, note))

def pick_probe(path):
    t = open(path, encoding='utf-8').read()
    for b in t.split('\n\n'):
        if len(b) >= 200 and not b.lstrip().startswith(('-', '[', '#', '!', '<', '>')) and '](#' not in b:
            for ln in [l.strip() for l in b.split('\n') if len(l.strip()) >= 14]:
                pr = ln[2:12]
                if t.count(pr) == 1:
                    return pr
    return None

def anchor_tests():
    books = glob.glob(os.path.join(ROOT, 'src_frozen', '*数学通识*.md')) + glob.glob(os.path.join(ROOT, 'src_frozen', '*来信3*.md'))
    if len(books) != 2:
        rec('锚点：需要 src_frozen 里的数学通识与来信3', False, f'找到 {len(books)} 本'); return
    tool = os.path.join(ROOT, 'scripts', 'anchor_tool.py')
    with tempfile.TemporaryDirectory() as tmp:
        rows = []
        for i, b in enumerate(books):
            dst = os.path.join(tmp, os.path.basename(b)); shutil.copyfile(b, dst)  # copyfile 不带权限位：源是 444 只读，副本须可写
            pr = pick_probe(dst)
            rc, out = run([tool, 'make', '--book', dst, '--probe', pr, '--id', f'T-{i}'])
            rows.append(out)
        ledger = os.path.join(tmp, 'ledger.md')
        open(ledger, 'w', encoding='utf-8').write('| 卡ID | 书文件名 | 行起 | 行止 | 字符起 | 字符止 | SHA1 | 指纹词 |\n|---|---|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n')
        rc, out = run([tool, 'verify', '--ledger', ledger, '--books-dir', tmp])
        rec('锚点：原文校验应通过', rc == 0, out.splitlines()[-1] if out else '')
        target = os.path.join(tmp, os.path.basename(books[0])); t = open(target, encoding='utf-8').read()
        cs = int(rows[0].strip('|').split('|')[4])
        open(target, 'w', encoding='utf-8').write(t[:cs + 3] + ('X' if t[cs + 3] != 'X' else 'Y') + t[cs + 4:])
        rc, out = run([tool, 'verify', '--ledger', ledger, '--books-dir', tmp])
        rec('锚点：篡改一字应被检出', rc == 1 and 'SHA1不符' in out)
        open(target, 'w', encoding='utf-8').write('多出的一行\n' + t)
        rc, out = run([tool, 'verify', '--ledger', ledger, '--books-dir', tmp])
        rec('锚点：前插一行应被检出', rc == 1 and '行号不符' in out)

def probe_tests():
    rc, out = run(['scripts/s01_probe.py', '--src', 'src_frozen', '--out', os.path.join(tempfile.gettempdir(), 'p0_probe_selftest.md')])
    rec('s01：与基线比对应通过', rc == 0, out.splitlines()[0] if out else '')
    with tempfile.TemporaryDirectory() as tmp:
        for p in glob.glob('src_frozen/*.md'):
            shutil.copyfile(p, os.path.join(tmp, os.path.basename(p)))  # 同上：不复制 444 权限位
        f = glob.glob(os.path.join(tmp, '*富足*.md'))[0]
        t = open(f, encoding='utf-8').read()
        i = t.index('\n### ')
        j = t.index('\n', i + 1)
        open(f, 'w', encoding='utf-8').write(t[:i] + t[j:])  # 整行删掉一个标题，两个单元会被合并
        rc, out = run(['scripts/s01_probe.py', '--src', tmp, '--out', os.path.join(tmp, 'x.md')])
        rec('s01：原文被破坏时应失败', rc == 1, out.splitlines()[0] if out else '')

def other_tests():
    rc, out = run(['scripts/status.py'])
    rec('status：能渲染 STATE.md', rc == 0, out.splitlines()[0] if out else '')
    if os.path.exists('MANIFEST.sha256'):
        rc, out = run(['scripts/verify_pack.py'])
        rec('verify_pack：包校验应通过', rc == 0, out.splitlines()[0] if out else '')

if __name__ == '__main__':
    if not glob.glob('src_frozen/*.md'):
        print('src_frozen/ 里没有原文：先 make freeze'); sys.exit(2)
    anchor_tests(); probe_tests(); other_tests()
    print('| 测试 | 结果 | 说明 |\n|---|---|---|')
    for n, ok, note in results:
        print(f"| {n} | {'PASS' if ok else 'FAIL'} | {note} |")
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)
