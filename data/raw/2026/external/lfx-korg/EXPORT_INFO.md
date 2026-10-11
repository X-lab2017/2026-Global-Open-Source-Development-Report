# EXPORT INFO — LFX Insights 项目数据快照（Linux Kernel）

| 项目 | 内容 |
|---|---|
| 来源 | LFX Insights（Linux 基金会）https://insights.linuxfoundation.org/project/korg/contributors |
| API | `https://insights.linuxfoundation.org/api/widget/contributors/<指标>`（公开免认证） |
| 获取方式 | `python scripts/fetch_lfx_data.py korg` |
| 导出时间 | 2026-10-11（UTC+8） |
| 操作人 | will-ww（经 Kimi Work 代理执行） |
| 查询参数 | `project=korg`、`limit=100`、`includeCollaborations=false`、未限定时间范围（全周期） |

## 文件清单

| 文件 | 内容 |
|---|---|
| `contributor-leaderboard.json` | 贡献者排行（全周期共 45,855 名；榜首 David S. Miller 236,673 次，3.73%） |
| `organization-leaderboard.json` | 贡献组织排行 |
| `active-contributors.json` | 活跃贡献者统计 |
| `active-organizations.json` | 活跃组织统计 |
| `geographical-distribution.json` | 贡献者地理分布（美国 7.21%、德国 1.95%、印度 1.91%、中国 1.89%；76% 未标注） |
| `contributor-dependency.json` | 贡献集中度（个人） |
| `organization-dependency.json` | 贡献集中度（组织） |
| `activity-types.json` | 活动类型分布 |
| `manifest.json` | 端点与字节数清单 |

## 使用注意

- **口径**：LFX 的"贡献"为 GrimoireLab 口径的**贡献活动数**（commit/issue/PR 等行为计数），与 OpenDigger 的 OpenRank 不同源，报告中引用必须注明口径，不可直接混算
- 其他项目可将 `korg` 换成对应 slug（如 `kubernetes`），留存(retention)等接口需额外时间参数，暂未纳入
- 建议用途：第一章/第四章基础设施类项目案例引用（Linux Kernel 作为全球协作基准案例）
