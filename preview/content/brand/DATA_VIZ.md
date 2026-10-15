# GOSD · 数据可视化规范（Data Visualization Spec v1）

> 本规范把本仓库 `data/visual-tokens-v5.json` 的品牌令牌落到图表层，适用于报告网站、发布会演示与 PDF 图表。
> 参考实现：本目录 `echarts/gosd-chart-tokens.ts`（令牌映射）+ `echarts/EChart.tsx`（ECharts 封装）+ `echarts/GeoMap.tsx`（地图封装），已在《2026 全球开源发展报告》交互网站（github.com/X-lab2017/2026-Global-Open-Source-Development-Report）双色主题验证。

## 1. 设计令牌

与 `data/visual-tokens-v5.json` 对齐，双主题取值如下（网站实现可以 CSS 变量承载，也可以用 `gosd-chart-tokens.ts` 直接取数）：

| 令牌 | 浅色（阅读模式） | 深色（演示模式） | 用途 |
| --- | --- | --- | --- |
| `--bg` | `#F3F8FA` | `#0A2C49` | 页面底 |
| `--surface` | `#FFFFFF` | `#123B58` | 面板/卡片 |
| `--ink` | `#10334D` | `#F6FBFF` | 标题与正文 |
| `--muted` | `#4C697B` | `#BAD2DE` | 说明文字 |
| `--line` | `#CADCE5` | `#3A657D` | 边框/分隔线 |
| `--brand` | `#156993` | `#76D5E4` | 主数据色 |
| `--cyan` | `#007D87` | `#67D5DB` | 次强调 |
| `--gold-text` | `#886400` | `#F2D15C` | 关键数字等**文字**强调（对应令牌 `gold`） |
| `--gold-display` | `#E7C652` | `#F2D15C` | **装饰**金：地图选中/hover、徽章（对应令牌 `goldDisplay`；白底对比度仅 ~1.67:1，禁止作文字色） |
| `--map-empty` | `#E0EBF0` | `#123750` | 地图无数据区 |

> 文字金与装饰金必须区分使用：`#E7C652` 在浅底上不满足文字对比度，只用于填充和描边类装饰；关键数字一律用 `--gold-text`。

四支柱色（`--p1`–`--p4`）只用于表达 OSDG 支柱语义；普通图表序列不使用支柱色，避免语义混淆。

## 2. 图表序列色板

多序列图表按顺序取色（同一图表内不超过 8 条序列，超出应拆图）：

```
浅色底: #156993 #279FA9 #4E87C5 #9973B7 #5C8A3C #C08A2D #8C5B3F #6B7F8C
深色底: #76D5E4 #68C8CC #77A9DE #AD8ACC #A0C86C #F2D15C #E8A06A #8FA9BB
```

规则：
- **时序折线**：首序列用 `--brand`，对比序列（如"中国 vs 美国"）用 `--brand` vs `--gold-text`（浅色图表中金色线条辨识度过低时，改用 `--cyan` 并保留非颜色编码）
- **地图**：连续色带见 §4；地图 hover/选中态统一 `--gold-display`（装饰金）
- **饼图/环图**：仅用于构成 ≤5 项的场景；排行优先条形图

## 3. 图表基准样式

| 元素 | 规范 |
| --- | --- |
| 标题 | 14px / 700，面板外置（`gv-panel-title`），不写入图表内 |
| 网格线 | `--chart-split`（浅 `#DDE9EE` / 深 `#234E66`），仅横向 |
| 坐标轴 | 轴线 `--chart-axis`，刻度标签 10–11px `--muted` |
| Tooltip | 面板底 + 1px 边框（跟随 `--surface`/`--line`），12px |
| Legend | 顶部，roundRect 图标 14×8，可多行 |
| 字号下限 | 任何场景 ≥ 10px；演示大屏等比放大 1.3–1.5× |
| 数字 | 千分位；大数用 `万/M` 缩写（`fmtCompact`） |

## 4. 地图规范

- **世界地图**：国家名匹配 GeoJSON `properties.name`（英文）；数据来自 open-share 平台快照
- **中国省级**：匹配 `properties.fullname`（如"北京市"）
- **连续色带**（visualMap）：
  - 浅色：`#DCEBF2 → #BCD8E4 → #8FBFD3 → #5B9FBE → #337FA6 → #156993`
  - 深色：`#123750 → #1C5A7A → #2A7D9C → #3FA3B8 → #68C8CC → #A0E6D8`
- **色阶上限**取 P95（避免美国等头部值压扁色阶），超出部分用最深色并标注
- **下钻**：世界地图点击"中国"→ 省级视图，提供返回按钮；选中态 `--gold-display`
- 无数据区使用 `--map-empty`，不使用纯白/纯黑

## 5. 交互与无障碍

规范要求（目标态）：

- 折线/面积图支持 `focus: 'series'` 悬停高亮；堆叠面积默认开启
- 键盘可达：轮盘/地图扇区可 tab 聚焦（参考第一章交互图实现）
- `prefers-reduced-motion: reduce` 时关闭动画（ECharts `animation: false`）
- 色彩之外必有冗余编码：排行榜用名次数字，地图 hover 显示精确值，不单独依赖颜色

当前参考实现**已支持**：reduced-motion 自动关动画（`EChart.tsx`）、地图键盘替代数据列表（`GeoMap.tsx` 的 `a11yList`，`<details>` 折叠列表可 tab 进入）、tooltip 精确值。

**尚未支持**（使用方需自行补齐）：canvas 图表本身的键盘漫游、轮盘扇区 tab 聚焦。引用本模块时请在项目文档中区分这两条边界，避免误认为开箱即用。

## 6. 数据与引用

- 一张图一个数据文件（报告仓库约定）：`data/processed/chapter{N}/fig-{章}-{节}-{序}_{slug}.csv`
- 地图快照（报告仓库）：`data/raw/2026/external/open-share/`，由 `scripts/fetch_open_share.py` 定期更新
- 每个图表脚注标明数据来源与统计周期（2022—2026）
