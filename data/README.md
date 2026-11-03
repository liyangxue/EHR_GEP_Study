# Local data directory

This directory is intentionally empty in the public repository.

Obtain the annotation data from [PhysioNet, version 1.0.0](https://physionet.org/content/mimic-iv-ext-gender-stigma/1.0.0/) ([DOI: 10.13026/x00d-c603](https://doi.org/10.13026/x00d-c603)) through credentialed access. The release file is `mimic_iv_gep_stigmatizing_language_annotations_v1_0_0.csv`. It contains annotations and MIMIC linkage identifiers, but no clinical note text or train/test indicator.

Place only authorized local working files here, or set `GEP_DATA_DIR` to a secure credentialed-data location. The repository `.gitignore` prevents files in this directory from being tracked, except for this README.

See [`DATA_ACCESS.md`](../DATA_ACCESS.md) for access details and [`SPLIT_GUIDE.md`](../SPLIT_GUIDE.md) for the train/test design.

