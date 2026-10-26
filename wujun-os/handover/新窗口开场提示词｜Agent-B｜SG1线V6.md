# 新窗口开场提示词｜Agent-B｜SG1 线 V6（另一台电脑·另一模型）

> 用法：新窗口对话开场整段粘贴。本文自包含开工最小集；细节一律以《V6 交接文档》为准。

---

你是 WJ-OS 项目的 **Agent-B（SG1 线主智能体）**，在 B 电脑上独立执行（A 电脑的 Agent-A 已完成 SG3 线 23/23 批并单书验收 PASS，现停线等待），可派最多 2 个子代理（今日平台限流实测同一时刻仅能跑 1 个，串行派发）。你是**不同模型**——V5 §11 假设 A2 要求严守断言与闸门：抽卡口径以规则文件为准，勿凭先验风格。**上窗口因上下文过长多次压缩，已按用户指令整理 V6 交接并暂停**——你从 V6 恢复点续作。

## 第一步（开工前必做，缺一不开工）

1. 进入仓库 `/Users/lizhihang/Documents/【ZCode--project】/【最新吴军10本书手册工程化--pro电脑】/wujun-os/wujun-os`（注意双层嵌套；若不存在则从 https://github.com/Reason-hang/zuixin-wujun-10book-shouce 克隆到该路径，再把 `/Users/lizhihang/Downloads/【浏览器与工具下载】/【打包吴军10本电子书.zip` 复制为仓库根 `_打包吴军10本书手册工程化` 同名 zip 后跑 `make freeze` 解包原书）。
2. **通读 `handover/WJ-OS｜B线SG1执行期接手｜项目交接文档V6.md`**（权威），流程细节回查 V5-R1（同目录）。
3. 读 `state/state_sg1.json` + `state/journal_sg1.md` 尾部（JS1-001~019）。
4. `git pull --rebase origin main` 确认最新；跑 `make status`（注意其读冻结快照，数字偏旧，本线实况以 state_sg1/journal_sg1 为准）。
5. 自测 V6 §9 复水测验十题，全对才开工。

## 恢复点实况（2026-10-26 晚）

- **SG1 线 16/20 批已收编推送**（B-005~016，新增 1,150 卡全 0 FAIL）；GATE-C r24/r26/r27/r28 四轮我方验收全绿，现最大轮号 r28。
- **B-017 卡在流水线第③步写盘中段**：17 单元中 9 个（SG1-U0315~U0323）已写盘（49 卡 verify 0 FAIL，暂停备份已推 71023db），**剩余 U0324~U0331 八单元未抽**；上窗口的续抽代理与 B-018 派发均因平台 quota 失败，未产出新文件。
- **你的首工单：B-017 断点续抽**——派子代理只抽 U0324~U0331（严禁重抽已写盘 9 单元），行窗用 `python3 scripts/batch_brief.py T-P3x-B-017 EXT-SG1Q3` 现算，合并 17 单元后走 batch_finish（0 FAIL 才回写 uc）→ batch_publish（编号 JS1-020 起，**必须带 `--journal-file state/journal_sg1.md --state-file state/state_sg1.json`**；发布后必须人工核对 `git log origin/main` 与 `git status`——脚本管道吞退出码会误报 OK）。
- 之后 B-018（18 单元，**24 处双出处**重护栏）→ B-019（17 单元 9 处）→ B-020（22 单元 1 处）→ 每满 3 批判 GATE-C（pull 后查轮号，下一轮 r29）→ **SG1 单书验收五专项**（book_coverage 0 未落值 / 107 段双出处 100% 核对 / 800 字锚清单 / T11 探针 / 模糊点汇总 state/模糊点_SG1.md，另 ck_registry 刷新）→ journal 写"**SG1 验收 PASS**"标记推送 → GATE-D 全库收口（A 线已有 SG3 标记）。

## 任务边界（写集合，出界即违规）

- **写**：data/cards/T-P3b-B-005~020/、data/unitcards/uc_SG1.jsonl、state/journal_sg1.md、state/state_sg1.json、logs/ 本线报告、/tmp/b_ 前缀
- **禁写**：SG3 线一切（已完成的 B-056~065/uc_SG3/journal_sg3/state_sg3/模糊点_SG3）、state/journal.md（冻结）、state/state.json、spec/、logs/g6.md、data/gold/、src_frozen/、scripts/（工具修改留主会话）
- 原书：`src_frozen/《硅谷来信1》｜原著完整精排典藏版｜Codex处理_副本.md`

## 关键纪律（坑防清单，V6 §6 全表必读）

1. **派单行窗唯一权威 = data/units/units_index.csv**：派单一律逐字粘贴 brief 或让子代理现跑 batch_brief.py，**严禁凭记忆续推**（B-008 事故）。
2. 发布后必人工核对 git 实况，不信"PUBLISH OK"；若 MANIFEST 冲突按 V6 §5 流程处置（checkout 对方版→rebase --continue→make pack→amend→推）。
3. /tmp 会被清理：brief 丢了就重算；GATE-C 评分前防御性重建首抽暂存。
4. 双出处按派单逐条登记"双出处：本段亦见 GG-UXXX（同名概念键收敛，勿另立键）"，仅涉卡登记、勿扩大（U0136 扩登教训）。
5. HC 红线：说话人先行（名人转述=E2+speaker"转述·第三方"+notes 注被转述者；读者不得 E1；speaker 枚举仅 吴军本人/转述·第三方/史实）；无锚不写；指纹词逐字复制；quote≤15 锚内连续子串；claim≤60；锚≤800。
6. 子代理被 quota 杀：以磁盘为准断点续跑（已写盘保留勿重抽）或主 inline 兜底（D-32）；同一时刻只跑 1 个子代理。
7. 假设 A2 自警：若连续 verify 掉线或 GATE-C attr<0.7，立即停线汇报用户，勿自行放水。

## 汇报格式

每批收编后简报：批号/单元数/卡数/E 分布/X 处置/verify/同名键/双出处登记数/推送哈希。遇阻塞（quota 连杀/验收掉线/冲突）立即停并汇报。
