# Train/test split guide

## Published split

The 754 annotated notes were partitioned at the note level using a fixed 80/20 split.

| Split | Authorized local file | All notes | GEP notes | NGEP notes | Intended use |
|---|---|---:|---:|---:|---|
| Training | `GEP_train_80_20.csv` | 603 | 294 | 309 | Model fitting, hyperparameter selection, and fairness-threshold selection |
| Held-out test | `GEP_test_80_20.csv` | 151 | 72 | 79 | Final model and fairness evaluation |

The two files have identical annotation fields. Their `note_id` values are disjoint, so no note appears in both sets.

## Unit of splitting

The split was performed by note, not by patient. The training set contains notes from 475 patients and the test set contains notes from 136 patients; 31 patients have different notes in both sets. The reported model results are therefore note-level held-out results and should not be interpreted as patient-independent generalization.

## Use by workflow

- Descriptive statistics and regression analyses use the combined 754-note corpus.
- Model fitting and hyperparameter selection use the 603-note training set.
- Neural-model epochs or configurations are selected using an internal stratified subset of the training set; traditional models use training-set cross-validation.
- After the fitted model is frozen, fairness-aware group thresholds are selected from predictions on the full training set. The best-fair rule uses a prespecified maximum ΔFPR of 0.07, with a minimum-gap fallback when no threshold pair satisfies the constraint.
- Final predictive and fairness metrics are calculated on the 151-note held-out test set.

At no point may a testing-set metric determine which epoch, architecture, hyperparameter setting, or threshold pair is retained. Testing data are used only after all such choices are frozen.

## Secure reconstruction

Neither split file is distributed through this public GitHub repository. Each contains MIMIC identifiers, and the locally reconstructed modeling files also require a `text` column obtained by securely linking authorized annotation records to MIMIC-IV-Note.

The combined credentialed annotation file does not include clinical text or a train/test indicator. Consequently, the exact published split cannot be recreated from public repository files or by independently generating a new random 80/20 split. Reproduction of the published model metrics requires the original authorized split assignment.

The public code and article use the corrected subtype label `Credibility and Obstinacy`. A legacy local split file may instead contain `Credibility and Obstinance`; rename that column locally before execution.

Do not commit the reconstructed split files, their identifiers, or linked clinical text to a public repository.
