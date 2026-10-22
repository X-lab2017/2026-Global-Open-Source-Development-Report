# Appendix A: indicators, data and research methods

This appendix explains how to read, check and reuse the report's evidence. Chapter 1 sets out the values and indicator framework; Chapters 2–5 examine maps, rankings, technology landscapes and model ecosystems; Chapter 6 develops recommended actions. For any finding, establish the observed population, measure, period and sample, together with the limits of the inference.

## A.1 The framework and three perspectives

OSDGs establish the development goals. OSDI organizes observations into four pillars, ten dimensions and twenty-nine indicators. A complete framework does not mean every indicator has been measured with equivalent coverage. The report does not combine different units, asset types or evidence states into one score, or interpret indicator roles as scoring weights.

Participation, contribution and influence answer different questions. Together they help explain an ecosystem, but none substitutes for the others. Growth in scale, changes in rank and public value also require distinct evidence.

| Perspective | Question | Check first |
| --- | --- | --- |
| Participation | Who joins collaboration, and where is participation distributed? | Activity rules, deduplication, platform and geographic coverage |
| Contribution | Who undertakes work within a collaboration? | Behaviors, relationship scope, contribution method and project boundary |
| Influence | Who connects a collaboration or reuse network? | Network scope, algorithm version, entity mapping and time window |

The indicator dictionary contains the full definitions. The population, source and comparison scope actually used are specified with each figure and its topic methods. Related files in the dictionary provide a route to evidence; their presence does not establish that a measure has been computed.

## A.2 Reporting periods, snapshots and platforms

The main code-ecosystem period runs from 1 July 2025 through 30 June 2026. Reporting years 2022–2026 use the same July–June convention. Implementations retain the precise interval boundaries and time zone. Retrieval dates identify a source version; they do not extend its observation period.

| Time basis | Use in this report | Comparison boundary |
| --- | --- | --- |
| Reporting year | Annual code maps, rankings and historical comparisons | Check consistent platforms, mappings and statistical rules |
| Monthly series | Technology-category changes, model additions and monthly rankings | Use the stated months; do not invent missing observations |
| Snapshot or retrospective series | Model geography, openness evidence and stocks reconstructed by creation date | Retrospection is not a set of independently preserved historical snapshots |

GitHub is the main observation platform for code. Gitee, AtomGit and GitLab supplement it where the source and scope are explicit. AtomGit is the current brand following the GitCode–AtomGit merger. Historical tables retain their original fields and dates; reuse records the correspondence to avoid double counting.

The GitHub map in Section 2.1, the compilation team's five-group statistics and the domestic-platform supplement have separate scopes. The supplement is used only in the platform-coverage comparison. It is neither added again to the five-group China record nor allocated proportionally to provinces. Model monthly series, annual retrospection and October snapshots likewise cannot be joined into one continuous series.

## A.3 Active entities, deduplication and attribution

Active developers are identified from qualifying collaboration within the period, excluding identified bots and automated service accounts. The report considers Issue creation, Issue comments, PR submissions, PR review comments and PR merges. Stars, forks and likes may serve their own supplementary purposes; they are not direct measures of this collaboration workload.

Stable account identifiers support within-platform deduplication, and verified identity mappings support cross-platform linkage. Project–repository mappings retain the effective boundaries for each reporting year, including multiple repositories, mirrors, transfers and splits. Whether particular results use the same mapping version must be checked; the availability of a mapping capability does not imply that all tables have been harmonized.

Developer location, organization affiliation and project attribution are different variables. Developer locations are standardized from public profiles, with the corresponding historical snapshots used for annual comparisons. They do not establish nationality. Conflicting locations are reviewed; unresolved levels remain unknown while reliable higher-level information is retained.

| Attributed entity | Meaning in this report | Does not establish |
| --- | --- | --- |
| Developer geography | An observed public-profile location | Nationality, birthplace or every workplace |
| Project or organization geography | The public organizational relationship used by the ranking | The location of all contributors or users |
| Model publisher geography | The linked organization or account attribution | Training, deployment or training-data location |

Unknown locations remain in the applicable global total and are identified separately in geographic analyses. Figures restricted to identifiable locations state that denominator. China's provincial view retains the corresponding Taiwan, Hong Kong and Macao records and uses the reviewed geographic resources and mappings. An uncovered location is not treated as having no activity.

## A.4 Activity, contribution and network influence

OpenDigger Activity takes the square root of the weighted sum of collaboration counts for a developer, repository and month. Repository activity then sums the developer-level results. It measures behavioral intensity, rather than developer headcount or an overall development score.

| Collaboration behavior | Weight listed in the official method |
| --- | --- |
| Issue creation | 2.2235 |
| Issue comment | 0.5252 |
| PR submission | 4.0679 |
| PR review comment | 0.7427 |
| PR merged | 2.0339 |

These weights follow the official OpenDigger documentation checked on 22 October 2026. They do not replace production records for individual datasets and are not weights for the twenty-nine OSDI indicators. Monthly headcounts cannot simply be added to obtain annual unique participants. Activity, counts and network scores retain their separate units and aggregation rules.

Community OpenRank observes contribution through project-level Issue, PR and collaboration relationships. Global OpenRank observes influence through developer–repository networks and incorporates historical inheritance. Comparing scores requires the algorithm type and version, input scope, period and entity-aggregation method. Historical inheritance also means that a positive OpenRank score alone does not establish current-period activity.

Project, company and foundation aggregates require effective mappings and rules for overlapping affiliations and aggregation. Repository scores are not automatically summed into a project score. The annual top-5% Global OpenRank rule used for talent observations requires a fixed comparison population and tie rule; it is not automatically applied to other entity types.

Method sources: [Activity](https://open-digger.cn/docs/user_docs/metrics/activity), [Community OpenRank](https://open-digger.cn/docs/user_docs/metrics/community_openrank), [Global OpenRank](https://open-digger.cn/docs/user_docs/metrics/global_openrank).

## A.5 Comparing maps, rankings and technology landscapes

Chapters 2–4 observe different aspects of the same ecosystem. Maps emphasize geography, rankings the relative positions of defined entities, and landscapes functions and categories. They share requirements for provenance and mappings without necessarily sharing a sample or denominator.

| Research area | Observations used | Boundaries to retain |
| --- | --- | --- |
| GOSO · Chapter 2 | Participation, contribution, influence, talent, assets, diversity and governance maps | Distinguish global coverage, identifiable locations, five-group statistics and topic samples; do not add arbitrary region groups |
| GOSR · Chapter 3 | Regional, company, foundation, project, emerging-project and model rankings | State entities, depth, selection and tie rules; first in a sample is not automatically first among all entities |
| GOSL · Chapter 4 | Classification, monthly comparisons and contribution in 4.1; landscapes and research frameworks in 4.2–4.6 | Categories describe functions, not quality scores; the later sections do not establish rankings or evolution from a landscape alone |

Section 2.2 uses directed contribution records from developer location to project attribution. Unlisted source shares are not allocated to countries. Map textures, directional particles and uniform line-width amplification aid reading without adding contributors, events or contribution values.

Monthly rank, score and share are distinct readings. A higher rank need not imply a higher absolute score. Top20, Top100 and Top1000 are nested and cannot be added. An entity outside a published list is not automatically assigned zero or the last rank.

Technology classifications retain their sources, versions and assignment rules. Projects can serve multiple functions, so aggregation across categories requires explicit overlap and deduplication rules. Agent Infra and Model Infra comparisons retain each figure's declared population and denominator.

## A.6 Model supply, derivation and openness evidence

Chapter 5 connects supply, reuse and openness through separate evidence sets. Repository counts are not independent model-family counts. Cumulative downloads are not users, deployments or performance. Public visibility alone does not establish compliance with a particular openness definition.

| Evidence set | Scope and timing | Valid comparison |
| --- | --- | --- |
| 5.1 Supply | Retrospection of models visible on 2026-09-13; platform and organization snapshots from 2026-10-16/17; separate monthly additions | Label organization-geography samples and platform-wide denominators separately; snapshot differences are not automatically growth |
| 5.2 Derivation network | Snapshot from 2026-10-16: 5,777 nodes and 5,111 declared relationships | Base to derived direction; non-random sample, not platform-wide coverage; year selection does not invent network history |
| 5.2 Cross-country flows | Original-report cross-country subset with identifiable countries at both ends: 10,943 relationships | Base-origin country to derived-publisher country; not flows of people, money or deployments |
| ModelRank rankings | Chapter 3 monthly rankings and the 2024-07–2026-08 national-seat series in 5.2 | Compare exact model IDs, months and ranking depths; seat share is not score share |
| 5.3 Openness | 870 report samples extracted on 2026-09-14; 884 supplementary records from 2026-10-17; independently selected fixed-version cases | Samples are not identity-aligned; the difference is not net growth; cases do not represent the population |

ModelRank is already used in the report's rankings and observations. The report preserves the monthly results and sources used; it neither substitutes downloads or assumed weights for those scores nor claims to have recomputed the complete upstream algorithm. Growth rates are not calculated directly from scores normalized across months. A blank monthly rank means the list does not cover the model, not that it was first released or exited.

Derivation edges reflect explicit publisher declarations, not independent verification of training. A missing declaration does not establish originality. Relationships, derived models and unique models are counted separately. The share with identifiable countries at both ends and the cross-country-subset share have different denominators.

Openness evidence is organized by a specific model release, with material completeness and licensing examined separately. L/O explanations, source-platform assessments and independent cases retain their identities. Unverified does not mean absent, and visible materials do not establish successful execution. Appendix B distinguishes the report's classifications, the OSI Open Source AI Definition and formal DPGA recognition.

## A.7 Missing data, illustrations and comparability

Faithful evidence states are essential to comparisons across regions and years. Missing observations, lack of coverage and observed zero are shown separately. Illustrations that explain relationships are also separated from statistics.

| State | Meaning | Presentation rule |
| --- | --- | --- |
| Observed zero | Zero under the stated scope and rules | Retain the value and applicable denominator |
| Unknown or unverified | Insufficient evidence for attribution, materials or judgment | Identify separately; do not replace with zero or absence |
| Not covered | Outside a platform, sample or published ranking | Do not infer activity, openness level or exit |
| Illustrative or simulated | Used to explain a relationship, interaction or research proposal | Label beside the view; exclude from measured totals and findings |

Ratios and growth rates are not computed with a zero denominator. Every proportion specifies its numerator, denominator, entity and period. Check overlap before aggregating categories and platform, mapping, location, algorithm and sample changes before comparing periods. Where needed, use a fixed comparable sample or display differing scopes separately.

Areas, colors, widths, node sizes and distances have only the meanings assigned by the legend. Relationship diagrams and flowing animation do not establish causality. Missing historical observations are not replaced with animated evolution. Chapter 6's connections express recommended pathways, not measured quantities, weights or established policy effects.

Behavioral, network and material data provide evidence for investigation. Economic benefits, governance quality and public outcomes additionally require records of use, maintenance, beneficiaries and evaluation.

## A.8 Provenance, verification and reuse

Trace a finding through its figure number and statement, underlying table or frozen snapshot, indicator and calculation, source and time scope, then algorithm, mapping and display transformations. Retrieval date, observation period and report edition are recorded separately.

Reusable materials identify at least the source and retrieval date; interval or snapshot; population and sample; measure and unit; missing-data treatment; transformations and aggregation; and file or version identifier. Tables preserve source precision while figures may apply consistent display precision. Display rounding does not rewrite source values.

The dataset inventory is maintained with the current repository rather than fixing a file count in prose. Original report data, supplemental snapshots, official cases and illustrations are registered separately. File availability, scope alignment, reproducibility and reviewed findings are different states. Revising a method description does not imply that every historical dataset has been recomputed.

Web and PDF use shared prose and figure data. Interactive filtering supports exploration; the PDF identifies its selected scope and retains the necessary comparisons. Direction, units, denominators, sample status and conclusions remain consistent. Reuse cites the report edition, section or figure, observation scope and original source.

Verification resources: [indicator dictionary](../data/meta/osdi_indicator_dictionary.csv), [dataset inventory](../data/meta/dataset_inventory.csv), [source register](../data/meta/source_register.csv). See [Appendix B](附录-开源人工智能数字公共产品-DPG-评估框架.md) for model openness and digital-public-goods references.
