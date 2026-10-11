# meta/：指标定义与口径数据

本目录存放报告**指标体系本身**的结构化数据，即附录 A《指标体系与数据来源》中各表格的 CSV 版本，是 `scripts/build_chart_data.py` 计算口径的依据。

## 规划中的文件（从飞书电子表格导出后填入）

| 文件 | 对应附录 A 内容 | 飞书 sheet-id |
|---|---|---|
| `behaviors.csv` | 五类核心贡献行为定义 | aQFhoQ |
| `indicators_activity.csv` | 活跃度指标 | vbC6vR |
| `indicators_influence.csv` | OpenRank 影响力指标 | hJg6W8 |
| `indicators_modelrank.csv` | ModelRank 模型影响力指标 | 96be4o |
| `indicators_diversity.csv` | 人才与贡献多样性指标 | pY7fWI |
| `indicators_governance_assets.csv` | 治理与数字资产指标 | vq3NsW |
| `data_sources.csv` | 数据来源与平台清单 | qJtcdB |
| `glossary.csv` | 术语对照表 | AiT42c |

> 飞书源表：token `AkvfsxJOBhmbqmt1zr0c42Synwg`。更新口径时先改本目录 CSV，再同步飞书与正文。
