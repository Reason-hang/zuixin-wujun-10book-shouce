# P4 步 12 执行手册（待用户签字后一键跑）

## 触发条件（须同时满足）

1. `logs/p4_step11_user_spotcheck_20.csv` 已填 `user_verdict`（或用户聊天授权「采纳提议稿」并已复制到该文件）。
2. 用户已回复 **「确认骨架」**（步 13）；在 `logs/p4_step13_dictionary_change_report_20261026.md` 顶部追加一行：`user_confirmed_skeleton: yes @ <ISO时间>`。

## 命令（cwd = `wujun-os/wujun-os`）

```bash
python3 scripts/s17_k_card_freeze_manifest.py
wc -l state/p4_k_card_freeze_manifest.sha256
make test
```

## 记账

- `state/journal_sg1.md` 增 **JS1-0xx**：P4 步 12 K 卡冻结完成，`card_files` 与 GATE-D 9019 对齐复核。
- `state/p4_workboard.md` 步 12 → ✅。

## 禁止

- 冻结后**不得**批量改 `data/cards/**` JSON；变更须 CHG + 解冻流程（待 spec 附录固化）。
