# 第一章双版本样章

原则：一份完整研究底稿，网页与 PDF 两种编排。两种版本独立可读，交互用于进一步探索。

## 内容与编排

- 共同底稿：`chapters/chapter1/本章介绍.md`、`chapters/chapter1/1.1-开源-数字公共品与可持续发展引擎.md`。
- 样章为 A4 纵向；按正文引用位置插图，整图不跨页，页数随版式自动计算并登记在 `sample-manifest.json`。PDF 逐段读取上述底稿，不维护另一份精简或加长的 PDF 正文。
- 沿用图 1-0-1、1-1-1、1-1-2、1-1-3；出版视图位于 `figures/chapter1/print/`，不增加研究图号。
- 图中文字不大于正文的 11.2 pt。Linux 同时展示两类前十排行与各自占比；模型图同时展示 28 个月趋势与四条 Qwen 声明关系；公共价值图采用 SDGs 圆轮与 DPGA 九宫格，完整保留 17 个目标与 9 项条件。
- 章、节与子小节采用明确编号；PDF 同时提供分层书签和页码。网页沿用已发布锚点，增加可见编号。
- 网页交互图保留原设计。浏览器打印调用出版视图；独立 PDF 提供专门的分页与嵌入字体。
- 1.2、1.3 仅同步标题编号，正文和图件不在本轮双版本样章范围内；英语正文仍待翻译。

## 复现

需要 Python、`reportlab`、`fontTools` 与一份合法使用的 Noto Sans CJK SC 常规字体（OFL）。

```bash
python3 preview/web/chapter1_print.py --font /path/to/NotoSansCJKsc-Regular.otf
python3 preview/web/check_chapter1_sample.py
```

生成 PDF：`output/pdf/GOSD-2026-chapter1-sample.pdf`。发布副本与内容校验清单位于 `preview/content/report-assets/chapter1/`。生成后需逐页渲染检查；不可只以文字提取通过作为视觉验收。

数据沿用仓库固定快照。新增派生数值、样本期变更或正文结论变更时，重新生成两种编排并核对清单。正文不堆放来源控制；必要统计范围保留在图中，完整来源登记仍在仓库数据目录与报告数据说明中。

SDGs 与 DPG Standard 的简述分别参考联合国 SDGs 和 DPGA 官方资料；DPG 条件改编注明 CC BY-SA 4.0。出版图不替代完整标准，不表示认证。
