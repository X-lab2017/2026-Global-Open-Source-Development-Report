# A-Map publication review · 2026-10-20 · v2

A-Map is section 2.5 in the current seven-map chapter. Its original source filename remains 2.7. D-Map remains section 2.6; no accepted previous publication is rolled back.

- One manuscript in `amap_publication.py`, exported to the original chapter path and `content/amap/chapter-2-5.md`. Web and PDF share questions, findings, figure titles, interpretations and three actions.
- Three evidence groups follow the latest supplied A-Map draft (4): code platform activity; model supply and downloads; dataset supply and downloads.
- Original platform CSV remains byte-identical. GitCode is displayed as AtomGit according to the report's brand mapping. Missing 2022/2023 values remain null. All annual code observations follow the established July–June report-year convention.
- Model and dataset evidence uses the draft's publisher sample: 63 countries/regions and 826 publishers, with 72,280 models and 12,291 datasets. These are cumulative sample counts, not whole-platform counts or annual qualified releases. The unspecified cumulative snapshot date is stated in the source detail and notes.
- China, US and Europe are selectable in both asset comparisons. Europe follows EU27 + UK; only the original listed members can be summed (models: 6 countries, 10,084; datasets: 5 countries, 2,359). These are explicitly labeled quantity lower bounds. Same-snapshot European download totals are unavailable and remain null, shown as “待补”, never zero or an estimated percentage. The newer chapter-5 snapshot is not mixed into the accepted original sample.
- Maps color only the 14 countries individually listed in the source. Quantity shares use the complete sample denominator. Only the original US/CN download shares are compared; no download geography is inferred for other countries.
- Original simulations and forecasts remain archived, but are not loaded or used in the new publication. Raw data was not rewritten to fit the layout.
- The code chart shows four small-multiple line charts in one row, above a common-scale current comparison with all four counts, annual net changes and growth rates. Both are visible together; one year selector updates the whole figure. Model/dataset figures combine country maps, rankings and paired quantity/download bars. Colors, units and meanings match across web and PDF.
- Light/dark surfaces, text, lines, four categorical series and sequential map colors follow the V-Map/C-Map tokens. Web and PDF retain the same semantic color encoding.
- The same live figure moves into and out of presentation, preserving selection state. Four explicit grid rows separate heading, controls, chart and caption; widths below 700 px reflow.
- Four-page vector PDF; all pages portrait. The code figure sits on page 1 next to its first reference; model and dataset figures sit on pages 2 and 3. Captions centered below figures. Body 11.2 pt; chart labels 8.5–10.5 pt. Figures are adjacent to the referring text.
- Verified: all four PDF pages visually inspected; text, bounds and shared prose checked; 598 bilingual DOM interaction assertions; 250 dynamic CSS cascade assertions across light/dark/read/fullscreen/narrow contexts; 73 publication/build checks passed.
- Actual browser rendering and physical printing were not run in this environment. DOM and CSS checks do not claim pixel-level browser verification.

Review focus: whether the three-asset sequence is clear, whether quantity and download comparisons are intuitive, and whether the source notes remain concise enough for independent reading.

The v1 versioned PDF remains available at its original URL. The stable PDF and the new v2 versioned PDF contain the new portrait edition.


## v3：视觉与叙事对齐

沿用 2.1、2.2 的明暗主题和蓝色地图色阶；图例精确对应六档色阶，地图使用统一底板，选择状态通过边线与侧栏表达。模型、数据集的数量份额采用实心蓝柱，下载份额采用青色空心柱，两版一致，避免深色模式下两种近似颜色难辨；地区选择不再改变柱条透明度。

共享正文按“供给增长—发布与使用差异—持续维护和复用”组织。引图先交代问题和样本，图后先给出发现再解释含义；增加中美比较中中国模型 +4.3、数据集 −6.2 个百分点的份额差异说明，不据此推断质量或因果。原始数据与欧洲数量下限、下载缺值处理保持不变。

PDF 四页均已逐页检查；598 项 DOM、250 项样式级联核验通过。未运行浏览器像素核验或实物打印。保留 v1、v2 下载，新入口使用 v3。


## v4：三类资产类别结构与增长

各原图新增“类别结构与增长”视角。矩形树图按数量分配面积，点击类别查看趋势；增长比较允许最多三个类别，年份和选择独立保留。代码采用十二个技术用途类别，模型七个主任务类别，数据集六个主任务类别。所有类别数量、历史轨迹均为模拟，不继承截图中不同样本的任务总量；2026 合计分别对齐 GitHub 活跃仓库、既有模型和数据集样本。底表 category-demo.json 独立保存，便于替换。

地图保留全部已有边界几何，对有值和未列明国家均画轮廓；新增主题边界色，非缩放描边，选择仅加强边线。PDF 保留三幅原图，并分别加入类别续图，共七页竖版；六幅图均紧邻相应说明。826 项 DOM 断言与 250 项样式级联核验通过；PDF 逐页渲染检查。模拟类别不得进入核心发现的实测论断。
