# P4 Step13 字典变更报告（待用户确认骨架）

`user_confirmed_skeleton`: **no**（2026-10-26）

## 变更摘要

| 类型 | 文件 | 变更 |
|------|------|------|
| 概念键别名 | `data/rules/concept_key_aliases.yaml` | +成功是成功之母；+CK-2014 簇（6 个别名示例，余 CK 见 registry） |
| L3 注册表 | `data/rules/p4_l3_registry.yaml` | **43** 个 L3 节点（自 61 增长门键合并） |
| 冲突台账 | `ledger/p4_conflicts_ledger.md` | F-045~F-054 |
| 支柱 | D10 | **保留**第 10 章（步 8 三道门） |
| K 卡 JSON | `data/cards/**` | **无批量改写**（P4 裁决：别名+台账优先） |

## L2/L3 骨架确认请求

- **L2**：维持 v0 **25** 个二级（§13 执行基线），未增删。
- **L3**：成稿目标 **43** 个核心模型节点（合并门后），落在 v2 目标区间 **32–44**。
- **重点三柱深加工**：D06 章已交付 2+1 张核心卡草稿；D01/D02 排队。

## 用户确认项（请回复「确认骨架」或逐条修改）

1. 别名：`成功是成功之母` → `成功才是成功之母`；`CK-20xx` → `CK-2014` 手册合并。
2. D10 保留为一级支柱。
3. 步 11 抽查：填 CSV 或授权 `deferred`（记入 D4 风险）。
4. 确认后允许执行步 12 manifest 冻结。

## 复算命令

```bash
python3 scripts/s16_kappa.py \
  --ground-truth logs/p4_step10_blind_cumulative_ground_truth.csv \
  --relabel logs/p4_step10_blind_cumulative_relabel.csv
wc -l data/rules/p4_l3_registry.yaml  # 节点见 l3_nodes 块
```
