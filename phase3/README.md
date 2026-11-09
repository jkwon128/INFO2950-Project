# INFO 2950 Phase 3

Inflation and monthly S&P 500 price returns, January 2017 through September 2026.

## Notebooks and data

- [Report notebook](Phase3_Report.ipynb) and [data-cleaning notebook](Phase3_Data_Cleaning.ipynb), both with saved outputs.
- [Raw data](data/raw), including the four Phase 2 snapshots and the FEDFUNDS snapshot added for Phase 3.
- [Processed data](data/processed), including the seven analysis samples, exclusion logs, source audit, and [SHA-256 manifest](data/processed/source_manifest.json).
- [Analysis amendment](support/analysis_amendment.md) and [package versions](requirements.txt).

## Reproduce the analysis

Clone or download the repository with its directory structure intact. Install the packages in `requirements.txt` and use `phase3/` as the working directory for both notebooks. Restart the kernel and run all cells in the cleaning notebook, then in the report notebook. The cleaning notebook regenerates `data/processed/` from the saved snapshots. The report reads those exports. Neither notebook downloads fresh data.

The source hashes cover the raw CSV bytes. If Git converts LF line endings to CRLF on checkout, the local hashes differ even when the CSV values match. Use a checkout that preserves LF to reproduce the committed hashes.

To regenerate the notebook cells from their source, run `python support/build_cleaning.py` and `python support/build_report.py` from `phase3/`. The builders write notebooks without outputs. Run them in a separate copy if you need to keep the saved outputs.

## Validation

The same-month and previous-month samples contain 116 and 114 unique months, respectively. The calendar lag preserves the October 2025 CPI gap. The March–April 2020 sensitivity samples contain 114 and 112 months. Checks on the original draft also compared the Phase 2 numeric values, matched the scikit-learn and statsmodels coefficients, and checked the calendar-aware HAC covariance against statsmodels on consecutive months and a pairwise calculation on gapped samples.

See the Acknowledgements and bibliography in the [report](Phase3_Report.ipynb) for the scope of OpenAI Codex assistance, including notebook execution and automated checks.
