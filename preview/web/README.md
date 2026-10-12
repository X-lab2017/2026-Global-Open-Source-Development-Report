# GOSD Preview 网站生成器

v0.6 输出中英文共 50 个静态页面。共享六项顶栏保留“报告概览、报告全文、指标与数据、互动演示、宣传影片、发布中心”的顺序。

## 内容维护

GitHub 根目录的 `chapters/`、`appendices/`、`data/` 和 `figures/` 是正式维护位置。第一章与附录 A 在线全文来自原 Markdown；指标词典来自 `data/meta/osdi_indicator_dictionary.csv`，文件目录来自 `data/meta/dataset_inventory.csv`。不要在网站快照中单独修改正文和数据。

`import_report.py` 生成 `content/report.json` 和 `content/report-assets/`，记录原稿引用版本、原文校验值及原样 CSV。更新 processed 文件后须同步登记文件清单及 SHA-256；导入校验防止网站沿用过期元数据。原始背景快照不进入指标文件计数。

报告仓库中运行：

```sh
python3 preview/web/import_report.py --repo-root . --source-ref main
python3 preview/web/build_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
python3 preview/web/check_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
python3 preview/web/check_report.py --output _site
```

GitHub Actions 使用当次提交 SHA 作为来源版本。Sites 镜像使用相同生成器与已导入快照，省略 `--base-path`。构建只输出网站，不修改报告原稿与数据。

## 阅读与查证

- 第一章连续阅读：本章路径、节内目录、稳定锚点、阅读进度、打印、两张 SVG 原图放大与下载。
- 附录 A 完整呈现方法、统计周期、样本与解释边界。
- 指标页 `q` / `pillar`、文件页 `q` / `chapter` 保留筛选；深链接展开对应条目。
- 图表页保留 `mode` / `year` / `regions` / `table`；八页内容导览保留 `slide`。
- 共享 `portal.js` 处理主题、六栏目导航、搜索及返回来处；`report.js` 处理正文与证据交互。
- 英文界面展示已接入的中文原稿并明确翻译状态，避免把结构翻译当作全文翻译。

## 状态边界

第一章框架批准进入 Preview 不表示 29 项指标全部测算完成。第二、三章 CSV 提供原文件下载和核验说明；其余章节继续保留结构与原稿入口。ModelRank 暂为概念说明。正式 PDF、宣传影片与媒体包保留待制作状态。

`check_portal.py` 检查双语路由、导航与内部链接；`check_report.py` 检查正文、指标对应及下载数据字节一致性。SVG 已使用轮廓字形。静态检查不替代实际浏览器和打印审阅。

## 第一章交互图

`chapter_visuals.py` 生成五幅交互图的可读默认状态，`chapter-visuals.js` 添加选择、悬停和键盘行为。Linux 可切换观察对象；模型图读取 28 个月的固定快照；目标图保留 14 个原图区域；OSDI 地图读取统一的29项定义。手机端提供目标选择菜单。

`content/story-data.json` 是 `data/raw/2026/external/` 中三份已指定快照的派生展示副本，包含原文件 SHA-256，不纳入 processed 计数。每次导入都会同步。静态图可通过 `export_chapter_visuals.py --repo-root <报告仓库>` 再生成，需安装 Noto Sans SC 才能保持相同字体。

校验：`python3 preview/web/check_chapter_visuals.py --output _site --repo-root .`。

交互链接可保留 `linux`、`modelMonth`、`sdg`、`dpg`、`goal`、`indicator` 和 `role` 选择参数。
