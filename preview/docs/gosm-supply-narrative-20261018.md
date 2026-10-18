# 5.1 narrative alignment — 2026-10-18

The opening now follows the 2.1 reading sequence: research question, visible goal/indicator positioning, a continuous core finding, scope note, and three perspectives. The 3.2 baseline informs the distinction between scale and influence and the move from totals to identifiable publishers. Each approved chart is followed by three paragraphs connecting evidence, interpretation and action. Three numbered, full-width actions identify participants, practical steps and observable outcomes.

The interactive chart geometry, JavaScript and source data are unchanged. Reading styles are scoped to `.s51-topic` and use existing light/dark theme tokens. The Chinese manuscript and rendered section share one content source. English routes retain their existing Chinese-review link and translation status.

## Evidence checked

- Platform summary: 3,158,803 models and 1,093,040 datasets.
- Annual retrospective: models +58.3%, publishing accounts +48.4%; same 2026-09-13 snapshot.
- Geography cohort: 826 organization accounts, 73,088 models, 12,502 associated datasets.
- China + US: 71.7% of cohort models, 86.6% of cohort cumulative model downloads.
- Top-three cumulative download shares: China/US models 79.3%/33.1%; datasets 29.1%/42.8%.
- Beijing, Shanghai, Zhejiang and Guangdong: 116 accounts and 5,408 models; 88.8% of the 6,093-model China cohort, retaining 149 provincially unassigned models in the denominator.
- China provincial counts, download totals and publisher counts reconciled with `supply-observation.json`.

Geography is publisher-account location, not contributor nationality or usage location. Organization accounts are not corporate groups. Dataset geography covers the same model-publisher cohort. Monthly completeness is unknown; the terminal decrease is not interpreted as deceleration.

## Validation

- Portal build and all internal-link checks passed (53 bilingual routes).
- Existing Chapter 5 source/denominator/export checks passed.
- DOM regression passed for chart controls, theme redraw, drilldowns, pagination, exports and fullscreen restore; new narrative order and section anchors checked.
- Manuscript equality and all narrative numeric claims checked against the retained source tables.
- Browser layout was not exercised: the managed Sites browser-control skill was unavailable. DOM checks are not browser screenshots.
