# 第一章图件

| 图件 | 用途 | 来源与数据 |
|---|---|---|
| [fig-1-0-1_report_logic.svg](fig-1-0-1_report_logic.svg) | 全书逻辑与章节衔接 | 本报告概念图；[统一框架](../../data/meta/osdg-framework.json)及本章导读 |
| [fig-1-2-1_osdg_framework.svg](fig-1-2-1_osdg_framework.svg) | OSDGs四支柱十维度 | osdg-brand v1.0中文框架母版，未经改写 |
| [fig-1-0-1_report_logic.editable.svg](fig-1-0-1_report_logic.editable.svg) | 全书逻辑图可编辑文字源 | 与路径化母版配套，编辑需要Noto Sans SC字体 |
| [visual-tokens.json](visual-tokens.json) | 保持颜色一致 | osdg-brand视觉参数v5 |

品牌源版本：`X-lab2017/osdg-brand`，`ad441ae810f878bcd53956da1f1b889b0defa45c`。框架母版来源：[ColorLight/Framework_ZH.svg](https://github.com/X-lab2017/osdg-brand/blob/ad441ae810f878bcd53956da1f1b889b0defa45c/brand/v1.0/svg/ColorLight/Framework_ZH.svg)。

两张图均为结构示意，不是定量图表，不虚构数据CSV。圈面积与分段不表示权重。本轮没有使用联合国徽记组合版。全文使用本地相对图件路径，避免依赖飞书图片权限。

## Preview v0.6：交互图与静态复用

第一章新增 Linux 协作、模型衍生、SDGs 与 DPGA、OSDI 指标地图四张静态 SVG；原 OSDGs 目标框架增加在线交互。对应原稿引用静态 SVG，网站按图名接入交互组件。

- Linux 与模型案例只使用 `data/raw/2026/external/` 的固定快照，不进入 OSDI 或 processed 数据计数。
- 目标与指标解释读取统一指标字典；资料关联不表示测算完成。
- DPGA 九项标准说明为简要翻译与概括，原标准来源及 CC BY-SA 4.0 许可在图注保留。
- 新 SVG 可编辑，使用 Noto Sans SC。重新生成：`python3 preview/web/export_chapter_visuals.py --repo-root .`。在线图的配色适配深浅主题，支持悬停、点击与键盘选择；关闭脚本仍保留默认图形与正文解释。
