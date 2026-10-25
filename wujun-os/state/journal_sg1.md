# SG1 线 journal（Agent-B 专用，V5 双机分线；总账本 state/journal.md 冻结至 J-143）

| 编号 | 日期 | 记录 | 凭证 |
|---|---|---|---|
| JS1-001 | 2026-10-26 | SG1⑤ B-005 完成收编（T-P3b-B-005 由子代理交付、batch_publish 一条龙发布）：K21+X0，118 卡 E1×73/E2×24/E3×21（转述·第三方 24），X 处置 22 条；verify 0 FAIL、覆盖 21 单元、uc 回写；批内同名键 反应比预测重要。主题带：隐私值多少钱/销售大师两连/金色大厅/一流的人投资系统/莎士比亚交友诚信/瑞士制造最后1%/生活是具体的/货殖列传/CES四连/向死而生/加速还是减速/2016总结/上火星/轩尼诗/伊比利亚火腿/撒切尔保守主义。转述·第三方24卡（王晓峰×3/撒切尔×3/司马迁×3/斯加鲁菲×3/爱因斯坦/周国平/凯利/道金斯/斯图林格等）；双出处登记1处（C-SG1-U0106-07↔GG-U0031，概念键保守主义渐进改良收敛）；批内同名键1（反应比预测重要×2，notes互引）；800字锚受限0处；模糊点4条入P4；SG1 5/20 | data/cards/T-P3b-B-005/、logs/ |
| JS1-002 | 2026-10-26 | **双机并行首例 push 冲突（V5 §2.6 首报）**：B-005 发布时 pull --rebase 撞 A 线 ebec2ef（B-056 收编+GATE-C r23 验收），冲突文件仅 MANIFEST.sha256——双方 publish 均跑 make pack 重算全库清单，属结构性共享写而非写集合越界；处置：取对方版 MANIFEST 落位完成 rebase→本方 make pack 重算并入收编提交（amend）→推送成功 c9a1e28。连带发现两个工具问题（留主会话裁决，本线不动 scripts/）：①batch_publish.py 的 pull --rebase/push 用管道 tail -1 吞退出码，rebase 中断仍误报 PUBLISH OK（实际未推）；②make status 读冻结的 state.json，双机并行期不反映双线实况，本线进度以 state_sg1+journal_sg1 为权威。GATE-C r23 已由 A 线消化（GAUD25 三单元验收全绿），本线后续按全局 3 批口径 pull 后查轮号触发 | ebec2ef、c9a1e28 |
