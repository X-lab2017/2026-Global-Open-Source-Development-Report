# 4.1 visual baseline and theme revision

Review version: `4.1-polish-v1`, 2026-10-17. This revision covers the complete 4.1 section. The accepted structural layout of the two landscapes, all project/category membership, the 18-month observations and the independent country simulation retain their prior data version, `4.1-v3`.

## Reading and visual design

The opening now pairs the section question with Agent/Model entry cards, a compact sample summary and explicit observed/simulated data labels. Five reading anchors connect the landscapes, evolution, geography, structural insights and action recommendations. All thirteen figures share a consistent title, status label, local controls, full-screen/export controls and expandable data/source footer. Category and country selectors remain inside each figure.

The visual adapter derives its theme tokens from the report's pinned `osdg-brand` baseline. Agent uses the baseline purple and Model the brand blue; surfaces, typography, primary controls, keyboard focus, data series and map bands use the report theme. Text gold is separate from display gold. Atlas class names are isolated from the unrelated report world-map classes to prevent inherited typography and clipping rules.

The two architectural plates retain their complete project names, owner icons, fixed locations, category groupings, scenario guides, in-chart detail strip and module zoom. Narrow screens retain horizontal inspection rather than compressing the complete architecture into illegible columns. Whole-section panel styles and the opening adapt to narrow widths; coarse-pointer controls receive larger touch targets.

Categorical evolution retains every line, highlighting the current top three and using neutral context for the remainder. Choosing a category emphasizes that complete trajectory. Comparisons of up to three categories use distinct sequential selection colours. Country series use stable presentation colours without mutating stored records. World maps use the baseline six-band scale with a P95 cap over mapped named countries, a visible legend and gold selection. The initial map selection remains empty.

Reading and fullscreen theme controls use the existing site preference and event. Theme changes preserve local selections. Composition labels recalculate contrast; numerical labels use readable text colours independent of mark colours. SVG export resolves the current theme, retains provenance and embeds owner-icon assets. CSV remains data-first with the existing observed/simulated labels and denominators.

## Validation

- Portal, report, all other chapter gates and v3 data checks pass without altering observations or geographic geometry.
- The atlas geometry gate verifies all 145 projects, all 25 categories and non-overlapping module/project bounds.
- The new theme gate checks the generated assets against the pinned brand, primary text contrast on both surfaces, Agent/Model accent contrast, primary button contrast, dialog scopes and local theme controls. It runs in the Pages pipeline.
- DOM interaction checks cover 6/12/18-month windows, flat category selection, maximum-three comparisons, project pagination, independent selectors, neutral map default, scenario/search/reset, keyboard activation, module zoom, fullscreen restoration and live theme switching with selections preserved.
- All thirteen SVG views are inspected in light and dark themes; complete SVG export is exercised for both themes (26 exports), plus CSV labels and provenance. The built observations match the preceding release byte for byte.

Actual browser viewport/touch QA is not claimed: the required control-browser capability is unavailable in this managed environment. Available checks are DOM interactions, generated asset contracts and SVG raster inspection. Publication uses the existing GitHub Pages pipeline; native Sites hosting is not introduced.
