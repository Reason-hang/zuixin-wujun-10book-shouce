# P6 步 10｜对抗式审查（脚本子集已核实 · 全文审查待 P5/M3 后）

> v2 §15.5.7 步 10。下表 **#4/#5** 已由自动化闸门核实；**#1–#3** 仍须人工深读（含你 20 张抽查）。

| # | 角度 | 高风险点 | 核实结论 | 修正 |
|---|------|----------|----------|------|
| 1 | 原著失真 / E2 当 E1 | 转述卡当吴军原话进手册 | 🔄 锚点草稿 0 FAIL；深读草稿见 `p6_adversarial_agent_notes_20261026.md` | E2 卡标「勿当原话」 |
| 2 | 映射冒充原著 | 手册「映射·非原著」漏标 | 🔄 `s17_mapping_split_check.py` 45/45 PASS（2026-10-26） | 持续 lint |
| 3 | 场景与卡错配 | S-xxx 指向不存在 M 卡 | 🔄 lint + AC-5.4 PASS；演练草稿见 `p6_scene_drill_log` + `p6_adversarial_agent_notes_20261026.md` | — |
| 4 | 工具步骤无锚点 | T1 缺锚点 | ✅ `s17_tools_check.py` 15 工具 0 issue | — |
| 5 | 冻结后 silent drift | K 卡或包被改 | ✅ `p4_freeze manifest` + `verify_pack`（`s15_check_all`） | 改卡须解冻流程 |

## 证据入口

- 抽查表：`out/覆盖与质检报告/P6_用户抽查20张_草稿.md`
- K 卡：`verify_cards` / `state/p4_k_card_freeze_manifest.sha256`
- G10：`logs/g10_sg3_highlight_recall.md`（无承接表 ~66% 为真实缺口）
- G0–G9 日志索引：`out/覆盖与质检报告/G0_G9_日志索引.md`（`make g-logs-index`）
- G9 单元↔K 卡子集：`logs/g9_subset_check_latest.md`（`make g9-subset`）
- 自动预检汇总：`logs/p6_adversarial_preflight_latest.md`（`make p6-adversarial-preflight`）
