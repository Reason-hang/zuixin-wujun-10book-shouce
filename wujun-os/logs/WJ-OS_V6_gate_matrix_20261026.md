# WJ-OS V6 闸门对照矩阵（完成审计用）

> 生成：2026-10-26｜**整体 V6：未完成**｜勿 `UpdateGoal` complete。

## 目标链（用户 V6）

| 阶段 | 要求 | 状态 | 证据 |
|------|------|------|------|
| SG1 B-017~020 | 收编 + 验收 | ✅ | `journal_sg1` JS1-021~027；`data/cards/T-P3b-B-017`…B-020 |
| SG1 单书验收 | book_coverage PASS | ✅ | JS1-026；`logs/book_coverage_SG1_20261026.md` |
| GATE-D | 全库 9019 0 FAIL | ✅ | `logs/gate_d_summary_20261026.md` |
| P4 冻结 | K 卡 manifest | ✅ | `state/p4_freeze.json`；1705 文件 |
| P5 | AC-5.1~5.8 + M3 v0.9 | 🔄 | 脚本 AC ✅；**步 11 待 `M3-确认`** |
| P6 | §15.5.7 步 1–12 | 🔄 | 子集绿；人工签收见下表 |
| P7 | §15.5.8 / AC-7.x | 🔄 | 草稿清单；**待 P6** |

## P5（Gate-P5 等价）

| 项 | 过关证据 | 现况 |
|----|----------|------|
| AC-5.1~5.8 | `make p6-subset` 内 S17 项 | ✅ |
| M3 试用 | `m3_trial_feedback_20261026.md` v0.9.1 | 🔄 三题**部分**；无 `M3-确认` |
| 合并稿 | `D1_主手册合并稿_v1.md` | ✅ |

## P6 逐步（T-P6-01…12）

| 步 | 脚本/产物可绿？ | 人工签收？ | 证据 |
|----|----------------|------------|------|
| 1 G0–G9 | 🔄 子集 | P0+G9 子集 ✅；非全套 S15 历史 G9 手册链 | `s15_check_all`；`g9_subset_check` |
| 2 覆盖矩阵 | 粗矩阵 ✅ | 语义 100% 未签 | `P6_核心论点覆盖矩阵_草稿.md` |
| 3 AC-3.6 召回 | 锚点 ping 135/135 ✅ | **正式「回读召回」列空** | `AC36_抽检召回表_草稿.md` |
| 4–5 G10 | ①③ strict ✅ | ② 漏收列空；无承接 ~66% 已文档化 | `g10_kw.md`；`G10②_盲抽单元表_草稿.md` |
| 6 数理映射 | 45 卡审计 ✅ | 全库率非本脚本 | `s17_math_mapping_audit_latest.md` |
| 7 五场景 | 索引+Agent 草稿 | **走通未签** | `p6_scene_drill_log_20261026.md` |
| 8 24 字重复 | ✅ | — | `s17_manual_dup_slide` |
| 9 锚点 | 8950 ✅ | 用户自助说明可选 | `verify-anchors` |
| 10 对抗审查 | 预检 fail=0 | #1/#3 深读未签 | `p6_adversarial_preflight_latest.md` |
| 11 20 张 | 锚点草稿 20/20 | **「你的判断」列空** | `P6_用户抽查20张_草稿.md` |
| 12 回修 | — | 未触发 | — |

## P7（Gate-P7）

| AC | 现况 |
|----|------|
| 7.1 六份齐 | `P7_交付清单_草稿.md`（草稿名） |
| 7.2 渲染 | `make render-check` / `make p7-preflight` |
| 7.3 可复算 | `D4_覆盖与质检报告_草稿.md`；`make d4-snapshot` |
| 7.4 事实源 | `make fact-source`；`out/事实源与冻结哈希_草稿.md` |
| 7.5 版本 | D6 决策日志增量 ✅ |

## 一键复验

```bash
cd wujun-os && make v6-engineering && make d4-snapshot && make v6-audit
```

## 用户最小动作（ unblock P5→P6 签字）

见 `logs/p6_user_signoff_checklist_20261026.md`。  
授权文件 → `make user-signoff-apply`（`logs/user_signoff_authorization_TEMPLATE.txt`）。  
聊天原文亦可：`python3 scripts/s13_user_signoff_apply.py --accept-text '…'`（**勿**与 `--dry-run` 同用写盘）。
