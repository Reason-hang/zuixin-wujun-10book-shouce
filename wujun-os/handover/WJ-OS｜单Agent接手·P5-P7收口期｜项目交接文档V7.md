# WJ-OS｜单 Agent 接手·P5–P7 收口期｜项目交接文档 V7

> **版本**：V7 定稿（2026-10-26；pro Mac **单 Cursor 主 Agent**；非双机双主 Agent）  
> **冷启动唯一权威**：**§4**（恢复→核对→阅读→抽查→测验→闸门→复述等开始）  
> **新窗口第一条消息**：仅 `handover/WJ-OS｜新窗口开场提示词V7.md`（§12 为入口说明）  
> **Agent 入口**：根目录 `AGENTS.md`（含换窗/推送前自检）  
> **根源**：以 `handover/WJ-OS｜项目交接文档V6｜A线Agent执行·收官收口期.md` 为结构基线，并入 B 线 V6 历史与 **2026-10-26 单 Agent 实作进度**（非双机暂停快照 `71023db`）。  
> **权威优先级**：**本文 V7** > `spec/v2_方案.md` + `spec/工程化总纲.md` > `logs/WJ-OS_V6_gate_matrix_20261026.md` > V6 历史档 > journal  
> **适用对象**：下一窗口 **唯一主 Agent**（≤2 子 Agent；**禁止** `composer-2.5-fast` 子代理，见 `state/agent_preferences.md`）  
> **仓库路径**：`/Users/lizhihang/Documents/【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os`  
> **远端**：`https://github.com/Reason-hang/zuixin-wujun-10book-shouce.git`（子目录 `wujun-os/`）

---

## 0. 本版撰写说明（对应你的需求）

| 你的要求 | V7 落点 |
|----------|---------|
| 梳理需求再写文档 | §0 + §1 |
| 当前进度 / 停手点 / 仓库状态 | §2–§4 |
| 后续执行步骤 | §5 |
| 验收标准 + AI 自检 | §6–§7 |
| 基于 V6、结合最新状态 | 全文；V6 双档见 §1.3 |
| V6 命名区分 A/B Agent | `项目交接文档V6｜A线Agent执行·…` / `…｜B线Agent执行·…` |
| 新窗口粘贴用提示词 | **仅** `handover/WJ-OS｜新窗口开场提示词V7.md`（§12 为入口说明） |
| **单 Cursor 主 Agent**（非双机） | §1.5 |
| **复水测验（全对才开工）** | §10；`spec/quiz.md` 可选加深 |
| **冷启动恢复（换窗/压缩后）** | §4（对齐 V1 `restore-check`、V5 §6、EP §6.3） |

---

## 1. 需求与范围（做什么 / 不做什么）

### 1.1 核心目标（V7 窗口）

在 **P3b 抽取与 GATE-D 已完成** 的前提下，按 v2 **§15.5.5–§15.5.8** 完成：

**P5**（手册 v0.9 试用门槛 + AC-5.x）→ **P6**（校验与对抗审查）→ **P7**（六份交付 + 说明），直至 **Gate-P7** 可审计过关。

用户 Goal 表述：**SG1 B-017~020、SG1 单书验收、GATE-D、P4–P7**，每道闸门有证据才可宣称完成。

### 1.2 做什么

- 以 **脚本闸门 + 日志证据** 推进；人工签收项（M3、AC-3.6 回读、G10②、抽查 20 张、场景演练等）**不得代签冒充**（除非用户写入授权文件并 `make user-signoff-apply`）。
- 维护 `make pack` 与 `verify_pack`；改 tracked 文件后 **先 pack 再 test/p6-subset**。
- 决策增量写入 `logs/ai_decisions/WJ-OS_decision_log.md`（D-WJ-0xx）。

### 1.3 不做什么

- **不**回到 P3b 批量抽卡改 `data/cards`（P4 已冻结，见 `state/p4_freeze.json`）。
- **不**宣称「V6 整体方案已全部完成」（当前 **P5 步 11 / P6 人工项 / P7 终版** 未齐）。
- **不**用子集脚本全绿替代 P6 步 7/10/11 人工签收。
- **不**擅自把 M3 桌面推演等同于 v2「3 个真实问题」（见 `logs/p6_step11_v2_requirements_gap_20261026.md`）。

### 1.4 历史文档对应关系

| 文件 | 角色 |
|------|------|
| `…V7.md`（本文） | **现行**单 Agent P5–P7 |
| `…V6｜A线Agent执行·收官收口期.md` | **历史**：双机期 A 线收官、GATE-D 前决策树 |
| `…V6｜B线Agent执行·SG1执行期.md` | **历史**：B 线 SG1 暂停点（B-017 在途等） |
| `…项目交接文档V5.md` | 双机 git/五步流水线细节补充 |

### 1.5 执行形态（必读——不是 V5/V6 双机双 Agent）

| 维度 | V7 现行 | 已下线（勿恢复） |
|------|---------|------------------|
| 主 Agent 数量 | **1**：本 Cursor 窗口唯一主 Agent（本机 pro 路径） | Agent-A + Agent-B 两台电脑各开 Cursor |
| 并行 push | 单主线；push 前 `git pull --ff-only` | 两模型同时收编、`journal_sg1` / `journal_sg3` 分线写集合 |
| 子智能体 | 主 Agent 派 **Task 子代理 ≤2**，合并验收 | 第二台机器上的「对等主 Agent」 |
| 文档身份 | 读 V5/V6 A·B 档 **仅考古** | 「我是 Agent-B / 只写 SG1」 |
| 「路径·已授权/未授权」 | **M3 签收** 两条恢复流程 | **不是** SG1/SG3 或 A 线/B 线 |

---

## 2. 整体方案：当前进行到哪个阶段？

```
P0–P3b 抽取 ✅ → GATE-D ✅ → P4 K 卡冻结 ✅
→ 【当前】P5（脚本 AC ✅，M3 步 11 🔄）→ P6（工程子集 ✅，人工签收 🔄）→ P7（草稿 🔄）
```

**一句话**：全局卡在 **P5 用户 M3 确认** 与 **P6/P7 人工签收 + 终版命名**；工程侧已具备 `make v6-engineering` 绿链能力。

### 2.1 已核实事实（有日志/命令证据）

| 里程碑 | 证据 |
|--------|------|
| SG1 B-017~B-020 收编 | `state/journal_sg1.md` JS1-021~027；`data/cards/T-P3b-B-017`…B-020 |
| SG1 单书验收 | JS1-026；`logs/book_coverage_SG1_20261026.md` |
| GATE-D 9019 卡 0 FAIL | `logs/gate_d_summary_20261026.md` |
| P4 冻结 | `state/p4_freeze.json`（1705 文件） |
| P5 脚本 AC-5.1~5.8 | `make p6-subset` → `logs/s15_check_all_latest.md` 无 FAIL 行 |
| D07 阶段 1 工程初稿 | S-129~131；`make d07-comm-index`；路线图草稿 |
| M3 题面 v0.9.1 | `logs/m3_trial_feedback_20261026.md` + 需求 `m3_user_feedback_requirements_20261026.md` |
| 锚点 8950 | `make verify-anchors` |
| P6 工程子集 | P0 重跑、`g9_subset`、G10①③、AC36 锚点 ping 135/135、对抗预检 fail=0 等 |

### 2.2 未确认 / 待用户

| 项 | 状态 |
|----|------|
| **M3-确认**（P5 步 11） | 无 `logs/user_signoff_authorization.txt`；无 `logs/m3_user_signoff_record.md` |
| P6 正式表列（AC36/G10/抽查） | `make p6-step-status` 典型 **0/135、0/20、0/20** |
| P6 步 7 五场景 | `p6_scene_drill_log` 表内仍 🔄 Agent 草稿 |
| P6 对抗 #1/#3 深读 | 有 Agent 笔记，未签收 |
| P7 终版命名（去「草稿」） | 无 `out/P7_交付说明_v1.0.md` 等 |
| v2「3 个真实问题」严格对齐 | 可选 `logs/p6_real3_problems_TEMPLATE.md` |

### 2.3 已确认用户偏好

- M3：**桌面推演 A**；三题判定均为「部分」可接受（须显式 `M3-确认` 句）。  
- 画像：**国内电商 PM**（非跨境主路径）；人读版 `C-…` 出处。  
- 子代理：**禁止 composer-2.5-fast**（`state/agent_preferences.md`）。

---

## 3. 暂停点：中断前在做什么？

**用户指令**：「暂停一下当前手头上的工作」（2026-10-26）。

**Agent 停手前最后一轮工程**（非抽卡）：

- 签收基建：`user_signoff_example.txt`、`make user-signoff-apply`、`make p6-step-status`、`make v6-audit`
- G10② 摘录修复（D-WJ-018/019）、`make v6-engineering`、`make p7-preflight`、`make v6-roll-forward`
- **未执行**：`make user-signoff-apply`（因无用户授权文件）

**阻塞根因**：等待用户 **`M3-确认：接受 v0.9.1…`**（可选第二行 `P6-代签：AC36,G10,SPOTCHECK20`）。

---

## 4. 新窗口冷启动恢复规程（开工前必做，缺一不开工）

> **七步记忆（用户定稿）**：**恢复 → 核对 → 阅读 → 抽查 → 测验 → 闸门 → 复述等开始**（下表 **A–H**；授权分支 **I**；红线 **J**）。  
> **不信对话摘要**；以仓库文件与命令输出为唯一真相（`spec/长任务稳定性与上下文工程方案.md` §6.3）。  
> V1/V4/V5 沿革已收敛进本表；P5–P7 **不再**领 P3b 批工单。维护时以 **本节为唯一表**，改一处即改 `新窗口开场提示词V7.md` 第一步 + `AGENTS.md`。

| 步 | 动作 | 通过标准 / 备注 |
|----|------|-----------------|
| **A** | `cd` §0 路径 → `git pull --ff-only origin main` | 与 `origin/main` 一致 |
| **B** | **环境 / 哈希核对**（二选一） | 任一路径 fail 即停，先修环境 |
| B1 **常规**（本机已有 `src_frozen/`，推荐） | `make verify-pack` | exit 0；怀疑原文被改时再 `make freeze` |
| B2 **全量冷启动**（换机、久未开、无 `src_frozen`） | 书籍 zip 复制为 `./_打包吴军10本电子书.zip` → **`make restore-check`**（= verify-pack + freeze + probe + test + status） | 全链 exit 0（见 V1/V4） |
| **C** | **状态快照** | `make v6-roll-forward` → 读 `logs/v6_roll_forward_check_latest.md` |
| | | `make status`：仅作渲染；**勿**把冻结的 `state/state.json`（J-143 快照）当 P5–P7 实况——以 `gate_matrix`、workboard、`journal_sg1` 尾行为准 |
| **D** | **权威阅读顺序** | 能复述阶段与阻塞 |
| | 1 | 本文 V7 **§0–§11**（含 §1.5 执行形态、本节 §4） |
| | 2 | `spec/constraints.md`（HC 红线编号） |
| | 3 | `state/STATE.md`、`state/p5_workboard.md`、`state/p6_workboard.md`（若有） |
| | 4 | `state/journal_sg1.md` **末 10 行**（抽卡/GATE-D 史；总账本 `state/journal.md` 冻结至 J-148，考古用） |
| | 5 | `logs/WJ-OS_V6_status_for_user_20261026.md`、`logs/WJ-OS_V6_gate_matrix_20261026.md`、`logs/p6_user_signoff_checklist_20261026.md` |
| **E** | **信任校准抽查**（继承 V5 §6 第 4 步） | 从 `state/p4_freeze.json` 列出的路径任选 **2 张** K 卡 JSON，对照 `src_frozen/` **复核锚点行号 + SHA1**（不重抽、不改卡） |
| **F** | **复水测验** | V7 **§10 十题全对**；首条回复附自答摘要；错则回读后再答。**禁止**测验未全对时改 tracked 文件 |
| | 可选 | `spec/quiz.md` 抽 12 题 ≥11（EP/ST-1 加深） |
| **G** | **工程闸门** | `make pack`（若本地有未打包改动）→ **`make v6-engineering`** exit 0 |
| **H** | **复述并待命** | 向用户报告：唯一主 Agent 确认、§10 是否全对、阶段/阻塞/签收路径、`v6-engineering` 一行证据；**等用户「开始」或书面授权**再跑签收 apply / 改正式表 |
| **I** | **授权后分支**（非冷启动必做） | 已授权：`make user-signoff-apply` → pack → `v6-engineering` → `v6-audit`；要先改 M3：改 trial/需求文档 → 相关 lint → 再收 `M3-确认` |
| **J** | **红线** | 未收 M3 前不得 `UpdateGoal` complete 或宣称 V6/P7 终局；子集脚本绿 ≠ 人工签收 |

**压缩 / 换 Agent**：视同冷启动，从 **A** 重做；摘要与仓库冲突时 **以仓库为准**，并在 `logs/` 留一条说明。

---

## 5. 后续执行流程（P5→P7）

### 5.1 P5 收尾

| 步 | 动作 | 过关 |
|----|------|------|
| 5.1–5.10 | 十章片段、工具、场景、lint | 脚本 ✅ |
| **5.11 M3** | 用户读 v0.9.1 → 授权 | `m3_user_signoff_record.md`；`p5_workboard` 步 11 ✅ |

授权文案：`logs/user_signoff_example.txt`

### 5.2 P6（v2 §15.5.7 摘要）

| 步 | 工程可绿 | 人工签收 |
|----|----------|----------|
| 1 G0–G9 | 子集 + `make p0` 重跑 | 全链历史 G9 手册链持续复核 |
| 2 矩阵 | `make p6-matrix` 粗矩阵 | 语义 100% |
| 3 AC-3.6 | ping 135/135 | 正式「回读召回」列 |
| 4–5 G10 | ①③ | ② 漏收 20 行；无承接 ~66% 已文档化 |
| 6–9 | 数理/滑窗/锚点 | — |
| 7 场景 | `make p6-scene-drill` | 演练表 ✅ |
| 10 对抗 | `make p6-adversarial-preflight` | 模板 #1/#3 |
| 11 抽查 | 锚点草稿 20/20 | 「你的判断」列 |
| 12 回修 | — | 缺陷触发时 |

### 5.3 P7（v2 §15.5.8）

1. `make render-check` / `make p7-preflight`  
2. `make d4-snapshot`；事实源 `make fact-source`  
3. D1–D6 **去草稿后缀**、进度台账终版  
4. `P7_交付清单` 清点 + `P7_交付说明` 终版  
5. 向用户交付范围/局限（见 `out/P7_交付说明_草稿.md`）

---

## 6. 验收标准（Gate 对照）

**总表**：`logs/WJ-OS_V6_gate_matrix_20261026.md`  
**自动审计**：`make v6-audit` → `logs/v6_completion_audit_latest.md`（**未完成时 exit 1 为预期**）

| Gate | 关键条件 |
|------|----------|
| Gate-P5 | AC-5.1~5.8 + **M3 签收** |
| Gate-P6 | 步 1–12 脚本项 + **人工表列满** + 对抗签收 |
| Gate-P7 | AC-7.1~7.5；六份齐；可复算 D4 |

**P5 脚本复验**：`make v6-engineering`  
**P7 工程预检**：`make p7-preflight`（`eng_fail=0`；终版文件名 FAIL 在 P6 前预期）

---

## 7. AI 自检清单（每轮结束）

- [ ] **换窗首轮**：§4 冷启动 **A–H** 已做（含 verify-pack 或 restore-check、roll-forward、2 卡抽查、§10 全对）
- [ ] `make pack`（若改过 tracked）且 `make v6-engineering` **exit 0**
- [ ] 未改 `data/cards/` 除非用户明确解冻流程
- [ ] `make p6-step-status` 与宣称的签收进度一致
- [ ] 未在无 `M3-确认` 时标 P5 步 11 ✅
- [ ] 未将 Agent 草稿列当作 P6 终签
- [ ] 重大决策已写 D-WJ-0xx
- [ ] 宣称「V6 完成」前：`make v6-audit` **全部 ✅**（含步 7、P7 终版）

---

## 8. 硬约束与风险

**硬约束（摘自 v2/交接 HC）**：事实源 `src_frozen/` 不改；P4 冻结 K 卡；覆盖三层口径；说话人纪律；锚点校验；`spec/` 变更须用户裁决。

**风险**：

| 风险 | 缓解 |
|------|------|
| 上下文压缩丢信息 | 以仓库与 `make v6-roll-forward` 为准，不信对话摘要 |
| 代签冒充人工过关 | 仅 `user_signoff_authorization.txt` + apply |
| verify_pack 红 | 改文件后 **先 make pack** |
| SG3 划重点无承接 ~66% | 已文档化，非 PASS 口径 |
| 双机 V6 快照与现况不符 | 以本文 §2 与 gate_matrix 为准 |

---

## 9. 关键路径索引

| 用途 | 路径 |
|------|------|
| 一页状态 | `logs/WJ-OS_V6_status_for_user_20261026.md` |
| 闸门矩阵 | `logs/WJ-OS_V6_gate_matrix_20261026.md` |
| P6/P7 缺口 | `logs/p6_p7_remaining_audit_20261026.md` |
| M3 题面 | `logs/m3_trial_feedback_20261026.md` |
| 签收清单 | `logs/p6_user_signoff_checklist_20261026.md` |
| 决策日志 | `logs/ai_decisions/WJ-OS_decision_log.md`（至 D-WJ-021+） |
| Agent 规则 | `AGENTS.md`、`state/agent_preferences.md` |

---

## 10. 复水测验（开工前自答，十题全对才可动手）

> 与 V5 §9 / V6 §8.1 同颗粒度，内容针对 **P5–P7 单 Cursor 主 Agent**。答卷写入首条回复；**错一题不得**改签收正式表、`user-signoff-apply`、或宣称 gate 过关。答错回读本文 §1–§9 与 `spec/quiz.md` 后重答。  
> 可选加深（EP/ST-1）：`spec/quiz.md` 题库抽 12 题 ≥11 正确。

**题目**

1. 本 Cursor 窗口有几个**主 Agent**？能否按 V5/V6 **双机两主 Agent** 同时 `git push` 收编？
2. 当前**阶段坐标**（P4 之后）？**首要阻塞**是什么？
3. P4 冻结后能否**默认**改 `data/cards/`？若必须改，走什么流程？
4. Gate-P5 **步 11** 过关产物文件名？缺什么不得标步 11 ✅？
5. `make user-signoff-apply` 的前置授权是什么？能否用 Agent 草稿列冒充 P6 **终签**？
6. 工程绿链**一键命令**？改 tracked 文件后**必先**执行？
7. 对外宣称「V6 整体完成」前必跑什么？未完成时 **exit 1** 是否一定代表工程坏了？
8. 列出至少 **3 项**本阶段**禁写**路径。
9. 子代理**禁止**使用的模型 slug？
10. `make p6-subset` 全绿能否替代 P6 **步 7/10/11 人工签收**？GATE-D 后全库 K 卡约多少张？

**答案键**（自答后对照；勿在首答前偷看）

1. **仅 1 个**主 Agent（§1.5）；**不能**双主 Agent 并行 push；Task 子代理≠第二主会话。  
2. **P5 步 11 M3 🔄** 为主阻塞；P6 人工签收、P7 终版 🔄（§2）。  
3. **不能**默认改；须用户明确 **P4 解冻**流程（§1.3）。  
4. `logs/m3_user_signoff_record.md`；无 `M3-确认`/授权文件不得 ✅（§5.1）。  
5. `logs/user_signoff_authorization.txt` 或用户聊天 **exact** 授权句 + 明示执行 apply；**不能**冒充终签（§1.2）。  
6. `make v6-engineering`；**先 `make pack`**（§6）。  
7. `make v6-audit` 逐项 ✅；exit 1 在未完工时 **为预期**（§6）。  
8. 例：`src_frozen/`、`data/cards/`（冻结）、`data/gold/`、`logs/g6.md`（§1.3、开场禁写表）。  
9. **`composer-2.5-fast`**（`state/agent_preferences.md`）。  
10. **不能**替代人工签收；约 **9019** 张、GATE-D **0 FAIL**（§2.1）。

---

## 11. 文档沿革（简）

自 V6 双 Agent 收口以来：**单 Cursor 主 Agent** 续 P5–P7；冷启动与复水以 **§4 + §10** 为准；历史 V4/V5/V6 执行期文档**仅考古**。细节修订不再逐条罗列——以 git 历史为准。

---

## 12. 新窗口开场提示词（一键复制）

**唯一正文文件**（禁止在本文 §12 再贴第二份副本，避免漂移）：

`handover/WJ-OS｜新窗口开场提示词V7.md`

复制方法：打开该文件，从 `--- 开场提示词开始 ---` 到 `--- 开场提示词结束 ---` 之间**整段**粘贴为新 Cursor 窗口第一条消息（含 `/goal` 行）。

维护：改冷启动步骤时 **先改 §4 表**，再改上述文件「第一步」与根目录 **`AGENTS.md`**，最后 `git commit` + `push`。

---

*文档结束。*
