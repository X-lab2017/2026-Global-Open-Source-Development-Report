# figures/：报告图片目录

本目录存放报告正文中出现的全部图片，与 `data/processed/` 中的图表源数据**同名同构**（同章目录 + 同文件主干名）。

## 规则

1. **一张图一个文件**，命名：`fig-<章号>-<节号>-<序号>_<英文短描述>.png`
2. 图片必须能从对应 CSV 重新生成（见 `scripts/render_figures.py`）；提交图片时**必须同时提交**对应的 `data/processed/` CSV
3. 从飞书文档导出图片时，按图在章节中的出现顺序编号，保持与正文图注一致
4. 优先使用 PNG（无损）；超大示意图可用 JPG

## 目录

```
figures/
├── chapter1/
├── chapter2/      # 2.1–2.7 七张地图的配图
├── chapter3/      # 排行榜配图
├── chapter4/
├── chapter5/
└── chapter6/
```
