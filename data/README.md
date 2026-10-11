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

## 报告年度与统计窗口

主编于 2026-10-11 确认：2022—2026 年主年度序列统一采用“上年 7 月 1 日至当年 6 月 30 日”。本报告中的年度标签指报告年度。

| 报告年度 | 统计开始日 | 统计结束日（含） |
|---|---|---|
| 2022 | 2021-07-01 | 2022-06-30 |
| 2023 | 2022-07-01 | 2023-06-30 |
| 2024 | 2023-07-01 | 2024-06-30 |
| 2025 | 2024-07-01 | 2025-06-30 |
| 2026 | 2025-07-01 | 2026-06-30 |

统计图在图注或方法说明中标明上述周期。存量指标另标截至日期；外部补充快照保留实际观测期间。周期定义已经确认，现有 CSV 是否与之完全一致仍需逐图核验，同时检查历年平台覆盖、算法和对象定义，不仅检查年份标签。

## 开发者身份与跨平台去重

主编于 2026-10-11 确认：已有并经过验证的跨平台开发者身份映射覆盖 **GitHub、Gitee、AtomGit、GitLab**，支持 **2022—2026 全部报告年度**，各年的统计窗口见上表。

主编进一步确认：上述四个平台的开发者活动数据全部支持 2022—2026 年连续、跨地区的同口径比较。在此基础上，主编决定：代码生态全球主榜与主趋势以 **GitHub 为主范围，Gitee、AtomGit、GitLab 作补充**。相关数据包应提供各平台各年的地区与事件覆盖说明，逐图检查实际导出与计算流程；此项确认不等于现有图表复核完成。

- **平台账号数**：按“平台—用户 ID”去重。
- **跨平台开发者数**：在映射适用范围内，合并同一开发者的跨平台账号后计数；保留平台账号数供核对，不能把各平台账号数直接相加当作去重人数。
- 每张相关图表的数据说明应登记实际纳入的平台、映射版本/方法、验证记录、匹配覆盖率、未匹配及冲突处理，并说明 GitLab 的实例范围。四个平台被覆盖不等于每个账号均已成功匹配。
- 主榜与 2022—2026 主趋势只纳入 GitHub 活动记录，使用共同报告窗口和指标方法，计数单位与去重规则随指标标明。跨平台身份映射不把其他平台活动并入主范围。
- Gitee、AtomGit、GitLab 的补充分析列明实际平台组合；合并开发者人数时使用适用的身份映射，保留账号数供核对。主榜与补充结果分别展示、命名与下载。
- 现有索引中含多平台来源的图表需在 B03 核清组成，取得 GitHub 单平台结果后才用于主趋势；经核验的多平台结果可单列补充。GitHub 主范围结果不得标为全部平台的完整总量。
- 此处记录主编确认的映射能力，不表示现有 CSV 已应用该映射。逐图核验时检查实际计算流程，必要时重算；本轮不修改现有数值。

## 机器人与自动化服务账号

主编于 2026-10-11 确认：**现有开发者统计已识别并剔除机器人和自动化服务账号**。开发者人数与活跃开发者人数的口径说明据此注明排除范围；配套账号数标明剔除前/后。

相关数据包应记录识别规则及版本、各平台各年度的剔除数量和执行流程，在逐图核验时检查一致性。本次确认不代表所有自动化账号均已被识别，也不推定 OpenRank 网络或项目影响力计算删除了同样的账号与事件。人类使用 AI 辅助工具不直接作为机器人判据，AI 生成代码检测不属于此次确认范围。

本轮记录主编确认的处理状态，不修改现有 CSV 数值。开发者所在地来源见下节，缺失处理与项目聚合规则仍按 A02 逐项确定。

## 开发者所在地来源

主编于 2026-10-11 确认：**使用公开个人资料中的所在地，经标准化处理**。国家/地区分布与跨地区贡献图表应注明这一依据；所在地不等同于国籍、出生地或雇主所在地，也不代表已独立验证实际居住地。

相关数据包登记位置字段来源、采集/快照时间与标准化方法/版本，并区分国家级、城市级等可识别粒度。主编已确认：**2022—2026年地区统计分别使用各报告年度对应的历史位置快照**，不以同一最新位置快照回算所有年份。

各年度需登记位置快照的实际日期、来源平台、文件/版本和报告年度的关联，不假定所有快照均采集于报告期末6月30日。GitHub主范围关联该年度GitHub快照，多平台补充记录各平台快照及其时点差异。位置代表快照时点公开资料所载所在地，不代表全年居住地；位置变化可能影响地区趋势。历史快照位置缺失按下述未知地区规则处理，不自动用最新位置回填。跨平台位置冲突的消解规则仍待确认。

主编已决定：**位置缺失或无法可靠标准化的开发者仍计入全球总量，地区标为未知并单列**。这些记录仍须满足该人数指标的活动、去重和机器人排除条件。国家可识别、城市不可识别时，进入相应国家统计，城市级保留为未知；不得强行推断具体地区。

同一平台范围、报告年度与计数单位下，各地理层级分别核对：全球总量 = 已定位数量 + 未知数量，位置识别率 = 已定位数量 / 全球总量。同一对象在同一层级仅计入一个地区或未知类别，逐年披露识别率。标为“占全球比例”的指标以含未知地区的全球总量为分母，并显示未知数量或占比；只在已定位样本内计算的比例须另标“已定位开发者中的占比”。分母为零时记为不适用。

GitHub主范围与各多平台补充范围分别计算以上数量与比例。开发者所在地规则不自动成为项目或组织的归属规则。本轮不修改现有CSV或计算未取得的识别率。

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
| 图 3-2-1 | figures/chapter3/fig-3-2-1_company_openrank_top10.png | processed/chapter3/fig-3-2-1_company_openrank_top10.csv | OpenRank 影响力 | scripts/build_chart_data.py | OpenDigger 2026-07 导出 |
| … | … | … | … | … | … |

新增图表时，**必须**在上表登记一行，并同步提交对应的 CSV 数据文件。

## 第二章报告表格数据

| 表编号 | 数据文件 | 指标口径 | 数据来源 |
|---|---|---|---|
| 表 2.1 | processed/chapter2/table-2-2-1_china_province_openrank_per_capita_top10.csv | 省市 OpenRank 贡献度 ÷ 活跃开发者数量 | OpenDigger 2026统计周期 |
| 表 2.2 | processed/chapter2/table-2-4-1_china_city_talent_top10.csv | 个人 OpenRank 累计值位居全部开发者前5% | OpenDigger，截至2026年7月 |
| 表 2.3 | processed/chapter2/table-2-5-1_china_us_project_contribution_top10.csv | 开发者来源国对项目所属国的 OpenRank 贡献度 | OpenDigger 2026统计周期 |

尚未接入统一原始数据构建管线的文件，在索引中标记为“待接入统一构建脚本”，后续应补齐对应查询或转换脚本，避免将人工整理结果误标为全流程自动生成。
