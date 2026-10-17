# 4.1 structural landscape review

Published revision: 2026-10-17. Scope is exclusively **01 / THE LANDSCAPE**, figures 4.1-01 and 4.1-02, with the necessary assets and release check. The following ranking, evolution, country, structural insight and policy sections retain their previous HTML and data.

## Visual and interaction design

The two user-provided reference images motivate fixed architectural regions rather than independent masonry cards. Each plate is a 1600×900 SVG with its own controls and a fixed detail strip inside the canvas.

- Agent Infra: application entries above frameworks/orchestration, then runtime capabilities. The bridge to model services is explicitly labelled. All 86 projects and 12 canonical categories appear once.
- Model Infra: serving beside post-training; training/acceleration below; data and compute form the base. Model API gateways remain in their canonical Model Infra category. All 59 projects and 13 categories appear once.
- Positions encode editorial functional groupings and common capability combinations, not verified repository dependencies, compatibility or a recommendation to adopt a specific project.
- Default is a complete structural view. Project names and owner icons remain visible, and monthly changes never rearrange positions.
- Module selection shows its role, coverage, influence, within-layer rank, history and three leading projects in the fixed detail strip. Project selection shows its repository, category, current value, rank and history in that same strip. Full source metadata remains available through an explicit detail button.
- Module zoom enlarges that region while retaining the fixed detail strip, with a visible return control. Keyboard users can activate module/project buttons and the zoom control; double-click is an optional shortcut.
- Three views: structure, influence and monthly change. Influence uses logarithmic colour/bar intensity within a plate. Change uses two-sided colours; project rates require both months and a nonzero previous value. Category rates use the model's common observed cohort. Unknown values remain missing.
- Three illustrative scenarios per plate highlight relevant functional modules. They are reading guides, not measured project integrations.
- Search, month selection, scenario and reset operate within each plate. Fullscreen retains state; SVG and CSV exports retain current selection, period, data provenance and missing-value status. The original shared month toolbar is replaced by two independent selectors.

The existing pink/blue distinction is retained with the report's typography and light/dark palette. Owner icons are labelled as such, rather than being presented as official product logos. Narrow screens can scroll the full plate horizontally; fullscreen adapts the canvas to a desktop viewport, and module zoom supports closer reading.

## Verification and limits

`check_landscape_atlas.py` verifies unique/exhaustive cohort coverage, category membership, names, controls and non-overlapping project/module geometry. It is included in the existing Pages pipeline. The v3 data gate remains unchanged.

Local DOM checks cover scenarios, focus, search/reset, independent months, project details, missing values, keyboard activation, module zoom, fullscreen restoration and SVG export. They also compare the following sections and the complete data payload with the previous release. Exported SVGs are rasterized and inspected in default, selected, zoomed and dark states.

The managed environment does not expose the required control-browser capability. Actual browser viewport/touch QA is therefore not claimed; DOM checks and SVG inspection are the available verification methods.
