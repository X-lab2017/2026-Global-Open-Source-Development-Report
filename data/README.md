# data/：报告数据目录规范

本目录存放《2026 全球开源发展报告》的全部数据资产，遵循**「一张图 ↔ 一个同名 CSV」**原则，保证报告中的每一张图都有可审查、可复现的数据来源。

## 目录结构

```
data/
├── README.md          # 本文件：规范与索引
├── meta/              # 指标定义类数据（对应附录 A 的口径表）
├── processed/         # 图表源数据：每张报告图片对应一个同名 CSV
│   ├── chapter1/
│   ├── chapter2/      # 2.1–2.7 七张地图
│   ├── chapter3/      # 3.1–3.6 排行榜
│   ├── chapter4/      # 各领域全景洞察
│   ├── chapter5/      # GOSM 大模型洞察
│   └── chapter6/
└── raw/               # OpenDigger 原始导出（只增不改，按统计周期归档）
    └── 2026/          # 统计周期：2025-07-01 ~ 2026-06-30
```

## 命名规范

- **图表数据**：`fig-<章号>-<节号>-<序号>_<英文短描述>.csv`
  - 例：`fig-2-1-1_global_activity_map.csv`、`fig-3-2-1_company_openrank_top10.csv`
- **图片**（存放在仓库根目录 `figures/`，与此处同章同主干名）：`fig-<章号>-<节号>-<序号>_<英文短描述>.png`
- 小写、下划线连接；序号按图在文档中出现的顺序编排
- 地图类数据的区域编码使用 ISO 3166（国家/地区）或附录 A 术语表中的标准地名

## 格式规范

| 数据形态 | 格式 | 说明 |
|---|---|---|
| 图表源数据 | CSV（UTF-8 无 BOM） | 宽表：列 = 图上可见的系列/维度，行 = 数据点 |
| 网络关系（OpenRank / ModelRank） | 边列表 CSV：`source,target,weight` | 网络可视化工具直接可读 |
| 地理边界 | GeoJSON | 与指标 CSV 通过同一 region_code 关联 |
| 时序 | 宽表 CSV：`date/month, 系列A, 系列B, ...` | |

**不要用 Excel（.xlsx）提交**——二进制无法 diff 和 review。原始拿到的是 Excel 时，在 `raw/` 保留原件，同时转为 CSV 进 `processed/`。

## 三层数据管线

```
data/raw/<周期>/…            OpenDigger 原始导出（只增不改）
        ↓  scripts/build_chart_data.py   按附录 A 指标口径计算
data/processed/chapterX/…    图表源数据（进 git，可 diff、可 review）
        ↓  scripts/render_figures.py     生成最终图片
figures/chapterX/…           报告用图（可由脚本随时重建）
```

## 容量红线

- 单文件 **> 50 MB**：使用 Git LFS
- 单文件 **> 100 MB**：GitHub 拒绝推送；只保留聚合结果，原始数据放 OpenDigger / OSS 并在本 README 登记链接

## 图表 ↔ 数据索引（维护这张表！）

| 图编号 | 图文件 | 数据文件 | 指标口径 | 生成脚本 | 数据来源 |
|---|---|---|---|---|---|
| 图 2-1-1 | figures/chapter2/fig-2-1-1_global_activity_map.png | processed/chapter2/fig-2-1-1_global_activity_map.csv | OpenRank 活跃度 | scripts/build_chart_data.py | OpenDigger 2026-07 导出 |
| 图 3-2-1 | figures/chapter3/fig-3-2-1_company_openrank_top10.png | processed/chapter3/fig-3-2-1_company_openrank_top10.csv | OpenRank 影响力 | scripts/build_chart_data.py | OpenDigger 2026-07 导出 |
| … | … | … | … | … | … |

新增图表时，**必须**在上表登记一行，并同步提交对应的 CSV 数据文件。
