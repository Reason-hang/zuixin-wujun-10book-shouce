# WJ-OS｜双机并行执行期接手｜项目交接文档 V5

> 版本：V5（2026-10-26，基于 V4+J-143 暂停检查点）
> 权威入口优先级：本文档 > state/state_{sg3,sg1}.json > state/journal_{sg3,sg1}.md > 本文件引用的一切凭证
> 适用对象：Agent-A（SG3 线）与 Agent-B（SG1 线），两台不同电脑、两个不同模型、并行执行

---

## 0. 项目一句话与当前快照

把吴军 10 本书（5,038,558 汉字、1,742 单元、108 批）抽成带锚点的论点卡，最终成手册。服务跨境电商供应链 B 端产品经理，重点 D06 职场/D01 认知/D02 成长。

**J-143 暂停点快照**：六书（FZ/GG/GJ/JJ/JS/SX/TD）+WJ2 已完成；P3b 55/86 批；单元 1,283/1,742（73.7%）；汉字 3,724,376/5,038,558（73.9%）；累计卡 ~5,800 全部官方 verify 0 FAIL；GATE-C r2~r21 共 19 轮无漂移（D-41a 新口径 r18~r21 四连绿）。

## 1. 双 Agent 分工总则（R3 工作完全分开）

| | Agent-A（SG3 线） | Agent-B（SG1 线） |
|---|---|---|
| 负责批次 | B-055~065 共 11 批（B-055 在途） | B-005~020 共 16 批 |
| 原书 | 《硅谷来信3》（src_frozen/《硅谷来信3》｜…副本.md） | 《硅谷来信1》（src_frozen/《硅谷来信1》｜…副本.md） |
| 写目录 | data/cards/T-P3b-B-055~065/ | data/cards/T-P3b-B-005~020/ |
| uc 回写 | data/unitcards/**uc_SG3.jsonl** | data/unitcards/**uc_SG1.jsonl** |
| journal | state/**journal_sg3.md**（编号 JS-001 起） | state/**journal_sg1.md**（编号 JS1-001 起） |
| state | state/**state_sg3.json** | state/**state_sg1.json** |
| 单书验收 | SG3 23/23 → SG3 验收 | SG1 20/20 → SG1 验收（+107 段双出处核对+800 字锚回补清单） |
| 暂存前缀 | /tmp/a_/ | /tmp/b_/ |

**写集合完全不相交**——这是零冲突的根基。两 Agent 严禁写：对方的目录/uc/journal/state、state/journal.md（总账本，冻结至 J-143）、state/state.json（暂停点快照）、spec/ 全部、logs/g6.md（107 段簇表）、data/gold/（黄金单元历史）、src_frozen/。

## 2. git 协作协议（R4 持续提交 + R5 零冲突）

1. 同一仓库同一 main 分支（策略已定，见 V5 方案对比：同 main+pull --rebase 优于双分支/双仓库）。
2. **每次推送前必须 pull --rebase**：`git pull --rebase origin main && git push`——batch_publish.py 已内置。
3. 若 rebase 冲突（理论上不会发生）：`git rebase --abort`，等 5 分钟对方推完再重试；绝不手工改对方文件。
4. 提交信息格式：`feat: {线}{批}收编{N}卡0FAIL（J-xxx）`，如 `feat: SG3⑫ B-055收编64卡0FAIL（JS-001）`。
5. 遗漏推送=违规：每批收编即推送，不积压。

## 3. 标准流水线五步（R6 流程和步骤——每批固定执行）

```
①派单  T7 batch_brief.py   python3 scripts/batch_brief.py T-P3x-B-0XX {代号} > /tmp/{前缀}_brief.md
        （SG1 批自动附 g6.md 双出处护栏；派单全文即子代理提示词）
②预检  T1 anchor_aid.py    sha 子命令取锚 SHA1；check 子命令预检 quote/指纹词
③写盘  T2 card_writer.py   卡片 JSON 管道传入（不含 sha1/claim_id），断言前置+防覆盖
④收尾  T3 batch_finish.py  python3 scripts/batch_finish.py T-P3b-B-0XX data/cards/T-P3b-B-0XX \
                            data/unitcards/uc_{书码}.jsonl --out logs/cards_verify_…md
                            （verify 0 FAIL 才回写；统计+JOURNAL素材行现算）
⑤发布  T6 batch_publish.py python3 scripts/batch_publish.py T-P3b-B-0XX data/cards/T-P3b-B-0XX \
                            data/unitcards/uc_{书码}.jsonl JS-0NN \
                            --journal-file state/journal_{线}.md --state-file state/state_{线}.json \
                            --title "…" --themes "…" [--extra "…"]
                            （journal 追加+state 刷新+pack+commit+pull --rebase+push 一条龙）
```

抽取执行者：各线主 Agent 派**子代理**抽取（派单即 T7 产物），主 Agent 只做审查+收编+发布；子代理阵亡（限流）→ 断点续跑（已写盘文件保留）或主 Agent inline 兜底（D-32）。

## 4. 提速工具清单（R6 使用的提速工具——6 件全在役）

| # | 工具 | 环节 | 要点 |
|---|---|---|---|
| T7 | scripts/batch_brief.py | 派单 | 行窗表现算（杜绝手抄错）；SG1 批自动附 g6.md 双出处护栏 |
| T1 | scripts/anchor_aid.py | 预检 | sha/check 双子命令；指纹词逐字锚内校验 |
| T2 | scripts/card_writer.py | 写盘 | JSON 管道传入；SHA1 重算；多错全量报告；--dry-run |
| T3 | scripts/batch_finish.py | 收尾 | verify 0 FAIL 才回写；uc 回写幂等；统计/JOURNAL 素材现算 |
| T6 | scripts/batch_publish.py | 发布 | **V5 新增 --journal-file/--state-file 参数（必须传本线的！）**+推送前自动 pull --rebase |
| T11 | scripts/sg1_dedup_probe.py | SG1 验收抽查 | 文字级重复探针（15 段存档 data/rules/sg1_gg_dupes.json） |

质量红线工具（禁止使用）：说话人自动分类、claim 自动生成——触碰 HC 红线一票否决。

## 5. 各阶段验收（R6 每个阶段后续的验收）

### 5.1 每批验收（GATE-B，两线相同）
- 官方 `verify_cards.py` 0 FAIL（SHA1 复算/行窗⊆/锚≤800/quote≤15 锚内子串/指纹≤3 锚内/claim≤60/枚举全检）
- 处置 100%：每单元 unit_disposal 必填 + x_disposals 记 X 子类；uc 回写覆盖 100%
- HC 红线抽查：名人转述=E2+speaker"转述·第三方"+notes 注被转述者；读者发言不得 E1

### 5.2 GATE-C 盲抽（每全局满 3 批一轮）
- 触发计数按**全局批次**（两线合计）：A 线收编后查 `ls logs/ | grep -o 'gate_c_r[0-9]*' | sort -V | tail -1` 得最大轮号，再数全局已完成批数÷3 决定是否触发
- 轮号全局递增，派单前查重（两线可能同时触发——后触发者跳过，由先到者覆盖；各自 journal 留痕）
- 黄金三单元与卡数指引（D-41a 口径：REF±2）：FZ-U0007 7~11、GG-U0013 5~9、GG-U0119 6~10（行窗见 logs/gate_c_* 历史）
- 验收：官方 verify 0 FAIL + s14 attr 三分量与目录级全 ≥0.7（strict 记录不判）+ 独立性声明
- 盲抽代理由各线自行派（代号自取 GAUD-XX 序列），**独立性红线**：禁读三单元已有卡与 logs/gate_c_* 历史

### 5.3 单书验收（各线完成后）
- `book_coverage.py --book {SG3|SG1}`：处置未落值 0 → PASS
- ck_registry 刷新（`ck_registry.py`，两线都完成后由先完成者执行一次即可，后完成者再刷新一次）
- SG1 专项：①107 段双出处 100% 登记（对照 logs/g6.md 簇表+各批派单护栏）②800 字锚受限行号清单移交 P4 ③T11 探针抽查
- 说话人纪律：转述·第三方名单 vs E2 卡数一致性抽查

### 5.4 GATE-D 收口（两线都完成后，任一 Agent 执行）
- 全库 1,742 单元处置未落值 0；107 段覆盖去重统计；全量 verify 复验（零污染确认）；GATE-C 总复盘

### 5.5 P4~P7（V5 定原则）
- P4 概念键归一：双 Agent 按柱码分片（如 A=D01~D05、B=D06~D10）+ 模糊点清单裁决（清单分散在各批 J 行与 gate_c_*_self.md，汇总待做）；用户 5 项待确认事项（移民 X8/科学定律 E1E2/GG-U0013 严口径/U0175/婚恋 X5）按既有口径继续不阻塞
- P5 成稿（M3）→P6 审计（M4）→P7 交付：细节届时由用户主会话另发工单，P5 估 43~140 轮是最大不确定项

## 6. 恢复流程（新 Agent 复水，§9 测验前不得开工）

1. 读本文档全文；2. 读本线 state_{线}.json（phase/in_flight/next_ticket）；3. 读本线 journal_{线}.md 尾部 10 条+总账本 state/journal.md 的 J-120~J-143；4. 抽查 2 张本线已收编卡（对原书复核锚点）；5. 跑 `make status`；6. 通过 §9 测验后领 next_ticket 开工。

## 7. 纪律与红线（违反即停）

HC-01 冻结只读；HC-10 说话人先行；HC-12 无锚不写；HC-21 数字脚本产生；D-31 主 Agent 禁任 GATE-C 盲抽者；D-32 代理阵亡主 inline 兜底合法；D-41a GATE-C 卡数指引=REF±2、通过线 attr≥0.7 不变；/tmp 自家前缀隔离（J-140 教训）；文档命名规范（全角竖线）；历史记录只增不改。

## 8. 风险与预案（V5 方案对比遗留）

| 风险 | 预案 |
|---|---|
| push 冲突 | pull --rebase 已内置；冲突则 abort 等 5 分钟重试 |
| GATE-C 撞号 | 派前查 logs 最大轮号 |
| 限流杀代理 | 断点续跑/主 inline 兜底；两机独立重试 |
| 两模型口径漂移 | card_writer 断言+各线 GATE-C+P4 统一裁决 |
| pack 覆盖 | pack 是快照非权威，git 为权威 |
| B-055 在途跨暂停 | 恢复后查 data/cards/T-P3b-B-055/ 已写盘数，缺单元续抽 |

## 9. 复水测验（开工前自答，答错重读）

①两线各自负责哪些批号？②uc 回写文件名？③journal/state 文件名与编号前缀？④publish 命令必须带哪两个 V5 新参数？⑤推送前必须执行什么 git 操作？⑥GATE-C 触发计数按什么口径？轮号如何防撞？⑦SG1 验收比 SG3 多哪两项？⑧哪些目录/文件绝对禁写？⑨卡数指引 FZ/GG13/GG119 各是多少、通过线是多少？⑩子代理阵亡的两种处置？

## 10. 权威凭证索引

- 总账本：state/journal.md（J-001~J-143，冻结）
- 线账本：state/journal_sg3.md（JS-xxx）、state/journal_sg1.md（JS1-xxx）
- 暂停快照：state/state.json（J-143）；线状态：state/state_sg3.json、state/state_sg1.json
- 规则：spec/rules_v0.9.md（冻结）、spec/pillars.yaml、spec/exclusions.yaml、spec/boundary_rules.md
- 行窗表：logs/batch_windows_pending_20261025.md（36 批预生成）；重复簇表：logs/g6.md（107 段）
- 历史交接：handover/WJ-OS｜执行期接手｜项目交接文档V4.md（V5 的基础，V4 时代流程细节仍在其中有效）
- 决策记录：state/decisions.md（D-21~D-41a）
