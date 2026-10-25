# WJ-OS｜双机并行执行期接手｜项目交接文档 V5

> 版本：V5（2026-10-26，基于 V4+J-143 暂停检查点）
> 权威入口优先级：本文档 > state/state_{sg3,sg1}.json > state/journal_{sg3,sg1}.md > 本文件引用的一切凭证
> 适用对象：Agent-A（SG3 线）与 Agent-B（SG1 线），两台不同电脑、两个不同模型、并行执行

---

## 0. 项目一句话与当前快照

把吴军 10 本书（5,038,558 汉字、1,742 单元、108 批）抽成带锚点的论点卡，最终成手册。服务跨境电商供应链 B 端产品经理，重点 D06 职场/D01 认知/D02 成长。

**J-143 暂停点快照**：六书（FZ/GG/GJ/JJ/JS/SX/TD）+WJ2 已完成；P3b 55/86 批；单元 1,283/1,742（73.7%）；汉字 3,724,376/5,038,558（73.9%）；累计卡 **6,599**（脚本实数：FZ 234/GG 1758/GJ 406/JJ 243/JS 389/SG1 347/SG3 970/SX 367/TD 218/WJ2 1667）全部官方 verify 0 FAIL；GATE-C r2~r22 共 20 轮无漂移（D-41a 新口径 r18~r22 五连绿）；另有 J-146 收编 B-055、J-140~147 为暂停前后闭环记录。

## 1. 双 Agent 分工总则（R3 工作完全分开）

| | Agent-A（SG3 线） | Agent-B（SG1 线） |
|---|---|---|
| 负责批次 | B-056~065 共 10 批（B-055 已于 J-146 收编） | B-005~020 共 16 批 |
| 原书 | 《硅谷来信3》（src_frozen/《硅谷来信3》｜…副本.md） | 《硅谷来信1》（src_frozen/《硅谷来信1》｜…副本.md） |
| 写目录 | data/cards/T-P3b-B-056~065/ | data/cards/T-P3b-B-005~020/ |
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
6. **push 冲突实战首报制度**：若 pull --rebase 真发生冲突（理论上写集合不相交不会发生），除 abort 重试外，必须在本线 journal 记录冲突文件与原因，并更新本文档 §8——首例冲突即触发零冲突设计复核。

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
| T11 | scripts/sg1_dedup_probe.py | SG1 验收抽查 | 逐字滑窗探针，实测 15 段存档 data/rules/sg1_gg_dupes.json；**口径注意**：g6.md 107 段为 P1 主题级口径（含改写），双出处登记以 g6.md 为准，T11 仅作逐字级补充抽查，两表不互替 |

质量红线工具（禁止使用）：说话人自动分类、claim 自动生成——触碰 HC 红线一票否决。

## 5. 各阶段验收（R6 每个阶段后续的验收）

### 5.1 每批验收（GATE-B，两线相同）
- 官方 `verify_cards.py` 0 FAIL（SHA1 复算/行窗⊆/锚≤800/quote≤15 锚内子串/指纹≤3 锚内/claim≤60/枚举全检）
- 处置 100%：每单元 unit_disposal 必填 + x_disposals 记 X 子类；uc 回写覆盖 100%
- HC 红线抽查：名人转述=E2+speaker"转述·第三方"+notes 注被转述者；读者发言不得 E1

### 5.2 GATE-C 盲抽（每全局满 3 批一轮）
- **触发判断前必先 `git pull`**：全局批数=本线+对方线已收编（对方进度只在其 journal/state，不 pull 就漏算）
- 黄金三单元行窗（写死勿查历史）：FZ-U0007=《富足…》179-232｜GG-U0013=《谷歌方法论…》1066-1118｜GG-U0119=同书 7987-8040
- GATE-C 轮次验收记录记入**触发线**的 journal
- 触发计数按**全局批次**（两线合计）：A 线收编后查 `ls logs/ | grep -o 'gate_c_r[0-9]*' | sort -V | tail -1` 得最大轮号，再数全局已完成批数÷3 决定是否触发
- 轮号全局递增，派单前查重（两线可能同时触发——后触发者跳过，由先到者覆盖；各自 journal 留痕）
- 黄金三单元与卡数指引（D-41a 口径：REF±2）：FZ-U0007 7~11、GG-U0013 5~9、GG-U0119 6~10（行窗见 logs/gate_c_* 历史）
- 验收：官方 verify 0 FAIL + s14 attr 三分量与目录级全 ≥0.7（strict 记录不判）+ 独立性声明
- 盲抽代理由各线自行派（代号自取 GAUD-XX 序列），**独立性红线**：禁读三单元已有卡与 logs/gate_c_* 历史

### 5.3 单书验收（各线完成后）
- `book_coverage.py --book {SG3|SG1}`：处置未落值 0 → PASS
- ck_registry 刷新（`ck_registry.py`）：各线单书验收后各刷新一次（幂等），GATE-D 后终刷
- **模糊点汇总（各线单书验收时必做）**：本线全部模糊点（各批 J 行+gate_c_*_self.md 自报）汇总为 `state/模糊点_SG3.md` / `state/模糊点_SG1.md` 移交 P4——不汇总=P4 备料缺失
- SG1 专项：①107 段双出处 100% 登记（对照 logs/g6.md 簇表+各批派单护栏）②800 字锚受限行号清单移交 P4 ③T11 探针抽查
- 说话人纪律：转述·第三方名单 vs E2 卡数一致性抽查

### 5.4 GATE-D 收口（两线都完成后，任一 Agent 执行）
- **跨机完成标记**：各线单书验收 PASS 后在本线 journal 写"SGX 验收 PASS"并推送；GATE-D 执行者先 `git pull` 确认两线标记齐全再执行
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
| **限流若按账号全局计**（两机同账号→互相杀对方代理）【待验证假设 A1】 | 双机收益归零的翻盘条件：首周观察两机代理存活率，若显著低于单机历史（约 80%+），改分时错峰（A 白班/B 夜班）并回写本表 |
| 两模型口径漂移 | card_writer 断言+各线 GATE-C+P4 统一裁决 |
| pack 覆盖 | pack 是快照非权威，git 为权威 |
| B-055 在途跨暂停 | 恢复后查 data/cards/T-P3b-B-055/ 已写盘数，缺单元续抽 |

## 9. 复水测验（开工前自答，答错重读）

①两线各自负责哪些批号？②uc 回写文件名？③journal/state 文件名与编号前缀？④publish 命令必须带哪两个 V5 新参数？⑤推送前必须执行什么 git 操作？⑥GATE-C 触发计数按什么口径？轮号如何防撞？⑦SG1 验收比 SG3 多哪两项？⑧哪些目录/文件绝对禁写？⑨卡数指引 FZ/GG13/GG119 各是多少、通过线是多少？⑩子代理阵亡的两种处置？

**答案键（自答后对照，每题 30 秒内答出为合格）**：
①A=B-056~065、B=B-005~020（§1）；②A=uc_SG3.jsonl、B=uc_SG1.jsonl（§1）；③A=journal_sg3.md/JS-xxx+state_sg3.json、B=journal_sg1.md/JS1-xxx+state_sg1.json（§1）；④--journal-file 与 --state-file（§3 步⑤）；⑤git pull --rebase origin main（§2 条 2，publish 已内置）；⑥全局两线合计每满 3 批一轮、派单前查 logs 最大 gate_c_r 轮号、触发判断前必先 pull（§5.2）；⑦107 段双出处 100% 登记（对照 g6.md）+800 字锚受限行号清单移交 P4（§5.3）；⑧对方线的 cards/uc/journal/state、state/journal.md 总账本、state.json 快照、spec/ 全部、logs/g6.md、data/gold/、src_frozen/（§1）；⑨FZ 7~11、GG13 5~9、GG119 6~10（REF±2），通过线 attr≥0.7（§5.2）；⑩断点续跑（保留已写盘文件）或主 Agent inline 兜底（D-32）（§3）。

## 10. 权威凭证索引

- 总账本：state/journal.md（J-001~J-143，冻结）
- 线账本：state/journal_sg3.md（JS-xxx）、state/journal_sg1.md（JS1-xxx）
- 暂停快照：state/state.json（J-143）；线状态：state/state_sg3.json、state/state_sg1.json
- 规则：spec/rules_v0.9.md（冻结）、spec/pillars.yaml、spec/exclusions.yaml、spec/boundary_rules.md
- 行窗表：logs/batch_windows_pending_20261025.md（36 批预生成）；重复簇表：logs/g6.md（107 段）
- 历史交接：handover/WJ-OS｜执行期接手｜项目交接文档V4.md（V5 的基础，V4 时代流程细节仍在其中有效）
- 决策记录：state/decisions.md（D-21~D-41a）

## 11. 对抗式审查记录（2026-10-26，V5-R1 修订依据）

**六问结论**（完整分析见当日主会话）：
1. **最没把握且已核实的事**：①batch_publish 参数化未实测——实测抓获 2 个真 bug（journal 日期硬编码 2026-10-25、units_done 按全库 uc 统计而非本线 uc——分线 state 会被写全局数），均已修复并夹具复测通过；②"零冲突"是纸面推导未经双机实测——已写入 §2 条 6 实战首报制度；③V5 初版快照"~5,800 卡"是**文件数口径错误**（1,260 个 JSON 文件），精确卡数 6,599（§0 已改）；④V4 文件名引用已核实非死链。
2. **双方最大遗漏**：用户侧——限流若按账号全局计则两机互相杀代理（比 git 冲突更致命，§8 已加预案）；GATE-C 全局计数依赖对方 logs 但原流程没要求先 pull（§5.2 已补）。我侧——publish 未测就上产线；V5 快照数字未核实；GATE-D 完成标记的跨机协调缺失（§5.4 补：单书验收 PASS 后在本线 journal 写"SGX 验收 PASS"标记并推送，GATE-D 执行者先 pull 确认两线标记齐全）。
3. **未明说假设（翻盘点）**：A1 限流按机器级独立（若按账号级→双机收益归零，§8 预案）；A2 新模型抽卡质量过闸（若连续掉线→该线回退已验证模型）；A3 写集合纪律纯文字无技术强制（若误写→污染清洗，§1 红线+J-140 /tmp 事件前车之鉴）。
4. **事实成立即作废（杀伤力排序）**：F1 平台限流按账号全局计算且额度不足→双机方案整段作废退分时制；F2 任一线模型连续无法通过 GATE-B/C→该线返工换模型；F3 main 历史被外部改写→rebase 协议失效改双分支。
5. **三个月后失效最可能原因**：双线设计只覆盖 P3b 抽取+收口，进入 P4/P5（语义耦合的全局工作）后分工失效而未出新设计，文档被弃用；次因=模糊点积压无人裁决致 P4 卡死（§5.3 已强制各线验收时汇总）。
6. **五角度攻击核实结果**：逻辑漏洞（零冲突未验证→已实测）；事实错误（卡数口径/B-055 状态过时→已改）；边界遗漏（GATE-C 触发先 pull/答案键/模糊点汇总→已补）；假设失效（A1~A3→已入 §8/§11）；过度设计（分线 state 的 progress.units_done 全局数误导→publish 已改按本线 uc 统计）。

**实测事故实录（J-148 同日）**：夹具测试 publish 时 git 阻断逻辑失效，假测试提交 JS-TEST2 被推上远端 main（3517f1c）——立即 `git revert`（8463f4f），但 revert 误伤回滚了混在同一提交里的 publish 真修复，随即重新应用（8938a1d）。教训：**测试任何会触发 git 写操作的代码，必须在隔离 clone 里做，不在主仓直接跑**；工具实测必须先审查其全部副作用命令。
