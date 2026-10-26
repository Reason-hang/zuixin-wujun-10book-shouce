# P4 聚类与归属｜工单看板（单一 Agent，v2 §15.5.5）

> 更新：2026-10-26 启动（JS1-028）

| 步 | 动作 | 状态 | 产出路径 |
|---|------|------|----------|
| 1 | P3 冻结快照 | ✅ | `logs/p4_step01_p3_freeze_20261026.md` |
| 2 | 概念键归一（registry + 书内跨批合并队列） | 🔄 | `concept_keys.csv`；`data/rules/concept_key_aliases.yaml`（首批 3 簇） |
| 3 | 近似卡对/键对候选 | ✅ 粗筛 | `logs/p4_step03_near_dup_pairs_20261026.md` |
| 4 | 7 类关系 + 冲突台账 F 编号 | 🔄 | `ledger/p4_conflicts_ledger.md`（F-001~004） |
| 5 | 支柱归属 + 判例 | 🔄 | `logs/p4_step05_d06_attribution_snapshot_20261026.md` |
| 6–8 | L3/L2、三道门 | ⏳ | |
| 9 | 数量核对 | ⏳ | |
| 10 | 盲重标 κ≥0.6 | 🔄 | 批次1 n=60 κ=**0.771** PASS（pilot）；余 390 张待重标 |
| 11 | 用户抽查 20 张 | ⏳ | `logs/p4_step11_user_spotcheck_20.csv`（待填 user_verdict） |
| 12 | K 卡冻结 | ⏳ | |
| 13 | 字典变更报告 + 用户确认骨架 | ⏳ | 需用户 |

**P4 裁决默认**：用户 5 项待终裁（移民 X8、E1/E2、GG-U0013、U0175、婚恋 X5）沿用 V5「不阻塞、记模糊点」直至用户改口。
