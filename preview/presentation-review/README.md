# GOSD 2026：封面至第一章互动演示评审稿

范围：封面、目录导引、执行摘要、引言与宣言、第一章 1.1—1.3。共 36 页；第二章及以后仅在全书定位和第一章阅读导引中提及，不展开其分析。

本目录独立构建，不修改公开 portal、报告正文或 Pages 工作流。评审通过后再把入口接入正式演示页。当前版本的源报告基线为 `c51e3441361407b68f10b339d97eff288319b503`。

## 内容与编辑

- `build_review.py`：共用内容与版式模型，直接读取已审定正文、摘要 JSON、OSDI 字典及案例数据。
- `review.html`：离线互动演示，含翻页、索引、深浅主题、全屏、完整正文、原图、29 项指标详情、月度趋势探索、评审意见保存/导出。
- `native_slides.mjs`：生成原生可编辑文本、图形及三张原生数据图表。每张图带完整数据；PPTX 内的图表工作簿是该次报告数据的快照。
- `build_pptx.mjs`：使用 Artifact Tool 导出并校验 PPTX。在线容器在完整备注下触发节点容量限制，因此采用完整离线 PPTX 交付。
- `attach_pptx.py`：将校验后的 PPTX 嵌入 HTML，使“下载 PPTX”离线可用。
- `check_review.cjs`：浏览器功能、边界检查及逐页截图。截图仅用于内部 QA。

七个编号图件全部保留在正文与来源面板，另保留 Qwen 局部关系图。29 项指标均有独立条目；全文及完整定义/状态也保留在讲者备注中。原始数据、观察范围和证据性质不因讲述版式而改变。

## 构建

在仓库根目录运行，`OUT` 使用绝对路径。需要 Python 3、Playwright Chromium、Noto Sans CJK SC，以及 Codex Artifact Tool 运行时。

```bash
OUT=/absolute/path/review-output
python3 preview/presentation-review/build_review.py --output "$OUT"
node preview/presentation-review/check_review.cjs "$OUT"
node preview/presentation-review/build_pptx.mjs "$OUT"
python3 preview/presentation-review/attach_pptx.py "$OUT"
node preview/presentation-review/check_review.cjs "$OUT"
```

可用 `GOSD_CHROMIUM_PATH` 指定现有浏览器。原生构建依赖 `CODEX_PRIMARY_RUNTIME_NODE_MODULES` 和 `CODEX_PRIMARY_RUNTIME_PYTHON`；校验脚本来自当前 Presentations 技能。最终文件与 `.native-build` 私有检查目录分开。原生导出不覆盖已有最终文件；修改后需另用版本文件名。

## 当前验证

36 页、29 项指标、三张原生图表；数据点分别为 10、10、84。图表嵌入工作簿、包结构、版式几何、字体策略与再次导入检查均通过。逐页渲染人工查看后修正了标点与短列断行。浏览器功能检查覆盖离线打开、键盘翻页、目录、正文、指标详情、趋势月份、全屏、评审记录与 PPTX 下载。

原生 PowerPoint / WPS 应用内的最终打开效果，留待用户本轮评审。未部署 GitHub Pages。
