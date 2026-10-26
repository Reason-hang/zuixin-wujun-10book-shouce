# P6 锚点全量校验（K 卡锚点表）

> **2026-10-26 更新**：`scripts/s12_export_anchor_ledger.py` 自冻结 K 卡导出 **8950** 行锚点 → `ledger/溯源与处置台账.md`；`make verify-anchors` **8950/8950 PASS**。

## 再生命令

```bash
python3 scripts/s12_export_anchor_ledger.py
make verify-anchors
```

## D3 完整交付仍缺

排除清单、K 降级审计、关系与冲突、说话人、判例库等分表（v2 §16.7）。**已有草稿**：锚点 8950、`单元处置表_草稿`（1742）、`论点卡表_草稿`（`make d3-export`）；单元处置列尚简化为 4 列，待对齐 §16.7 全列。
