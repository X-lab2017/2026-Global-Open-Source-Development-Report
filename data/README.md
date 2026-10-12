# data/：报告数据目录规范

本目录存放《2026 全球开源发展报告》的全部数据资产，遵循**「一张图 ↔ 一个同名 CSV」**原则，保证报告中的每一张图都有可审查、可复现的数据来源。

## 方法与准备状态

[统一指标字典](meta/osdi_indicator_dictionary.csv)维护框架定义，[数据可用性清单](meta/数据可用性清单.md)登记当前文件与待办。GitHub 是数据与方法的维护基准。`raw/2026/external/` 的 LFX korg、ATOM、open-share 快照仅用于背景案例与地图交互底数，不纳入 OSDI。下方索引中的计划路径和脚本不表示均已实现；当前实际文件见[文件清单](meta/dataset_inventory.csv)。

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

## 外部平台快照

### open-share GOSO 地图快照（`raw/2026/external/open-share/`）

第二章 2.1–2.3 世界地图（开发者数量 / 贡献度 / 影响力）的交互底数来自 [open-share.com GOSD 视图](https://open-share.com/insight/open-world/gosd)（GitHub 账号登录，支持中国下钻省级）。端点由站点前端包逆向发现，可用 `scripts/fetch_open_share.py` 全量重取：

- 全球：`https://selfoss.open-digger.cn/openshare/overview/{metric}.json`，`metric ∈ developers | contribution | influence`；`overview_half_year/` 为半年度变体
- 国家下钻：`.../overview/{CC}/{metric}.json`（当前仅 CN、US 开放下钻）
- 地理边界：`https://open-share.com/geo/{world|CN|US}.json`

文件结构：`leaderboards[].data[]` 含 `rank / name（英文国名，与世界 GeoJSON 的 properties.name 匹配）/ name_zh / value / change / code（ISO 3166）`。省级数据 `name_zh` 与中国 GeoJSON 的 `properties.fullname` 精确匹配。快照时间：2026-10-11。

## 图表 ↔ 数据索引（维护这张表！）

| 图编号 | 图文件 | 数据文件 | 指标口径 | 生成脚本 | 数据来源 |
|---|---|---|---|---|---|
| 图 2-1-1 | figures/chapter2/fig-2-1-1_global_activity_map.png | processed/chapter2/fig-2-1-1_global_activity_map.csv | Activity 活跃度 | scripts/build_chart_data.py | OpenDigger 2026-07 导出 |
| 图 2-1-2 | figures/chapter2/fig-2-1-2_five_region_total_developers.png | processed/chapter2/fig-2-1-2_five_region_total_developers.csv | 开发者总量 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2026统计周期 |
| 图 2-1-3 | figures/chapter2/fig-2-1-3_five_region_active_developers_trend.png | processed/chapter2/fig-2-1-3_five_region_active_developers_trend.csv | 年度活跃开发者数量 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2-2-2 | figures/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.png | processed/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.csv | 开发者 OpenRank 贡献度 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2-3-2 | figures/chapter2/fig-2-3-2_five_region_project_openrank_influence_trend.png | processed/chapter2/fig-2-3-2_five_region_project_openrank_influence_trend.csv | 项目 OpenRank 影响力 | 待接入统一构建脚本 | OpenDigger、Gitee、AtomGit，2022—2026 |
| 图 2-4-1 | figures/chapter2/fig-2-4-1_global_open_source_talent_map.png | processed/chapter2/fig-2-4-1_global_open_source_talent_map.csv | 前5%开源人才数量（国家/地区分布） | 待接入统一构建脚本 | OpenDigger，截至2026年7月 |
| 图 2-4-2 | figures/chapter2/fig-2-4-2_five_region_open_source_talent_trend.png | processed/chapter2/fig-2-4-2_five_region_open_source_talent_trend.csv | 前5%开源人才数量（五域趋势） | 待接入统一构建脚本 | OpenDigger，2022—2026 |
| 图 2-4-3 | figures/chapter2/fig-2-4-3_china_city_open_source_talent_map.png | processed/chapter2/fig-2-4-3_china_city_open_source_talent_map.csv | 前5%开源人才数量（中国市级分布） | 待接入统一构建脚本 | OpenDigger，截至2026年7月 |
| 图 2-4-4 | figures/chapter2/fig-2-4-4_china_top10_city_talent_trend.png | processed/chapter2/fig-2-4-4_china_top10_city_talent_trend.csv | 前5%开源人才数量（城市趋势） | 待接入统一构建脚本 | OpenDigger，2022—2026 |
| 图 2-5-1 | figures/chapter2/fig-2-5-1_country_contribution_share_trend.png | processed/chapter2/fig-2-5-1_country_contribution_share_trend.csv | 国家贡献占全球比例 | 待接入统一构建脚本 | OpenDigger，2022—2026 |
| 图 2-5-2 | figures/chapter2/fig-2-5-2_cross_border_project_contribution_flow.png | processed/chapter2/fig-2-5-2_cross_border_project_contribution_flow.csv | 开发者来源国对项目所属国的 OpenRank 贡献流向 | 待接入统一构建脚本 | OpenDigger，2026统计周期 |
| 图 2-6-1 | figures/chapter2/fig-2-6-1_foundation_share_and_active_repositories.png | processed/chapter2/fig-2-6-1_foundation_share_and_active_repositories.csv | 基金会项目 OpenRank 占比、活跃仓库数 | 待接入统一构建脚本 | OpenDigger、基金会项目清单，2022—2026 |
| 图 2-6-2 | figures/chapter2/fig-2-6-2_active_repository_license_trend.png | processed/chapter2/fig-2-6-2_active_repository_license_trend.csv | 按许可证统计的活跃仓库数 | 待接入统一构建脚本 | OpenDigger events，2022—2026 |
| 图 2-6-3 | figures/chapter2/fig-2-6-3_mulan_permissive_license_trend.png | processed/chapter2/fig-2-6-3_mulan_permissive_license_trend.csv | 累计活跃仓库数、项目 OpenRank 影响力 | 待接入统一构建脚本 | OpenDigger events，2022—2026 |
| 图 2-7-1 | figures/chapter2/fig-2-7-1_platform_active_repository_trend.png | processed/chapter2/fig-2-7-1_platform_active_repository_trend.csv | 有效活跃仓库数 | 待接入统一构建脚本 | GitHub、Gitee、GitCode、GitLab，2022—2026 |
| 图 3.1 | figures/chapter3/fig-3-1-1_gosr_framework.png | 无（框架图，数据即各榜榜首） | - | - | - |
| 图 3.2 | figures/chapter3/fig-3-2-1_global_company_yearly_rank.png | processed/chapter3/fig-3-2-1_global_company_yearly_rank.csv | 企业 OpenRank 年度排名（2026 为统计周期口径） | OSreport2026/export_top100/dump_chapter3_data.py | OpenDigger，2016—2026 |
| 图 3.3 | figures/chapter3/fig-3-2-2_global_company_monthly_rank.png | processed/chapter3/fig-3-2-2_global_company_monthly_rank.csv | 企业 OpenRank 月度排名 | 同上 | OpenDigger，2025.7—2026.6 |
| 图 3.4 | figures/chapter3/fig-3-2-3_china_company_yearly_rank.png | processed/chapter3/fig-3-2-3_china_company_yearly_rank.csv | 中国企业 OpenRank 年度排名 | 同上 | OpenDigger，2016—2026 |
| 图 3.5 | figures/chapter3/fig-3-2-4_china_company_monthly_rank.png | processed/chapter3/fig-3-2-4_china_company_monthly_rank.csv | 中国企业 OpenRank 月度排名 | 同上 | OpenDigger，2025.7—2026.6 |
| 图 3.6 | figures/chapter3/fig-3-3-1_foundation_monthly_rank.png | processed/chapter3/fig-3-3-1_foundation_monthly_rank.csv | 基金会 OpenRank 月度排名（Linux 家族合并口径） | 同上 | OpenDigger，2025.7—2026.6 |
| 图 3.6-1 | figures/chapter3/fig-3-6-1_model_influence_top20.png | processed/chapter3/fig-3-6-1_model_influence_top20.csv | ModelRank 2026年8月模型影响力 Top 20；分值为数值，不是占比 | 待接入统一构建脚本 | OpenGauge ModelRank v1、Hugging Face，2026-08 |
| 图 3.6-2 | figures/chapter3/fig-3-6-2_model_influence_country_publishers.png | processed/chapter3/fig-3-6-2_model_influence_country_publishers.csv | Top 20 按发布者国家与发布者计数 | 待接入统一构建脚本 | 同上 |
| 图 3.6-3 | figures/chapter3/fig-3-6-3_model_influence_task_distribution.png | processed/chapter3/fig-3-6-3_model_influence_task_distribution.csv | Top 20 按模型任务计数与占比 | 待接入统一构建脚本 | 同上 |
| 图 4.2-1 | figures/chapter4/fig-4-2-1_model_landscape_recent_downloads.png | processed/chapter4/fig-4-2-1_model_landscape_recent_downloads.csv | 六任务领域各 Top 16；近30天下载量 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2026-10-02 |
| 图 4.2-2 | figures/chapter4/fig-4-2-2_model_landscape_total_downloads.png | processed/chapter4/fig-4-2-2_model_landscape_total_downloads.csv | 六任务领域各 Top 16；累计下载量 | 待接入统一构建脚本 | 同上 |
| 图 4.2-3 | figures/chapter4/fig-4-2-3_model_landscape_likes.png | processed/chapter4/fig-4-2-3_model_landscape_likes.csv | 六任务领域各 Top 16；累计点赞量 | 待接入统一构建脚本 | 同上 |
| 图 5-2（5.1-1） | figures/chapter5/fig-5-1-1_hf_cumulative_models_publishers.png | processed/chapter5/fig-5-1-1_hf_cumulative_models_publishers.csv | 各年9月13日累计模型数与发布者数 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2026-09-13快照回溯 |
| 图 5-3（5.1-2） | figures/chapter5/fig-5-1-2_country_model_contribution.png | processed/chapter5/fig-5-1-2_country_model_contribution.csv | 国家模型数、累计下载量、点赞量及其已识别国家内份额；含未知归属；region_code 为 ISO 3166 编码 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2026-09-13 |
| 图 5-4（5.1-3） | figures/chapter5/fig-5-1-3_country_monthly_new_models.png | processed/chapter5/fig-5-1-3_country_monthly_new_models.csv | 中、美、法、德月度新增模型数 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2025-09—2026-08 |
| 图 5-5（5.2-1） | figures/chapter5/fig-5-2-1_hf_cumulative_derivation.png | processed/chapter5/fig-5-2-1_hf_cumulative_derivation.csv | 各年9月13日累计派生模型数及其在累计模型中的占比 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2026-09-13快照回溯 |
| 图 5-6（5.2-2） | figures/chapter5/fig-5-2-2_cross_country_derivation_flows.png | processed/chapter5/fig-5-2-2_cross_country_derivation_flows.csv | 双端国家可识别且跨国的10,943对基座—派生关系；ISO国家编码 | 待接入统一构建脚本 | Hugging Face、OpenGauge，2026-09-13 |
| 图 5-7（5.2-3） | figures/chapter5/fig-5-2-3_modelrank_country_head_trend.png | processed/chapter5/fig-5-2-3_modelrank_country_head_trend.csv | Top 20/100/1000 国家席位与逐月 Top 100 变化；未知归属保留 | 待接入统一构建脚本 | OpenGauge ModelRank v1，2024-07—2026-08 |
| 图 5-8（5.3-1） | figures/chapter5/fig-5-3-1_openness_quadrants.png | processed/chapter5/fig-5-3-1_openness_quadrants.csv | 870模型的完整性×开放性四类数量与占比 | 待接入统一构建脚本 | OpenGauge 既有开放性评估，2026-09-14提取；未重新评估 |
| 图 5-9（5.3-2） | figures/chapter5/fig-5-3-2_openness_region_structure.png | processed/chapter5/fig-5-3-2_openness_region_structure.csv | 中国、美国、欧洲、其他国家、归属未知五组样本量与四类结构 | 待接入统一构建脚本 | 同上 |
| 图 5-10（5.3-3） | figures/chapter5/fig-5-3-3_openness_publisher_types.png | processed/chapter5/fig-5-3-3_openness_publisher_types.csv | 四类发布主体的模型数与“双高”数量、比例；非营利组织和高校合并 | 待接入统一构建脚本 | 同上 |

新增定量图表时，**必须**在上表登记一行，并同步提交对应的 CSV 数据文件。框架和流程等概念图在 `figures/` 中登记结构来源，不为概念图虚构数据CSV。

本轮仅补充 3.6、4.2 和第五章的图表数据，图文件列为以后统一绘图使用的计划路径，**图片尚未上传**。图 5-2、图 5-4、图 5-5 按2026年9月13日仍可见的模型仓库回溯创建时间，不是历年独立留存的历史快照。图 5-3 已在本地用对应 CSV 的2026年9月13日国家数据重绘地图，并更新 5.1 报告插图；原2026年8月23日截图仅作为历史留档，未用于新版插图。第4.2节仓库按发布者国家标注，不代表其上游基座模型的开发者国家；未知归属保留，不按模型名称猜测。第5.3节使用既有870模型评估，2026年9月14日提取结果，未在该日重新评估。

### 本轮图表字段与重绘说明

- 3.6 的 `modelrank_value` 对应 OpenGauge ModelRank v1 的 `score_normalized`，采用当月归一化分值 `score` × 当月模型数的数值尺度；2026年8月模型数为931,886，分值不是百分比。榜单按该分值降序排列。
- 4.2 的 `rank` 在每个 `domain_key` 内独立排序，每领域16个模型；领域按文本、图像与视频、语音与音频、多模态、嵌入与检索、机器人排列。`downloads` 为近30天下载量，`downloads_all_time` 为累计下载量，`likes` 为累计点赞量。`model_name` 仅去掉 `model_id` 的发布者前缀。`publisher_logo_url` 和 `publisher_logo_sha256` 提供原图所用发布者公开标识的地址与SHA-256校验值；只提交引用信息，不提交图片内容。国旗由 `country_code` 生成；空编码结合 `country` 区分 Unknown 与 International。
- 图5-3地图使用全部52个已识别国家的 `models` 值；未知归属不映射到地图。右侧显示US、CN、FR、DE、FI、GB、KR、JP、SG、CA、IN，按模型数降序排列；其余已识别国家合计为“其他国家”，列于末尾。`*_known_share_pct` 的分母为已识别国家相应指标合计，`*_global_share_pct` 的分母包含未知归属；百分比字段使用0—100尺度。
- 图5-7左侧取最新月份的 `k=20/100/1000` 国家席位，右侧取逐月 `k=100` 席位；同一个月在不同 `k` 下各有一行，不是重复记录。`china`、`us`、`other_known`、`unknown` 合计等于 `k`，各比例字段使用0—100尺度。
- 5.3 的高完整为L3—L5，低完整为L1—L2；高开放为O2—O4，低开放为O1。四类占比分母为全部870个评估模型；区域图中的 `high_open_pct` 分母为本组 `n`，组织类型图中的 `double_high_pct` 分母为本类 `models`。“双高”同时满足高完整和高开放。欧洲采用评估结果已有的Europe标签；中国和美国单列，其余已知国家归为其他国家，国家未知单列。非营利组织和高校按两类数量相加，比例使用合并后的数量重新计算。

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
| 表 3.6-1 | processed/chapter3/table-3-6-1_model_series_versions.csv | ModelRank Top 20中 Qwen、Llama 入榜系列与版本 | OpenGauge ModelRank v1，2026-08 |

尚未接入统一原始数据构建管线的文件，在索引中标记为“待接入统一构建脚本”，后续应补齐对应查询或转换脚本，避免将人工整理结果误标为全流程自动生成。
