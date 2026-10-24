#!/usr/bin/env python3
"""make_handover.py — 交接刷新文档生成（T-00-05 收口）
用法（在仓库根目录 wujun-os/ 执行）:  python3 scripts/make_handover.py
作用: 只读 state/state.json、state/journal.md（末 10 条）、state/board.md（done/doing/backlog 统计）、
      ledger/（台账文件清单），生成 logs/handover_refresh.md——不动 handover/ 冻结区。
      内容：当前阶段快照、下一工单、阻塞项、journal 末 10 条、board 统计、
      新鲜度校验和（SHA-256( state.json 字节 + journal.md 字节 ) 前 16 位）、日期。
      state.json 或 journal.md 缺失返回非零；其余缺失降级注明。
"""
import datetime, glob, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fresh_checksum(sp, jp):
    """SHA-256( state.json 字节 + journal.md 字节 ) 前 16 位——两文件任一更新，校验和即变。"""
    h = hashlib.sha256()
    h.update(open(sp, 'rb').read())
    h.update(open(jp, 'rb').read())
    return h.hexdigest()[:16]

def journal_tail(jp, n=10):
    """journal.md 是只增表格，取末 n 条数据行（| J-xxx | …）。"""
    rows = [l.rstrip('\n') for l in open(jp, encoding='utf-8') if l.startswith('| J-')]
    return rows[-n:]

def board_stats(bp):
    """board.md 工单表：按状态列前缀统计 done/doing/review/backlog/blocked/ready。"""
    cnt, doing_ids = {}, []
    for l in open(bp, encoding='utf-8'):
        if not l.startswith('| T-'):
            continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 4:
            continue
        st = c[3].split('（')[0].strip()
        cnt[st] = cnt.get(st, 0) + 1
        if st in ('doing', 'blocked'):
            doing_ids.append(f'{c[0]}（{st}）')
    return cnt, doing_ids

def main():
    sp = os.path.join(ROOT, 'state', 'state.json')
    jp = os.path.join(ROOT, 'state', 'journal.md')
    bp = os.path.join(ROOT, 'state', 'board.md')
    ld = os.path.join(ROOT, 'ledger')
    for p in (sp, jp):
        if not os.path.exists(p):
            print(f'缺少必需文件: {p}'); return 1
    st = json.load(open(sp, encoding='utf-8'))
    today = datetime.date.today().isoformat()
    ck = fresh_checksum(sp, jp)
    jt = journal_tail(jp)
    bs, active = ({}, []) if not os.path.exists(bp) else board_stats(bp)
    ledgers = sorted(glob.glob(os.path.join(ld, '*.md')), key=os.path.getmtime)
    prog = st.get('progress', {})
    prog_line = f'- 进度：单元 {prog.get("units_done", "?")}/{prog.get("units_total", "?")}，汉字 {prog.get("chars_done", "?")}/{prog.get("chars_total", "?")}'
    lines = [
        '# 交接刷新（handover refresh）', '',
        f'- 生成日期：{today}；生成器：scripts/make_handover.py（make handover）',
        f'- 新鲜度校验和：`{ck}`（SHA-256( state.json 字节 + journal.md 字节 ) 前 16 位；两文件任一更新即失效，需重跑 make handover）',
        f'- 定位：handover/ 为冻结区不动，本文件是可随时重生成的快照，放 logs/', '',
        '## 1. 当前阶段快照（state.json）', '',
        f'- 阶段：{st.get("phase", "未知")}',
        f'- 步骤：{st.get("step", "未知")}',
        prog_line,
        f'- 冻结：{st.get("frozen", {}).get("status", "未知")}',
        f'- 最近工单：{st.get("last_ticket", "未知")}', '',
        '## 2. 下一工单', '',
        f'- {st.get("next_ticket", "未知")}', '',
        '## 3. 阻塞项', '',
    ]
    blocked = st.get('blocked_by') or []
    lines += [f'- blocked_by：{"、".join(blocked)}' if blocked else '- blocked_by：无']
    lines += [f'- 在办/受阻工单（board）：{"、".join(active)}' if active else '- 在办/受阻工单（board）：无']
    for it in st.get('open_items', []):
        lines.append(f'- open_item：{it}')
    for r in st.get('risks_top', [])[:5]:
        lines.append(f'- 风险：{r}')
    lines += ['', '## 4. journal 末 10 条', '',
              '| 条目 | 日期 | 内容 | 产出 |', '|---|---|---|---|'] + jt
    lines += ['', '## 5. board 统计', '',
              f'- 状态计数：{"；".join(f"{k} {v}" for k, v in sorted(bs.items()))}',
              f'- 台账文件（ledger/）：' + ('、'.join(os.path.basename(p) for p in ledgers) if ledgers else '无'),
              f'- 最新台账：{os.path.basename(ledgers[-1])}' if ledgers else '- 最新台账：无', '',
              '> 复水提示：先 `make restore-check`（包校验+冻结+探测+自测），再读本文件与 handover/项目交接文档.md，对不上时以校验和口径排查 state 是否过期。', '']
    out = os.path.join(ROOT, 'logs', 'handover_refresh.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'交接刷新已生成: {out}（journal 末 {len(jt)} 条，board {sum(bs.values())} 张工单，校验和 {ck}）')
    return 0

if __name__ == '__main__':
    sys.exit(main())
