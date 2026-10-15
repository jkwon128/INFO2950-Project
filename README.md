# INFO2950-Project

## Research Question
How does U.S. inflation relate to monthly S&P 500 price returns between January 2017 and
September 2026?

## Group Members
- Jaemin Kwon (jk2975)
- Mike Zhang (hz727)

## Data Sources
- **S&P 500 index level** (`SP500`), daily, S&P Dow Jones Indices LLC via FRED —
  https://fred.stlouisfed.org/series/SP500
- **Headline CPI**, all items, not seasonally adjusted (`CPIAUCNS`), monthly, U.S. Bureau of
  Labor Statistics via FRED — https://fred.stlouisfed.org/series/CPIAUCNS
- **Core CPI**, less food and energy, not seasonally adjusted (`CPILFENS`), monthly, BLS via
  FRED — https://fred.stlouisfed.org/series/CPILFENS
- **Inflation expectations** (`MICH`), monthly, University of Michigan Surveys of Consumers via
  FRED — https://fred.stlouisfed.org/series/MICH

## Repository Structure
```
data/raw/          The four source .csv files exactly as downloaded, unmodified
data/processed/    The analysis-ready dataset, the exclusion log, and summary statistics
notebooks/         Phase2_INFO2950.ipynb, the executed Phase II notebook
phase1/            Phase I submission
phase2/            Phase II notebook rendered as HTML
```

## Running the Notebook
`notebooks/Phase2_INFO2950.ipynb` reads its data from the `DATA` setting in Step 1. Set it to a
local `data/raw` folder, or to this repository:

```python
DATA = "https://raw.githubusercontent.com/jkwon128/INFO2950-Project/main/data/raw"
```

## Analysis Dataset
`data/processed/analysis_dataset.csv` holds 116 monthly observations from January 2017 to
September 2026. October 2025 is excluded because the CPI for that month was never published
during the federal government shutdown; the excluded row is recorded in
`data/processed/excluded_months.csv`.
