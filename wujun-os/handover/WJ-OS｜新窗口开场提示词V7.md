# 新窗口开场提示词 V7（整段复制到第一条消息）

你是 WJ-OS 的**唯一主 Agent**（可用 ≤2 子 Agent；**禁止** `composer-2.5-fast`）。仓库：

`/Users/lizhihang/Documents/【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os`

**权威交接**：`handover/WJ-OS｜单Agent接手·P5-P7收口期｜项目交接文档V7.md`（必读全文）。历史双机档：`handover/WJ-OS｜项目交接文档V6｜A线Agent执行·收官收口期.md`、`…V6｜B线Agent执行·SG1执行期.md`。

**当前阶段（2026-10-26 核实）**：P3b+GATE-D+P4 ✅；**P5 步 11（M3）🔄**；**P6/P7 人工签收与终版 🔄**。整体 **V6 用户方案未完成**，勿宣称交付完成。

**暂停前阻塞**：无 `logs/user_signoff_authorization.txt`。用户需发 `logs/user_signoff_example.txt` 两行或说「已写授权」后你才能 `make user-signoff-apply`。

**你恢复后立刻执行**：
1. `git pull --ff-only` → `make pack` → `make v6-engineering`（必须 exit 0）
2. 读 `logs/WJ-OS_V6_status_for_user_20261026.md`、`logs/p6_user_signoff_checklist_20261026.md`
3. 若用户已授权：`make user-signoff-apply` → `make pack` → `make v6-engineering` → `make v6-audit`
4. 否则：等 M3 或按用户指示改 `logs/m3_trial_feedback_20261026.md`

**硬约束**：不改 P4 冻结 K 卡；不代签 P6 正式表；改 tracked 后先 `make pack`；决策写 `logs/ai_decisions/WJ-OS_decision_log.md`。

**自检**：`make v6-engineering` + `make p6-step-status`；完成审计 `make v6-audit`（未完成时 exit 1 正常）。

请先复述：当前阶段、下一动作、阻塞项，再开始执行。
