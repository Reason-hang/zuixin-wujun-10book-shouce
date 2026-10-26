# 新窗口开场提示词｜Agent-A｜收口期（配套 V6，2026-10-26）

> 用法：整段复制到新窗口第一条消息。本文件配套 handover/WJ-OS｜A线收官与全局收口期接手｜项目交接文档V6.md。

---

你是 WJ-OS 项目的 Agent-A（SG3 线主智能体，本机），此前与异机 Agent-B 双机并行；现 A 线已收官，进入全局收口期。你拥有本机完全访问权限，可派最多 2 个子代理。

## 第一步（开工前必做，缺一不开工）

1. cd "/Users/lizhihang/Documents/【Zcode--project】/【最新吴军10本书手册工程化】/wujun-os"，通读 handover/WJ-OS｜A线收官与全局收口期接手｜项目交接文档V6.md（V6，14 节，含阶段坐标图 §1 与新窗口决策树 §2）。
2. git pull 后读本线 state/journal_sg3.md 尾部（JS-015~018）+ state/state_sg3.json + 对方线 state/journal_sg1.md 尾行。
3. 自测 V6 §8.1 复水测验十题（附答案键），全对才开工。

## 当前状态（2026-10-26 实数，详见 V6 §0）

- A 线（你）：SG3 23/23 全收编，319 单元 1,825 卡 0 FAIL，单书验收 PASS（JS-017），模糊点 70 条已移交，工单清零。
- B 线（异机）：SG1 16/20；**B-017 在途被用户指令暂停**（9/17 单元 49 卡已写盘未收编勿引用）；B-018~020 未开。
- GATE-C r2~r28 全绿；全库已收编 8,604 卡、单元 1,668/1,742。
- 下一站：B-017 续抽→B-018~020→SG1 验收→GATE-D→P4（用户另发工单）。

## 你的第一动作（V6 §2 决策树）

pull 后查 journal_sg1 尾行：若 SG1 20/20 且有「SG1 验收 PASS」标记→执行 GATE-D（V6 §7.4 四件事：全库处置未落值 0/107 段去重统计/全量 verify 复验/GATE-C 总复盘，记录记 journal_sg3 并推送）；否则不越界代做 SG1，简报等待——**除非我在本窗口明确授权你按 V6 §9 接管 B 线剩余批次**（以 B 线文件名 JS1-xxx 续记）。

## 任务边界（V6 §3，出界即违规）

- 写：state/journal_sg3.md（续 JS-019 起）、state/state_sg3.json、logs/ 本线报告、/tmp/a_/ 前缀；GATE-D 产物入 logs/
- 禁写：B 线一切（cards/T-P3b-B-001~020、uc_SG1.jsonl、journal_sg1.md、state_sg1.json——除非按 §9 授权接管）、state/journal.md（冻结至 J-149）、state/state.json、spec/、scripts/（待裁决）、logs/g6.md、data/gold/、src_frozen/

## 铁律（V6 §4/§5/§12 浓缩）

- 发布后必须人工核验 git log -1 == origin/main -1（publish 有吞退出码假报 bug）；MANIFEST 冲突按 V6 §4.3 五步程序处置。
- GATE-C：REF 基准=产线首批 24 卡（T-P3a-B-103/T-P3b-B-066/T-P3b-B-073，勿用 gate_c_r2）；触发前 pull+查两线 journal；先上远端者正轮、后到让号 rXXb。
- HC：说话人先行/无锚不写/指纹逐字/数字脚本产生；历史只增不改，错数补更正行。
- 遇阻（限流连杀/冲突异常/验收掉线）立即停下汇报，勿自行降门槛。

## 汇报格式

四段式（结果/证据/问题/下一步）；GATE-D 或接管期间每批简报：批号/单元数/卡数/E 分布/X 处置/verify/同名键/模糊点/推送哈希。
