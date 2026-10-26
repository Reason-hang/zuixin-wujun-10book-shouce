# WJ-OS V6 一页状态（给你）

> 工程 Agent 续作快照；**不等于** V6 已全部完成。

## 已过（有命令/日志）

| 里程碑 | 你怎么验 |
|--------|----------|
| SG1 + GATE-D + P4 冻结 | `journal_sg1`、9019 卡 0 FAIL |
| P5 脚本 AC（除 M3） | `make v6-engineering`（含 test + p6-subset + 对抗/P7 预检） |
| G10① 关键词 | `logs/g10_kw.md` |
| G10③ 划重点 | `logs/g10_sg3_highlight_recall.md`（含无承接表 ~66%） |
| 锚点 8950 | `make verify-anchors` |
| 单元处置 1742 | `make d3-export` → 锚点/单元/论点卡/X 排除子表 |
| P6 抽查表 | `make p6-spotcheck-v20` → `out/覆盖与质检报告/P6_用户抽查20张_草稿.md` |

## P5 步 11（M3）

你已提交深度反馈；工程已出 **v0.9.1 题面** + [`m3_user_feedback_requirements_20261026.md`](m3_user_feedback_requirements_20261026.md)。Q2 方向：**D07 阶段 1 初稿**——沟通簇索引（`make d07-comm-index`）、场景 **S-129~131**、章首度量表（见 `D07_沟通专题_路线图_草稿.md`）。

请阅改版 [`m3_trial_feedback_20261026.md`](m3_trial_feedback_20261026.md)。**方式 A** 聊天发两行；**方式 B** 复制 [`user_signoff_example.txt`](user_signoff_example.txt) → `logs/user_signoff_authorization.txt` → `make user-signoff-apply`：

```text
M3-确认：接受 v0.9.1 题面改版；三题均部分，判定见 m3_trial_feedback 表。
P6-代签：AC36,G10,SPOTCHECK20
```

v2 步 11「3 个真实问题」与 M3 关系见 [`p6_step11_v2_requirements_gap_20261026.md`](p6_step11_v2_requirements_gap_20261026.md)。

## 完成审计矩阵

[`logs/WJ-OS_V6_gate_matrix_20261026.md`](WJ-OS_V6_gate_matrix_20261026.md) — SG1/GATE-D/P4~P7 逐项证据（**V6 未完成**）。  
自动汇总：`make v6-audit` → [`v6_completion_audit_latest.md`](v6_completion_audit_latest.md)（未完成时 exit 1，属预期）。

## 签收进度（数字）

[`logs/p6_step_status_latest.md`](p6_step_status_latest.md) — `make p6-step-status`（M3 0/1 · AC36 0/135 · G10 0/20 · 抽查 0/20）。

## 签收入口（一页）

[`logs/p6_user_signoff_checklist_20261026.md`](p6_user_signoff_checklist_20261026.md) — M3、AC-3.6（含 **24 条优先包**）、G10②、场景演练、20 张抽查。

## 仍未做（勿误以为已完工）

- 明细清单：`logs/p6_p7_remaining_audit_20261026.md`
- **P0 链**已 `make p0` 重跑（G2–G8 PASS，见 `G0_G9_日志索引.md`）；仍缺 G9 全闭环签字、AC-3.6 语义回读、G10② 填表、20 张判断列
- **P7** D1–D6 终版命名与打包
- v2 **★2** 等（见 `logs/user_open_questions_20261026.md`）

## 本地自检

```bash
cd wujun-os && make test && make p6-subset
```
