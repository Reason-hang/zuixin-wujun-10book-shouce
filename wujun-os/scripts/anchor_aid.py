#!/usr/bin/env python3
"""anchor_aid.py — 抽取提速辅助（J-111）：写盘前一次性预计算锚 span SHA1 并预检断言

用法（在 wujun-os/ 执行）:
  # 1) 列出某单元行窗内候选锚 span 的 SHA1（供卡片 anchor 直接抄用）
  python3 scripts/anchor_aid.py sha <原书路径> <start> <end>
  # 2) 预检一批卡（stdin 传 JSON 数组：[{start,end,quote,fingerprint[]}），全部通过退出码 0
  echo '[{"start":186,"end":190,"quote":"做减法","fingerprint":["断舍离"]}]' | python3 scripts/anchor_aid.py check <原书路径>

规则口径与 R7/R8/verify_cards 完全一致：锚=原文行文本（含页码行）；
quote≤15字且锚内连续子串；指纹词≤3且锚内子串。本脚本只前移校验、
不替代官方 verify_cards（GATE-B 闸门照跑）。HC-21：数字由脚本产生。
"""
import sys, json, hashlib

def load_lines(book):
    return open(book, encoding='utf-8').read().split('\n')

def span_text(L, s, e):
    return '\n'.join(L[s-1:e])

def sha_of(L, s, e):
    return hashlib.sha1(span_text(L, s, e).encode()).hexdigest()

def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('sha', 'check'):
        print(__doc__); sys.exit(2)
    if sys.argv[1] == 'sha' and len(sys.argv) < 5:
        print(__doc__); sys.exit(2)
    cmd, book = sys.argv[1], sys.argv[2]
    L = load_lines(book)
    if cmd == 'sha':
        s, e = int(sys.argv[3]), int(sys.argv[4])
        t = span_text(L, s, e)
        print(json.dumps({"start": s, "end": e, "len": len(t), "sha1": sha_of(L, s, e)},
                         ensure_ascii=False))
        return
    if cmd == 'check':
        cards = json.load(sys.stdin)
        errs = []
        for i, c in enumerate(cards):
            s, e, q = c['start'], c['end'], c.get('quote', '')
            fp = c.get('fingerprint', [])
            t = span_text(L, s, e)
            if len(t) > 800: errs.append((i, '锚超800', len(t)))
            if not (0 < len(q) <= 15 and q in t): errs.append((i, 'quote非法', q))
            if len(fp) > 3 or not all(f in t for f in fp): errs.append((i, '指纹词非法', fp))
        if errs:
            for e_ in errs: print('FAIL', e_, file=sys.stderr)
            sys.exit(1)
        print(f'预检通过 {len(cards)} 卡（SHA1 请用 sha 子命令逐卡取）')
        return
    print(__doc__); sys.exit(2)

if __name__ == '__main__':
    main()
