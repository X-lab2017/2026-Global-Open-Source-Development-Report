# 4.1 Agentic AI landscape v3

Revision for review on 2026-10-17, published to the existing report route. Two landscape maps remain the main entry point. E5/E6 and the selection checklist remain excluded.

## Interaction changes

- 4.1-04 replaces the rank/share matrix with monthly trajectories. Agent Infra and Model Infra have separate tabs; category chips focus individual lines. Rank, OpenRank and share views support 6/12/18 months. Rank is calculated within the selected infrastructure layer.
- 4.1-05 shows all 25 categories in two flat groups and compares one to three categories. Rank is calculated across all 25 categories, with current rank, interval change and coverage shown above the chart.
- 4.1-06 combines the project ranking and project history in one figure, including flat category choices, paginated project rows, up to three comparison lines and a local selected month. The former standalone 4.1-07 is merged into this figure. Category selection links 05 and 06, while both figures remain independently operable.
- 4.1-08 starts with no country selected. Its map and ranking share local layer/category filters and 6/12/18-month periods; clicking a selected country again or clearing selection restores the neutral map.
- 4.1-09 contains its own country ranking and category distribution. All nine available country/residual groups are shown, rather than inventing extra countries to fill a Top-10 list. Selecting a country does not depend on 08.
- 4.1-10 uses country checkboxes, a direct share-comparison dot plot, and an optional 100% composition view. Hidden countries keep their contribution in the denominator and appear as a residual in composition mode. No selected-subset renormalization is performed.
- E1 combines category concentration and its leading projects. E2 combines common-cohort share movement and a selected category's trajectory. E3 compares up to three countries' specialization with an LQ=1 baseline. E4 has its own country/category/window controls. Each figure can be operated without jumping to another figure.

All figures retain semantic tables, CSV/SVG downloads and fullscreen. Downloads disclose the data type, period, scope and attention selection. Time windows are closed intervals ending in August 2026; they are not calendar windows ending at the current date.

## Historical data and boundaries

The canonical classification remains the pinned `antgroup/agentic-ai-landscape` commit `e330d75ea4ca314bc81f6868df63425c8acca5e3`: 145 projects, 86 Agent Infra and 59 Model Infra, 25 categories. This is a current-classification backcast, not a historical membership census.

The series now covers March 2025 through August 2026. September 2025 through August 2026 preserves the previously reviewed values. The earlier six months are backfilled from OpenDigger `https://oss.open-digger.cn/github/{owner}/{repository}/openrank.json`, retrieved on October 17, 2026. Raw responses, source URLs, retrieval times and SHA-256 hashes are retained in `preview/content/landscape/opendigger-20261017/manifest.json` and its companion files. 144 requests returned records; `zai-org/ZCode` returned HTTP 404 and remains explicitly missing. The observation export carries each observation's source.

Missing values and months before repository creation remain null; observed zero remains zero. Monthly observation coverage is 93, 99, 107, 107, 108, 111, 116, 118, 122, 125, 130, 135, 140, 141, 142, 140, 135 and 140. The latest total remains 5706.38 (Agent 3306.63; Model 2399.75). Common-cohort comparisons require observations throughout the selected interval.

Country views remain separately labelled deterministic simulation (seed 341), never country allocations derived from real OpenRank. The original 12 months of synthetic records remain stable; the preceding six months are added. Synthetic contribution totals are 50000/100000/150000 for 6/12/18 months. Developer counts use unions of synthetic actor IDs. Other/unknown groups stay in all denominators.

Generated assets use the `v3-` prefix; shared CSS and JS URLs use `?v=4.1-v3` to invalidate the previous release cache. `landscape_v2.py` retains its filename as the existing builder module and emits the v3 payload.

## Verification

The release gate `check_landscape_v3.cjs` checks all 18 coverage totals, rankings, zero/missing/creation distinctions, common-cohort share conservation, 6/12/18-month country denominators, deduplicated actor counts and 144 raw-snapshot hashes. Existing report and other chapter gates remain enabled.

Additional local DOM checks exercise all 13 figure renderers, flat selections and maximum selection limits, project pagination/month linking, neutral map startup, local country selectors, E1–E4 controls, fullscreen restoration and labelled CSV/SVG exports. Generated SVGs are rasterized and inspected for chart readability.

Browser viewport, keyboard and touch QA is not claimed: the managed environment did not expose the Sites skill's required control-browser capability. DOM checks and SVG inspection do not replace device-level review.
