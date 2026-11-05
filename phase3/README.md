# INFO 2950 Phase 3

Inflation and monthly S&P 500 price returns, January 2017-September 2026.

## Files

- `Phase3_Report.pdf`: report for review and submission to Gradescope.
- `Phase3_Report.ipynb`: fully executed report notebook.
- `Phase3_Report.html`: browser-readable export used to produce the PDF.
- `Phase3_Data_Cleaning.ipynb`: fully executed, separate cleaning notebook.
- `data/raw/`: original four Phase 2 snapshots plus the added FEDFUNDS snapshot.
- `data/processed/`: seven analysis-ready samples, exclusion logs, source audit, and source hashes.
- `support/analysis_amendment.md`: Phase 3 method additions and their distinction from the original preregistration.
- `requirements.txt`: package versions used to execute the notebooks.

## Run the project

Download or clone the entire folder, keeping its structure. Open a notebook with this folder as its working directory. Install the packages in `requirements.txt` if needed, then restart and run all cells in this order:

1. `Phase3_Data_Cleaning.ipynb`
2. `Phase3_Report.ipynb`

Both notebooks run from saved files and do not require new data downloads. The report does not run the cleaning pipeline or silently refresh source data. The cleaning notebook recreates all report inputs.

The main models retain the final Phase 2 plan: same-month headline inflation (116 observations), and previous-calendar-month headline inflation (114 observations). Core inflation and expectations remain descriptive. Added analyses are explicitly labeled; inference accounts for calendar gaps and is accompanied by ordinary OLS and bandwidth comparisons.

## Before submission

Review the findings, code, and AI-assistance acknowledgement with both group members. Submit the PDF on Gradescope and tag its sections to the appropriate rubric questions. Phase 3 is due November 10, 2026; peer review is November 13; Phase 4 is due November 19. The 20-page PDF meets the requested 5-40-page range. This package has not been submitted to Gradescope.

The PDF links to the separate cleaning notebook on the `phase3-draft-2026-11-05` branch of the existing project repository. The branch preserves the main project while making the reproducibility materials accessible to course staff.

## Validation

- All numeric columns shared with the Phase 2 analysis dataset reproduce within floating-point tolerance.
- Main and lagged samples contain 116 and 114 unique months; no row-shift bridges the missing October 2025 CPI value.
- The 2020 sensitivity samples contain 114 and 112 months, excluding only March and April 2020.
- scikit-learn and statsmodels produce matching main-model coefficients.
- The calendar-aware HAC covariance matches statsmodels HAC on a consecutive sample and an independent pairwise calculation on each gapped sample.
- Both notebooks were executed from fresh kernels. The final report contains no error or warning outputs.
- The PDF was generated from the executed notebook through HTML and visually inspected for clipping, crowded labels, missing plots, and pagination.

OpenAI Codex assisted with preparation, execution, and these automated checks; these are not claims of checks personally performed by the student authors.

The exported PDF and HTML are provided in the local submission package. This branch hosts the notebooks, source data, cleaned inputs, and supporting scripts.
