# OpenShare source alignment · captured 2026-10-15

The report's map geometry now uses the same public geographic resources as OpenShare:

- World: https://open-share.com/geo/world.json (217 geographic features).
- China: https://open-share.com/geo/CN.json (34 provincial polygons, southern-islands inset and maritime line features). The original `meta` retains GeoJSON.CN version 1.6.3, copyright and source URL.
- The public page module `https://open-share.com/assets/index-CLEI9-UG.js` registers these GeoJSON resources in an ECharts `type: "map"` series without a custom projection or aspectScale override.
- Its ECharts bundle `https://open-share.com/assets/vendor-echarts-D_hXCcIe.js` specifies the GeoJSON default `aspectScale: .75`. This is reproduced by `web/build_vmap_geometry.py`: x = .75 × longitude; y = −latitude, followed by a single uniform fit and translation. No Robinson transform, independent stretching, outline simplification or manual island relocation is applied.
- The global China feature already contains Taiwan; an automated containment check verifies this. Provincial records include Taiwan (710000), Hong Kong (810000) and Macao (820000). Source maritime/inset geometry is preserved.

## Current report-year source — confirmed 2026-10-20

Current maps, national/provincial rankings and five-year mini-trends use the report-year window **2025-07-01 inclusive to 2026-07-01 exclusive**. Historical labels 2022–2026 use the same July–June convention.

- `data-meta.json`: report-year metadata from `overview_half_year/meta.json`.
- `report-developers.json`: world totals, activity rankings and trends from `overview_half_year/developers.json`.
- `report-CN-developers.json`: provincial totals/activity and China trend from `overview_half_year/CN/developers.json`.
- There are 242 merged country/region identifiers and 34 provincial records. China active = 2,504,824.88; world total = 193,896,100; world active = 28,903,652.45. The 34 provincial activity records sum to the national value.
- Preserve source precision; display 万人 with the platform's two-decimal truncation. Provincial developer totals retain their platform-estimate identity.
- `report-CN-developers-reference.json` is a byte-identical earlier capture of the current provincial file.

The compilation team confirmed the two original five-group CSVs under `data/processed/chapter2` and supplied matching original figures. These records populate both current five-group comparisons and 2022–2026 trends. Their aggregate coverage is distinct from the GitHub map; no domestic supplement is added to those five-group totals.

Domestic supplementary activity of approximately 1.2 million is compilation-team-confirmed data from official Gitee/AtomGit platform statistics combined with questionnaire research and deduplication, not a hypothetical scenario. It is used only for the platform-coverage panel, not allocated across provinces or added again to the five-group China record.

### Historical captures

The three `calendar-*.json` files and earlier screenshots remain unchanged for provenance. They describe calendar 2025, including China active 2,344,657.55, and are no longer used in current 2.1 figures. Original source arrays and global/region reconciliation fields remain in the source registry; no geographic residual is invented or assigned to a country.

Rebuild current derived records with `python3 preview/web/build_vmap_data.py`. URLs and SHA-256 hashes are in `../fig-2-1-2_platform-coverage.json`; map transforms remain in `../map-provenance.json`.
