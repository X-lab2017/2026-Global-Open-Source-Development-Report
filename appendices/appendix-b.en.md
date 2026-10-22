# Appendix B: Model openness and digital public goods

Open materials enable shared improvement; public value also needs evidence of use and sustained maintenance. This appendix connects Chapter 5’s model observations with Chapter 6’s recommendations. It explains how to define an assessment object and retain versioned evidence while distinguishing report categories, openness definitions and digital public good recognition. Appendix A covers measures, samples and statistical methods; Appendix B connects materials, rights and public uses.

## B.1 Three kinds of judgment

Before interpreting “open model” or “digital public good”, identify the rules and object behind the claim. A model family, a particular weights release and a complete solution with services and data have different boundaries.

| Judgment | Question | Appropriate basis |
| --- | --- | --- |
| Report observations | What materials are available, and how did the source classify them? | Section 5.3’s L/O explanations, source assessments and version evidence |
| OSI’s definition | Are the freedoms to use, study, modify and share supported by the required materials? | OSAID 1.0 and the applicable terms |
| DPGA recognition | Has the nominated digital solution passed the standard’s review? | The DPG Standard, official review and a valid Registry entry |

Section 5.3 presents material completeness (L) and licensing openness (O) separately. Its high-completeness and high-openness groups support structural comparison. They have no automatic conversion into OSI conformity or DPGA recognition. This report awards no certification, aggregate score, gold or silver status, or separate DPG passing threshold.

Official references were checked on 22 October 2026. Cases retain their frozen records from 17 October 2026. Standard revisions, case updates and report editions have separate dates; a new reference check does not make old case evidence current.

## B.2 Fix the version and inspect the materials

Begin with a specific release: retain its full model ID, publisher, revision, material locations and checking date. Record upstream models, data and runtime dependencies separately. Findings do not automatically transfer to other sizes, fine-tunes or later versions in the same family.

The report organises evidence into six categories. These are research record requirements, not a substitute for a standard’s complete assessment checklist.

| Material | Record to retain |
| --- | --- |
| Weights and configuration | Files, configuration, tokenizer and access conditions; the version and inspection scope |
| Inference implementation | Implementation and dependency versions, execution entry points, environment and tasks actually run |
| Complete pretraining code | Data processing, training configuration and execution chain; distinguish pretraining, fine-tuning and inference |
| Training data information | Provenance, composition, access and processing rules; distinguish public, restricted and unknown materials |
| Licences and use conditions | Separate terms for code, weights, data and dependencies, with specific texts and dates |
| Maintenance and feedback | Maintainers, issue channels, revisions and migration records; an available channel alone does not verify responsiveness |

“Observed” means a material or statement was found; completeness still depends on its details. “Unknown” means insufficient evidence. “Not applicable” needs a reason. Record actual execution separately, including environment, task, result and failure. Do not sum the six fields into a score or equate visibility with independent validation.

[OSAID 1.0](https://opensource.org/ai/open-source-ai-definition) links the four freedoms to data information, complete training and runtime code, parameters and open terms. Data information must enable a skilled person to build a substantially equivalent system and describe provenance and access as required. This does not simply mean redistributing every raw dataset. Downloadable weights or a licence name such as Apache-2.0 alone cannot establish conformity of the whole system.

## B.3 Reading four fixed-version cases

Chapter 5 retains four purposively selected cases to demonstrate evidence organisation, not population estimates. The table summarises records from 17 October 2026. Full revisions, field-level sources and checking notes remain in the case dossiers.

| Fixed-version case | What the recorded evidence supports |
| --- | --- |
| Qwen2.5-7B · d1497293 | Weights and inference entries are documented, with Apache-2.0 recorded. The complete pretraining chain remains unverified; a data overview is not a complete material package. |
| OLMo-2-1124-7B · 7df9a825 | Weights, staged training configurations and named datasets form a more extensive material chain. The report did not rerun full training; data licences still need component-level checks. |
| Llama-3.1-8B · d04e592b | Weight access and execution entries are documented. Read the version’s community terms and use conditions; visible files do not imply unrestricted rights. |
| Gemma-2-9B · 33c19302 | Access requires acceptance of terms, with overview information on data and processing. The complete pretraining chain remains unverified; identify the applicable terms by their recorded date. |

A model revision pins its repository. External terms, datasets and maintenance pages may have separate versions. Retain their dates too; one model commit does not freeze all dependencies.

The cases are excluded from both the 870-model report sample and the 884-record platform snapshot, and do not replace source grades. Those cohorts have not been identity-aligned, so their difference is not growth. The 22 licensing-field discrepancies in the 884 records remain pending review. Appendix A explains the statistical boundaries; [Section 5.3’s dossiers (Chinese)](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/05/#gm-dossiers) provide detailed evidence.

## B.4 The DPG Standard and formal recognition

DPG recognition applies to the nominated digital solution. DPGA’s nine indicators cover public goals, openness, governance and harm prevention. This table summarises what to examine; the [DPG Standard](https://www.digitalpublicgoods.net/standard) and its category-specific requirements govern formal review.

| Indicator | Evidence to examine |
| --- | --- |
| 1 SDG relevance | Public problem, development goals and supporting evidence |
| 2 Open licensing | Approved licences or terms for each component category |
| 3 Clear ownership | Who owns, stewards and is accountable for the assets |
| 4 Platform independence | Required dependencies, their restrictions and open alternatives |
| 5 Documentation | Instructions for understanding, deployment, use and adaptation |
| 6 Non-personal data extraction | Open-format import or export of non-personal data, where applicable |
| 7 Privacy and applicable laws | Privacy arrangements, data handling and legal compliance statements |
| 8 Standards and best practices | Interoperability, accessibility and relevant technical practices |
| 9 Do no harm by design | Data privacy and security, content governance and protection from harassment |

AI systems have additional component requirements. DPGA’s 2025 update requires open training, validation and test data, alongside relevant code, architecture and parameters. OSAID’s detailed data-information requirement cannot substitute for this. Model and data documentation, risks and mitigation information are also required; see the [AI systems guidance](https://www.digitalpublicgoods.net/blog/ai-systems-as-dpgs).

Formal recognition rests on official review and a valid [DPG Registry](https://www.digitalpublicgoods.net/registry) entry. Current rules give recognition a one-year validity before reassessment. Record the entry, evaluation date and lookup date. Alliance membership and product recognition must be checked separately.

DPGA reviews the core solution’s design, not every local deployment. Recognition still leaves context-specific suitability, maintenance and outcomes to be evaluated. The report’s public-value observations do not replace formal review.

## B.5 Connecting openness with public value

Chapter 1 establishes sustained co-creation as a direction; Chapter 6 translates it into shared tasks. A particular model or solution still needs evidence of who can use it, how people contribute, what problem it solves and who maintains it. Downloads, ranks and material counts can identify objects for study, but do not establish these outcomes alone.

The following are this report’s proposed research and delivery records, not new DPGA certification requirements. Select measures appropriate to the use case rather than obscuring context through a uniform score.

| Public-value question | Suggested evidence |
| --- | --- |
| Who can actually use it? | Intended users, language and accessibility needs, deployment cost, hardware and groups not reached |
| Does it solve a specific problem? | Task and baseline, evaluation scope, use outcomes, limitations and independent checks |
| Who can keep improving it? | Contribution channels, documentation and validation tasks, issue handling, downstream changes and feedback |
| How can it remain available? | Maintenance responsibility, resources, migration, dependency updates and exit or handover arrangements |

Outcomes can differ across languages, places and resource conditions. Record the time, population, task and comparison method. Separate observed results from causal claims when comparison or evidence is insufficient. Multilingual support, lightweight deployment and shared maintenance can be development priorities without becoming universal official recognition thresholds.

## B.6 Delivery, updates and sources

A reviewable delivery should let another team identify the evidence, completed work and responsibility for what follows. Keep four groups of records and maintain them as versions change.

| Record group | Minimum information |
| --- | --- |
| Object and basis | Model or solution boundary, publisher, full version, upstream relations, applicable rules and their versions |
| Materials and judgments | Material and licence sources, checking dates, evidence status, validation tasks and results, unresolved questions |
| Use and responsibility | Use case, intended users, known limitations, maintenance and feedback owners, further validation |
| Changes and review | What changed and why, affected findings, reviewer and date; valid official records where recognition is claimed |

When materials, terms, dependencies, standards or uses change, identify the affected judgments before updating the records. A new release does not prove that gaps in an old one have been resolved. Preserve historical evidence and change unknown statuses only when evidence supports doing so.

Appendix A explains measures, time windows, samples and comparison boundaries. Appendix B explains materials, recognition and public uses. Return from a specific figure to its sources, then validate against the actual task to turn report observations into sustained shared work.

Report entries: [Appendix A](附录A-指标体系与数据来源.md), [Section 5.3](/2026/zh/chapters/05/#ch05-s03) and [Chapter 6](/2026/zh/chapters/06/). Full case records are in the [version dossiers](../preview/content/gosm/cases.json).

Official references: [OSI OSAID 1.0](https://opensource.org/ai/open-source-ai-definition), [DPG Standard](https://www.digitalpublicgoods.net/standard), [AI system requirements](https://www.digitalpublicgoods.net/blog/ai-systems-as-dpgs) and [review and renewal policy](https://github.com/DPGAlliance/dpg-resources/blob/main/docs/dpg-review-policy.md). This appendix is a research synthesis; applications must follow the official requirements in force.
