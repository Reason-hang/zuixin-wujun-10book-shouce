# P4 Step12 K 卡冻结｜过关门禁（未执行冻结）

> 冻结 = 锁定论点卡分母与 JSON 内容，P5/P6 仅只读引用（v2 §15.5.5 步 10）。

## 前置条件核对

| 条件 | 状态 | 证据 |
|------|------|------|
| GATE-D 9019 卡 verify 0 FAIL | ✅ | `logs/gate_d_summary_20261026.md` |
| 孤儿卡 0 | 待脚本复跑 | `verify_cards.py` / GATE-D 口径 |
| 概念键多处定义 0 | 🔄 | 别名表 + 合并门；未全库语义审计 |
| 冲突处置率 100% | 🔄 | F-001~054 已登记；Step3 余对待补 |
| κ ≥ 0.6 | ✅ | 累计 120 张 κ=0.683 |
| 步 11 用户抽查 20 无重大异议 | ⏳ | `p4_step11_user_spotcheck_20.csv` 未填 |
| L2/L3 数量不超红线或已批准 | 🔄 | 合并后 L3=**43**（在 32–44 目标内）待用户步 13 确认 |

## 冻结动作（待步 11+13 后执行）

1. 生成 `state/p4_k_card_freeze_manifest.sha256`（`data/cards/**` 全量哈希）。
2. 在 `state/state_sg1.json` 或专用 `state/p4_freeze.json` 写入：`frozen_at`、`card_count`、`manifest_path`。
3. CI/本地：`make verify-cards` 对比 manifest，变更需走 CHG 流程。

**当前判定**：**不得执行步 12 物理冻结**（步 11 阻塞）。P5 草稿已标「只读引用」，不改卡 JSON。
