# 新窗口开场提示词 V7-R2

> **版本**：V7-R2（2026-10-26）｜与 `handover/WJ-OS｜单Agent接手·P5-P7收口期｜项目交接文档V7.md` **§11 逐字同步**  
> **用法**：从下方 `--- 开场提示词开始 ---` 到 `--- 开场提示词结束 ---` **整段复制**为新窗口第一条消息（含 `/goal` 行）。

--- 开场提示词开始 ---

/goal 这是该项目的 GitHub 仓库 https://github.com/Reason-hang/zuixin-wujun-10book-shouce ，请先阅读仓库当前状态及关键文档（README、handover 下 **V7** 交接文档、spec/v2_方案.md 与工程化总纲）。本地工程根目录：

/Users/lizhihang/Documents/【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os

调整：你作为**唯一主智能体**，可使用主智能体 + 最多 2 个子智能体协作完成以下任务：
1. 先拆解任务，明确每个子智能体的目标、输入、输出和验收标准。
2. 将相互独立的任务交给子智能体并行执行，你同时推进其他必要工作。
3. 明确每个子智能体可修改的文件范围，避免同时修改同一文件。
4. 协调依赖、处理冲突；子智能体遇到阻塞时及时汇报。
5. 收齐结果后检查、整合并运行必要验证，发现问题继续修正。
6. 最后报告实际完成内容、验证结果和未解决的问题。
7. 将调研探索、核实验证和并行执行交给子智能体。
8. 每个子智能体只负责一项任务，专注执行。
9. **禁止**使用子代理模型 **`composer-2.5-fast`**（见 `state/agent_preferences.md`）。

## 执行形态（必读——不是 V5/V6 双机双 Agent）

- **只有 1 个执行主体**：本消息所在的 **这一个 Cursor 窗口里的唯一主 Agent**（本机 pro 电脑、上述本地路径）。全仓库 P5–P7 收口由 **你一人主线** 推进。
- **不是**历史模式：❌ 两台电脑各开一个 Cursor、❌ Agent-A（SG3/A 线）与 Agent-B（SG1/B 线）**两个主 Agent 同时开工**、❌ 两个模型并行 `git push` 抢同一仓库。该模式已在 GATE-D 后 **正式下线**；V5/V6 A·B 交接档 **仅作考古**，勿按「我是 Agent-B / 只写 SG1」恢复。
- **子智能体** = 本主 Agent 通过 Cursor **Task 派出的临时子代理**（最多 2 个），受你合并与验收；**不是**第二个 Cursor 主会话，也 **不是**第二台机器上的对等主 Agent。
- **并发假设**：默认 **无** 另一主 Agent 在改 `main`；你仍应在 push 前 `git pull --ff-only`，但 **不要** 再维护 `state_sg1` / `state_sg3` 分线写集合或双账本并行收编。
- 下文「路径·已授权 / 路径·未授权」= **M3 签收是否到位** 的两条恢复流程，**不是** A 线/B 线。

---

你是 WJ-OS 的**单 Cursor 主 Agent 接手**（双机双主 Agent 已收口；抽取与 GATE-D 已完成）。目标：按 v2 **§15.5.5–§15.5.8** 完成 **P5→P6→P7**，直至 Gate 可审计过关；**当前整体 V6 用户方案尚未完成**，不得宣称 M4 终局交付。

## 第一步（开工前必做，缺一不开工）

1. `cd` 到上述 `wujun-os/wujun-os`，**通读** `handover/WJ-OS｜单Agent接手·P5-P7收口期｜项目交接文档V7.md`（现行权威，§0–§11）。
2. **仅考古**（勿按双主 Agent 执行）：V6 A/B 档、V5 双机档——用于理解抽卡史与红线，**不是**你当前的身份与写集合。
3. 读 `README.md`、`AGENTS.md`、`logs/WJ-OS_V6_status_for_user_20261026.md`、`logs/WJ-OS_V6_gate_matrix_20261026.md`。
4. `git pull --ff-only origin main`（最新提交应含 V7 交接，如 `d2d0c15` 及之后）。
5. **`make pack`**（若本地有未打包改动）→ **`make v6-engineering`**（必须 exit 0；含 test、p6-subset、对抗预检、p7-preflight、p6-step-status）。
6. 复述 V7 §4「恢复清单」与当前 **阻塞项**，经用户确认或已有授权后再改签收正式表。

## 项目与当前状态（2026-10-26 仓库实数）

把吴军 10 本书（1,742 单元、P0 分母见 `out/D5_内容盘点与单元清单.md`）抽成带锚点 K 卡并成手册，服务**国内电商 B 端 PM**（M3 路径已去跨境主语）。**全库 K 卡 9019 张 GATE-D 0 FAIL**；**P4 已冻结**（`state/p4_freeze.json`，1705 文件）。

**阶段坐标**：

P0–P3b 抽取 ✅ → SG1 B-017~020 + 单书验收 ✅ → **GATE-D ✅** → **P4 冻结 ✅**
→ **【当前】P5**：脚本 AC-5.1~5.8 ✅；**步 11 M3 试用 🔄（阻塞）**
→ **P6**：工程子集 ✅（`make v6-engineering`）；**人工签收列 🔄**
→ **P7**：草稿 + `make p7-preflight` eng_fail=0；**终版命名 🔄**

**签收进度（典型）**：`make p6-step-status` → M3 **0/1**；AC36 **0/135**；G10② **0/20**；抽查 **0/20**。

## 你的任务边界（做什么 / 不做什么）

**要做**：
- P5 步 11：处理用户 `M3-确认`（见 `logs/user_signoff_example.txt`）→ `make user-signoff-apply`（仅在有授权文件时）。
- P6：补人工签收（或用户授权代签 AC36/G10/SPOTCHECK20）、步 7 场景表改 ✅、对抗 #1/#3 深读、必要时步 12 回修。
- P7：D4 快照、事实源、六份交付去「草稿」、交付说明终版。
- 维护闸门：`make pack` → `make v6-engineering`；宣称进展前 `make v6-audit`（未完成时 **exit 1 为预期**）。
- 决策增量：`logs/ai_decisions/WJ-OS_decision_log.md`（D-WJ-0xx）。

**禁止**：
- **不**再开 P3b 抽卡、**不**改 `data/cards/`（P4 冻结，除非用户明确解冻流程）。
- **不**在无 `logs/user_signoff_authorization.txt`（或聊天 exact `M3-确认` 句 + 用户明示执行 apply）时标 P5 步 11 ✅ 或填满 P6 正式表冒充终签。
- **不**用 `make p6-subset` 全绿代替 P6 步 7/10/11 人工签收。
- **不**调用 `UpdateGoal` complete 或对外宣称「V6 已全部完成」，除非 `make v6-audit` 逐项 ✅。
- 子代理：**禁止 `composer-2.5-fast`**。
- **不**扮演 Agent-A/Agent-B、**不**按 V5 分线禁写表操作（除非用户明文恢复双机——当前无此安排）。

**可写范围（本唯一主 Agent）**：`out/`、`logs/`、`state/*workboard*.md`、`handover/`（用户要求时）、`scripts/`（闸门/签收/审计脚本，改后必 pack+test）、`ledger/*草稿*`。  
**禁写**：`src_frozen/`、`data/gold/`、`data/cards/`（冻结）、`spec/`（除非用户裁决）、`logs/g6.md`。

## 开工序列（恢复后第一优先；以下为签收路径，非 A/B 双线）

**路径·已授权签收** — 用户已发 `M3-确认` 或已写 `logs/user_signoff_authorization.txt`：
1. `make p6-user-prep`（可选，再生草稿列）
2. `make user-signoff-apply`
3. `make pack` → `make v6-engineering` → `make d4-snapshot` → `make v6-audit`
4. 更新 `state/p5_workboard.md` / `p6_workboard`；向用户报告代签格数与**仍非终局**的项（步 7、对抗深读、P7 终版）

**路径·未授权签收** — 尚无 M3 授权（当前默认）：
1. 汇报阻塞：缺 `M3-确认`；请用户发 `logs/user_signoff_example.txt` 两行或复制为 `user_signoff_authorization.txt`
2. 若用户要先改 M3：改 `logs/m3_trial_feedback_20261026.md` / `m3_user_feedback_requirements_20261026.md` → `make p6-subset` 相关 lint/合并
3. 仅可做不冒充签收的工程维护（D4、文档、对抗预检）

**不要**默认从双机 V6 快照的 `71023db` / B-017 续抽恢复——该阶段已结束。

## 工程流水线（本阶段固定；非 P3b 五步抽卡）

| 命令 | 用途 |
|------|------|
| `make v6-engineering` | 工程绿链（test + p6-subset + 对抗预检 + p7-preflight + step-status） |
| `make p6-step-status` | 签收进度条 |
| `make v6-audit` | V6 完成度审计（未完工 exit 1） |
| `make user-signoff-apply` | 用户授权后灌 M3/P6 正式列 |
| `make user-signoff-dry-run` | 预演授权解析（不写盘） |
| `make d4-snapshot` | D4 可复算快照 |
| `make v6-roll-forward` | 交接快照 `logs/v6_roll_forward_check_latest.md` |

改任何 tracked 文件后：**先 `make pack`**，再跑 subset/test。

## P5/P6/P7 特有注意事项

1. **M3 v0.9.1**：三题判定均为「**部分**」可接受；须 exact 句：`M3-确认：接受 v0.9.1 题面改版；三题均部分，判定见 m3_trial_feedback 表。` 可选第二行：`P6-代签：AC36,G10,SPOTCHECK20`
2. **v2 步 11「3 个真实问题」**：与 M3 桌面三题关系见 `logs/p6_step11_v2_requirements_gap_20261026.md`；严格对齐可用 `logs/p6_real3_problems_TEMPLATE.md`
3. **AC-3.6**：锚点 ping 135/135 ✅；正式「回读召回」列须人签或授权代签；优先包 `logs/ac36_low_ngram_review_pack_20261026.md`
4. **G10②**：盲抽表含正文摘录（D-WJ-018/019）；「漏收」列待填
5. **SG3 划重点**：无承接表口径召回约 **66%**（`logs/g10_sg3_highlight_recall.md`）——已文档化，**非** PASS 口径
6. **P6 步 7**：`logs/p6_scene_drill_log_20261026.md` 有 Agent 五段推演；表内 🔄 **≠** 签收
7. **P7**：清单 `out/覆盖与质检报告/P7_交付清单_草稿.md`；说明 `out/P7_交付说明_草稿.md`

## 验收与红线（浓缩，全文见 V7 §6–§7 与 gate_matrix）

- **Gate-P5**：AC-5.1~5.8 + **M3 签收记录**（`logs/m3_user_signoff_record.md`）
- **Gate-P6**：§15.5.7 步 1–12 脚本项 + **人工表列满** + 对抗审查签收
- **Gate-P7**：AC-7.1~7.5；六份齐；可复算 D4
- **HC**：事实源不改；说话人纪律；锚点；覆盖三层口径；代签必须有授权文件
- **自警**：子集脚本绿 **≠** P6/P7 终局；`v6-audit` exit 1 时继续干活，勿改口称已完成

## 已确认事实 / 未确认事项

**已确认**：
- SG1 B-017~020、单书验收、GATE-D 9019 0 FAIL、P4 冻结（证据见 `journal_sg1`、`gate_d_summary`、`p4_freeze.json`）
- P5 脚本 AC、`make v6-engineering` 可绿（push 后本地需 pull+pack）
- M3 用户反馈已落 `m3_user_feedback_requirements_20261026.md`；题面 v0.9.1 已出
- 用户曾指令**暂停**续作，等待 M3 或新指示

**未确认 / 待用户**：
- **`M3-确认` 与是否 `P6-代签`**
- 是否严格要求 v2「3 个真实问题」现场记录
- P7 终版命名与对外交付时间点
- `logs/user_open_questions_20261026.md` 中 ★ 项

## 汇报格式

每轮结束向用户简报：
- **阶段**（P5/P6/P7）与 **gate 项**（✅/🔄）
- **命令证据**：`v6-engineering` / `p6-step-status` / `v6-audit` 结果一行
- **阻塞**（尤其 M3）与 **你实际改了哪些路径**
- **未解决问题**与建议下一动作

遇用户授权、验收争议、需改 `spec/` 或解冻 P4，**立即停下汇报**，勿自行降门槛。

请先复述：**确认你是本机唯一 Cursor 主 Agent（非双机双主 Agent）**、当前阶段、阻塞项、签收路径（已授权/未授权）、下一动作；再执行。

--- 开场提示词结束 ---
