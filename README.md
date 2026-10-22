# 2026 全球开源发展报告（Global Open Source Development Report 2026）

> 年度主线：**从普惠到质量，从参与到影响**
>
> 逻辑主线：目标 — 观测 — 评估 — 洞察 — 行动

《2026 全球开源发展报告》追踪全球开源生态在人工智能时代的演进，以开源发展目标（OSDGs）明确研究方向，以开源发展目标指标体系（The OSDGs Indicator System，OSDI）组织可追溯的观测与分析。本仓库以开源方式运作本报告的撰写与发布。

## 2026 在线版 · 更新于 2026 年 10 月 18 日

[报告首页](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/) · [全书目录](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/) · [执行摘要](outline/执行摘要.md) · [引言](chapters/引言-人工智能时代的开源发展.md)

- 第一章正式发布，保留三个小节与七幅交互图；全书结构图集中在第一章，按第一章基础、第二至第五章研究、第六章行动展开；首页、目录、引言和摘要各自提供适合上下文的阅读入口。
- 第二、三、五章的正文与交互图已上线。第四章深入展开 4.1，其余五节先提供研究框架与首幅技术全景。
- 第六章完成五节图文，以三项共同任务组织九条主体建议，配有五幅动态连线图，现已上线供审阅。
- 首页、目录、引言、摘要与当前章节同步；全书以“持续共同创造及其公共价值”为收束。中文正文和双语导航、深浅主题已提供，英文全文仍在准备。

当前发布站由本仓库 `preview/` 构建，GitHub Pages 工作流负责部署。`outline/` 与 `chapters/` 是前置文字与第一章的源稿；`preview/content/manifest.json` 维护六章、30 个小节及两篇附录的导航结构。图表规范与 [osdg-brand](https://github.com/X-lab2017/osdg-brand) 对齐，早期 [gosd-web](https://github.com/X-lab2017/gosd-web) 保留为历史实现。

[附录 A：指标、数据与研究方法](appendices/附录A-指标体系与数据来源.md)、[二十九项指标字典](data/meta/osdi_indicator_dictionary.csv)与[数据可用性清单](data/meta/数据可用性清单.md)说明定义、范围及证据状态。图表上线不等于全部测算完成；观测、派生、模拟与预测按图标明。

附录已收敛为两篇：A 说明正文采用的指标、统计范围、模型样本与查证方法；B 提供模型开放条件与数字公共品研究参照。宣言来源说明并入引言。附录 A 网页与 PDF 共用正文，更新于 2026-10-22。

## 目录结构

```
├── outline/                 # 大纲、目录、执行摘要
├── chapters/
│   ├── 引言-人工智能时代的开源发展.md
│   ├── 引言-宣言.md          # 历史宣言稿，独立于当前引言
│   ├── chapter1/            # 开源发展目标（OSDGs）与开源发展指标体系（OSDI）
│   ├── chapter2/            # 全球开源生态观测地图（GOSO，2.1–2.7）
│   ├── chapter3/            # 全球开源影响力排行榜（GOSR）
│   ├── chapter4/            # 全球开源技术全景洞察（GOSL）
│   ├── chapter5/            # 全球开源大模型发展洞察（GOSM）
│   └── chapter6/            # 未来展望与政策建议
├── appendices/              # 附录 A：指标、数据与研究方法；附录 B：模型开放条件与数字公共品研究参照
├── data/                    # 数据资产（规范见 data/README.md）
│   ├── meta/                # 指标定义与口径（附录 A 各表的 CSV 版）
│   ├── processed/           # 图表源数据：每张图对应一个同名 CSV
│   └── raw/                 # OpenDigger 原始导出（只增不改）
├── figures/                 # 报告图片（与 data/processed/ 同名同构）
└── scripts/                 # 数据计算与图表生成脚本
```

## 数据规范（协作者必读）

报告遵循「**一张图 ↔ 一个同名 CSV**」原则：正文每张图的数据存放于 `data/processed/<章节>/fig-<章号>-<节号>-<序号>_<描述>.csv`，图片存放于 `figures/` 同章同主干名。新增图表时必须同时在 `data/README.md` 的索引表登记。详见 [data/README.md](data/README.md)。

## 协作方式

由报告负责人统一统筹内容、方法与数据。**GitHub 是正文、数据、方法和引用的最终维护基准**；飞书只用于过渡协作，确认后的修改进入仓库。修改建议通过 Issue 与 Pull Request 提出，保留可审查的版本历史。

## 参考资料

- [2025 全球开源发展报告（完整版）](https://f16qo26uhe1.feishu.cn/wiki/ZmbtwsFz3ibxoekbHhwcj9QJn8g)
- 《2026 全球开源发展报告》三级目录

附录 A 与前置合订版的 PDF 由发布流程从当前源稿生成。独立构建时先安装工作流固定版本的 PDF 依赖，运行 `python3 preview/web/build_publication_pdfs.py`，再运行原有 `import_report.py` 与 `build_portal.py`；构建检查核对正文、两篇附录的导航及 PDF 排版边界。
