# 4.1 Agentic AI landscape v2

Implemented 2026-10-17 for review on the existing GitHub Pages report. This is the approved second design's 4.1 scope, excluding the additional E5/E6 exploration directions and the selection checklist. Other chapter content and raw datasets remain unchanged.

## Reading order

1. Agent Infra and Model Infra: every selected project in two stable-position classification maps, owner logos and complete project names; project search, zoom, detail dialog.
2. Category OpenRank ranking and 12-month rank/value/share matrix; selected-category history; within-category monthly project ranking and selected-project history or complete monthly rank matrix.
3. Country map/ranking, selected-country category breakdown, and category-by-country shares. The map and list are linked; selecting a category updates project and country views.
4. E1 Top-3 concentration; E2 share migration on the cohort observed in every month of the selected interval; E3 country specialization LQ; E4 country share evolution.
5. Three evidence-linked policy recommendations and expandable methods/sources.

Every chart supports SVG/CSV export and paginated semantic data tables. Fullscreen uses the same panel and state, restores its original position on close/Escape, and exits before in-page source navigation. Print expands complete table records. No new site or hosting service is introduced.

## Data and provenance

- Source: `antgroup/agentic-ai-landscape` commit `e330d75ea4ca314bc81f6868df63425c8acca5e3`, existing pinned canonical CSV.
- Filter: keep/add; unique repo_id; 145 projects, 86 Agent Infra / 59 Model Infra, 25 categories. Classification is a current-snapshot backcast, not a reconstructed historical census.
- Window: 2025-09 through 2026-08. Latest observed coverage: 140/145; latest sum: 5706.38 (Agent 3306.63; Model 2399.75).
- Missing and pre-creation observations remain null, observed zero remains zero. Project ranks are recalculated each month; categories use observed sums and disclose coverage. Category month-on-month growth uses the intersection of the two observed cohorts.
- Country views are a separate deterministic simulation, seed 341. Each category contributes 4000 over the 12 months; total 100000 synthetic contribution units. Synthetic actor IDs overlap across categories and months. Developer counts use set unions, not summed subcategory counts. Synthetic contribution units are never combined with real OpenRank.
- Real country allocation is a future data integration, requiring complete project-community contributor records and time-stamped public location snapshots. No country superiority or governance conclusion is inferred from simulation.
- Geography reuses `content/vmap/source/world.json`, including the report's existing China geometry. Other/unknown are kept in the denominator and table; unlisted geographic units are not assigned their combined residual.
- Generated `assets/landscape/v2-data.json`, `v2-observations.csv`, and `v2-simulation.csv` are reproducible build products. Original pinned files and their hashes remain unchanged.

## Implementation and validation

`landscape_v2.py` supplies semantic HTML, the full static maps, source records and simulation. `landscape.js` contains the pure calculation model plus the UI; `landscape.css` is scoped to 4.1. `landscape_content.py` retains legacy provenance and delegates the Chinese section to v2. The existing English route explicitly links to the Chinese sample without claiming a full translation.

The release pipeline adds `check_landscape_v2.cjs` to validate cohort dimensions, all monthly coverage totals, source sums, per-month ranking, missing/creation/zero distinctions, common-cohort share differences, country share conservation and actor-set deduplication.

Local checks also exercised the actual DOM with LinkeDOM: 14 SVG views, all filters, category/country linking, project selection, search, paging, dialogs, fullscreen restoration, CSV labels, and standalone SVG exports with embedded logos and resolved theme colors. Generated SVGs were rasterized and visually inspected, with heatmap contrast and label layout corrected. Existing portal, report, Chapter 1, GOSO, maps and GOSR checks passed.

Browser layout QA was not performed: this managed environment did not expose the required control-browser capability. DOM checks and SVG inspection do not substitute for a browser viewport/keyboard/touch test. Responsive CSS, native dialog Escape handling, and reduced-motion/print support are implemented; device-level visual review remains a stated review limitation.
