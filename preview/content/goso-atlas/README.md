# GOSO interactive atlas — review v0.8

## Three distinct evidence layers

1. **Report series**: the 15 unchanged CSVs referenced by `assets/goso/evidence-manifest.json`, pinned to report GitHub commit `95ffe2d3ae52191555a40af25e1a00b26ffc65cc`. Annual code observations use report years. Talent snapshots and September model observations retain their own labels.
2. **OpenShare geographic snapshot**: https://open-share.com/insight/open-world/gosd, captured through its public visible UI on 2026-10-12; page displayed update `2026-10`. Developer stock, active developers, contribution: 100 world ranking entries, 34 China province entries each. Project influence: 29 country entries; no provincial drill-down. No sign-in or privileged API used. The page's separate organization ranking is excluded. Values with 万 preserve the displayed, rounded precision. Missing ranking entries are not zero. Page deltas were not imported because their comparison period was not aligned with report-year data. Raw visible snapshots are retained under `source/`. These observations do not overwrite annual data or justify annual conclusions.
3. **Uploaded illustrated drafts**: eight PDFs (chapter introduction + seven sections), all 26 pages visually inspected. All 24 embedded figures from the seven section PDFs are preserved as WebP under `original/`. `originals.json` records original filenames, PDF SHA-256, page numbers and dimensions. Images remain reference evidence; unverified or mismatched numbers are not silently adopted.

## Cartography

- World: Natural Earth 1:50m Admin 0 Countries v5.1.1, public domain. https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/
- Download: https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip
- China: DataV.GeoAtlas, https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json, captured 2026-10-12.
- Geographic shapes are simplified for presentation, projected to SVG coordinates and bundled locally. Global geometry combines mainland China, Taiwan, Hong Kong and Macao under CN; China province drilldown retains Taiwan province (710000), Hong Kong and Macao. This is a geometry and label correction only: the captured world rankings already contain a single China row and no separate TW/HK/MO observations. No source statistical values have been summed or changed. See geography-policy.json. Australia-coded component geometries are combined under one SVG identifier. Chinese southern-island geometries are shown in an inset. No statistical values are allocated to blank geometries.
- World uses a Robinson-style tabulated projection. City markers use approximate city-centre coordinates for presentation, with quantitative talent counts from the original CSV. Position does not describe a person's precise location. Marker area, not radius, represents talent counts.
- Country values use six linear colour classes with a P95 cap (same index convention as the merged brand reference); values above the cap share the top colour and retain exact displayed readings. actual values remain in linked rankings and the readout. The view contains a subset of countries as defined by its source. Asset geography includes only the 52 identified countries; 2,990,573 models with unknown attribution remain separate.
- Contribution ribbons encode source country → project-country collaboration, not migration. The source table's original shares are preserved (top ten total: China 93.24%, US 77.94%). Domestic contributions are included as source-to-project ribbons. All ribbons share one linear OpenRank scale; missing sources are not imputed.

## Delivery and verification

Five map panels, a contribution Sankey, contribution composition and governance small multiples + the original seven-section narrative and 19 comparison views; all 24 original figures available for comparison. Keyboard selection, China drill-down and global return, metric switching, linked ranking/search, SVG download, URL state, city year selection, model metric switching, original-image dialog and responsive layouts.

Checks: all page anchors/assets; original report CSV byte equality; source coverage and geography mappings; missing/zero distinctions; invalid URL-state normalization; DOM simulation of metric switching, China drill-down, disabled influence drill-down, global return, search, contribution highlighting, figure tabs, Taiwan province/city labels, city years, asset metrics and zoom. Standalone geographic SVGs rendered and visually inspected. Full browser visual/layout testing was not available in this Sites environment.

This version is published only to the existing private review Preview. The report's canonical GitHub manuscript, datasets and public Pages remain untouched.


## Brand alignment · v0.10

Pinned osdg-brand merge commit 7fe12a5b03698df25be3d56e31aa8e9777febe1b. Brand JSON is vendored byte-for-byte; chart series/map extensions follow data-viz/echarts/gosd-chart-tokens.ts. Native SVG adapter preserves this site’s existing geometry, source precision and keyboard controls. Map scales now use the P95 cap per view, including China drilldown; this changes visual encoding only. Fonts in generated SVG are at least 10 px; the original supplied images remain untouched. Light/dark exports resolve tokens to literal colors. Ten-city trend shows up to eight selected series, with full CSV/table retained.
