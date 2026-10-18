# 第一章正式发布 · 2026-10-18

保留三个小节与已审定的六幅交互图。OSDI 的正文合并为“用指标理解发展”“从参与、贡献到影响与开放”“在共同范围内比较，带着问题进入观察”三部分。

本次删除第一章正文中的参考文献标记和链接、辅助对照表、图内及图外的来源弹窗入口。统计期、样本边界、模拟标记和指标定义仍在对应位置解释。数据、来源归档与指标字典继续保存在仓库和数据栏目。

模型故事保留 ATOM 的 28 个月宏观趋势，并可切换到 Qwen2.5-7B 的四个直接下游实例。图 1-3-2 新增四大支柱与七个主题地图的交互导览：选择支柱或主题高亮研究联系，右侧可进入第二章对应小节。关联与第二章的指标定位一致，不代表计算权重。连线可暂停，尊重系统减少动态效果设置。

图件继续采用 1280 × 800 画布，由同一呈现机制等比例缩放。正文与全屏移动同一个图件节点，保持选择状态。打印使用静态 SVG 同伴图；Qwen 实例另外提供独立 SVG，便于后续 PDF 与演示制作。

实现：`chapter1_theme_map.py`、`chapter1-theme-map.js`、`chapter1-release.css`，以及保留的 `chapter1-restored.*`。静态导览图可通过 `python3 preview/web/chapter1_theme_map.py` 再生成。动态连线借鉴 Archify 的节点选择与路径追踪交互思路，使用本报告的 HTML/SVG/CSS 实现，没有引入第三方运行时。

验证：完整 Pages 构建与既有章节检查；662 次 DOM 交互验证；3536 次明暗主题和正文/全屏样式一致性比较；导览 SVG 渲染检查。DOM 检查覆盖 1366×768、1440×900、1920×1080 下的呈现比例与还原。

本环境没有浏览器控制能力，未执行真实浏览器视口与打印截图校验；上述 DOM 和 CSS 校验不替代浏览器排版验证。

手动复验命令（Node.js 环境须可解析 `linkedom`）：

```sh
python3 preview/web/import_report.py --repo-root . --source-ref main
python3 preview/web/build_portal.py --output _site --base-path /2026-Global-Open-Source-Development-Report
node preview/web/check-chapter1-restored.cjs _site
node preview/web/check-chapter1-style-parity.cjs _site
```
