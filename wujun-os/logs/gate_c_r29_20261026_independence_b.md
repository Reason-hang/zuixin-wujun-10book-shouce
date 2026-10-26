# GATE-C r29 盲抽独立性声明（B 窗口，extractor GAUD31）

## 声明

本次对 FZ-U0007、GG-U0013、GG-U0119 三个单元的抽取，**没有读取**以下被 D-31 禁止的来源：

- 这三个单元现有的生产论点卡；
- `data/gold/` 下的任何文件；
- 此前 `logs/gate_c_*` 下的任何卡文件（含 r9、r9b 等历史批次的 attr/strict/self 报告）；
- `/tmp/b_r29_first_all` 下的 REF 文件。

没有对上述路径做过读取、列目录或检索。操作中只列过 `logs/` 的目录名，没有打开其中任何文件，也没有用 `rg` 扫描过 `data/` 或 `logs/` 的内容。

## 实际读取的来源

| 类别 | 文件 |
|---|---|
| 原书（冻结，只读） | 富足 179–232 行；谷歌方法论 1066–1118、7987–8040 行 |
| 规则与字典 | `spec/rules_v0.9.md`、`spec/exclusions.yaml`（前 80 行）、`spec/v2_方案.md` 中支柱字典片段（D03/D04/D05/D06/D08/D09/D10 定义） |
| 工具 | `scripts/card_writer.py`、`scripts/verify_cards.py`；`rg` 搜索只在 `spec/`、`prompts/`、`scripts/` 内查关键词（`concept_key` 等） |
| 文档 | `prompts/R-EXT-P3工单模板.md` 仅在搜索结果中显示了片段，没有整份读取 |

没有读取 `data/rules/concept_keys.csv`，概念键均由抽取者按吴军概括自行命名。

## 产出

- 输出目录：`logs/gate_c_r29_20261026_cards_b/`
- FZ-U0007：10 卡；GG-U0013：8 卡；GG-U0119：9 卡，共 27 卡，均在 REF±2 指引范围内。
- `verify_cards` 自检：27 张，0 FAIL，结论 PASS（`logs/gate_c_r29_20261026_verify_self_b.md`）。

## 过程中发现的工具口径冲突（如实记录）

`card_writer.py` 的 speaker 校验用前缀 `史实·`，而 `verify_cards.py` 只接受精确值 `史实`，二者互斥，导致 speaker 为"史实"的卡无法同时通过两道校验。本次案例类卡（乔布斯、莱特兄弟、Zoom、L 君）统一用 `吴军本人` + `E3`，没有改动工具。

## 未执行事项

- 未使用 git，未改动 `state/`、`state.json`，只写入指定的 `logs/gate_c_r29_20261026_*` 路径。
