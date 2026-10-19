# 第一章：同一研究底稿，两种编排

原则：一份完整研究底稿，网页与 PDF 两种编排。两种版本独立可读，交互用于进一步探索。

当前审定基线：**GOSD-PUB-20261019**。后续章节先阅读 [BASELINE.md](BASELINE.md)，以其中固定的审定版本作为内容、视觉与交互编排的复用参照。

## 从样章验证到完整章

共同底稿为 `chapters/chapter1/` 下的本章介绍及 1.1、1.2、1.3 四份 Markdown。网页与 PDF 均读取这些文件；不另写一份精简的网页正文或加长的 PDF 正文。章首提出研究路径，1.1 解释共同创造与公共价值，1.2 建立目标，1.3 说明证据及观察方法。

本轮验证形成以下编排规则，可用于后续章节：

1. 先确定正文要解释的判断，再选择静态图必须展示的证据。不能把交互图的某个默认状态直接当作出版图。
2. 图题统一置于图下居中，使用共同的图号与标题；图内保留必要范围、日期、单位和证据边界，删除按钮说明、界面提示及重复标题。
3. 正文先引用，再放图。保持整图不跨页，尽量与引用同页，最多相邻一页；完整段落与节首保留必要阅读空间。
4. 图中文字不大于正文的 11.2 pt。优先调整图的布局和信息层次，不靠放大字号或密集缩排解决问题。
5. 章、节、子小节明确编号；PDF 提供分层书签、页码与页眉，网页保留既有锚点并展示编号。
6. 静态版完整展现理解正文所必需的内容。网页保留筛选、详情及动态连线，打印时采用同一出版视图。
7. 逐页渲染核验字形、图题、分页和留白，并检查正文一致性、数据快照及图文距离；文字提取通过不能替代视觉检查。
8. 同一图件保持主要图形与视觉含义一致：图形结构、对象颜色、顺序和关系共同核验。网页标签页可在 PDF 中展开为分面，悬停信息转为标注。详见 [本轮逐图核验](../docs/publication-visual-parity-20261020.md)。

## 七幅既有图的出版职责

| 图号 | 静态版必须保留的信息 |
| --- | --- |
| 1-0-1 | 六章结构及共同的研究路径 |
| 1-1-1 | Linux 组织与贡献者两类前十排行、贡献记录与各自占比 |
| 1-1-2 | 与网页同形同色的 28 个月占比堆叠柱图，以及四条选定的 Qwen 基础模型声明关系 |
| 1-1-3 | SDGs 圆轮的 17 个目标、DPGA 九宫格的 9 项条件 |
| 1-2-1 | 四大支柱、十个维度及各自观察问题 |
| 1-3-1 | 全部 29 项指标及北极星、驱动、诊断三类用途；不暗示全部指标已经实测 |
| 1-3-2 | 四个支柱与七个主题地图之间的阅读关联及第二章节号 |

出版视图位于 `figures/chapter1/print/`，不新增研究图号。图题、文件名与下载版本由 `preview/web/chapter1_publication.py` 统一管理。中文为本次完整出版正文；英文界面的中文正文仍待翻译。

## 复现与发布

需要 Python、`reportlab`、`fontTools` 与一份合法使用的 Noto Sans CJK SC 常规字体（OFL）。

```bash
python3 preview/web/chapter1_print.py --font /path/to/NotoSansCJKsc-Regular.otf
python3 preview/web/import_report.py --repo-root . --source-ref YOUR_COMMIT
python3 preview/web/build_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
python3 preview/web/check_chapter1_sample.py --output _site --inspect-pdf
```

生成文件：`output/pdf/GOSD-2026-chapter1.pdf`。发布副本与 `chapter-manifest.json` 位于 `preview/content/report-assets/chapter1/`。清单登记页数、图件位置、标题及底稿和数据哈希；页数随编排自动计算。旧样章 PDF 地址保留为完整章副本，避免已分享的下载链接失效。检查脚本保留原文件名以兼容部署流程。

数据沿用仓库固定快照。新增派生数值、样本期或正文结论变更时，应重新生成两种编排并核对清单。完整来源登记保留在仓库数据目录与报告数据说明中。

SDGs 与 DPG Standard 的简述分别参考联合国 SDGs 和 DPGA 官方资料；DPG 条件改编注明 CC BY-SA 4.0。出版图不替代完整标准，不表示认证。

## 前置内容的延伸

统一基线见 [BASELINE.md](BASELINE.md)。首页、目录、执行摘要与引言使用 `outline/frontmatter-editorial.json`、`outline/executive-summary.json`、章节清单及引言原稿作为共同来源。执行摘要 Markdown 从同一内容生成；宣言正文保持原文。

```bash
python3 preview/web/frontmatter_print.py --font /path/to/NotoSansCJKsc-Regular.otf --cover-font /path/to/NotoSerifCJKsc-Regular.otf
python3 preview/web/import_report.py --repo-root . --source-ref YOUR_COMMIT
```

`GOSD-2026-opening-and-chapter1.pdf` 合订前置篇目与已核验的第一章 PDF。前置页采用罗马页码，第一章沿用 1–12 页及原有书签。打印封面将网页悬浮报告的深蓝书封转为平面构图，沿用标题、横线、OSDG 圆盘与 CCOSI 标识，并说明阶段合订范围。执行摘要采用同源专业正文，不含图表或交互切换；宣言全景保留三层七原则，去掉重复图题与编号。封面可使用 Noto Serif CJK SC（OFL）匹配网页衬线标题；未指定时使用正文字体。
