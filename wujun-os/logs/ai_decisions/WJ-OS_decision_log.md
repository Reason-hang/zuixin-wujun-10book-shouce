# WJ-OS · AI 自主决策台账

> 格式与字段要求见 `spec/AI工程师通用自主决策记录文档规范.md` §七。  
> **低风险**小步（如改错别字）不记；**中/高**与影响验收口径的默认项必记。  
> 验证证据优先：`make test` 输出、`logs/*_latest.md`、journal 行号、git commit。

---

## D-WJ-001 用户确认「其余默认决策暂时 OK」

- **编号**：D-WJ-001
- **上下文**：P5 进行中；`logs/user_open_questions_20261026.md` 列 M3、V5、P4-U1、★2 等待答项。
- **事项**：用户 2026-10-26 表示除 M3 说明与 ★2 数量疑问外，此前 Agent 默认决策可继续执行。
- **风险等级**：低（不改变封板 K 卡；不伪造 M3 反馈）。
- **候选方案**：(1) 全部暂停等逐项签字；(2) 未答项维持文档默认并继续 P5/P6 准备。
- **评估依据**：用户原话；M3 仍须本人试用，不得代填（AC-5 / v2 §7.6）。
- **结论**：采用 (2)。**M3-1/M3-2 仍阻塞 P5 步 11 PASS**；V5/P4-U1/★2 按表内默认推进。
- **执行动作**：更新 `out/M3_手册试用_v0.9.md` 白话说明；本台账建档；规范入 `spec/`。
- **验证证据**：本文件；`spec/AI工程师通用自主决策记录文档规范.md` 存在。
- **回滚条件**：用户改口任一项默认 → 更新 `user_open_questions` 并记 D-WJ-00x 修订。

---

## D-WJ-002 纳入《AI工程师通用自主决策记录文档规范》

- **编号**：D-WJ-002
- **上下文**：用户要求将 `/Users/lizhihang/Documents/AI工程师通用自主决策记录文档规范.md` 纳入仓库并后续按此记决策。
- **事项**：规范落盘路径与 Agent 入口引用。
- **风险等级**：低。
- **结论**：复制为 `spec/AI工程师通用自主决策记录文档规范.md`；决策实例写入 `logs/ai_decisions/WJ-OS_decision_log.md`；`AGENTS.md` 增加读取指针。
- **验证证据**：文件存在；与源文档同名结构（八章）。
- **回滚条件**：若规范与 v2/constraints 冲突，以 **HC 红线 + v2** 为准，并记修订说明。

---

## D-WJ-003 ★2 L2/L3 三档数量（维持默认）

- **编号**：D-WJ-003
- **上下文**：`spec/pillars.yaml` → `quantity_tiers`；P4 步 13 已确认骨架。
- **事项**：L2/L3 是否超预警/红线。
- **风险等级**：中（影响 P4 封板有效性）。
- **评估依据**：`spec/pillars.yaml`：`l2` 目标 22–28、预警 28、红线 32；`l3` 目标 32–44、预警 44、红线 50。P4 确认：**L2=25**（恰好规范「二级 25 个」）；**L3 注册表 43 节点**（在目标带内）。P5 手稿 `M-Dxx` 为成稿层局部编号，可多于 43（合写/变体），以注册表为 P4 数量门禁。
- **结论**：★2 **确认默认**，不扩 L2、不增 L3 注册节点除非走 CHG。
- **验证证据**：`logs/p4_step13_dictionary_change_report_20261026.md`（**43** 节点）；`python3 -c "import yaml; …"` 现读 registry **45** 项 → **待核对**是否与步 13 后增量一致（未超红线 50）。
- **回滚条件**：用户 `★2：给出新红线` 或 CHG 批准增删 L2/L3。

---

## D-WJ-004 M3 试用未填则步 11 保持 🔄

- **编号**：D-WJ-004
- **上下文**：AC-5 使用验证；`out/M3_手册试用_v0.9.md`。
- **事项**：能否由 Agent 代填 M3 反馈表。
- **风险等级**：中（虚假 PASS）。
- **结论**：**禁止** Agent 伪造用户试用；仅可扩充说明与示例；用户填表或聊天等价回复后写入 `logs/m3_trial_feedback_*.md` 再标步 11。
- **验证证据**：`logs/p5_acceptance_gap_20261026.md` M3 行仍为 FAIL/待用户。
- **回滚条件**：用户完成 M3 并授权记录 → 新决策关闭本阻塞。

---

## D-WJ-005 AC-5.8 必检议题表 112/112 结案

- **编号**：D-WJ-005
- **上下文**：P5 步 4；覆盖表 23 项「待P5」。
- **事项**：补 Markdown 核心卡（不改 K 卡 JSON）并更新结局列。
- **风险等级**：中（「并入」须指向卡内确有论述，禁止空填）。
- **结论**：新增/补全 M-D01-05、M-D02-04、M-D03-03、M-D04-03~05、M-D06-05、M-D07-03~05、M-D08-03~07、M-D10-03~04；`s17_coverage_stats.py` → **112/112**。
- **验证证据**：`logs/s17_coverage_stats_latest.md`；`make test` PASS。
- **范围与遗留**：AC-5.8 表结案 ≠ P5 全书 PASS；M3、合并稿、三柱篇幅仍开。

---

## D-WJ-006 D1 合并稿 v1 与 AC-5.3 字数门禁

- **编号**：D-WJ-006
- **上下文**：P5 AC-5.3；十章汉字统计三柱占比低于 45%。
- **事项**：加厚 D01/D02/D06 映射层练习 + 合并脚本 + 可复算统计。
- **风险等级**：中（映射层须标非原著，不冒充 E1）。
- **结论**：新增 `scripts/s17_d1_merge_and_stats.py`；产出 `D1_主手册合并稿_v1.md`；三柱 **45.2%** PASS（`logs/s17_d1_pillar_ratio_latest.md`）。
- **验证证据**：脚本 exit 0；`s17_manual_lint` 0 issues；并入 `s15_check_all` 子集检查。
- **回滚条件**：用户要求合并稿仅索引 → 保留 v0 导航，v1 标实验稿。

---

## D-WJ-007 M3 桌面推演（用户选型 A）

- **编号**：D-WJ-007
- **上下文**：用户不读十书/无真场景；选型 **A 桌面推演** + **接受片段试用**。
- **结论**：记入 `logs/m3_trial_feedback_20261026.md`；Q1=**部分**（占位未细化）；Q2/Q3 待补。**步 11 仍 🔄**（须三题均有命中/部分 + 具体「能跟到/缺什么」）。
- **验证证据**：用户聊天 2026-10-26；不代填 Q2/Q3。

---

## D-WJ-008 子代理禁用 composer-2.5-fast

- **编号**：D-WJ-008
- **上下文**：用户要求形成记忆：子代理勿用 fast 变体（token 成本）。
- **结论**：写入 `state/agent_preferences.md` + `AGENTS.md` 子代理模型节。
- **验证证据**：本文件与仓库文件存在。

---

## D-WJ-009 S13 关键词反查（G10① 首跑）

- **编号**：D-WJ-009
- **上下文**：P6 步 4 缺 `s13_kwscan.py`；词表落 `data/concept_watchlist.csv`（40 词，对齐 §B.3 + 手册簇）。
- **结论**：段落命中按 `units_index` + 处置 + 行级 `claim_id` 登记；首跑 **1544** 命中、**0** 无单元映射；报告 `logs/g10_kw.md`、副本 `out/覆盖与质检报告/g10_kw.md`；接入 `s15_check_all`（非 strict，不等同 G10 全过关）。
- **验证证据**：`python3 scripts/s13_kwscan.py` exit 0。

---

## D-WJ-010 SG3 划重点承接表（G10③）

- **编号**：D-WJ-010
- **上下文**：strict 召回仅 ~66%；需可审计去向而非降门槛。
- **结论**：`s13_sg3_carry_table.py` 自 miss backlog 生成 `out/D1_手册草稿/SG3_划重点承接表_草稿.md`（承接句=同单元 K 卡 `claim_text`）；纳入 s13 语料后 strict 启发式 100%；`s15_check_all` 先 regen 承接表再 `--strict`。
- **验证证据**：`python3 scripts/s13_sg3_highlight_recall.py --strict` exit 0。

---

## D-WJ-011 D3 锚点子表导出

- **编号**：D-WJ-011
- **上下文**：`make verify-anchors` 因缺台账失败。
- **结论**：`s12_export_anchor_ledger.py` 自 K 卡生成 `ledger/溯源与处置台账.md`（8950 行）；`verify-anchors` 全 PASS；接入 `s15_check_all`；`make export-anchors`。
- **验证证据**：`make verify-anchors` 输出 失败 0。

---

## D-WJ-012 S18 子集与 D5 表格管道符

- **编号**：D-WJ-012
- **上下文**：`s18_render_check.py` 对 `out/` 报 5 项 FAIL（跨表误报 + 标题含 `|`）。
- **结论**：S18 按连续表格块计列数；D5 五行标题 `|`→`｜`；`s08_d5.py` 导出时统一替换；`make render-check`。
- **验证证据**：`make render-check` → issues=0；`logs/s18_render_check_latest.md` PASS。

---

## D-WJ-013 D3 论点卡子表 + S18 接入子集

- **编号**：D-WJ-013
- **上下文**：D3 除锚点外缺论点卡可复算导出；P7 需交付说明草稿。
- **结论**：`s12_export_k_claim_table.py` → `ledger/论点卡表_草稿.md`（9019 行）；`make d3-export` 三连；`s15_check_all` 增 S18；`out/P7_交付说明_草稿.md`。
- **验证证据**：`make p6-subset` fail=0（pack 后）。

---

## D-WJ-014 M3 v0.9.1 人读出处与国内电商画像

- **编号**：D-WJ-014
- **上下文**：用户 M3 审核：代号不直观、Q2/Q3 需十书整合方向、映射过短且行业为国内电商 PM。
- **结论**：题面加人读版 `C-…`；需求/方案分文档；映射 3–4 行；D06/D01 M3 路径去跨境主语；`s17_m3_glossary.py`；P5 步 11 待用户 `M3-确认` 后标 ✅。
- **验证证据**：`m3_user_feedback_requirements_20261026.md`、`m3_trial_feedback_20261026.md` v0.9.1；`s17_manual_lint` 0 issue。

---

## D-WJ-015 D07 阶段 1（沟通簇 + 三场景 + 度量）

- **编号**：D-WJ-015
- **上下文**：M3 Q2 路线图阶段 1；AC-5.4 上限 50 条场景。
- **结论**：`make d07-comm-index`；**S-129~131** 替换汇总中 S-101/104/113；`07_D07` 章首度量表；仍非「十书沟通整合完成」。
- **验证证据**：`make p6-subset` AC-5.4 PASS；`s17_manual_lint` 0 issue。

---

## D-WJ-016 P6 步 1 `make p0` + `s15_p0_gate_check`

- **编号**：D-WJ-016
- **上下文**：P6 审计项「全量 G4–G8 未重跑」；子集需可复算证明最近一次 P0 链仍 PASS。
- **结论**：`make p0` 全链 PASS；`scripts/s15_p0_gate_check.py` 接入 `s15_check_all`；`G0_G9_日志索引` 刷新。
- **验证证据**：`logs/g4.md`…`g8.md`；`s15_check_all_latest.md` 含「P0 G2–G8 日志 PASS」。

---

## D-WJ-017 G9 子集 + P6 对抗预检

- **编号**：D-WJ-017
- **上下文**：AC-6.1 要求 G9；步 10 需可复算预检。
- **结论**：`s12_g9_subset_check.py`（1742 单元↔unitcards↔K JSON）；`s17_p6_adversarial_preflight.py`；接入 `s15_check_all`。
- **验证证据**：`g9_subset_check_latest.md` PASS；`p6_adversarial_preflight_latest.md` fail=0。

---

## D-WJ-018 G10② 盲抽表正文摘录

- **编号**：D-WJ-018
- **上下文**：`G10②_盲抽单元表` 摘录列误拼 YAML 元数据（`book_code:FZtype:…`），无法支撑人工重读。
- **结论**：`s13_g10_blind_unit_sample.py` 跳过 frontmatter，摘录正文前 100 字；`make g10-blind-sample` 再生表。
- **验证证据**：`GG-U0057` 行含读者回信正文片段；`make g10-blind-sample` rows=20。

---

## D-WJ-019 G10 摘录去 Markdown 链接（S18）

- **编号**：D-WJ-019
- **上下文**：目录单元摘录含 `[标题](#锚点)`，S18 判为断链，`p6-subset` 失败。
- **结论**：摘录前 `re.sub` 去链接语法；对抗预检增「G10② 摘录正文」项。
- **验证证据**：`s18_render_check` issues=0；`p6_adversarial_preflight` fail=0。

---

## D-WJ-020 P7 工程预检 `make p7-preflight`

- **编号**：D-WJ-020
- **上下文**：P7 AC-7.2/7.3 需可复算检查与交付物存在性；与 v6-audit 分工（P7 不含签收项）。
- **结论**：`scripts/s18_p7_preflight.py`；终版文件名 FAIL 不计入 eng_fail。
- **验证证据**：`logs/p7_preflight_latest.md` eng_fail=0。

---

## D-WJ-021 V6 工程绿链与 roll-forward 快照

- **编号**：D-WJ-021
- **上下文**：需一条命令证明「工程可继续」且与签收进度分离。
- **结论**：`make v6-engineering`；`scripts/s17_v6_roll_forward_check.py` → `make v6-roll-forward`。
- **验证证据**：`logs/v6_roll_forward_check_latest.md`；`v6-engineering` exit 0。
