# Chapter 4 opening and 4.1 publication revision

Edition: `2026-10-21-a-landscape-publication-v1`.

## Scope

Continue the accepted `4.1-v3` observations and `4.1-atlas-v1` full architecture maps. The chapter opening now explains the six technology fields through reader questions. Section 4.1 follows technology structure, influence distribution, concentration and common-cohort change, simulated contribution examples, and accountable actions. No current classification, historical observation, geographic geometry or simulation record is rewritten. Sections 4.2–4.6 retain their existing content unchanged.

`landscape_publication.py` is the shared Web/PDF manuscript. The old 69-project annual manuscript is not merged into the current 145-project monthly sample. Figures use continuous numbers 4-1-1 through 4-1-13; their existing DOM IDs and interactions remain. Former E1/E2 are now 7/8; the five simulated geographic views are grouped together as 9–13.

## Reading and print

- Full-width prose and centered figures follow Chapters 1–3. Every panel has one complete bottom caption, retained in fullscreen.
- Remove review status language, repetitive source footers and reader-facing CSV/SVG export controls. One optional source/method disclosure remains in the first figure; data details and existing interactive exploration remain available.
- Keep the actual March 2025–August 2026 observation window. Every simulated geographic figure retains a visible simulation label, in both media.
- Default comparison selects the three leading categories. Concentration and common-cohort change default to the whole sample; chart height expands to fit all 25 rows.
- The local review PDF contains the chapter opening and 4.1 on 11 pages, including two landscape architecture plates. All 145 names and available owner icons remain; the 13 figures retain their meaning and denominators. The PDF is delivered privately and is not added to GitHub or the website.

## Evidence and limits

The latest observed month covers 140/145 projects, OpenRank 5,706.38. Leading categories are personal assistants 752.76, inference engines 662.78 and agentic coding 563.09 (34.7% combined). Personal assistants' first two projects account for 77.2%, first three for 82.4%. The 12-month common cohort contains 107 projects; multi-agent orchestration moves from 1.33% to 6.58% and agentic coding from 16.85% to 11.55%. These are fixed-sample observations, not global market shares or causal findings. Country data remain independent simulation seed 341.

## Verification

- All `v3-data.json` bytes remain identical; 4.2–4.6 generated section HTML is unchanged.
- Existing v3 calculation, complete-atlas geometry, theme, other GOSL landscape, portal and report gates pass.
- `check_landscape_publication.cjs` covers 87 caption, SVG bounds, fullscreen restoration, independent controls, sample and simulation assertions.
- PDF text verification covers all 145 project names, thirteen figure titles, critical values, simulation labels and both landscape pages. All eleven pages are rendered and visually inspected.

Reproduce after building the portal:

```sh
python preview/web/landscape_print.py --font /path/to/NotoSansCJKsc-Regular.otf
node preview/web/check_landscape_publication.cjs _site
```

The DOM check requires `jsdom` in the Node module path. PDF generation uses the existing ReportLab, PyMuPDF and fontTools workflow and the same JavaScript calculation model as the Web charts.
