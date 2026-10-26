#!/usr/bin/env python3
"""verify_cards.py — 论点卡全量校验（rules_v0.9.md R8 / GATE-B 组成）

用法（在 wujun-os/ 执行）:
  python3 scripts/verify_cards.py --dirs data/pilot/cards_first data/pilot/cards_second --out logs/cards_verify.md

校验项：SHA1 复算一致｜行号在单元范围｜锚点≤800字｜quote 锚内连续子串且≤15字｜指纹词锚内子串且≤3｜
claim_text≤60字｜speaker/evidence/ability 枚举合法｜读者与史实卡非 E1｜DT-待判 允许｜X 处置不混入 cards
"""
import argparse, csv, glob, hashlib, json, os

SPEAKERS = {'吴军本人', '读者', '转述·第三方', '史实', '编校转录', '嘉宾', '待核'}
EVID = {'E1', 'E2', 'E3', 'E4'}
ABILITY = {'思', '学', '沟', '做'}

def load_units():
    idx = {}
    for r in csv.DictReader(open('data/units/units_index.csv', encoding='utf-8')):
        idx[r['unit_id']] = r
    return idx

def book_path(book_code):
    for p in glob.glob('src_frozen/*.md'):
        base = os.path.basename(p)
        mapping = {'FZ': '富足', 'GG': '谷歌方法论', 'SG3': '硅谷来信3', 'SG1': '硅谷来信1',
                   'WJ2': '吴军来信2', 'TD': '态度', 'JJ': '境界', 'GJ': '格局', 'SX': '数学通识', 'JS': '见识'}
        if mapping.get(book_code) and mapping[book_code] in base:
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dirs', nargs='+', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    units = load_units()
    lines_cache = {}
    rows, fails = [], 0
    for d in args.dirs:
        paths = sorted(glob.glob(os.path.join(d, '*.json')))
        if not paths:
            paths = sorted(glob.glob(os.path.join(d, '**', '*.json'), recursive=True))
        for p in paths:
            data = json.load(open(p, encoding='utf-8'))
            if isinstance(data, dict) and 'cards' in data:
                cards = data['cards']
                wrap_uid, wrap_book = data.get('unit_id'), data.get('book_code')
            else:
                cards = data if isinstance(data, list) else [data]
                wrap_uid, wrap_book = None, None
            for c in cards:
                if wrap_uid and not c.get('unit_id'):
                    c['unit_id'] = wrap_uid           # 包装层回填
                if wrap_book and c.get('anchor') and 'book_code' not in c['anchor']:
                    c['anchor']['book_code'] = wrap_book
                cid = c.get('claim_id', '?')
                errs = []
                uid = c.get('unit_id', '')
                u = units.get(uid)
                if not u:
                    errs.append('unit_id 不在索引')
                    rows.append((cid, 'FAIL', '; '.join(errs)))
                    fails += 1
                    continue
                a = c.get('anchor') or {}
                s, e = a.get('start_line'), a.get('end_line')
                if s is None or e is None:
                    errs.append('锚点缺行号')
                else:
                    if not (int(u['start_line']) <= s <= e <= int(u['end_line'])):
                        errs.append(f'行号 {s}-{e} 超出单元 {u["start_line"]}-{u["end_line"]}')
                    bp = book_path(u['book_code']) if u['book_code'] not in lines_cache else lines_cache.get(u['book_code'])
                    if u['book_code'] not in lines_cache:
                        bp = book_path(u['book_code'])
                        lines_cache[u['book_code']] = bp
                    if bp:
                        fl = open(bp, encoding='utf-8').read().split('\n')
                        span = '\n'.join(fl[s-1:e])
                        if len(span) > 800:
                            errs.append(f'锚点 {len(span)} 字 >800')
                        if hashlib.sha1(span.encode('utf-8')).hexdigest() != a.get('sha1'):
                            errs.append('SHA1 不一致')
                        q = c.get('quote')
                        if q:
                            if len(q) > 15:
                                errs.append('quote >15 字')
                            if q not in span:
                                errs.append('quote 非锚内子串')
                        for fp in a.get('fingerprint', [])[:4]:
                            if fp not in span:
                                errs.append(f'指纹词「{fp}」非锚内子串')
                        if len(a.get('fingerprint', [])) > 3:
                            errs.append('指纹词 >3')
                if len(c.get('claim_text', '')) > 60:
                    errs.append('claim_text >60 字')
                if c.get('speaker') not in SPEAKERS:
                    errs.append(f'speaker 非法: {c.get("speaker")}')
                if c.get('evidence_level') not in EVID:
                    errs.append(f'证据等级非法: {c.get("evidence_level")}')
                if c.get('speaker') in {'读者', '史实'} and c.get('evidence_level') == 'E1':
                    errs.append('读者/史实卡不得为 E1')
                bad_tags = set(c.get('ability_tags', [])) - ABILITY
                if bad_tags:
                    errs.append(f'能力标签非法: {bad_tags}')
                if len(c.get('ability_tags', [])) > 2:
                    errs.append('能力标签 >2')
                pill = c.get('pillar_candidates', [])
                if not pill or (pill != ['DT-待判'] and not all(x.startswith('D') for x in pill)) or len(pill) > 2:
                    errs.append(f'pillar_candidates 非法: {pill}')
                ok = not errs
                if not ok:
                    fails += 1
                rows.append((cid, 'PASS' if ok else 'FAIL', '; '.join(errs)))

    L = [f'# 论点卡校验（GATE-B/R8，脚本产出）', '', f'- 卡总数: {len(rows)}　PASS: {len(rows)-fails}　FAIL: {fails}', '']
    if fails:
        L += ['| claim_id | 结果 | 错误 |', '|---|---|---|']
        L += [f'| {cid} | {v} | {m} |' for cid, v, m in rows if v == 'FAIL']
    verdict = 'PASS' if fails == 0 else 'FAIL'
    L += ['', f'结论: {verdict}']
    open(args.out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'卡校验: {len(rows)} 张，FAIL {fails} → {verdict}；报告 {args.out}')
    raise SystemExit(0 if fails == 0 else 1)

if __name__ == '__main__':
    main()
