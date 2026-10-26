# P5/P6 用户签收清单（一页）

> 工程侧 `make p6-subset` 可绿；**下列项缺一不得标 P5 步 11 / P6 / P7 终版**。

## P5 步 11（M3）

```text
M3-确认：接受 v0.9.1 题面改版；三题均部分，判定见 m3_trial_feedback 表。
```

代签 P6 列（可选第二行）→ `make user-signoff-apply` 将灌入 **AC36 135 / G10 20 / 抽查 20** 格（启发式与 Agent 草稿，**仍须你知悉授权**）。

**可选一键代签**（把上句 + 下行写入 `logs/user_signoff_authorization.txt` 后 `make user-signoff-apply`）：

```text
P6-代签：AC36,G10,SPOTCHECK20
```

模板：`logs/user_signoff_authorization_TEMPLATE.txt`

## P6 步 3（AC-3.6）

| 动作 | 文件 |
|------|------|
| 优先回读 24 条 | `logs/ac36_low_ngram_review_pack_20261026.md`（含 Agent 草稿判定） |
| 全量 135 条填「回读召回」 | `out/覆盖与质检报告/AC36_抽检召回表_草稿.md` |
| 可选对照 | `logs/ac36_recall_agent_draft_column_20261026.md` |

## P6 G10②

| 动作 | 文件 |
|------|------|
| 20 行填「漏收核心论点？」 | `G10②_盲抽单元表_草稿.md`（摘录列为**正文**前 100 字，D-WJ-018） |

## P6 步 7

| 动作 | 文件 |
|------|------|
| 五类场景是否走通 | `logs/p6_scene_drill_log_20261026.md`（将 🔄 改为 ✅ 或写异常） |

## P6 步 11

| 动作 | 文件 |
|------|------|
| 20 张判断列 | `out/覆盖与质检报告/P6_用户抽查20张_草稿.md` |
| Agent 草稿对照 | `make p6-spotcheck-agent` → `logs/p6_spotcheck_agent_draft_20261026.md`（20/20 锚点 PASS；**V-14** `C-JJ-UU0023-01` 双 U 笔误待 P6 记模糊点） |

## 一键工程自检

```bash
make test && make p6-subset && make p6-adversarial-preflight && make p6-step-status
```

进度条：`logs/p6_step_status_latest.md`
