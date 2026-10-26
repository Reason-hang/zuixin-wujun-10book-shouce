# P4 聚类与归属｜工单看板（单一 Agent，v2 §15.5.5）

> 更新：2026-10-26 启动（JS1-028）

| 步 | 动作 | 状态 | 产出路径 |
|---|------|------|----------|
| 1 | P3 冻结快照 | ✅ | `logs/p4_step01_p3_freeze_20261026.md` |
| 2 | 概念键归一（registry + 书内跨批合并队列） | 🔄 | `concept_key_aliases.yaml`（5 簇）；`p4_l3_registry.yaml` |
| 3 | 近似卡对/键对候选 | ✅ 粗筛 | `logs/p4_step03_near_dup_pairs_20261026.md` |
| 4 | 7 类关系 + 冲突台账 F 编号 | 🔄 | `ledger/p4_conflicts_ledger.md`（F-001~054） |
| 5 | 支柱归属 + 判例 | 🔄 | `logs/p4_step05_d06_attribution_snapshot_20261026.md` |
| 6–8 | L3/L2、三道门 | 🔄 | 步6–7 见上；步8 `logs/p4_step08_d10_three_gates_20261026.md`（D10 保留） |
| 9 | 数量核对 | 🔄 | `logs/p4_step09_l2_l3_quantity_20261026.md`（L3 候选 61 超红线→合并门） |
| 10 | 盲重标 κ≥0.6 | ✅ | 累计 **120** 张 κ=**0.683** PASS（`s16_kappa.py` 可复算） |
| 11 | 用户抽查 20 张 | ⏳ | 正式 CSV 空；**提议稿** `p4_step11_proposed_user_verdicts.csv`（19 ok / 1 unsure） |
| 12 | K 卡冻结 | ⏳ | `logs/p4_step12_k_card_freeze_gate_20261026.md`（步11 阻塞） |
| 13 | 字典变更报告 + 用户确认骨架 | 🔄 | `logs/p4_step13_dictionary_change_report_20261026.md` |

**P4 裁决默认**：用户 5 项待终裁（移民 X8、E1/E2、GG-U0013、U0175、婚恋 X5）沿用 V5「不阻塞、记模糊点」直至用户改口。
