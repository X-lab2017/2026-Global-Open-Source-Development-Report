# GOSO chart brand adapter

Upstream: https://github.com/X-lab2017/osdg-brand/tree/7fe12a5b03698df25be3d56e31aa8e9777febe1b/data-viz

The original visual-tokens-v5.json and DATA_VIZ.md are pinned to the merged PR #1. web/goso_brand.py derives both themes from the JSON and copies the exact series/map extension constants from gosd-chart-tokens.ts. This Preview uses native SVG, preserving existing report routing, geographic geometry, accessible region buttons and source evidence. The React reference is not installed here.

Presentation-only adaptations: inline chapter headings retain the established report hierarchy; numeric series and map colors follow the brand; at most eight simultaneous city curves, all ten retained in data tables. Snapshot readings and unknown geography are unchanged. Static downloads use literal light tokens, interactive exports use the current theme.

Verification: source CSV byte equality, geometry mapping, P95 bounds and missing values, DOM simulation of map drilldown and chart tabs, eight-curve selection cap, literal SVG export in both themes. Standalone SVG light/dark renders inspected. Full browser layout testing unavailable in this Sites environment.
