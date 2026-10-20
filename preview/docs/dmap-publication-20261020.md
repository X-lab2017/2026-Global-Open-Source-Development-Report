# D-Map publication review · 2026-10-20

The original draft is named 2.5; the current seven-map chapter places D-Map in section 2.6, after A-Map. This release keeps that navigation and aligns the web, PDF and figure numbering to 2.6.

- One manuscript in `dmap_publication.py`, exported to the original chapter source path and `content/dmap/chapter-2-6.md`.
- Three source-based figure groups: global sources and five-year shares; China/US source shares; cross-region contribution flows. The former hypothetical organizations/roles/retention demonstration is retired from the publication.
- Original data JSON and all three source CSVs remain byte-identical. Their hashes are pinned in the publication gate.
- The fixed five-country series, Top 10 source-share table and 60-edge flow sample keep separate denominators. The map retains its explicit 2025 natural-year exception; other annual observations use the established report-year convention.
- Main text distinguishes shares from scale, contributions from people, cross-region contribution from migration, and source diversity from governance or measured intervention effects.
- Same chart families in both editions: map, line charts, proportional local/overseas bars with source rankings, and Sankey flows. The web also offers chord and geographic flow views of exactly the same filtered edges.
- Same live figure moves into and out of presentation. Four explicit grid rows protect heading, toolbar, chart and caption. Narrow views reflow rather than shrink the text.
- Five-page vector PDF, with one landscape figure page. Captions are centered below figures. Body is 11.2 pt; chart text is 8.5–10.5 pt.
- Verified: all five PDF pages visually inspected, text and bounds checked; 398 bilingual DOM interaction assertions; 180 CSS cascade assertions; 69 publication/build gates.
- Actual browser rendering and physical printing were not run in this environment. DOM and CSS checks are not a substitute for those reviews.

Review focus: the three evidence questions, compact interaction controls, and whether the retained source boundaries are clear without dominating the story.
