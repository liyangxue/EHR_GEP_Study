# Stigmatizing Language in Gender-Expansive Patient Records

[![JMIR article](https://img.shields.io/static/v1?label=JMIR&message=e91089&color=1769aa)](https://www.jmir.org/2026/1/e91089)
[![DOI](https://img.shields.io/static/v1?label=DOI&message=10.2196%2F91089&color=1769aa)](https://doi.org/10.2196/91089)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository accompanies the following article:

> Xue L, Chayko M, Singh VK. Stigmatizing Language in Gender-Expansive Patient Records: Corpus Development, Disparity Analysis, and Natural Language Processing–Based Detection Study. *Journal of Medical Internet Research*. 2026;28:e91089. [https://doi.org/10.2196/91089](https://doi.org/10.2196/91089)

## Overview

This study examines stigmatizing language in electronic health record documentation concerning gender-expansive patients. We constructed and manually annotated a corpus of 754 deidentified MIMIC-IV clinical notes, including 366 notes from gender-expansive patients and 388 demographically matched comparison notes.

Annotations cover three nonmutually exclusive categories of stigmatizing language—credibility and obstinacy, compliance, and descriptors—as well as misgendering. We conducted parallel analyses with and without misgendering, quantified disparities using multivariable logistic regression, evaluated natural language processing models for automated detection, and tested fairness-aware threshold adjustments.

## Key findings

- Stigmatizing language was identified in 62.3% (228/366) of notes from gender-expansive patients and 25.5% (99/388) of matched comparison notes.
- After misgendering was excluded, stigmatizing language remained more prevalent in notes from gender-expansive patients at 41.8% (153/366).
- Gender-expansive status remained associated with stigmatizing documentation after adjustment both when misgendering was included (adjusted odds ratio 4.87, 95% CI 3.54-6.70) and excluded (adjusted odds ratio 2.12, 95% CI 1.54-2.91).
- Fairness-aware threshold optimization reduced subgroup differences in model error rates while maintaining similar overall accuracy.

## Repository scope

This repository is intended to provide publicly shareable analysis, evaluation, and visualization code associated with the study. It does not redistribute MIMIC-IV or MIMIC-IV-Note records, clinical note text, or MIMIC identifiers.

The public notebooks have been cleared of outputs and use repository-local paths or environment variables instead of personal or Google Drive paths. Re-execution requires credentialed access to the source data and locally reconstructed analysis files. Some multistage transfer notebooks also require intermediate model checkpoints generated during the study; model checkpoints are not included in this repository.

## Repository structure

```text
.
├── notebooks/
│   ├── analysis/      # Cohort, reliability, descriptive, and regression analyses
│   ├── models/        # Traditional ML, BERT, ClinicalBERT, and Longformer training
│   ├── evaluation/    # Held-out and transfer-learning evaluation
│   ├── subtypes/      # Stigma-subtype models and comparisons
│   └── fairness/      # Subgroup metrics and threshold optimization
├── scripts/figures/   # Scripts used to generate Figures 2-7
├── scripts/threshold_protocol.py # Shared leakage-safe threshold utilities
├── figures/           # Publication-ready versions of Figures 2-7
├── results/aggregate/ # Non–patient-level aggregate results
├── data/              # Documentation only; source data are not tracked
├── DATA_ACCESS.md
├── SPLIT_GUIDE.md
├── FILE_MANIFEST.md
└── requirements.txt
```

## Train and test sets

The annotated corpus was divided at the note level into a training set of 603 notes (80%) and a held-out test set of 151 notes (20%). The corresponding authorized local files are `GEP_train_80_20.csv` and `GEP_test_80_20.csv`.

The note identifiers are disjoint across the two files. The split is not patient-disjoint: 31 patients have different notes in both sets. Results should therefore be interpreted as note-level held-out performance rather than patient-independent generalization.

Under the published workflow, model fitting, hyperparameter selection, and fairness-threshold selection use the training set; the test set is reserved for final evaluation. Descriptive and regression analyses use the full 754-note corpus. Exact split assignments are not included in this public repository because they require MIMIC identifiers.

For neural models, epoch or configuration selection is performed on an internal stratified subset drawn only from the 603-note training set. For traditional models, selection uses cross-validation within the training set. After a fitted model has been frozen, group-specific fairness thresholds are selected from its predictions on the official training set. The prespecified best-fair rule uses a maximum ΔFPR of 0.07; if no threshold pair satisfies that constraint, the pair with the smallest training-set ΔFPR is retained. The selected thresholds are then applied unchanged to the 151-note held-out test set.

See [SPLIT_GUIDE.md](SPLIT_GUIDE.md) for counts, intended use, and reconstruction details.

## Getting started

Python 3.10 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run Jupyter from the repository root so that the default relative paths resolve correctly:

```bash
jupyter lab
```

Alternatively, set one or more of the following environment variables:

```bash
export GEP_DATA_DIR=/path/to/authorized/local/data
export GEP_MODEL_DIR=/path/to/local/model/checkpoints
export GEP_RESULTS_DIR=/path/to/output/results
export GEP_FIGURES_DIR=/path/to/output/figures
```

See [DATA_ACCESS.md](DATA_ACCESS.md) for the required local data structure and access restrictions, and [SPLIT_GUIDE.md](SPLIT_GUIDE.md) for the published train/test design.

The fairness notebooks expect local prediction files under `results/predictions/`. Each file must contain `label`, `GEP`, and `probability`, and the paired training and testing files must be generated by the same frozen fitted model. These patient-level prediction files are intentionally excluded from the public repository.

## Data availability

The annotation dataset is being prepared for release through PhysioNet under credentialed access. It contains note-level annotations and MIMIC identifiers that allow authorized users to link the annotations to source records. Clinical note text is not included.

Access to the underlying records requires separate credentialed access to [MIMIC-IV](https://physionet.org/content/mimiciv/) and [MIMIC-IV-Note](https://physionet.org/content/mimic-iv-note/2.2/), completion of the required human-subjects research training, and acceptance of the applicable PhysioNet data use agreement.

Do not commit reconstructed clinical text, MIMIC identifiers, patient-level predictions, model-error examples, or credentialed annotation files to a public repository. The included `.gitignore` excludes the expected local data and model directories by default.

## Citation

If you use this work, please cite:

```bibtex
@article{xue2026stigmatizing,
  author  = {Xue, Liyang and Chayko, Mary and Singh, Vivek Kumar},
  title   = {Stigmatizing Language in Gender-Expansive Patient Records: Corpus Development, Disparity Analysis, and Natural Language Processing–Based Detection Study},
  journal = {Journal of Medical Internet Research},
  year    = {2026},
  volume  = {28},
  pages   = {e91089},
  doi     = {10.2196/91089},
  url     = {https://www.jmir.org/2026/1/e91089}
}
```

## Authors

- Liyang Xue
- Mary Chayko
- Vivek Kumar Singh

Department of Library and Information Science, Rutgers, The State University of New Jersey

## License

The software and code in this repository are available under the [MIT License](LICENSE). The license does not grant access to MIMIC-IV, MIMIC-IV-Note, or credentialed annotation data; those resources remain subject to their respective access requirements and data use agreements.
