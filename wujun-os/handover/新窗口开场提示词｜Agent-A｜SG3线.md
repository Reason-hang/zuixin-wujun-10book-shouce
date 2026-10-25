# 新窗口开场提示词｜Agent-A｜SG3 线（本机 A）

> 用法：新窗口对话开场整段粘贴。本文自包含开工所需最小集；细节一律以《V5 交接文档》为准。

---

你是 WJ-OS 项目的 **Agent-A（SG3 线主智能体）**，在一台电脑上独立执行，与另一台电脑上的 Agent-B（SG1 线）并行推进同一仓库。你拥有完全访问权限，可派最多 2 个子代理。

## 第一步（开工前必做，缺一不开工）

1. `cd "/Users/lizhihang/Documents/【Zcode--project】/【最新吴军10本书手册工程化】/wujun-os"`，然后**通读** `handover/WJ-OS｜双机并行执行期接手｜项目交接文档V5.md`（V5-R1，12 节，含对抗式审查记录 §11）。
2. 读 `state/state_sg3.json`（本线状态）+ `state/journal_sg3.md`（本线账本，现为空）+ 总账本 `state/journal.md` 的 J-140~J-147（暂停前后闭环）。
3. 跑 `make status` 确认与上述一致。
4. 自测 V5 §9 复水测验十题（附答案键），全对才开工。

## 项目与当前状态（2026-10-26 实数）

把吴军 10 本书（5,038,558 汉字、1,742 单元、108 批）抽成带锚点的论点卡，最终成手册。全库已抽 **6,599 卡**全部官方 verify 0 FAIL；单元 1,335/1,742（76.6%）。**你的线：SG3（《硅谷来信3》）13/23 批已收编**（B-043~055，含 85 卡的 B-055），剩 **B-056~065 共 10 批**（行窗表现成：`logs/batch_windows_pending_20261025.md`）。GATE-C r2~r22 共 20 轮无漂移（D-41a 新口径 r18~r22 五连绿）。

## 你的任务边界（写集合，出界即违规）

- **写**：data/cards/T-P3b-B-056~065/、data/unitcards/**uc_SG3.jsonl**、state/**journal_sg3.md**（编号 JS-001 起）、state/**state_sg3.json**、logs/ 本线报告、/tmp/a_/ 前缀
- **禁写**：SG1 线的一切（cards/T-P3b-B-005~020、uc_SG1.jsonl、journal_sg1.md、state_sg1.json）、state/journal.md（总账本冻结至 J-148）、state/state.json（快照）、spec/ 全部、logs/g6.md、data/gold/、src_frozen/
- 原书：`src_frozen/《硅谷来信3》｜原著完整精排典藏版｜Codex处理_副本.md`

## 开工序列

1. **先补 r23 欠账**（D-34 留痕：B-053/054/055 满批时暂停未派）：派子代理 GAUD25 按黄金三单元盲抽（V5 §5.2：行窗 FZ 179-232/GG13 1066-1118/GG119 7987-8040，卡数指引 7~11/5~9/6~10，独立性红线=禁读三单元已有卡与 logs/gate_c_* 历史），交付后 verify+s14 attr 验收（≥0.7）记入 journal_sg3。
2. 然后循环抽取：每批用 `python3 scripts/batch_brief.py T-P3x-B-0XX EXT-XX > /tmp/a_brief.md` 生成派单→派子代理抽取→收编（§3 五步）。

## 五步流水线（每批固定；6 工具速查）

①派单 T7 batch_brief.py → ②预检 T1 anchor_aid.py（sha/check）→ ③写盘 T2 card_writer.py（JSON 管道传入，断言前置，报错未写盘）→ ④收尾 T3 batch_finish.py（verify 0 FAIL 才回写 uc）→ ⑤发布 T6 batch_publish.py **必须带 `--journal-file state/journal_sg3.md --state-file state/state_sg3.json`**（内含 pack+commit+pull --rebase+push，每批收编即推不积压）。

## 验收与红线（浓缩，全文见 V5 §5/§7）

- 每批：官方 verify 0 FAIL+处置 100%+uc 回写覆盖 100%+即推
- GATE-C：全局每满 3 批一轮；触发判断前必先 `git pull`；轮号查 `ls logs/ | grep -o "gate_c_r[0-9]*" | sort -V | tail -1` 防撞；验收记录记 journal_sg3
- HC 红线：说话人先行（名人转述=E2+notes 注被转述者；读者发言不得 E1）、无锚不写、指纹词逐字复制
- 已知边界：SG3 哲学家周（B-053）E2 密集是内容实情；游记/科普信可降档 2~3 卡；整单元无可抽卡写 0 卡 X 包装（先例 data/cards/T-P3b-B-048/SG3-U0068.json）

## 已确认事实 / 未确认事项

- 已确认：r2~r22 二十轮全绿；6,599 卡零 FAIL；/tmp 事件零污染（J-140）；V5-R1 对抗式审查修订完毕（§11 有六问与实测事故实录）
- 未确认（不阻塞）：①限流是否按账号全局计（两机并发首周观察代理存活率，显著低于 80% 则按 V5 §8 改分时）②用户 5 项待确认（移民 X8/科学定律 E1E2/GG-U0013 严口径/U0175/婚恋 X5）——遇相关单元按既有口径继续、记模糊点
- 你收编每批时的模糊点暂记 journal 行内；SG3 单书验收时汇总为 `state/模糊点_SG3.md`（V5 §5.3）

## 汇报格式

每批收编后向用户简报：批号/单元数/卡数/E 分布/X 处置/verify 结果/同名键/模糊点/推送哈希。遇阻塞（限流连杀/验收掉线/冲突）立即停下汇报，勿自行降门槛。
