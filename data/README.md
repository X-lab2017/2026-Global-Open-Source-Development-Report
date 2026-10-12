# data/：报告数据目录规范

本目录存放《2026 全球开源发展报告》的全部数据资产，遵循**「一张图 ↔ 一个同名 CSV」**原则，保证报告中的每一张图都有可审查、可复现的数据来源。

## 方法与准备状态

[统一指标字典](meta/osdi_indicator_dictionary.csv)维护框架定义，[数据可用性清单](meta/数据可用性清单.md)登记当前文件与待办。GitHub 是数据与方法的维护基准。`raw/2026/external/` 的 LFX korg、ATOM 快照仅用于背景案例，不纳入 OSDI。下方索引中的计划路径和脚本不表示均已实现；当前实际文件见[文件清单](meta/dataset_inventory.csv)。

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
| 图 2-1-1 | figures/chapter2/fig-2-1-1_global_activity_map.png | processed/chapter2/fig-2-1-1_global_activity_map.csv | Activity 活跃度 | scripts/build_chart_data.py | OpenDigger 2026-07 导出 |
| 图 2.2 | figures/chapter2/fig-2-1-2_five_region_total_developers.png | processed/chapter2/fig-2-1-2_five_region_total_developers.csv | 开发者总量 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2026统计周期 |
| 图 2.3 | figures/chapter2/fig-2-1-3_five_region_active_developers_trend.png | processed/chapter2/fig-2-1-3_five_region_active_developers_trend.csv | 年度活跃开发者数量 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2.6 | figures/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.png | processed/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.csv | 开发者 OpenRank 贡献度 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2.9 | figures/chapter2/fig-2-3-2_five_region_project_openrank_influence_trend.png | processed/chapter2/fig-2-3-2_five_region_project_openrank_influence_trend.csv | 项目 OpenRank 影响力 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2.13 | figures/chapter2/fig-2-4-4_china_top10_city_talent_trend.png | processed/chapter2/fig-2-4-4_china_top10_city_talent_trend.csv | 前5%开源人才数量 | 待接入统一构建脚本 | OpenDigger，2022—2026 |
| 图 2.14 | figures/chapter2/fig-2-5-1_country_contribution_share_trend.png | processed/chapter2/fig-2-5-1_country_contribution_share_trend.csv | 国家贡献占全球比例 | 待接入统一构建脚本 | OpenDigger，2022—2026 |
| 图 2.16 | figures/chapter2/fig-2-6-1_foundation_share_and_active_repositories.png | processed/chapter2/fig-2-6-1_foundation_share_and_active_repositories.csv | 基金会项目 OpenRank 占比、活跃仓库数 | 待接入统一构建脚本 | OpenDigger、基金会项目清单，2022—2026 |
| 图 2.17 | figures/chapter2/fig-2-6-2_active_repository_license_trend.png | processed/chapter2/fig-2-6-2_active_repository_license_trend.csv | 按许可证统计的活跃仓库数 | 待接入统一构建脚本 | OpenDigger events，2022—2026 |
| 图 2.18 | figures/chapter2/fig-2-6-3_mulan_permissive_license_trend.png | processed/chapter2/fig-2-6-3_mulan_permissive_license_trend.csv | 累计活跃仓库数、项目 OpenRank 影响力 | 待接入统一构建脚本 | OpenDigger events，2022—2026 |
| 图 2.19 | figures/chapter2/fig-2-7-1_platform_active_repository_trend.png | processed/chapter2/fig-2-7-1_platform_active_repository_trend.csv | 有效活跃仓库数 | 待接入统一构建脚本 | GitHub、Gitee、GitCode、GitLab，2022—2026 |
| 图 3.1 | figures/chapter3/fig-3-1-1_gosr_framework.png | 无（框架图，数据即各榜榜首） | - | - | - |
| 图 3.2 | figures/chapter3/fig-3-2-1_global_company_yearly_rank.png | processed/chapter3/fig-3-2-1_global_company_yearly_rank.csv | 企业 OpenRank 年度排名（2026 为统计周期口径） | OSreport2026/export_top100/dump_chapter3_data.py | OpenDigger，2016—2026 |
| 图 3.3 | figures/chapter3/fig-3-2-2_global_company_monthly_rank.png | processed/chapter3/fig-3-2-2_global_company_monthly_rank.csv | 企业 OpenRank 月度排名 | 同上 | OpenDigger，2025.7—2026.6 |
| 图 3.4 | figures/chapter3/fig-3-2-3_china_company_yearly_rank.png | processed/chapter3/fig-3-2-3_china_company_yearly_rank.csv | 中国企业 OpenRank 年度排名 | 同上 | OpenDigger，2016—2026 |
| 图 3.5 | figures/chapter3/fig-3-2-4_china_company_monthly_rank.png | processed/chapter3/fig-3-2-4_china_company_monthly_rank.csv | 中国企业 OpenRank 月度排名 | 同上 | OpenDigger，2025.7—2026.6 |
| 图 3.6 | figures/chapter3/fig-3-3-1_foundation_monthly_rank.png | processed/chapter3/fig-3-3-1_foundation_monthly_rank.csv | 基金会 OpenRank 月度排名（Linux 家族合并口径） | 同上 | OpenDigger，2025.7—2026.6 |

新增定量图表时，**必须**在上表登记一行，并同步提交对应的 CSV 数据文件。框架和流程等概念图在 `figures/` 中登记结构来源，不为概念图虚构数据CSV。

## 第二章报告表格数据

| 表编号 | 数据文件 | 指标口径 | 数据来源 |
|---|---|---|---|
| 表 2.1 | processed/chapter2/table-2-2-1_china_province_openrank_per_capita_top10.csv | 省市 OpenRank 贡献度 ÷ 活跃开发者数量 | OpenDigger 2026统计周期 |
| 表 2.2 | processed/chapter2/table-2-4-1_china_city_talent_top10.csv | 个人年度全域 OpenRank 前5%（总体与汇总规则待核验） | OpenDigger，截至2026年7月 |
| 表 2.3 | processed/chapter2/table-2-5-1_china_us_project_contribution_top10.csv | 开发者来源国对项目所属国的 OpenRank 贡献度 | OpenDigger 2026统计周期 |

## 第三章报告表格数据

| 表编号 | 数据文件 | 指标口径 | 数据来源 |
|---|---|---|---|
| 表 3.1 | processed/chapter3/table-3-0-1_gosr_top1_overview.csv | 五大榜单榜首与中国最高位次速览 | OpenDigger 2026统计周期 |
| 表 3.2 | processed/chapter3/table-3-1-1_global_division_openrank_top30.csv | 行政区划开发者 OpenRank（OpenWorld 口径） | OpenDigger 2026统计周期 |
| 表 3.3 | processed/chapter3/table-3-1-2_division_country_entry_counts.csv | Top 100 各国入选行政区数量（全量） | OpenDigger 2026统计周期 |
| 表 3.4 | processed/chapter3/table-3-1-3_china_province_openrank_top30.csv | 中国省级行政区开发者 OpenRank | OpenDigger 2026统计周期 |
| 表 3.5 | processed/chapter3/table-3-1-4_china_city_openrank_top30.csv | 中国城市级开发者 OpenRank | OpenDigger 2026统计周期 |
| 表 3.6 | processed/chapter3/table-3-2-1_global_company_openrank_top30.csv | 企业 OpenRank、活跃仓库数、活跃开发者数 | OpenDigger 2026统计周期 |
| 表 3.7 | processed/chapter3/table-3-2-2_china_company_openrank_top30.csv | 中国企业 OpenRank、活跃仓库数、活跃开发者数 | OpenDigger 2026统计周期 |
| 表 3.8 | processed/chapter3/table-3-3-1_global_foundation_openrank.csv | 基金会 OpenRank（Linux 家族合并口径）、活跃开发者数 | OpenDigger 2026统计周期 |
| 表 3.9 | processed/chapter3/table-3-4-1_global_project_openrank_top30.csv | 项目 OpenRank、活跃开发者数 | OpenDigger 2026统计周期 |
| 表 3.10 | processed/chapter3/table-3-4-2_project_country_distribution_top100.csv | Top 100 项目发起组织国家分布（全量） | OpenDigger 2026统计周期 |
| 表 3.11 | processed/chapter3/table-3-4-3_china_project_openrank_top30.csv | 中国项目 OpenRank、活跃开发者数 | OpenDigger 2026统计周期 |
| 表 3.12 | processed/chapter3/table-3-4-4_china_project_rising.csv | 中国项目两期名次对比（跃升先锋） | OpenDigger 2026统计周期 vs 基期 |
| 表 3.13 | processed/chapter3/table-3-5-1_new_repo_openrank_top30.csv | 本年新创建仓库 OpenRank、创建时间 | OpenDigger 2026统计周期 |
| 表 3.14 | processed/chapter3/table-3-5-2_new_project_openrank_top30.csv | 本年新创立项目 OpenRank、平台、创建时间 | OpenDigger 2026统计周期 |
| 表 3.15 | processed/chapter3/table-3-5-3_new_repo_domain_distribution.csv | 新仓库技术领域分布（人工标注复核） | OpenDigger 2026统计周期 |
| 表 3.16 | processed/chapter3/table-3-5-4_new_repo_language_distribution.csv | 新仓库主要编程语言分布 | OpenDigger repo_info + 人工标注 |

尚未接入统一原始数据构建管线的文件，在索引中标记为“待接入统一构建脚本”，后续应补齐对应查询或转换脚本，避免将人工整理结果误标为全流程自动生成。
