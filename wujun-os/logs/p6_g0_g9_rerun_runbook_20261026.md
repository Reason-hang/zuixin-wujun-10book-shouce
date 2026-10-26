# P6 步 1｜G0–G9 全量重跑 runbook（未标完成）

> 子集闸门见 `scripts/s15_check_all.py`（verify_pack、P4 冻结、S17、K 卡校验、G10①）。**全量**须另跑下列命令并归档到 `out/覆盖与质检报告/`。

## 命令链（在 `wujun-os/` 根目录）

```bash
make verify-pack    # G0
make freeze probe   # 输入冻结探测（若 zip 未变可跳过 freeze）
make p0             # G2–G8 + D5 分母（split → check-units → s03–s08）
make export-anchors && make verify-anchors # 锚点子表（8950 行，见 logs/p6_anchor_verify_blocker_20261026.md）
python3 scripts/s13_kwscan.py --out logs/g10_kw.md   # G10①（已接入 s15 子集）
```

## 注意

- `make p0` 会重写 `data/units` 与多份 `logs/g*.md`；**不得在 P4 K 卡冻结后**用 p0 结果覆盖 `data/cards`。
- P5 M3 步 11 未完成前，仅作预备跑，不得宣称 P6 过关。
