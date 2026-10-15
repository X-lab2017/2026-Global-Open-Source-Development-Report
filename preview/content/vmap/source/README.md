# OpenShare source alignment · captured 2026-10-15

The report's map geometry now uses the same public geographic resources as OpenShare:

- World: https://open-share.com/geo/world.json (217 geographic features).
- China: https://open-share.com/geo/CN.json (34 provincial polygons, southern-islands inset and maritime line features). The original `meta` retains GeoJSON.CN version 1.6.3, copyright and source URL.
- The public page module `https://open-share.com/assets/index-CLEI9-UG.js` registers these GeoJSON resources in an ECharts `type: "map"` series without a custom projection or aspectScale override.
- Its ECharts bundle `https://open-share.com/assets/vendor-echarts-D_hXCcIe.js` specifies the GeoJSON default `aspectScale: .75`. This is reproduced by `web/build_vmap_geometry.py`: x = .75 × longitude; y = −latitude, followed by a single uniform fit and translation. No Robinson transform, independent stretching, outline simplification or manual island relocation is applied.
- The global China feature already contains Taiwan; an automated containment check verifies this. Provincial records include Taiwan (710000), Hong Kong (810000) and Macao (820000). Source maritime/inset geometry is preserved.

## Snapshot identity — do not mix the two windows

The author's latest screenshots match the public **natural-year** dataset:

- `calendar-meta.json`: https://selfoss.open-digger.cn/openshare/overview/meta.json
- `calendar-developers.json`: https://selfoss.open-digger.cn/openshare/overview/developers.json
- `calendar-CN-developers.json`: https://selfoss.open-digger.cn/openshare/overview/CN/developers.json
- Window: 2025-01-01 inclusive to 2026-01-01 exclusive. China active = 2,344,657.55, displayed by OpenShare as 234.46万. World active = 27,621,084.85 in the trend data (summary rounds to 27,621,085).
- All 40 comparable current total/active screenshot readings were verified against the same source display rule, truncating to two decimals in 万人. Full precision is retained for calculations and CSVs.
- World total ranking contains 224 entries; active ranking contains 241; the combined table has 244 identifiers. Only geographic features in the source map can be coloured. Data absent from the geometry remain available in the complete download.
- The sum of the 34 Chinese provincial active values equals the national value. The world active-region table does not equal the global summary; its difference is retained as an unresolved scope/attribution difference, not attributed to a specific country.
- The provincial total table labels its measure `Estimated Developers`; the active-allocation method still needs documentation. Do not infer observation precision from the number of decimal places.

`data-meta.json` is the separate **report-year** metadata used by `/insight/open-world/gosd`: 2025-07-01 inclusive to 2026-07-01 exclusive. Its current China active series ends at 2,504,824.88. It is retained only to explain the time-window difference. These values are not substituted into the author-confirmed 234.46万 baseline.

The old five-group 2022–2026 repository CSV remains byte-identical and explicitly provisional with respect to this natural-year baseline. The 2021–2025 mini-trends in the maps come from the matching natural-year source, not estimates. Domestic Gitee + AtomGit numbers are separate conditional coverage, never injected into these series or provinces.

Geographic and dataset URLs and SHA-256 hashes are recorded in `../fig-2-1-2_platform-coverage.json`; the coordinate transform is recorded in `../map-provenance.json`.
