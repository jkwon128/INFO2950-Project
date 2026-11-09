# INFO 2950 Phase 3

This project examines how U.S. CPI inflation relates to monthly S&P 500 price returns from January 2017 through September 2026.

- [Data cleaning](Phase3_Data_Cleaning.ipynb) builds the analysis samples from the five archived [raw CSVs](data/raw) and writes them to [processed data](data/processed). That folder also contains the exclusion logs, source audit, and source manifest.
- [Report](Phase3_Report.ipynb) analyzes the processed data and contains the statistical tables and figures.
- [Analysis amendment](support/analysis_amendment.md) records how the Phase 3 methods and exploratory checks extend the final Phase 2 plan.

## Reproduce the results

Use Python 3.12 in an activated virtual environment and start in the repository's `phase3/` directory. Install the pinned packages in [requirements.txt](requirements.txt), then run the cleaning notebook before the report. The analysis uses pandas, NumPy, Matplotlib, scikit-learn, SciPy, and statsmodels. Jupyter runs both notebooks.

```sh
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace Phase3_Data_Cleaning.ipynb
jupyter nbconvert --to notebook --execute --inplace Phase3_Report.ipynb
```

To export the executed report, run `jupyter nbconvert --to html Phase3_Report.ipynb`, then open the HTML in a browser and print to PDF. The notebooks use the archived data. A Git checkout that preserves LF line endings also reproduces the raw-file hashes.

## AI acknowledgement

AI tools assisted with writing portions of the code, polishing the writing, and reviewing the draft. The authors are responsible for the final analyses and interpretations.
