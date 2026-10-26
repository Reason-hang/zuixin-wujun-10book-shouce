# P6 步 2｜核心论点覆盖矩阵（runbook，未执行）

> 前置：P4 冻结 ✅；P5 未 PASS（M3、112 议题）。

## 目标

逐书双向矩阵：原著单元/划重点 ↔ K 卡 ↔ 手册模型（v2 §15.5.7 步 2）。

## 建议命令（本机有 `src_frozen` 时）

```bash
cd wujun-os
python3 scripts/book_coverage.py --help   # 核对子命令
# 按书生成覆盖片段 → out/覆盖与质检报告/（待建目录）
```

## 当前可先做

- 手册侧：`必检议题覆盖表_骨架.md`（`s17_coverage_stats.py`）
- K 卡侧：`verify_cards` + `state/p4_k_card_freeze_manifest.sha256`
- 勿在 P5 M3 未完成前标 P6 过关
