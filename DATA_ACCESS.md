# Data access and local setup

## What is not included

This repository does not contain MIMIC-IV or MIMIC-IV-Note clinical records, clinical note text, MIMIC identifiers, patient-level predictions, or the credentialed annotation dataset.

Access to MIMIC-IV and MIMIC-IV-Note is governed by PhysioNet. Users must independently obtain credentialed access, complete the required training, and comply with the applicable data use agreement.

## Annotation data

The annotations are published as [MIMIC-IV-Ext Gender-Expansive Patient Stigmatizing Language Annotations, version 1.0.0](https://physionet.org/content/mimic-iv-ext-gender-stigma/1.0.0/) on PhysioNet. The version-specific DOI is [10.13026/x00d-c603](https://doi.org/10.13026/x00d-c603), and the release date is October 19, 2026.

The release file, `mimic_iv_gep_stigmatizing_language_annotations_v1_0_0.csv`, contains 754 note-level records from 580 patients and 19 columns. It includes stigma labels, demographic fields, and MIMIC linkage identifiers. It does not contain clinical note text or a train/test indicator. The data dictionary and annotation definitions are provided on the PhysioNet release page.

To use the data:

1. Follow the credentialing and training requirements on the PhysioNet release page and sign the applicable data use agreement. The annotation files are governed by the PhysioNet Credentialed Health Data License 1.5.0, not the repository's MIT software license.
2. Obtain authorized access to [MIMIC-IV](https://physionet.org/content/mimiciv/) and [MIMIC-IV-Note](https://physionet.org/content/mimic-iv-note/2.2/) for the source records.
3. Download the annotation CSV from PhysioNet to an authorized local environment. Link it to the source discharge summaries using `note_id` and, where appropriate, `subject_id`. Check that the join preserves one row per annotation record.
4. Create local analysis files as required by the notebooks. Keep the data and linked text out of public version control.

Within an authorized environment, users may link the annotation records to MIMIC-IV-Note and construct local analysis files. Do not move the linked files outside the authorized environment or commit them to this repository.

### Relationship to the published analyses

As disclosed on PhysioNet, the release includes updates to selected demographic variables compared with the dataset used for the associated publication. The underlying notes and stigma annotations remain unchanged. Analyses using the updated demographic variables may produce results that differ from the publication. Do not interpret a rerun on the release as an exact reproduction of every published regression estimate or subgroup result.

The public repository retains the study's code, figures, and aggregate results. These have not been regenerated for the PhysioNet release. Cite both the article and the dataset when using the annotations, and follow the additional citation instructions on PhysioNet. Citation details are in [README.md](README.md#citation).

## Expected local files

Most notebooks expect the following locally reconstructed files under `GEP_DATA_DIR`:

| File | Notes | Intended role |
|---|---:|---|
| `GEP_train_80_20.csv` | 603 | Model fitting, hyperparameter selection, and fairness-threshold selection |
| `GEP_test_80_20.csv` | 151 | Held-out final evaluation |

This is a note-level split. No note appears in both files, but 31 patients have different notes in both sets; it is therefore not a patient-disjoint split. Do not create a new random split if the goal is to reproduce the published metrics.

The public GitHub repository cannot include the original split assignments because they contain MIMIC identifiers. The combined PhysioNet annotation file does not contain clinical text or a train/test indicator. Exact reconstruction therefore requires the original authorized split assignment in addition to credentialed MIMIC-IV-Note access. Do not rename the combined release CSV as either split file or assume that a new random 80/20 partition recreates the published split. See [SPLIT_GUIDE.md](SPLIT_GUIDE.md).

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

