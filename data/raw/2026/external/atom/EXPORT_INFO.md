# EXPORT INFO — ATOM 项目数据快照

| 项目 | 内容 |
|---|---|
| 来源 | https://www.atomproject.ai/ （The ATOM Project: American Truly Open Models） |
| 获取方式 | `scripts/fetch_atom_data.js`（下载 Next.js page chunk，解析内嵌图表数据；站点无公开 API） |
| 导出时间 | 2026-10-11（UTC+8） |
| 操作人 | will-ww（经 Kimi Work 代理执行） |
| 数据口径 | 各图注明来源：HuggingFace 下载量/衍生数、OpenRouter 推理 Token、LMArena Elo、ArtificialAnalysis 智能排名、Microsoft AI 用户份额 |

## 文件清单

16 个 JSON 对应站点 16 张图表的完整源数据，命名与图表内容对应（见文件名），`manifest.json` 记录每份数据的字段签名与行数，可用于校验站点改版后的结构漂移。

## 使用注意

- 快照时点数据为页面所示最新（各图更新时间标注为 2025-12 至 2026-03 不等）
- 复现方式：`node scripts/fetch_atom_data.js`（站点改版导致提取数量不符时会输出警告）
- 建议用途：报告第五章（GOSM 大模型）供给格局 / 第一章 AI 时代背景引用
