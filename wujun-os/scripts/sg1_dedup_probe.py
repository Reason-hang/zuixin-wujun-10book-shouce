#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sg1_dedup_probe.py — SG1↔GG 重复段映射探测器（J-128 提速工具 6）

《硅谷来信》第1季（SG1）与《谷歌方法论》（GG）存在约 107 段原文重复（V4 记录）。
本工具对两书做段落级签名匹配，产出 data/rules/sg1_gg_dupes.json：
  [{sg1_unit_hint, sg1_lines, gg_lines, chars}]  按 SG1 行序排列
用途：①SG1 派单时把映射附给代理（重复段只登记出处勿重复抽卡，双出处登记）；
②SG1 验收时核对重复段处置。纯只读分析，不改任何数据。

用法：python3 scripts/sg1_dedup_probe.py [--out data/rules/sg1_gg_dupes.json]
"""
import json, sys, re, argparse

def paras(path):
    """按标题/空行切段，返回 [(start_line, end_line, text)]，1-based 行号含头尾"""
    lines = open(path, encoding='utf-8').read().split('\n')
    out, buf, start = [], [], 1
    for i, l in enumerate(lines, 1):
        if l.startswith('#') or l.startswith('<a id') or l.startswith('<!-- source'):
            if buf:
                out.append((start, i - 1, ''.join(buf)))
                buf = []
            start = i + 1
        elif l.strip():
            buf.append(l.strip())
            if sum(len(x) for x in buf) > 1200:
                out.append((start, i, ''.join(buf)))
                buf, start = [], i + 1
        else:
            if buf and sum(len(x) for x in buf) > 150:
                out.append((start, i - 1, ''.join(buf)))
            if buf:
                buf, start = [], i + 1
    if buf:
        out.append((start, len(lines), ''.join(buf)))
    return out

def sig(t):
    """归一化签名：去空白标点后的前 40 字"""
    t = re.sub(r'[\s，。；：、！？""''（）《》\*\[\]\d##>|-]', '', t)
    return t[:40]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='data/rules/sg1_gg_dupes.json')
    a = ap.parse_args()
    sg1 = paras('src_frozen/《硅谷来信1》｜原著完整精排典藏版｜Codex处理_副本.md')
    gg = paras('src_frozen/《谷歌方法论》[吴军]-原著完整精排版_副本.md')
    gg_idx = {}
    for s, e, t in gg:
        gg_idx.setdefault(sig(t), []).append((s, e, len(t)))
    hits, seen_gg = [], set()
    for s, e, t in sg1:
        if len(t) < 150:
            continue
        k = sig(t)
        if k in gg_idx:
            for gs, ge, glen in gg_idx[k]:
                if abs(glen - len(t)) / max(glen, len(t)) < 0.10:
                    hits.append({'sg1_lines': [s, e], 'gg_lines': [gs, ge], 'chars': len(t)})
                    seen_gg.add((gs, ge))
                    break
    json.dump(hits, open(a.out, 'w'), ensure_ascii=False, indent=1)
    print(f"SG1 段 {len(sg1)}、GG 段 {len(gg)}；命中重复段 {len(hits)}（GG 去重 {len(seen_gg)} 段）-> {a.out}")

if __name__ == '__main__':
    main()
