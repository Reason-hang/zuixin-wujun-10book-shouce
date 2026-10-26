# WJ-OS｜B线SG1执行期接手｜项目交接文档 V6

> 版本：V6（2026-10-26 晚，基于 V5-R1 + B 线 2026-10-26 全天执行实况；由 **Agent-B（SG1 线，另一台电脑·另一模型）** 按用户指令撰写并推送）
> 权威入口优先级：本文档 > V5-R1（handover/WJ-OS｜双机并行执行期接手｜项目交接文档V5.md，流程细节仍有效）> state/state_sg1.json > state/journal_sg1.md > 凭证文件
> 适用对象：下一窗口的 **Agent-B 继任者（SG1 线，B 电脑）**；Agent-A（SG3 线）已 23/23 完成并单书验收 PASS，处于停线等待状态

---

## 0. 项目一句话与暂停点快照（2026-10-26 晚实数）

把吴军 10 本书（5,038,558 汉字、1,742 单元、108 批）抽成带锚点的论点卡，最终成手册。服务跨境电商供应链 B 端产品经理，重点 D06 职场/D01 认知/D02 成长。

**暂停点快照（全部有 git 凭证，脚本可复核）**：
- **P3b 全局 68/86 批**：SG3 线 23/23 全部完成+单书验收 PASS（A 线 JS-017，模糊点 70 条已汇总 state/模糊点_SG3.md）；**SG1 线 16/20 批收编**（B-001~016），B-017 在途 9/17 单元
- **SG1 已收编单元 296/390**（B-001~004 共 87 + B-005~016 共 209）；全库单元约 1,668/1,742（95.8%）
- **SG1 已收编卡 1,497**（B-001~004 共 347 + B-005~016 共 1,150，全部官方 verify 0 FAIL）；B-017 在途 49 卡已写盘未收编不计入
- **全库累计卡约 8,604**（暂停基线 6,599 + A 线十批 855 + B 线十二批 1,150；GATE-D 时由脚本终算）
- **GATE-C r2~r28 共 27 轮无漂移**（本日新增 r23~r28 六轮：r23/r25 A 线验收，r24/r26/r27/r28 B 线验收，全部 attr≥0.7 全绿；另有 r24b/r25b/r26b 三次并发让号归档，协议闭环正常）
- 暂停备份推送：`71023db`（B-017 在途 9 单元）；其后 journal/state 有增量提交

## 1. 当前进行到哪个阶段、哪一步（用户要求必答）

```
P1 试点 ✓ → P3a 六书+WJ2（22批1,857卡）✓ → 【当前】P3b 末段：SG1 收尾
→ SG1 单书验收 → GATE-D 全库收口 →（P4 概念键聚类 → P5 成稿 → P6 审计 → P7 交付，届时用户另发工单）
```

**五步流水线位置**（①batch_brief 派单→②anchor_aid 预检→③card_writer 写盘→④batch_finish 收尾→⑤batch_publish 发布）：
- B-005~B-016 十二批：五步全部走完、逐批推送，0 积压；
- **B-017：卡在第③步写盘中段**——17 单元中 9 个（U0315~U0323）已写盘（49 卡 verify 0 FAIL，断言前置产物，有效），第④⑤步未开始；
- B-018/019/020：未开始（派单文件已预生成，见 §7）。

## 2. 当前暂停的手头工作（用户要求必答）

**暂停任务 = B-017 断点续抽**。经过：用户 2026-10-26 傍晚指令"立刻暂停并推送"→ 主智能体 TaskStop 当时的 B-017 抽取代理（已写 9/17）→ 暂停备份推 `71023db` → 用户恢复后重派续抽代理（只做剩余 U0324~U0331 八单元），**该代理与并行的 B-018 派发均因平台 quota/并发限制失败**（B-017 续抽未产出任何新文件，仍为 9/17；B-018 未启动）。用户随即指令终止目标、撰写本 V6 换窗口。

**无数据丢失**：远端 main 与本机一致；B-017 的 9 个单元是 card_writer 断言通过的有效文件，续抽时严禁重抽这 9 个（card_writer 防覆盖会拦截）。

## 3. 剩余工作清单（继任者执行顺序）

1. **B-017 断点续抽**：派子代理只抽 U0324~U0331（8 单元），与已写盘 9 单元合并后走④batch_finish→⑤batch_publish（JS1-019 起编号顺延，注意 §6 工具坑）。行窗以 `python3 scripts/batch_brief.py T-P3x-B-017 EXT-XX` 重算输出为准（本批无 GG 同源段）。
2. **B-018**（18 单元，**24 处双出处**重护栏批）、**B-019**（17 单元，9 处双出处）、**B-020**（22 单元，1 处双出处）：派单文件已预生成 `/tmp/b_brief_B-018.md`、`_B-019.md`、`_B-020.md`（/tmp 若被清理则用 batch_brief.py 重算，勿手抄行窗——见 §6 教训 T2）。
3. **GATE-C 触发判断**：全局每满 3 批一轮；A 线已停线，计数只看本线。r28 后已收 2 批（B-016 算 1，B-017 收编后再满 3 触发 r29；准确口径：pull 后数全局已收批数÷3）。轮号查 `ls logs/ | grep -o "gate_c_r[0-9]*" | sort -V | tail -1`（当前最大 r28）。
4. **SG1 单书验收**（B-020 收编后，V5 §5.3 全项）：
   - `python3 scripts/book_coverage.py --book SG1`：处置未落值 0 → PASS
   - **107 段双出处 100% 核对**（对照 logs/g6.md；本日 B 线已登记：B-005×1、B-007×4、B-010×8、B-012×1、B-013×7、B-015×7 处卡；B-018~020 的登记数待抽后累加）
   - 800 字锚受限行号清单移交 P4（B-005~016 均为 0 处，B-017~020 待查 unit_disposal_reason）
   - T11 探针抽查：`python3 scripts/sg1_dedup_probe.py`（口径：g6.md 107 段为 P1 主题级，T11 仅逐字级补充，两表不互替）
   - **模糊点汇总** `state/模糊点_SG1.md`（各批 J 行+子代理自报，含 U0287 目录导航 N1/X1 消解、U0136 扩登修正、speaker"史实"前缀工具口径差等）
   - 说话人纪律抽查：转述·第三方名单 vs E2 卡数一致性
   - ck_registry 刷新（`python3 scripts/ck_registry.py`，幂等）
   - 完成后在本线 journal 写"**SG1 验收 PASS**"标记并推送（GATE-D 跨机完成标记，A 线已有"SG3 验收 PASS"）
5. **GATE-D 收口**（两线标记齐全后由 B 线执行，A 线已停线）：pull 确认双标记 → 全库 1,742 单元处置未落值 0 → 107 段覆盖去重统计 → 全量 verify 复验 → GATE-C 总复盘 → P4~P7 待用户主会话另发工单。

## 4. 双线分工与写集合（沿 V5 §1，A 线已完成）

- **B 线（你）写**：data/cards/T-P3b-B-005~020/、data/unitcards/uc_SG1.jsonl、state/journal_sg1.md（已用到 JS1-018，下号 JS1-019）、state/state_sg1.json、logs/ 本线报告、handover/ 本 V6 与开场提示词（用户指令授权）、/tmp/b_ 前缀
- **禁写**：SG3 线一切（已完成的 cards/T-P3b-B-056~065、uc_SG3.jsonl、journal_sg3.md、state_sg3.json、模糊点_SG3.md）、state/journal.md（冻结至 J-149）、state/state.json、spec/ 全部、logs/g6.md、data/gold/、src_frozen/、scripts/（工具修改留主会话裁决）
- 原书：`src_frozen/《硅谷来信1》｜原著完整精排典藏版｜Codex处理_副本.md`（本机已由 `_打包吴军10本电子书.zip` 经 `make freeze` 解包，基线比对 0 失败；zip 在仓库根，gitignore 已排除不入公开库）

## 5. git 协作协议（沿 V5 §2 + 本日实战更新）

1. 同仓库同 main：`https://github.com/Reason-hang/zuixin-wujun-10book-shouce`；本机克隆于 `【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os`（注意双层 wujun-os 嵌套）
2. 每次推送前 `git pull --rebase origin main`（batch_publish 已内置，但见 §6 坑 ①）
3. **MANIFEST 冲突处置流程（本日实战 5 次全部成功）**：publish 触发 rebase 冲突时（冲突文件必为 MANIFEST.sha256，系双方 make pack 重算清单的结构性共享写，非越界）→ `git checkout origin/main -- MANIFEST.sha256 && git add MANIFEST.sha256 && GIT_EDITOR=true git rebase --continue` → `make pack && git add MANIFEST.sha256 && git commit --amend --no-edit` → `git pull --rebase origin main && git push`。A 线已停线，此后冲突概率归零，但流程保留。
4. 提交信息：`feat: SG1⑰ B-017完成收编——NN卡 0 FAIL、覆盖 17 单元（JS1-0NN）` 格式；发布命令必须带 `--journal-file state/journal_sg1.md --state-file state/state_sg1.json`
5. 遗漏推送=违规：每批收编即推。

## 6. 工具坑与教训清单（本日实测，全部已验证处置）

| # | 坑 | 处置 |
|---|---|---|
| ① | batch_publish 的 pull --rebase/push 用 `2>&1 \| tail -1` 管道吞退出码：rebase 中断仍打印"PUBLISH OK"（实际未推，B/A 两线独立证实） | 发布后**必须**核对 `git log origin/main --oneline -1` 与 `git status` 是否干净，不能信脚本输出；工具修复留主会话 |
| ② | 主智能体凭记忆续推编造派单行窗（B-008 事故：首行恰好对、后续 19 单元全错位） | **派单一律逐字粘贴 brief 文件或让子代理自跑 batch_brief.py 重算**；行窗唯一权威=data/units/units_index.csv（verify 即按它校验，错窗会被拦但浪费一轮） |
| ③ | /tmp 会被系统清理：brief 文件、首抽暂存目录、盲抽暂存都可能消失 | 派单前检查存在性，丢了就 batch_brief.py 重算；GATE-C 评分前防御性重建首抽暂存（曾致 0/28 假 FAIL） |
| ④ | make status 读冻结的 state.json（J-143 暂停快照），双机并行期数字偏旧 | 本线进度以 state_sg1.json + journal_sg1.md 为权威 |
| ⑤ | batch_brief.py 生成的派单头部"工作目录"是硬编码旧机器路径 | 派单时以提示词中本机路径为准（双层 wujun-os 嵌套目录） |
| ⑥ | gate_c 目录两线同路径相撞（r25 事故） | 盲抽目录带线别后缀 `gate_c_rXX_..._cards_b`（r26 起已执行）；撞上已推送的官方件时 git restore 复位、己方产出让号归档 |
| ⑦ | 子代理两处 speaker 工具口径差：card_writer 接受"史实·X"前缀、verify_cards 只认精确枚举"史实" | 子代理写盘后自行规范化即可过检（B-012/B-016 先例）；口径统一留 P4 前置工单 |
| ⑧ | 子代理可能写盘+自检完成后长时间不返回最终消息（B-015）或直接被 quota 杀（B-017 续抽） | 交付以磁盘为准：`ls data/cards/T-P3b-B-0XX/` 计数 + verify 报告存在即接管审查收编（D-32 主智能体兜底合法）；quota 恢复后重派断点续抽 |
| ⑨ | 平台 quota/并发限流今日实际发生：一次只能跑 1 个子代理、quota 用尽连主智能体也停 | 串行派单不并行；遇 quota 停线即按本 V6 换窗口续作 |

## 7. 派单与验收速查（继任者直接照用）

**派单模板**：`python3 scripts/batch_brief.py T-P3x-B-0XX EXT-SG1X > /tmp/b_brief_B-0XX.md` → 子代理读该文件执行（工作目录以其提示词为准）→ 主智能体审查（形式：处置/reason/x_subtype/E2 speaker+notes/读者非E1；语义：抽卡对原文）→ `batch_finish.py T-P3b-B-0XX data/cards/T-P3b-B-0XX data/unitcards/uc_SG1.jsonl --out logs/cards_verify_...md`（0 FAIL 才回写）→ `batch_publish.py ... JS1-0NN --journal-file state/journal_sg1.md --state-file state/state_sg1.json --title --themes --extra`。

**每批验收（GATE-B）**：官方 verify 0 FAIL + 处置 100%（unit_disposal/reason/x_disposals 子类理由齐）+ uc 回写覆盖 100% + 即推 + 双出处按派单逐条登记（仅涉卡登记，未成卡内容不登记）。

**GATE-C（r29 起轮号顺延）**：黄金三单元行窗写死 FZ-U0007=《富足》179-232｜GG-U0013=《谷歌方法论》1066-1118｜GG-U0119=同书 7987-8040；卡数指引 7~11/5~9/6~10（REF±2）；验收=verify 0 FAIL + s14 attr 三分量与目录级全 ≥0.7（strict 记录不判）+ 独立性声明；评分用 `/tmp/b_r24_first_all`（首抽=data/cards 原件：FZ=T-P3a-B-103、GG13=T-P3b-B-066、GG119=T-P3b-B-073；分口径必须单单元×单单元配对）。

**硬约束（HC 红线）**：HC-01 冻结只读；HC-10 说话人先行（名人转述=E2+speaker"转述·第三方"+notes 注被转述者；读者发言不得 E1；speaker 枚举只有 吴军本人/转述·第三方/史实）；HC-12 无锚不写；HC-21 数字脚本产生；指纹词逐字复制；quote≤15 字锚内连续子串；claim≤60 字；锚≤800 字；每单元 4~9 卡（史实/游记/品味类可 2~3 卡并在 reason 说明；整单元排除写 0 卡包装，先例 data/cards/T-P3b-B-048/SG3-U0068.json 与本线 U0112/U0119/U0121/U0184/U0251/U0287）。

## 8. 已确认事实 / 未确认事项

**已确认（本日新增）**：
- B-005~016 十二批 1,150 卡全 0 FAIL；r24/r26/r27/r28 四轮 attr 均值 0.84~0.92（三分量最低 0.750），假设 A2（新模型过闸）持续成立
- A 线 SG3 全部完成并验收 PASS；r26 归属更正双方留痕闭环（B 线为正轮）
- 双出处登记累计（B-005~016，以 g6.md 为准）：B-005×1（U0106↔GG-U0031）、B-007×4（U0134↔GG-U0119；U0136 扩登 4 卡已按权威表移除并记模糊点）、B-010×8（U0197×7↔GG-U0223、U0199×1↔GG-U0130，覆盖派单 11 段）、B-012×1（U0242-05↔GG-U0168）、B-013×7（U0255×4↔GG-U0175 八条目、U0259×3↔GG-U0199 三条目）、B-015×7（U0285↔GG-U0224 覆盖全部 13 段，行号逐段核对无缺口）；B-006/008/009/011/014/016 派单载明无同源段

**未确认（不阻塞，遇相关单元按既有口径继续+记模糊点）**：
- 用户 5 项待终裁沿 V5：移民 X8/科学定律 E1E2/GG-U0013 严口径/U0175 读者留言/婚恋 X5
- quota 限流何时恢复（今日杀掉 B-017 续抽与 B-018 派发）；恢复后串行派单
- P4~P7 细节届时用户主会话另发工单（P5 估 43~140 轮是最大不确定项）

## 9. 复水测验（开工前自答，答错重读本文档与 V5）

①SG1 剩哪几批？各多少单元、多少双出处？②B-017 已写盘哪 9 个单元？续抽从哪个单元开始？③publish 必带哪两个参数？④发布后必须人工核对什么？⑤行窗的唯一权威文件？⑥GATE-C 当前最大轮号？触发口径？⑦单书验收五专项？⑧B 线禁写清单？⑨黄金三单元行窗与卡数指引？⑩quota 杀掉子代理后怎么处置？
（答案：①B-017 余8单元无同源段/B-018 18单元24处/B-019 17单元9处/B-020 22单元1处；②U0315~U0323、从U0324续；③--journal-file state/journal_sg1.md --state-file state/state_sg1.json；④git log origin/main 与 git status（脚本会误报 OK）；⑤data/units/units_index.csv；⑥r28、全局已收批数满3触发、A线停线后只看本线；⑦book_coverage 0未落值/107段100%核对/800字锚清单/T11探针/模糊点汇总（另+ck_registry 刷新+journal 写"SG1 验收 PASS"标记）；⑧见 §4；⑨FZ 179-232 7~11｜GG13 1066-1118 5~9｜GG119 7987-8040 6~10；⑩以磁盘为准断点续跑（已写盘保留勿重抽）或主智能体 inline 兜底 D-32。）

## 10. 凭证索引

- 本线账本 state/journal_sg1.md（JS1-001~018：12 批收编+r24/r26/r27/r28 验收+r25 让号+冲突首报+事故留痕）；线状态 state/state_sg1.json
- 总账本 state/journal.md（冻结至 J-149）；A 线账本 journal_sg3.md（JS-001~018，含 SG3 验收 PASS 与 r26 归属更正）
- 本日关键提交：c9a1e28（B-005 首收编）/ e727218（r24）/ 84a15a1 / 24471ec / 205f6b7 / 21eb2e1（r26）/ d26ba19（r27）/ 580fae1（r28）/ e57e528（B-016）/ **71023db（B-017 暂停备份）**
- 行窗表 logs/batch_windows_pending_20261025.md；重复簇表 logs/g6.md（107 段）；规则 spec/rules_v0.9.md + pillars.yaml + exclusions.yaml + boundary_rules.md
