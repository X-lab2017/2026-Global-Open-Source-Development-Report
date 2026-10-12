# GOSD · 全球开源发展报告 Preview

这是报告的架构与阅读体验预览 v0.4，完整研究正文与核验后的数据将按章逐步上线。

## 报告逻辑

GOSD 是报告主品牌；OSDG / OSDGs 连接联合国可持续发展目标；OSDI 是量化评估体系。第一章提供共同框架，第二至第五章是四个核心研究章节，第六章连接行动。

| 章节 | 标签 | 对应研究问题 |
|---|---|---|
| 第二章 全球开源生态观测地图 | GOSO | 全球开源生态的规模、结构与参与格局如何变化？ |
| 第三章 全球开源影响力排行榜 | GOSR | 谁在贡献，贡献如何形成全球影响力？ |
| 第四章 全球开源技术全景洞察 | GOSL | 关键开源技术生态如何组织与演进？ |
| 第五章 全球开源大模型发展洞察 | GOSM | 开源大模型的供给、复用与开放治理如何发展？ |
| 第六章 未来展望与行动建议 | 行动建议 | 不同参与者下一步可以采取哪些行动？ |

## 与研究原稿的边界

本目录是独立网站层，只维护预览的结构、呈现、导航和发布。仓库根目录下的 `chapters/`、`data/`、`figures/`、`outline/`、`appendices/` 和既有 README 均未被本次发布替换。

`content/manifest.json` 为预览目录与状态快照，保留六章、30 个小节及原稿链接。原稿链接仍指向已有规划分支；本次不合并该分支中的研究内容修改。`chapters/` 下仅有先前已审阅的预览引言副本，不充当原研究目录的替代。

`content/assets/` 和 `content/chart-data.js` 是既有预览的数据快照，数值不因网站发布而变更。指标清单不代表全部完成测算，图表试读保留待核验标识。报告 PDF、影片和最终发布资料待后续制作。

## 构建与发布

```bash
python3 preview/web/build_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
python3 preview/web/check_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
```

需要 Python 3.12+，无第三方 Python 或前端依赖。`web/build_portal.py` 复用 `web/build_reader.py` 的章节编排；不要单独运行旧生成器覆盖新页面。

GitHub Actions 工作流只在 `preview/` 或对应工作流变化时生成 `_site/` 并部署 GitHub Pages；使用 Pages 提供的 `base_path`，同时兼容项目子路径与自定义域名。站点发布不回写研究源文件或计算数据。

六项顶栏按“了解—阅读—查证—观看—复用”组织：报告概览、报告全文、指标与数据、互动演示、宣传影片、发布中心。中英文共 48 个页面，支持来源返回、栏目与章节定位、搜索、语言和主题切换；筛选与演示页码保留在 URL。

## 逐章上线方式

先核验研究源稿、方法和配套图表数据，再为对应小节接入正文及证据，更新预览状态，最后审阅后发布。研究正文仍由原目录维护；网站生成结果不作为正文源稿覆盖回仓库。
