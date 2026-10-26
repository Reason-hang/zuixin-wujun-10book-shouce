# WJ-OS｜A线收官与全局收口期接手｜项目交接文档V6

> 版本：V6（2026-10-26，基于 V5-R1 + A 线 JS-001~018 + B 线 JS1-001~018 双机实战修订）
> 适用对象：**Agent-A（SG3 线，本机执行）**；Agent-B（SG1 线，异机异模型）参照本文 + 其线内文件
> 权威入口优先级：本文档 > state/state_{sg3,sg1}.json > state/journal_{sg3,sg1}.md > 其余一切凭证
> 历史：V1 规划期→V2/V3/V4 执行期→V5/V5-R1 双机并行期→**V6 A 线收官与全局收口期**

---

## 0. 项目一句话与 V6 快照（2026-10-26 脚本实数）

把吴军 10 本书（5,038,558 汉字、1,742 单元、108 批）抽成带锚点的论点卡，最终成手册。服务跨境电商供应链 B 端产品经理，重点 D06 职场/D01 认知/D02 成长。

- **A 线（本机）终态**：SG3《硅谷来信3》**23/23 批全部收编**，全书 319 单元 **1,825 卡**全 0 FAIL（E1×1496/E2×317/E3×12；转述·第三方 317）；**单书验收 PASS**（JS-017）；模糊点 70 条移交 `state/模糊点_SG3.md`；ck_registry 刷新 7,756 键；说话人纪律全量核查 PASS（JS-018）。**0 在途、0 悬置、0 未推**，工单清零。
- **B 线（异机）进度**：SG1《硅谷来信1》**16/20 批收编**（B-001~016，JS1-018），uc_SG1 316/390 单元；**B-017 抽取中被用户指令暂停**（71023db：9/17 单元 49 卡已写盘、card_writer 断言通过，但未跑 batch_finish/未回写 uc/未计入任何统计，**勿引用**）；B-018~020 未开。
- **GATE-C**：r2~r28 **27 轮全绿**；D-41a 新口径（REF±2 密度指引）canonical r18~r28 十一轮连绿。正轮归属：A 线 r23/r25；B 线 r24/r26/r27/r28；并发档 r24b（A）/r25b（B）/r26（A 档，B 为正轮）。
- **全库**：已收编 **8,604 卡**（6,599@J-147 + A 线 855 + B 线 1,150），另有 B-017 在途 49 卡落盘未收编（合计落盘 8,653）；单元已处置 **1,668/1,742（95.8%）**，剩余 74 单元全部在 SG1（B-017 剩 8 单元 + B-018~020）。
- **当前 HEAD**：`71023db`（SG1 线用户指令暂停备份）；远端=本地一致。

## 1. 整体方案进行到哪一步（阶段→步骤→流水线位置）

```
P1 试点 ✅ → P2 冻结/拆分 ✅ → P3a 六书+WJ2 ✅（22 批 1,857 卡）→ P3b 双机并行抽取（当前阶段）
                                                              │
   流水线五步（派单→预检→写盘→收尾→发布）：                       │
   ├─ A 线：B-043~065 共 23 批 —— 五步全部走完 ✅ + 单书验收 PASS ✅（本线闭环）
   └─ B 线：B-001~016 五步走完 ✅；B-017 卡在第③步（写盘 9/17 单元）⏸ 用户指令暂停
                                                                 │
   下一站：B-017 断点续抽 → B-018~020 → SG1 单书验收（107 段双出处+800 字锚清单+T11）
                                                                 → GATE-D 全局收口 → P4 概念键归一 → P5 成稿 → P6 审计 → P7 交付
```

- 抽取总量口径：108 批中 P3b 共 86 批（其余为 P3a 及早前批次）；A 线 10 批 + B 线 12 批均在本轮双机期完成。
- **GATE-D 触发条件尚未满足**：需两线单书验收 PASS 标记齐全（A 已立 SG3 PASS；B 未立）。B 线收完 SG1 前全局收口不可执行。

## 2. 当前暂停的手头工作（新窗口第一动作依据）

| 线 | 手头状态 | 恢复动作 |
|---|---|---|
| A 线（本机） | **无手头工作**（工单清零，等 GATE-D 前置） | pull → 查 B 线进度（journal_sg1 尾行）→ 满足则执行 GATE-D（§7.4） |
| B 线（异机） | **B-017 在途暂停**（9/17 单元写盘，用户指令 71023db） | 由 B 线断点续抽剩余 8 单元（SG1-U0324~U0331）→ 五步收编 → B-018~020 |

**新窗口 A 线决策树**：
1. `git pull` 后读 `state/journal_sg1.md` 尾行；
2. 若 SG1 20/20 且 journal_sg1 有「SG1 验收 PASS」标记 → **执行 GATE-D**（§7.4 四件事，记 JS-0xx 推送）；
3. 若 B 线仍暂停/未完成 → **不越界代做 SG1**（§3 写集合禁令），向用户简报等待；**除非用户在新窗口明确授权 A 线接管 B 线剩余批次**——届时按 §9 接管规程执行（以 B 线文件名/编号续记，不混线）；
4. 空闲期可做（经用户点头）：§10 待裁决 4 工具项修复（需授权改 scripts/）、5 项口径终裁。

## 3. 双 Agent 分工与写集合（V5 §1 延续，禁令不变）

| | Agent-A（SG3，本机） | Agent-B（SG1，异机） |
|---|---|---|
| 批次 | B-043~065（23/23 ✅） | B-001~020（16/20，B-017 在途⏸） |
| 原书 | src_frozen/《硅谷来信3》｜…副本.md | src_frozen/《硅谷来信1》｜…副本.md |
| uc 回写 | data/unitcards/uc_SG3.jsonl（319/319 ✅） | uc_SG1.jsonl（316/390） |
| journal | state/journal_sg3.md（JS-001~018） | state/journal_sg1.md（JS1-001~018） |
| state | state/state_sg3.json | state/state_sg1.json |
| /tmp 前缀 | /tmp/a_/ | /tmp/b_/ |

**共同禁写**：对方线全部文件、state/journal.md（总账本冻结至 J-149）、state/state.json（暂停快照）、spec/ 全部、logs/g6.md、data/gold/、src_frozen/、**scripts/（V6 新增：两线均不改，待主会话裁决）**。GATE-C 证据两线均归档 logs/（data/gold/ 为冻结区）。

## 4. git 协作协议（V6 实战修订版）

1. 同仓库同 main，推送前 `git pull --rebase origin main`（publish 内置）。
2. 提交格式：`feat: {线}{序}{批}收编{N}卡0FAIL（{J编号}）`；每批收编即推不积压。
3. **MANIFEST.sha256 结构性冲突（已 5 例实证，非越界）**：两线 publish 均跑 make pack 全库重算必相撞。程序化处置：`git checkout --ours MANIFEST.sha256 && git add MANIFEST.sha256 && GIT_EDITOR=true git rebase --continue` → `make pack` → `git add && git commit --amend --no-edit` → `git pull --rebase` → `git push`。
4. **发布后必须人工核验**：`git log --oneline -1` 与 `git log --oneline origin/main -1` 一致才算推上（batch_publish 管道 tail -1 吞退出码，"PUBLISH OK" 会误报——两线独立证实，见 §6 bug 清单）。
5. **GATE-C 证据线别后缀约定（r26 起生效）**：A 线文件无后缀，B 线带 `_b` 后缀（如 gate_c_r28_20261026_attr_b.md）；同轮并发时后到者让号 rXXb 归档（先上远端者为正轮），journal 补更正行（先例 JS-018）。
6. push 冲突首报制度：每例冲突在本线 journal 留痕（已记 JS-004/JS-008；B 线 JS1-002/JS1-007）。

## 5. 五步流水线与 GATE-C 验收流程

### 5.1 五步流水线（每批固定；A 线已停用——无剩余批次，B 线在用）
```
①派单 T7 batch_brief.py  python3 scripts/batch_brief.py T-P3x-B-0XX {代号} > /tmp/{前缀}_brief.md
②预检 T1 anchor_aid.py   sha/check 子命令
③写盘 T2 card_writer.py  卡片 JSON 管道传入（断言前置，报错未写盘无脏文件）
④收尾 T3 batch_finish.py verify 0 FAIL 才回写 uc；统计现算
⑤发布 T6 batch_publish.py 必带 --journal-file state/journal_{线}.md --state-file state/state_{线}.json
                          （journal+state+pack+commit+pull --rebase+push；推后人工核验 hash）
```
抽取执行者=子代理（每批一代码 EXT-SGxx；GATE-C 盲抽=GAUDxx），主智能体只审查+收编+发布；子代理阵亡→断点续跑（保留已写盘）或主 inline 兜底（D-32）；GATE-C 盲抽者禁主智能体兼任（D-31）。

### 5.2 GATE-C 验收流程（V6 修订：REF 基准写死+线别后缀+让号）
- **触发**：全局（两线合计）每满 3 批一轮；触发判断前必先 `git pull`，且**查两线 journal 最新轮号**（防并发双触发——已发生 3 组：r24/r24b、r25/r25b、r26 双档）。
- **REF 基准（V6 写死，勿再查 gate_c_r2！）**：黄金单元的**产线首批卡**共 24 卡——FZ-U0007=`data/cards/T-P3a-B-103/FZ-U0007.json`（9 卡）、GG-U0013=`data/cards/T-P3b-B-066/GG-U0013.json`（7 卡）、GG-U0119=`data/cards/T-P3b-B-073/GG-U0119.json`（8 卡）。（JS-001 曾误用 data/gold/gate_c_r2 作基准，追查历史轮首抽数 24 卡后纠正。）
- 黄金三单元行窗：FZ-U0007=《富足》179-232｜GG-U0013=《谷歌方法论》1066-1118｜GG-U0119=同书 7987-8040；卡数指引（REF±2）：FZ 7~11/GG13 5~9/GG119 6~10。
- 验收命令模板（A 线）：
  ```
  python3 scripts/verify_cards.py --dirs {盲抽目录} --out logs/gate_c_rXX_20261026_verify.md
  # 分单元 attr：s14_overlap.py --first {单单元REF暂存} --second {单单元新抽} --mode attr
  # 目录级：--first {三REF合并暂存} --second {盲抽目录} --mode attr|strict
  ```
- 通过线：官方 verify 0 FAIL + 三分量与目录级 attr 全 ≥0.7（strict 记录不判）；独立性红线=盲抽代理禁读三单元已有卡/gate_c 历史/data/gold/。
- 卡片证据归档 `logs/gate_c_rXX_20261026_cards/`（B 线 `_cards_b/`）；验收记录记触发线 journal。

## 6. 工具清单与已知 bug（6 件套全在役 + 4 项待修）

| # | 工具 | 用途 | 状态 |
|---|---|---|---|
| T7 | batch_brief.py | 派单生成（行窗现算；SG1 附 g6.md 双出处护栏） | ✅ |
| T1 | anchor_aid.py | sha/check 预检 | ✅ |
| T2 | card_writer.py | 断言前置写盘 | ✅（bug③见下） |
| T3 | batch_finish.py | verify 闸门+uc 回写+统计现算 | ✅ |
| T6 | batch_publish.py | 一条龙发布（--journal-file/--state-file 必传本线） | ⚠️bug①② |
| T11 | sg1_dedup_probe.py | SG1 逐字重复抽查（g6.md 107 段为主题级口径，两表不互替） | ✅（SG1 验收用） |

**待主会话裁决的 bug（两线均未修，scripts/ 禁写）**：
① batch_publish 管道 tail -1 吞退出码——rebase 冲突中断仍报 PUBLISH OK（两线各抓获 ≥1 次假成功；修复前每批发布后人工核验远端 hash，§4.4）；
② MANIFEST 结构性冲突无自动处置（§4.3 手工程序已固化；建议：冲突自动取对方版+continue+重算 amend）；
③ card_writer speaker 枚举宽于 verify（前者收"转述·"任意后缀，后者仅收"吴军本人/转述·第三方"——盲抽代理曾 6 卡首轮 FAIL；派单模板已统一口径规避）；
④ make status 读冻结 state.json，双机期显示滞后（各线权威=state_sgX+journal_sgX）。

## 7. 验收标准全集

### 7.1 GATE-B 每批（两线相同）
官方 verify 0 FAIL（SHA1 复算/行窗⊆/锚≤800/quote≤15 锚内子串/指纹≤3 锚内/claim≤60/枚举全检）+ 处置 100%（unit_disposal 必填+x_disposals 记 X 子类）+ uc 回写覆盖 100% + 即推。

### 7.2 GATE-C（§5.2）
### 7.3 单书验收
- 通用：book_coverage --book {SG3|SG1} 处置未落值 0 → PASS；ck_registry 刷新（幂等）；**模糊点汇总为本线全部（各批 J 行+盲抽自报）→ state/模糊点_{线}.md 移交 P4**；说话人纪律一致性核查（A 线做法：脚本全量——speaker 仅两枚举值、E2 数=转述卡数、E2 notes 全非空注被转述者、读者 0 张 E1，JS-018）。
- SG1 专项：107 段双出处 100% 登记（对照 logs/g6.md）+ 800 字锚受限行号清单移交 P4 + T11 探针抽查。
- PASS 后在本线 journal 写「SGX 验收 PASS」标记并推送（跨机完成标记，GATE-D 前置）。
- **A 线已完成全部四项**（JS-017/018），可作 B 线范本。

### 7.4 GATE-D 收口（当前下一站；两线 PASS 标记齐全后由任一 Agent 执行）
执行者先 `git pull` 确认两线标记齐全，然后四件事：①全库 1,742 单元处置未落值 0；②107 段覆盖去重统计；③全量 verify 复验（零污染确认）；④GATE-C 总复盘（r2~rXX 全轮）。产出入 logs/，记录入执行线 journal。

### 7.5 P4~P7
P4 概念键归一（双 Agent 按柱码分片 A=D01~D05/B=D06~D10 + 模糊点清单裁决；用户主会话另发工单）；P5 成稿（估 43~140 轮，最大不确定项）；P6 审计；P7 交付。

## 8. AI 自检清单

### 8.1 复水测验（V6 版，开工前自答，答案键附后）
①两线各剩什么工作？②GATE-D 触发条件与执行前置？③REF 基准具体是哪三个文件共几张卡？④发布后为什么必须人工核验 hash？MANIFEST 冲突五步处置？⑤GATE-C 并发触发怎么处置？线别后缀约定？⑥publish 必带哪两个参数？⑦B-017 当前状态与恢复方式？A 线能否代做 SG1？⑧哪些目录/文件绝对禁写（含 V6 新增）？⑨数字落账口径（手写 vs 脚本）？⑩说话人纪律核查四要素？

**答案键**：①A 线零（等 GATE-D），B 线 B-017 续抽 8 单元+B-018~020+SG1 验收（§2）；②两线单书验收 PASS 标记齐全+pull 确认（§7.4）；③T-P3a-B-103/FZ-U0007.json 9 卡+T-P3b-B-066/GG-U0013.json 7 卡+T-P3b-B-073/GG-U0119.json 8 卡=24 卡（§5.2）；④publish 吞退出码会假报成功（§6①）；checkout --ours MANIFEST→continue→make pack→amend→pull→push（§4.3）；⑤先上远端者正轮、后到者让号 rXXb 归档+journal 更正行；A 无后缀/B `_b`（§4.5）；⑥--journal-file state/journal_{线}.md --state-file state/state_{线}.json；⑦B-017 在途 9/17 单元 49 卡已写盘未收编勿引用，B 线断点续抽；A 线默认禁碰 SG1，唯用户明示授权才接管（§2/§9）；⑧§3 全部+scripts/（V6 新增）；⑨一律以脚本实数为准（batch_finish/s14 现算），手写仅叙述，错数补更正行（JS-017a 先例）；⑩speaker 两枚举/E2=转述数/E2 notes 全注被转述者/读者零 E1（§7.3）。

### 8.2 每批/每轮例行自检
每批：verify 0 FAIL+处置 100%+uc 覆盖 100%+即推+**推后核验远端 hash**；每轮 GATE-C：独立性声明+卡数指引内+attr 全过线+证据归档+journal 留痕；每天：/tmp 自家前缀检查（J-140 教训）。

## 9. A 线接管 B 线规程（仅用户明示授权时启用）

1. 授权标志：用户新窗口明确说「A 线接管 SG1/代做 B 线」等同等表述；届时写集合临时扩展，仍**以 B 线文件名续记**（journal_sg1.md 编号续 JS1-019、state_sg1.json、uc_SG1.jsonl、cards/T-P3b-B-017~020），不与 A 线混账。
2. B-017 恢复：已有 9 单元文件有效（card_writer 断言通过），续抽 U0324~U0331 共 8 单元（batch_brief T-P3x-B-017 重新生成派单，代理只抽缺失单元）→ batch_finish → publish（JS1-0xx）。
3. 之后 B-018~020 → SG1 单书验收（§7.3 含三项专项）→「SG1 验收 PASS」标记 → GATE-D。
4. 接管期间 GATE-C 触发照常（全局每满 3 批），代理代号续 GAUD 序列，证据 A 线无后缀归档（已接管即单机，无并发风险）。

## 10. 已确认 / 已核实 / 未确认事项

**已确认（方案与授权）**：双机按书切分+同 main+pull --rebase；五步流水线+六件工具；GATE-C 全局 3 批口径+让号+线别后缀；模糊点各线单书验收时汇总；用户授权未解决问题按最优方案处理留痕 decisions.md、每轮四段式报告、复水通过直接开工不停。
**已核实（本轮实证）**：SG3 1,825 卡 0 FAIL+验收 PASS+说话人纪律全量 PASS；GATE-C r2~r28 全绿；REF 基准=产线首批 24 卡（JS-001 纠正）；publish 误报 bug 两线独立证实；MANIFEST 冲突 5 例+程序化处置固化；/tmp 事件零污染（本轮每批自查）。
**未确认（不阻塞，待用户/主会话）**：①4 项工具修复授权（§6①~④）；②5 项口径终裁：移民 X8 子类/科学定律 E1E2/GG-U0013 严口径（注：新口径下 r18~r28 全过线，观察项可降级）/U0175/婚恋 X5（A 线已按"X5+方法论例外"执行 12+ 处）；③U0318 书单 X1 的 N 类消解口径；④B 线机器是否继续执行（或授权 A 接管）；⑤限流是否账号级全局计（两机并发期代理存活率未见异常，A1 假设暂维持）。

## 11. 已完成 / 待完成

**已完成（累计）**：P1~P3a 全部；P3b A 线 23/23+单书验收 PASS；B 线 16/20；GATE-C 27 轮全绿；模糊点_SG3.md（70 条）；ck_registry 7,756 键；本会话 A 线 JS-001~018（r23 欠账闭环+10 批 855 卡+4 轮 GATE-C+验收+2 更正行）。
**待完成（依赖序）**：①B-017 续抽收编（B 线或授权 A 接管）→ ②B-018~020 → ③SG1 单书验收+PASS 标记 → ④GATE-D 四件事 → ⑤P4 工单（用户主会话）→ P5~P7。
**A 线本机即刻可做**：GATE-D（条件满足时）；空闲期经授权做 §10 未确认①②。

## 12. 风险、硬约束、纪律红线

**硬约束**：HC-01 src_frozen 冻结只读；HC-10 说话人先行（名人转述=E2+speaker"转述·第三方"+notes 注被转述者；读者发言不得 E1）；HC-12 无锚不写；HC-21 数字脚本产生；指纹词逐字复制；锚≤800 字/quote≤15 字/claim≤60 字；质量红线工具（说话人自动分类、claim 自动生成）禁用——一票否决。
**纪律**：D-31 GATE-C 盲抽禁主兼任；D-32 代理阵亡主 inline 兜底合法；D-41a GATE-C 卡数指引=REF±2、attr≥0.7 不变；/tmp 自家前缀隔离；文档命名全角竖线；**历史记录只增不改（错数补更正行，JS-017a/JS-018 先例）**；**测试会触发 git 写操作的代码必须在隔离 clone 做（J-148 教训）**。
**风险与预案**：MANIFEST 冲突（§4.3 程序化处置）；GATE-C 并发触发（让号+查两线 journal）；限流杀代理（断点续跑/inline 兜底）；B 线机器不可用（§9 接管规程待授权）；pack 覆盖（git 为权威，pack 是快照）。

## 13. 权威凭证索引

- 线账本：state/journal_sg3.md（JS-001~018）、state/journal_sg1.md（JS1-001~018）；总账本 state/journal.md（冻结至 J-149）
- 线状态：state/state_sg3.json（A 线已更新为收官态）、state/state_sg1.json；暂停快照 state/state.json（J-143，滞后勿引用）
- 规则：spec/rules_v0.9.md（冻结）、spec/pillars.yaml、spec/exclusions.yaml、spec/boundary_rules.md
- 行窗表：logs/batch_windows_pending_20261025.md；重复簇表：logs/g6.md（107 段）
- 模糊点：state/模糊点_SG3.md（70 条，P4 备料）；SG1 验收时出 模糊点_SG1.md
- 决策：state/decisions.md（D-21~D-41a）；历史交接：V1~V5（handover/）
- 本轮关键凭证：logs/book_coverage_SG3_20261026.md、logs/gate_c_r2{3~6}_20261026_*（A 线）、*_b（B 线）、71023db（B-017 暂停备份）

## 14. V6 相对 V5-R1 的修订记录

①快照全面更新为收官实数（SG3 23/23、8,604 卡、r28、B-017 暂停）；②新增 §1 阶段坐标图与 §2 当前暂停工作+新窗口决策树；③§4 git 协议增 MANIFEST 冲突五步程序/发布后人工核验/线别后缀/让号（全部实战固化）；④§5.2 REF 基准写死为产线首批 24 卡（纠正 gate_c_r2 误认风险）；⑤§6 新增 4 项待裁决 bug 清单；⑥§7.3 单书验收补 A 线四项范本（含说话人纪律全量核查）；⑦§8 复水测验换 V6 版十题；⑧§9 新增 A 线接管 B 线规程；⑨scripts/ 升格为共同禁写；⑩历史只增不改、脚本实数口径入纪律。
