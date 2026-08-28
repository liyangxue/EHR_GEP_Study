# Stigmatizing Language in Gender-Expansive Patient Records

[![JMIR article](https://img.shields.io/badge/JMIR-2026-e91089-1769aa)](https://www.jmir.org/2026/1/e91089)
[![DOI](https://img.shields.io/badge/DOI-10.2196%2F91089-1769aa)](https://doi.org/10.2196/91089)

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

## Data availability

The annotation dataset is being prepared for release through PhysioNet under credentialed access. It contains note-level annotations and MIMIC identifiers that allow authorized users to link the annotations to source records. Clinical note text is not included.

Access to the underlying records requires separate credentialed access to [MIMIC-IV](https://physionet.org/content/mimiciv/) and [MIMIC-IV-Note](https://physionet.org/content/mimic-iv-note/2.2/), completion of the required human-subjects research training, and acceptance of the applicable PhysioNet data use agreement.

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
