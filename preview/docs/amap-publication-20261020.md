# A-Map publication review · 2026-10-20

A-Map is section 2.5 in the current seven-map chapter. Its original source filename remains 2.7. D-Map remains section 2.6; no accepted previous publication is rolled back.

- One manuscript in `amap_publication.py`, exported to the original chapter path and `content/amap/chapter-2-5.md`. Web and PDF share questions, findings, figure titles, interpretations and three actions.
- Three evidence groups follow the latest supplied A-Map draft (4): code platform activity; model supply and downloads; dataset supply and downloads.
- Original platform CSV remains byte-identical. GitCode is displayed as AtomGit according to the report's brand mapping. Missing 2022/2023 values remain null. All annual code observations follow the established July–June report-year convention.
- Model and dataset evidence uses the draft's publisher sample: 63 countries/regions and 826 publishers, with 72,280 models and 12,291 datasets. These are cumulative sample counts, not whole-platform counts or annual qualified releases. The unspecified cumulative snapshot date is stated in the source detail and notes.
- Maps color only the 14 countries individually listed in the source. Quantity shares use the complete sample denominator. Only the original US/CN download shares are compared; no download geography is inferred for other countries.
- Original simulations and forecasts remain archived, but are not loaded or used in the new publication. Raw data was not rewritten to fit the layout.
- The code chart shows four small-multiple line charts and a common-scale current comparison. Model/dataset figures combine country maps, rankings and paired quantity/download bars. Colors, units and meanings match across web and PDF.
- The same live figure moves into and out of presentation, preserving selection state. Four explicit grid rows separate heading, controls, chart and caption; widths below 700 px reflow.
- Five-page vector PDF; one landscape page for code. Captions centered below figures. Body 11.2 pt; chart labels 8.5–10.5 pt. Figures are adjacent to the referring text.
- Verified: all five PDF pages visually inspected; text, bounds and shared prose checked; 684 bilingual DOM interaction assertions; 180 light/dark/read/fullscreen/narrow CSS cascade assertions; 73 publication/build checks passed.
- Actual browser rendering and physical printing were not run in this environment. DOM and CSS checks do not claim pixel-level browser verification.

Review focus: whether the three-asset sequence is clear, whether quantity and download comparisons are intuitive, and whether the source notes remain concise enough for independent reading.
