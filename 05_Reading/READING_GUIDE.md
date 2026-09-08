# Reading guide and resource index

Start with the provider README and the Pf8 paper, then read the two closely related Kenyan studies. Three full open-access PDFs are included for offline reading. Fidock et al. and software documentation are linked online. This is a focused starter reading set, not an exhaustive literature review.

## 1. Understand the dataset

**Malaria Genomic Epidemiology Network (MalariaGEN) et al. (2025).** “Pf8: an open dataset of Plasmodium falciparum genome variation in 33,325 worldwide samples.” *Wellcome Open Research*, 10:325. [Published article](https://doi.org/10.12688/wellcomeopenres.24031.1).

- Included PDF: `MalariaGEN_2025_Pf8.pdf` (20 pages; version 1).
- Why read it: explains the resource, sequence-derived genotypes, filtering and available analyses. It also places chloroquine-resistance marker trends in a wider context.
- Extract for your report: data release, collection scope, source processing and the limits of using derived marker calls.
- Read alongside: `02_Datasets/Original_Pf8/Pf8_README.txt`, which documents the actual file columns and call encoding.

**Official data landing page:** [MalariaGEN Pf8 open dataset](https://www.malariagen.net/data_package/open-dataset-plasmodium-falciparum-v80/).

| Resource | Direct original download | Included locally? |
|---|---|---|
| Worldwide metadata | [Pf8_samples.txt](https://zenodo.org/records/18681980/files/Pf8_samples.txt?download=1) | Yes, unchanged in `02_Datasets/Original_Pf8`. |
| Resistance marker calls | [Pf8_drug_resistance_marker_genotypes.tsv](https://zenodo.org/records/18681980/files/Pf8_drug_resistance_marker_genotypes.tsv?download=1) | Yes, unchanged in `02_Datasets/Original_Pf8`. |
| Provider documentation | [Pf8_README.txt](https://zenodo.org/records/18681980/files/Pf8_README.txt?download=1) | Yes, unchanged in `02_Datasets/Original_Pf8`. |
| Supplementary resource / contributing-study information | [Pf8 supplementary resource on Figshare](https://figshare.com/articles/online_resource/Supplementary_data_to_Pf8_an_open_dataset_of_i_Plasmodium_falciparum_i_genome_variation_in_33_325_worldwide_samples/29153447) | Online link; use when investigating source study designs. |
| Genome-wide calls, sequencing access and additional applications | [Pf8 resource catalogue](https://www.malariagen.net/data_package/open-dataset-plasmodium-falciparum-v80/) | Online only; not required by the supplied marker-level analysis. |

Source links and hashes are recorded in `07_Reproducibility/source_manifest.json`. The project preserves the retrieved files as a fixed snapshot rather than silently following later releases.

## 2. Read the closest prior Kilifi study

**Omedo, I. et al. (2022).** “Spatio-temporal distribution of antimalarial drug resistant gene mutations in a Plasmodium falciparum parasite population from Kilifi, Kenya: A 25-year retrospective study.” *Wellcome Open Research*, 7:45. [Published article, version 1](https://doi.org/10.12688/wellcomeopenres.17656.1).

- Included PDF: `Omedo_2022_Kilifi.pdf` (21 pages; version 1).
- Why read it: directly related work on Kilifi samples collected during 1994–2018, using amplicon sequencing and multiple resistance markers.
- Extract: sample selection, assay, marker definitions, denominators, temporal patterns and limitations.
- Implication for your proposal: the broad biological trend is already studied. Your intended contribution is a focused Pf8 reanalysis through 2020 with explicit mixed-call and sampling sensitivity checks. Lecturer acceptance of that distinction is still necessary.

## 3. Compare another long-term coastal Kenyan analysis

**Wamae, K. et al. (2019).** “No Evidence of Plasmodium falciparum k13 Artemisinin Resistance-Conferring Mutations over a 24-Year Analysis in Coastal Kenya but a Near Complete Reversion to Chloroquine-Sensitive Parasites.” *Antimicrobial Agents and Chemotherapy*, 63(12):e01067-19. [Published article](https://doi.org/10.1128/AAC.01067-19).

- Included PDF: `Wamae_2019_Coastal_Kenya.pdf` (12 pages).
- Why read it: provides related longitudinal resistance-marker evidence and local biological context.
- Extract: collection window, sample design, marker detection and how the authors support their interpretation.
- Comparison task: explain differences from your scope and determine whether data sources overlap before describing the paper as independent validation. Do not transfer the title's phenotype wording directly to a single-codon analysis.

## 4. Understand why PfCRT matters biologically

**Fidock, D. A. et al. (2000).** “Mutations in the P. falciparum Digestive Vacuole Transmembrane Protein PfCRT and Evidence for Their Role in Chloroquine Resistance.” *Molecular Cell*, 6(4):861–871. [DOI](https://doi.org/10.1016/S1097-2765(05)00077-8) · [PubMed record](https://pubmed.ncbi.nlm.nih.gov/11090624/) · [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC2944663/).

- Access: online links; a PDF is not bundled.
- Why read it: foundational experimental work connecting PfCRT mutations with chloroquine resistance.
- Extract: the protein's cellular role and the evidence supporting the resistance association.
- Keep clear: experimental mechanism evidence and the descriptive temporal archive analysis answer different questions. Your data observe marker calls; they do not reproduce a drug-susceptibility experiment.

## 5. Learn the tools used here

| Need | Official resource | Use in this project |
|---|---|---|
| A separate Python environment | [Python venv documentation](https://docs.python.org/3/library/venv.html) | Install the recorded packages without changing other projects. |
| Read and manipulate tables | [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html) | Joins, filters, group counts and CSV export. |
| Understand array calculations | [NumPy user guide](https://numpy.org/doc/stable/user/index.html) | Numerical operations used by the analysis helpers. |
| Learn plots and labels | [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html) | Reproduce and improve the scientific figures. |
| Understand the period test | [SciPy chi2_contingency](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html) | Assumptions and interpretation of the exploratory contingency-table comparison. |
| Open a notebook locally | [JupyterLab installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) | Run the starter notebook in the same Python environment. |
| Work in a browser | [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) | Understand notebook sessions, uploads and temporary files. |
| Import the bibliography | [Zotero importing guidance](https://www.zotero.org/support/adding_items_to_zotero) | Import `references.bib`, then check metadata against each paper. |

The starter scripts are Python-based. You may use another tool your group knows if it reproduces the documented inclusion rules and measures. Record any change and verify the resulting counts and figures.

## Literature notes template

For each paper, record: full citation; research question; samples and collection years; assay/dataset; marker definition; main finding relevant to your question; limitations; possible sample overlap; and how your project differs. Write notes in your own words and keep page/figure references for checking.

The full PDFs retain their authorship, article version and Creative Commons attribution notices. Do not treat included papers or the supplied analysis as work performed by your group. See `ATTRIBUTION_AND_REUSE.md`.
