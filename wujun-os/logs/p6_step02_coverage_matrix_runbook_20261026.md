# P6 步 2｜核心论点覆盖矩阵（粗矩阵已出，AC-3.6 未做）

> 前置：P4 冻结 ✅；P5 未 PASS（**仅 M3 步 11**）；112 议题 ✅。

## 目标

逐书双向矩阵：原著单元/划重点 ↔ K 卡 ↔ 手册模型（v2 §15.5.7 步 2）。

## 建议命令（本机有 `src_frozen` 时）

```bash
cd wujun-os
python3 scripts/book_coverage.py --help   # 核对子命令
# 十书单书处置覆盖（Z2-09，2026-10-26 已跑 PASS）：
#   out/覆盖与质检报告/book_coverage_<书码>.md
make p6-matrix   # → out/覆盖与质检报告/P6_核心论点覆盖矩阵_草稿.md
```

## 当前已有

- 粗矩阵：`make p6-matrix`（十书 K 卡/单元/手册锚点引用 + book_coverage PASS）
- 手册侧：`必检议题覆盖表_骨架.md`（112/112）
- K 卡侧：`verify_cards` 9019；冻结 manifest
- **缺**：AC-3.6 成书 15 条/来信 10 条原文回读抽检
- 勿在 P5 M3 未完成前标 P6 过关
