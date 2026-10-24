# 黄金样例 gold_v1（ST-3 漂移回归基准）｜2026-10-24 冻结

来源：P1 放量双盲复验（N4 vs N1/N2/N3），attr 重合率全过 0.7。每 3 批（GATE-C）由全新窗口对下列单元重抽，attr ≥0.7 为通过；<0.7 触发 §15.12 停线检查。

| unit_id | 标准卡集 | 检验点 | 复验基线 |
|---|---|---|---|
| FZ-U0007 做减法比做加法重要 | data/pilot/batch2/N1/FZ-U0007.json（9 卡）+ N4 复验（12 卡） | R1 转述双卡（断舍离）、R3 案例卡、X2 时效处置 | attr 0.857 / strict 0.667 |
| GG-U0013 第008封·三条边 | data/pilot/batch2/N2/GG-U0013.json（8 卡）+ N4（7 卡） | 三条边结论句归属判例（D05/D04 互设辅助标签） | attr 0.933 / strict 0.933 |
| GG-U0119 拉里·佩奇 | data/pilot/batch2/N3/GG-U0119.json（8 卡）+ N4（9 卡） | R1 双卡并存（牙刷原话转述 E2 vs 吴军概括 E1）、D10-1 使用、X2/X6 处置 | attr 0.824 / strict 0.824 |

微试跑 3 单元（FZ-U0020/GG-U0256/SG3-U0110，cards_first vs cards_second）为辅基准：attr 0.737（规则 v0.9 前口径，仅作对照不作门槛）。
