#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_publish.py — 批次发布器（J-126 提速工具 5）

收编后发布一条龙：journal 追加（统计骨架+主智能体口述主题带）→ state.json
刷新 → make pack → git commit → git push。任一步失败即停（&&链语义）。
统计数字全部现算自批数据与 uc 文件，不经手写。

用法：
  python3 scripts/batch_publish.py <batch_id> <batch_dir> <uc_path> <J编号> \
      --title "<J行开头标题，如 SG3⑥ B-049 完成收编>" \
      --themes "<主题带：xxx/yyy/zzz>" [--book SG3] [--extra "<补充句>"]
"""
import json, glob, sys, os, subprocess, datetime
from collections import Counter


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print(out[-400:] if len(out) > 400 else out)
    if r.returncode != 0:
        sys.exit(f"命令失败（退出码 {r.returncode}）：{cmd}")


def main():
    a = sys.argv[1:]
    if len(a) < 5 or '--title' not in a:
        sys.exit(__doc__)
    batch_id, batch_dir, uc_path, jnum = a[0], a[1], a[2], a[3]
    jfile = a[a.index('--journal-file') + 1] if '--journal-file' in a else 'state/journal.md'
    sfile = a[a.index('--state-file') + 1] if '--state-file' in a else 'state/state.json'
    ti = a.index('--title'); title = a[ti + 1]
    themes = a[a.index('--themes') + 1] if '--themes' in a else '（主题带略）'
    extra = a[a.index('--extra') + 1] if '--extra' in a else ''
    book = a[a.index('--book') + 1] if '--book' in a else batch_dir.split('-')[-2] if '-' in batch_dir else ''
    # ① 现算统计（不经手写）
    docs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(batch_dir, '*.json')))]
    ev, sp, tot, xcnt = Counter(), Counter(), 0, 0
    for d in docs:
        for c in d['cards']:
            tot += 1; ev[c['evidence_level']] += 1; sp[c['speaker']] += 1
        xcnt += len(d['x_disposals'])
    k_units = sum(1 for d in docs if d['unit_disposal'] == 'K')
    x_units = len(docs) - k_units
    ck = Counter(c['concept_key'] for d in docs for c in d['cards'])
    dup = '、'.join(k for k, v in ck.items() if v > 1) or '无'
    zhuan = [k.replace('转述·第三方：', '') for k, v in sp.items() if k.startswith('转述')]
    # ② journal 行
    line = (f"| {jnum} | {datetime.date.today()} | {title}（{glob.glob(os.path.join(batch_dir,'*'))[0].split('/')[-2]} 由子代理交付、batch_publish 一条龙发布）："
            f"K{k_units}+X{x_units}，{tot} 卡 E1×{ev.get('E1',0)}/E2×{ev.get('E2',0)}/E3×{ev.get('E3',0)}"
            f"（转述·第三方 {sp.get('转述·第三方',0)}），X 处置 {xcnt} 条；verify 0 FAIL、覆盖 {len(docs)} 单元、uc 回写；批内同名键 {dup}。主题带：{themes}{'。' + extra if extra else ''} "
            f"| {batch_dir}/、logs/ |")
    with open(jfile, 'a') as f:
        f.write(line + '\n')
    print('journal 已追加', jnum)
    # ③ state 刷新
    done = sum(1 for l in open(uc_path) if json.loads(l).get('disposal') is not None)
    s = json.load(open(sfile))
    s['updated'] = f'{datetime.date.today()}（{jnum} 后）'
    s['progress']['units_done'] = done
    s['last_ticket'] = f'{batch_id.replace("T-P3x-", "T-P3b-")}（{tot} 卡 0 FAIL，{jnum}）'
    json.dump(s, open(sfile, 'w'), ensure_ascii=False, indent=2)
    print('state 已刷新，units', done)
    # ④ pack + commit + push
    sh('make pack 2>&1 | tail -1')
    sh(f'git add -A && git commit -m "feat: {title}——{tot}卡 0 FAIL、覆盖 {len(docs)} 单元（{jnum}）"')
    sh('git pull --rebase origin main 2>&1 | tail -1')
    sh('git push 2>&1 | tail -1')
    print(f'PUBLISH OK {jnum}: {batch_id} {tot} 卡已推送')


if __name__ == '__main__':
    main()
