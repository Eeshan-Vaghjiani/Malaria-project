# Dataset guide and dictionary

## Which file should we use?

| File | Rows | Purpose |
|---|---:|---|
| `Original_Pf8/Pf8_samples.txt` | 33,325 | Original worldwide sample metadata; tab-separated despite its `.txt` extension. |
| `Original_Pf8/Pf8_drug_resistance_marker_genotypes.tsv` | 24,409 | Original worldwide marker calls for QC-passing samples. The project uses `Sample` and `crt_76[K]`. |
| `Original_Pf8/Pf8_README.txt` | — | Original provider documentation, including encoding and QC definitions. |
| `Kilifi_Subsets/kilifi_pfcrt_qcpass.csv` | 1,872 | Main prepared dataset; one retained sample per row. Start here for analysis. |
| `Kilifi_Subsets/kilifi_pfcrt_unambiguous.csv` | 1,703 | Secondary subset excluding mixed and uncallable codon-76 calls. |
| `Kilifi_Subsets/kilifi_inclusion_audit.csv` | 2,078 | Every Kilifi metadata record, source QC information and inclusion decision. |
| `Kilifi_Subsets/study_inventory.csv` | 4 | Sample counts and first/last observed year for each contributing study. |
| `Kilifi_Subsets/year_coverage.csv` | 27 | Every year from 1994 to 2020; includes explicit zero sample counts for 2001 and 2002. |

These counts describe the bundled snapshot, verified against the [official Pf8 downloads](https://www.malariagen.net/data_package/open-dataset-plasmodium-falciparum-v80/). They are not counts of current malaria cases in Kilifi.

## Preparation rules

1. Read both original tables as text and join by `Sample`, requiring one-to-one identifiers.
2. Retain metadata where `Country = Kenya` and `Admin level 1 = Kilifi`.
3. Require `QC pass = True` and a valid integer collection year from 1994 through 2020, inclusive.
4. Keep original marker text, then normalize the order of comma-separated K/T calls.
5. Keep uncallable calls in the QC cohort, but exclude them from marker-specific denominators. This snapshot has none among retained Kilifi records.
6. Check the provider's recorded same-case groups. The retained rows have 1,872 distinct recorded case groups. This checks recorded linkage; it cannot identify unrecorded repeat sampling.
7. Retain study identifiers and collection year for sensitivity analyses. Preserve missing years explicitly.

The script records 206 source-QC exclusions and no additional year exclusions after QC. It does not invent a new coverage threshold or reinterpret excluded records as K-only. Changing these rules requires a documented revision and regeneration of the derived files.

## Main dataset fields

Both prepared sample-level CSVs use this schema. Empty CSV cells indicate missing/not applicable values; no numeric missing-value code is used.

| Field | Type / values | Meaning and source |
|---|---|---|
| `sample_id` | Text; unique | Public sample identifier from `Sample`; the join key. Preserve as text. |
| `study` | Text | Contributing study ID from `Study`. It is not a treatment assignment. |
| `country` | Text | `Kenya`, from source metadata. |
| `admin1` | Text | `Kilifi`, from source administrative-area metadata; not an individual address. |
| `year` | Integer | Sample collection year from `Year`; 1994–2020. Publication year must not replace it. |
| `case_group` | Text | Sorted, comma-separated sample IDs from `All samples same case`, identifying recorded samples from the same individual. Treat the whole cell as one group key. |
| `qc_pass` | Boolean | Source `QC pass`; all rows here are `True`. |
| `genome_callable_pct` | Number, percent | Source `% callable`, a genome coverage/callability measure. It is not a within-host allele fraction. |
| `sample_type` | Text | Source `Sample type`, retained without recoding. Consult the provider README for its codes. |
| `ena_accessions` | Text | Source ENA sequencing accession information, retained unchanged. No sequencing reads are downloaded by the starter analysis. |
| `raw_crt76_call` | Text | Exact source value from `crt_76[K]`, before project recoding. CSV quoting preserves embedded commas. |
| `marker_call` | Category | `K_only`, `T_only`, `mixed_KT` or `uncallable`; see mapping below. |
| `marker_callable` | Boolean | `True` for K-only, T-only or mixed K/T; `False` for unresolved/missing calls. |
| `has_76T` | Integer 0 / 1 / blank | Primary outcome: 0 for K-only; 1 for T-only or mixed K/T; blank for uncallable. |
| `unambiguous_76T` | Integer 0 / 1 / blank | Secondary outcome: 0 for K-only; 1 for T-only; blank for mixed or uncallable. |
| `time_period` | Text category | Predefined groups: 1994–1999, 2000–2004, 2005–2009, 2010–2014, 2015–2020. Stored with ordinary hyphens. |
| `source_release` | Text | `MalariaGEN Pf8`; identifies the source release. |

The audit CSV retains source column names. `included_qc_cohort` is the final inclusion Boolean; `inclusion_reason` is `included_QC_cohort`, `excluded_QC` or `excluded_year`. If both QC and year are invalid, the audit labels QC first. The source `Exclusion reason` is preserved.

## Exact marker mapping

| Original `crt_76[K]` | Project category | `has_76T` | `unambiguous_76T` |
|---|---|---:|---:|
| `K` | `K_only` | 0 | 0 |
| `T` | `T_only` | 1 | 1 |
| `K,T` or `T,K` | `mixed_KT` | 1 | blank |
| Missing, `-`, unresolved symbols or unexpected calls | `uncallable` | blank | blank |

The provider README describes `-` as missing, `*` as an unresolved haplotype with multiple heterozygous positions, and `!` as a frameshift call. Those symbols are handled conservatively by the starter code and do not occur in the retained codon-76 subset. Unexpected values should be investigated before an updated analysis is accepted.

`K` is lysine and `T` is threonine at PfCRT amino-acid position 76. A mixed call means that the pipeline detected both residue states in the sample. It must not automatically be converted to half a resistant allele. A K-only call describes this position; it does not establish that the whole gene is wild type or that a patient's infection is clinically chloroquine-sensitive. See [Fidock et al.](https://doi.org/10.1016/S1097-2765(05)00077-8) for experimental background and the provider README for technical encoding.

## Denominators and uncertainty

- **Primary sample carriage:** `(T_only + mixed_KT) / (K_only + T_only + mixed_KT)`.
- **Secondary unambiguous proportion:** `T_only / (K_only + T_only)`.
- **Composition:** each of K-only, T-only and mixed K/T divided by all callable records.

The scripts export proportions on a **0–1 scale**, not percentages. Multiply by 100 only for percentage display. Wilson 95% confidence intervals accompany each binomial proportion. These intervals describe binomial sampling uncertainty under the working independence assumption; they do not correct archive selection bias or study differences.

Annual summaries contain 27 rows. For years with no samples, counts are 0 but proportions and confidence limits are blank. Do not replace those blanks with zero. The secondary result is not an estimate of within-host clone frequency or a universal correction of the primary measure.

## Opening the files

CSV files can be opened in Excel or another spreadsheet viewer. Import original TXT/TSV files using a **tab** delimiter, and keep identifiers as text. Do not save edits over the original files. Commas within a quoted field are part of its value; use a CSV parser rather than splitting lines manually. The notebook reads the original files itself, so spreadsheet software is optional.
