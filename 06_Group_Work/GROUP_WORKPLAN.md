# Group work plan

Use the supplied course instructions as the authority for dates, assessment and submissions. This plan maps the folder to the course checkpoints; it does not invent deadlines or mark allocations. Fill in your official class group and group number in the proposal.

## What makes the proposal defensible

The proposed question is narrow enough to finish: one organism, one location, one gene position and one defined historical archive. The useful analytical contribution is to quantify how mixed-call handling, unequal sampling and changing study contributions affect interpretation. Existing studies already describe related resistance trends in Kilifi. Explain that relationship honestly and ask the lecturer to assess overlap with classmates' proposals.

Strong work will show a clear biological question, traceable data, justified preparation, interpretable analysis, readable figures and limitations supported by the evidence. An app, machine learning model or elaborate extra analysis is not needed to establish those strengths. Marks depend on the course rubric and the group's execution.

## Checkpoint deliverables

| Stage | Deliverable to prepare | Resources in this folder |
|---|---|---|
| Checkpoint 1: definition | Refined title, biological problem, question, scope, beneficiaries and 2–4 objectives; initial data idea. | Proposal DOCX; original course instructions; reading guide. |
| Checkpoint 2: data sources | Source table with release, access link, unit of observation, relevant fields, availability and limitations. | Original Pf8 README; source manifest; data dictionary; Pf8 paper. |
| Checkpoint 3: preparation and exploration | Reproducible join/filter workflow, inclusion audit, marker mapping, coverage and study summaries. | Notebook; prepared CSVs; validation JSON; yearly sample-count chart. |
| Checkpoint 4: bioinformatics analysis | Annual/period marker estimates, uncertainty and justified sensitivity comparisons. | Analysis helpers; summary CSVs; comparison figures; method notes. |
| Checkpoint 5: biological interpretation | Explain observed patterns, compare literature, discuss study composition and distinguish marker surveillance from clinical conclusions. | Reading guide; example-output questions; decision record. |
| Final report and presentation | Integrated report, readable selected figures, reproducible methods, references, contribution record and practiced answers. | Report outline; notebook; outputs; group notes. |

Use lecturer feedback to decide whether the table-based analysis of sequence-derived genotypes is sufficient for your Genomics track. The supplied scope does not claim to perform read alignment, de novo variant calling or a whole-genome analysis.

## Six work areas — choose owners yourselves

No names are assigned. For a smaller group, combine adjacent areas; the course allows a maximum of six members. Each area should have an owner and a second person who can reproduce or explain it.

| Work area | Concrete responsibilities | Cross-review |
|---|---|---|
| Biology and prior studies | Explain PfCRT/K76T, extract relevant study methods, write evidence-backed background and comparison. | Review the interpretation with the sensitivity owner. |
| Sources and sample quality | Verify provenance, source fields, exclusions, same-case checks and study inventory. | Rebuild the prepared cohort with the primary analysis owner. |
| Primary analysis | Explain category coding, denominators, annual/period summaries and Wilson intervals. | Check selected calculations manually with the source-quality owner. |
| Sensitivity and inference | Compare mixed-call definitions, largest-study restriction and annual weighting; assess the period test's limits. | Explain the results to the biology owner. |
| Figures and validation | Reproduce charts, check labels/counts/missing years, write captions and identify misleading displays. | Review each chart with the primary analysis owner. |
| Reproducibility and integration | Run the full workflow from a fresh extracted folder, maintain decisions, integrate report and presentation evidence. | Have a second member repeat the complete run. |

Everyone should contribute to interpretation, review the final report and be able to explain the full research question. Record actual contributions; do not claim a task was done because it appears in this plan.

## First group meeting

1. Read the proposed question aloud and agree on its unit of analysis: archived samples.
2. Confirm class group, official group number, submission dates and lecturer feedback process.
3. Open the main prepared CSV and identify sample, year, study and marker columns.
4. Read the outcome definitions and explain one mixed K/T example together.
5. Run the script or notebook and compare the outputs with the supplied examples.
6. Assign work areas and record any question or scope revision in the decision template.
