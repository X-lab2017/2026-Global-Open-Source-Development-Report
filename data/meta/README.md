# meta/：统一框架、指标定义与证据状态

GitHub 是本报告正文、数据、方法与引用的维护基准。飞书用于过渡协作；确认的修改先进入仓库，再按需同步到飞书与展示端。

| 文件 | 用途 |
|---|---|
| [osdg-framework.json](osdg-framework.json) | 四支柱、十维度、二十九指标的统一结构，沿用确认的框架编码 |
| [osdi_indicator_dictionary.csv](osdi_indicator_dictionary.csv) | 二十九指标的工作定义、对象、计算规则、单位、状态与数据路径 |
| [chapter_indicator_map.csv](chapter_indicator_map.csv) | 四个研究板块的指标规划用途；不表示相关结果已经产生 |
| [dataset_inventory.csv](dataset_inventory.csv) | 当前34份processed数据（第二章13份、第三章21份）的字段、行数、关联、待办与校验值 |
| [数据可用性清单.md](数据可用性清单.md) | 面向审阅的可用性与待补事项 |
| [behaviors.csv](behaviors.csv) | 五类协作行为；区分报告概念与OpenDigger事件实现 |
| [data_sources.csv](data_sources.csv) | 来源、用途与纳入边界 |
| [glossary.csv](glossary.csv) | 中英文术语 |
| indicators_activity / influence / modelrank / diversity / governance_assets.csv | 按专题保留的口径摘要；以统一字典及附录A为准 |
| [source_register.csv](source_register.csv) | 第一章及方法基础的引用与核验记录 |

## 状态解释

框架收录、方法明确、数据入库、完成复现和允许发布是不同状态。`method_status` 描述规则成熟度；`data_status` 描述当前仓库资料；待补问题写入 `remaining_evidence`。暂缺数据不填零，不用外部故事数据补足本报告指标。

第一章介绍原理，[附录 A](../../appendices/附录A-指标体系与数据来源.md)维护全书共同方法。报告正文的定义修订不意味着既有CSV已经按新定义重算；必须保留原值并记录后续核验或版本变更。

Preview 中的框架文件是展示副本。当前线上仍为已验收的架构预览；本次内容审阅通过后，再由这里的统一结构同步展示副本和全文页面。
