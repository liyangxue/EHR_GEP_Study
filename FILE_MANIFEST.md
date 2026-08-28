# Public file manifest

This manifest describes the curated files intended for the public GitHub repository. Original notebook outputs, execution counters, personal paths, Google Drive mounts, and credentialed data are not included.

## Documentation

- `README.md`: project overview, repository structure, and main results
- `DATA_ACCESS.md`: credentialed-data requirements and secure local setup
- `SPLIT_GUIDE.md`: published 80/20 note-level split, counts, intended uses, and reconstruction limits
- `CITATION.cff`: machine-readable citation metadata
- `LICENSE`: MIT License for the software and code in this repository

## Analysis notebooks

- `01_cohort_and_demographic_matching.ipynb`: cohort construction and demographic matching
- `02_intercoder_reliability.ipynb`: manual-annotation agreement statistics
- `03_descriptive_analysis.ipynb`: cohort summaries, stigma prevalence, overlap counts, and consistency checks
- `04_regression_and_balanced_subsamples.ipynb`: multivariable, subtype-specific, sensitivity, and balanced-subsample analyses

## Model notebooks

The `notebooks/models/` directory contains paired analyses including and excluding misgendering for traditional machine learning, BERT, ClinicalBERT, task-only Longformer, and the Longformer transfer stages reported in the article.

## Evaluation notebooks

The `notebooks/evaluation/` directory contains the direct-transfer, retrained-transfer, and consolidated held-out evaluation workflows.

## Subtype notebooks

The `notebooks/subtypes/` directory contains accuracy- and F1-optimized subtype training for traditional machine learning, BERT, ClinicalBERT, and Longformer, plus the consolidated subtype evaluation.

## Fairness notebooks

The `notebooks/fairness/` directory contains subgroup metric calculation and training-prediction-based group-threshold selection for BERT, ClinicalBERT, base Longformer, and the multistage transfer model, with parallel outcome definitions. `scripts/threshold_protocol.py` implements the shared threshold-pair search, the prespecified ΔFPR≤0.07 rule, and application of frozen thresholds to held-out testing predictions.

## Figures and aggregate results

- `scripts/figures/figure_2_subtype_overlap.py`: Figure 2 and its aggregate count workbook
- `scripts/figures/figure_3_balanced_or_distribution.py`: Figure 3
- `scripts/figures/figure_4_mstl_performance_including_misgendering.py`: Figure 4
- `scripts/figures/figure_5_mstl_performance_excluding_misgendering.py`: Figure 5
- `scripts/figures/figures_6_7_accuracy_and_fairness.py`: Figures 6 and 7
- `figures/`: final PNG versions of Figures 2-7
- `results/aggregate/figure_2_subtype_overlap_counts.xlsx`: non–patient-level counts and consistency checks
- `results/aggregate/table_8_best_models_accuracy.csv`: aggregate subtype-model results selected by accuracy
- `results/aggregate/table_8_best_models_f1.csv`: aggregate subtype-model results selected by F1-score

## Intentionally excluded from the public bundle

- MIMIC-IV and MIMIC-IV-Note records or clinical note text
- Note, encounter, admission, stay, or patient identifiers
- Credentialed annotation data
- Patient-level predictions and error-analysis examples
- Trained model checkpoints
- Notebook outputs and embedded plots
- Dependency-discovery notebook and redundant copies
- Exploratory fairness ablations and older experiments not reported as final article results
- Legacy multihead evaluation CSV files whose results were not used in the final article
