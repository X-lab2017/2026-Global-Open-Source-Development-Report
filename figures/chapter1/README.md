# 第一章图件

七幅图的可编辑 SVG 与 PDF 共用 `print/` 下的出版视图。根目录同名文件保留既有引用地址，内容同步更新；`fig-1-1-2_qwen_case.svg` 为同一图中 B 分面的单独导出。

- 图 1-0-1：六章结构，四个研究章节并列。
- 图 1-1-1：Linux 组织与贡献者横向排行。
- 图 1-1-2：28 个月占比堆叠柱图与 Qwen 声明关系。
- 图 1-1-3：SDG 圆轮与 DPGA 九宫格。
- 图 1-2-1：四行支柱与十个维度。
- 图 1-3-1：2×2 支柱全貌，展开 29 项指标。
- 图 1-3-2：四支柱与七主题之间的阅读关联。

图号、题名、数据、颜色含义、顺序及拓扑与网页保持一致。说明与交互详情可以按媒介展开，结构示意不代表权重或因果关系。

生成全部图件与 PDF：`python3 preview/web/chapter1_print.py --font /path/to/NotoSansCJKsc-Regular.otf`。
仅同步单图文件：`python3 preview/web/export_chapter_visuals.py --repo-root .`。

完整规则见 [出版基线](../../preview/print/BASELINE.md)。品牌来源与历史母版保留于 `X-lab2017/osdg-brand` 及版本历史；当前框架为按相同指标词典编排的出版视图。SDGs 与 DPGA 条件保留原始归属，DPG Standard 简述遵循 CC BY-SA 4.0。
