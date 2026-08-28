# Data access and local setup

## What is not included

This repository does not contain MIMIC-IV or MIMIC-IV-Note clinical records, clinical note text, MIMIC identifiers, patient-level predictions, or the credentialed annotation dataset.

Access to MIMIC-IV and MIMIC-IV-Note is governed by PhysioNet. Users must independently obtain credentialed access, complete the required training, and comply with the applicable data use agreement.

## Annotation data

The study annotation release contains note-level labels and identifiers that allow authorized users to link the annotations to MIMIC-IV records. It does not contain clinical note text and is intended for credentialed distribution through PhysioNet.

Within an authorized environment, users may link the annotation records to MIMIC-IV-Note and construct local analysis files. Do not move the linked files outside the authorized environment or commit them to this repository.

## Expected local files

Most notebooks expect the following locally reconstructed files under `GEP_DATA_DIR`:

| File | Notes | Intended role |
|---|---:|---|
| `GEP_train_80_20.csv` | 603 | Model fitting, hyperparameter selection, and fairness-threshold selection |
| `GEP_test_80_20.csv` | 151 | Held-out final evaluation |

This is a note-level split. No note appears in both files, but 31 patients have different notes in both sets; it is therefore not a patient-disjoint split. Do not create a new random split if the goal is to reproduce the published metrics.

The public GitHub repository cannot include the original split assignments because they contain MIMIC identifiers. The combined credentialed annotation file does not contain clinical text or a train/test indicator. Exact reconstruction therefore requires the original authorized split assignment in addition to credentialed MIMIC-IV-Note access. See [SPLIT_GUIDE.md](SPLIT_GUIDE.md).

The code expects a `text` column containing authorized local note text and analysis columns used in the article, including:

- `GEP`
- `label`
- `label_exclude_misgendering`
- `Credibility and Obstinacy`
- `Compliance`
- `Descriptors`
- `Descriptors_exclude_misgendering`
- `Misgendering`
- `race_grouped`
- `language_grouped`
- `age_group`

The article and public code use the corrected subtype name `Credibility and Obstinacy`. If a legacy authorized file contains `Credibility and Obstinance`, rename that column locally before running the notebooks.

Some cohort-construction notebooks also expect locally available MIMIC-IV demographic tables and the MIMIC-IV-Note discharge-note table. Their paths should remain inside the credentialed data environment.

## Environment variables

The cleaned notebooks use these optional variables:

- `GEP_PROJECT_ROOT`: repository root; defaults to the current working directory
- `GEP_DATA_DIR`: local credentialed data directory; defaults to `data/`
- `GEP_MODEL_DIR`: local model and checkpoint directory; defaults to `models/`
- `GEP_RESULTS_DIR`: generated result directory; defaults to `results/`
- `GEP_FIGURES_DIR`: generated figure directory; defaults to `figures/`

Launch Jupyter from the repository root or set the variables explicitly before running a notebook.

## Intermediate checkpoints

The multistage transfer-learning notebooks reference locally generated intermediate Longformer checkpoints. These model files were not present in the supplied archive and are not included in the public repository. Users who do not have those checkpoints can still review the workflow and reproduce analyses that begin from publicly available base models, but the full multistage sequence requires the corresponding intermediate training artifacts.
