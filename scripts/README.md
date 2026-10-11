# scripts/：数据计算与图表生成脚本

本目录存放报告数据的处理管线脚本，实现「原始数据 → 图表源数据 → 图片」的可复现流程。

## 约定

| 脚本 | 职责 | 输入 | 输出 |
|---|---|---|---|
| `build_chart_data.py` | 按附录 A（`data/meta/`）的指标口径，从原始数据计算图表源数据 | `data/raw/<周期>/` | `data/processed/chapterX/*.csv` |
| `render_figures.py` | 从图表源数据渲染报告用图 | `data/processed/` | `figures/chapterX/*.png` |

## 要求

- 脚本只读取 `data/raw/`，**不修改原始数据**
- 所有中间参数（统计周期、指标权重、过滤条件）通过命令行参数或配置文件显式传入，不硬编码
- 新增图表时同步更新脚本和 `data/README.md` 索引表
- 依赖写入 `requirements.txt`，保证协作者可一键复现
