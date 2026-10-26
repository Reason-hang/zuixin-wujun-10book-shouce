# AGENTS.md（WJ-OS 给任何 AI Agent 的入口）

## 权威文档（冲突时优先级）

| 优先级 | 文档 | 用途 |
|--------|------|------|
| 1 | `handover/WJ-OS｜单Agent接手·P5-P7收口期｜项目交接文档V7.md` | **现行交接**；**§4 = 冷启动唯一表** |
| 2 | `handover/WJ-OS｜新窗口开场提示词V7.md` | **新窗口第一条消息**（一键复制） |
| 3 | `logs/WJ-OS_V6_gate_matrix_20261026.md`、一页状态 log | 闸门与阻塞 |
| — | `handover/…V4.md`、`V5`、`V6 A/B` | **仅考古**，勿作恢复入口 |

**阶段（2026-10-26）**：GATE-D / P4 冻结 ✅ → **P5 M3 阻塞** → P6 人工签收 → P7 草稿。画像：**国内电商 B 端 PM**。V6 用户方案**未完成**。

---

## 七步记忆 = V7 §4（A–H）

**恢复 → 核对 → 阅读 → 抽查 → 测验 → 闸门 → 复述等开始**

| 七步 | §4 | 要点 |
|------|-----|------|
| 恢复 | A | `git pull --ff-only` |
| 核对 | B,C | `make verify-pack` 或 `make restore-check`；`make v6-roll-forward` + `make status`（勿单信冻结 `state/state.json`） |
| 阅读 | D | V7 §0–§11、`constraints.md`、STATE/workboard、`journal_sg1` 尾、gate_matrix / 签收清单 |
| 抽查 | E | `p4_freeze.json` 任选 2 张 K 卡对 `src_frozen/` 核锚点+SHA1 |
| 测验 | F | V7 **§10 十题全对**；可选 `spec/quiz.md` 12≥11 |
| 闸门 | G | `make pack` → `make v6-engineering` exit 0 |
| 复述 | H | 报主 Agent/测验/阻塞/路径；**等用户「开始」或授权** |

授权后分支 **I**、红线 **J**：见 V7 §4 表。

---

## Agent 换窗 / 上下文总结 / 推送仓库前规程（用户定稿，每次必跑）

当用户要求 **总结上下文、换窗、更新开场词、或 push 前收口** 时，Agent **不得**只改聊天里的片段；须按本清单自检并落盘：

1. **唯一真相**：冷启动步骤只维护 **V7 §4 表** + **`新窗口开场提示词V7.md` 第一步** + **本文件「七步记忆」**；**禁止**在 V7 内再贴开场词全文副本。
2. **交叉核对**：§1.5 单主 Agent、§10 测验、签收路径、禁写集合 — 三处表述一致。
3. **状态页**：若阶段/阻塞变化，更新 `logs/WJ-OS_V6_status_for_user_*.md` 或用户指定的一页 log（勿宣称 gate 已过除非有命令证据）。
4. **工程**（若改了 tracked）：`make pack` → `make v6-engineering`（文档-only 提交可跳过，但 handover/脚本改动须跑）。
5. **提交**：`git add` 相关路径 → `commit` 清晰说明 → `git push origin main`。
6. **交付用户**：commit hash、改了哪些文件、一键复制路径（`新窗口开场提示词V7.md` 标记区间）、仍存在的阻塞（如 M3）。

---

## 子代理与工程命令

- **禁止** Task 子代理使用 `composer-2.5-fast`（`state/agent_preferences.md`）。
- 绿链：`make v6-engineering`；签收：`logs/user_signoff_example.txt` → `make user-signoff-apply`（须授权文件）；进度 `make p6-step-status`；总审计 `make v6-audit`（未完成 exit 1 正常）。
- 决策：`logs/ai_decisions/WJ-OS_decision_log.md`（D-WJ-xxx）。

---

## 红线摘要

完整见 `spec/constraints.md`。HC-01 事实源只读；HC-12 无锚不写；HC-21 数字脚本产生；P4 冻结不改 `data/cards/`；无 M3 授权不冒充 P5/P6 终签；子集脚本绿 ≠ P6/P7 人工签收。

---

## 嵌入式最短开场（仅当 Agent 只读本文件时）

```text
你是 WJ-OS 单 Cursor 主 Agent（非双机双主 Agent）。仓库：
/Users/lizhihang/Documents/【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os

开工前严格执行 V7 §4：恢复→核对→阅读→抽查→测验→闸门→复述等开始（详见上文「七步记忆」）。
新窗口完整提示词：handover/WJ-OS｜新窗口开场提示词V7.md（---开场提示词开始--- 至 ---结束---）。
不得凭对话摘要改仓库；§10 十题全对才可动手；等用户说「开始」或授权后再签收。
```
