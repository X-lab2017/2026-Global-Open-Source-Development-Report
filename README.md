# 2026 全球开源发展报告（Global Open Source Development Report 2026）

> 年度主线：**从普惠到质量，从参与到影响**
>
> 逻辑主线：目标 — 观测 — 评估 — 洞察 — 行动

《2026 全球开源发展报告》追踪全球开源生态在人工智能时代的演进，以开源发展目标（OSDGs）明确研究方向，以开源发展目标指标体系（The OSDGs Indicator System，OSDI）组织可追溯的观测与分析。本仓库以开源方式运作本报告的撰写与发布。

## 当前 Preview · v0.6

- [第一章正文入口](chapters/chapter1/本章介绍.md)：价值—目标—指标，衔接四个核心研究板块。
- [附录 A 方法基础](appendices/附录A-指标体系与数据来源.md)与[二十九项指标字典](data/meta/osdi_indicator_dictionary.csv)。
- [数据可用性清单](data/meta/数据可用性清单.md)与[写作和演示复用规范](editorial/章节写作与内容复用规范.md)。
- [本轮修订说明](editorial/第一章修订说明-20261012.md)。第一章与方法基础已接入 [在线 Preview](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/01/)，沿用已验收的六栏目导航。下列旧稿进度不代表相关发现已完成数据核验。

## 目录结构

```
├── outline/                 # 大纲、目录、执行摘要
├── chapters/
│   ├── 引言-宣言.md          # 引言：《全球开源与人工智能国际合作宣言》
│   ├── chapter1/            # 开源发展目标（OSDGs）与开源发展指标体系（OSDI）
│   ├── chapter2/            # 全球开源生态观测地图（GOSO，2.1–2.7）
│   ├── chapter3/            # 全球开源影响力排行榜（GOSR）
│   ├── chapter4/            # 全球开源技术全景洞察（GOSL）
│   └── chapter6/            # 未来展望与政策建议
├── appendices/              # 附录 A：指标体系与数据来源；附录：开源 AI DPG 评估框架
├── data/                    # 数据资产（规范见 data/README.md）
│   ├── meta/                # 指标定义与口径（附录 A 各表的 CSV 版）
│   ├── processed/           # 图表源数据：每张图对应一个同名 CSV
│   └── raw/                 # OpenDigger 原始导出（只增不改）
├── figures/                 # 报告图片（与 data/processed/ 同名同构）
└── scripts/                 # 数据计算与图表生成脚本
```

## 数据规范（协作者必读）

报告遵循「**一张图 ↔ 一个同名 CSV**」原则：正文每张图的数据存放于 `data/processed/<章节>/fig-<章号>-<节号>-<序号>_<描述>.csv`，图片存放于 `figures/` 同章同主干名。新增图表时必须同时在 `data/README.md` 的索引表登记。详见 [data/README.md](data/README.md)。

## 历史原稿进度（待按 Preview 归位）

以下保留原稿盘点，尚未按已验收的六章框架全部重排；涉及模型的旧节号将在GOSM内容修订时统一归位。

**已完成（初稿）**：执行摘要、引言宣言、第一章（1.1–1.3）、第二章（2.1–2.7）、第三章（3.1–3.5）、第四章（4.1、4.3–4.6）、第六章、附录 A、附录（开源 AI DPG 评估框架）。

**待撰写**：

- 3.6 全球开源大模型影响力排行榜（M-Ranking）
- 4.2 AI 大模型全景洞察（M-Landscape）
- 第五章 全球开源大模型发展洞察（GOSM）：5.1 供给与贡献 / 5.2 网络与影响力 / 5.3 开源开放与分级体系
- 结语：迈向可持续的数字未来
- 附录 C：开源人工智能数字公共产品评估框架（当前 DPG 框架文档暂定编号为附录 B，待与目录对齐）

## 协作方式

由报告负责人统一统筹内容、方法与数据。**GitHub 是正文、数据、方法和引用的最终维护基准**；飞书只用于过渡协作，确认后的修改进入仓库。修改建议通过 Issue 与 Pull Request 提出，保留可审查的版本历史。

## 参考资料

- [2025 全球开源发展报告（完整版）](https://f16qo26uhe1.feishu.cn/wiki/ZmbtwsFz3ibxoekbHhwcj9QJn8g)
- 《2026 全球开源发展报告》三级目录
