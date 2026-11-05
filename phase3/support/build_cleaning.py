from pathlib import Path
import nbformat as nbf
ROOT = Path(__file__).resolve().parents[1]
cells=[]
def md(s): cells.append(nbf.v4.new_markdown_cell(s.strip()))
def code(s): cells.append(nbf.v4.new_code_cell(s.strip()))
md('''# INFO 2950 Phase 3: Data Cleaning
Jaemin Kwon (jk2975) and Mike Zhang (hz727)

This notebook starts from the saved raw files and exports all datasets used by the Phase 3 report. It preserves the Phase 2 sample and transformations. The additions are a calendar-aligned inflation lag, named sensitivity samples, and a monthly interest-rate series for one exploratory model. No return regressions are fitted here.

Run this notebook from its folder before running `Phase3_Report.ipynb`. The five raw files are in `data/raw`. The original four files are unchanged copies of the Phase 2 snapshots; FEDFUNDS was downloaded from FRED for this phase. The source manifest records file hashes so later revisions can be detected.''')
md('''## 1. Read the raw files and check coverage
We keep the original values, parse dates, and create a month key. Increasing `Year * 12 + Month` by one always gives the next calendar month, including December to January. The checks catch duplicate source dates before a merge can multiply rows.''')
code('''from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from IPython.display import display

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
series = ["SP500", "CPIAUCNS", "CPILFENS", "MICH", "FEDFUNDS"]
raw = {}
audit = []
for name in series:
    frame = pd.read_csv(RAW / f"{name}.csv")
    frame["date"] = pd.to_datetime(frame["observation_date"])
    frame["Year"] = frame["date"].dt.year
    frame["Month"] = frame["date"].dt.month
    frame["month_index"] = frame["Year"] * 12 + frame["Month"]
    assert not frame["date"].duplicated().any()
    raw[name] = frame
    audit.append({"Series": name, "Rows": len(frame),
                  "Missing": int(frame[name].isna().sum()),
                  "First": str(frame.date.min().date()),
                  "Last": str(frame.date.max().date())})
display(pd.DataFrame(audit))''')
md('''## 2. Calculate month-end price returns
Remove daily rows without a closing price. Within each month, select the last recorded trading-day close, then match it to the preceding calendar month's close. Return is `100 * (close / previous_close - 1)`. This uses changes between actual closing levels, not changes in monthly averages. It excludes dividends and does not adjust for inflation.''')
code('''prices = raw["SP500"].dropna(subset=["SP500"]).copy()
ends = prices.groupby("month_index", as_index=False)["date"].max()
prices = ends.merge(prices, on=["month_index", "date"],
                    validate="one_to_one")
prices = prices.rename(columns={"SP500": "sp500_close",
                                "date": "last_trading_date"})
previous = prices[["month_index", "sp500_close"]].copy()
previous["month_index"] += 1
previous = previous.rename(columns={"sp500_close": "previous_close"})
prices = prices.merge(previous, on="month_index", how="left",
                      validate="one_to_one")
prices["sp500_return_pct"] = 100 * (
    prices["sp500_close"] / prices["previous_close"] - 1)
print("Monthly closing prices:", len(prices))
print("Daily rows without prices:", int(raw["SP500"].SP500.isna().sum()))''')
md('''## 3. Calculate year-over-year inflation
For each CPI series, match the current index to the same calendar month twelve months earlier. The not-seasonally-adjusted series is appropriate for this same-month-across-years comparison, although it does not remove every seasonal influence. A missing index stays missing. The October 2025 gap is documented in the BLS shutdown FAQ; we do not estimate a replacement.''')
code('''def inflation_table(name, level_name, rate_name):
    frame = raw[name][["month_index", name]].rename(
        columns={name: level_name})
    base = frame.copy()
    base["month_index"] += 12
    base = base.rename(columns={level_name: "base_value"})
    frame = frame.merge(base, on="month_index", how="left",
                        validate="one_to_one")
    frame[rate_name] = 100 * (frame[level_name] / frame.base_value - 1)
    return frame.drop(columns="base_value")

headline = inflation_table("CPIAUCNS", "headline_cpi", "headline_yoy_pct")
core = inflation_table("CPILFENS", "core_cpi", "core_yoy_pct")
expect = raw["MICH"][["month_index", "MICH"]].rename(
    columns={"MICH": "expected_inflation_pct"})
rates = raw["FEDFUNDS"][["month_index", "FEDFUNDS"]].rename(
    columns={"FEDFUNDS": "fedfunds_pct"})
display(raw["CPIAUCNS"].loc[raw["CPIAUCNS"].CPIAUCNS.isna(),
                          ["observation_date", "CPIAUCNS"]])''')
md('''## 4. Rebuild the Phase 2 analysis sample
Keep January 2017 through September 2026. Require both a return and headline inflation; missing expectations do not remove an otherwise usable month. FEDFUNDS is a monthly average in percent, not a month-end policy announcement or a monetary-policy surprise. We add it without changing the original sample.''')
code('''columns = ["month_index", "Year", "Month", "last_trading_date",
           "sp500_close", "sp500_return_pct"]
all_months = prices[columns].copy()
for frame in [headline, core, expect, rates]:
    all_months = all_months.merge(frame, on="month_index", how="left",
                                 validate="one_to_one")
all_months = all_months.loc[
    all_months.month_index.between(2017 * 12 + 1, 2026 * 12 + 9)
].sort_values("month_index").reset_index(drop=True)
all_months["date"] = pd.to_datetime(dict(
    year=all_months.Year, month=all_months.Month, day=1))
required = ["sp500_return_pct", "headline_yoy_pct"]
excluded = all_months.loc[all_months[required].isna().any(axis=1)].copy()
excluded["reason"] = "Missing same-month CPI: October 2025"
main = all_months.dropna(subset=required).copy()
print("Candidate months:", len(all_months))
print("Main sample:", len(main))
display(excluded[["Year", "Month", "reason"]])''')
md('''## 5. Prepare the lag and the named comparison samples
The final Phase 2 plan constructs the lag within the already restricted main sample. We keep that choice: January 2017 has no prior month in this sample, and November 2025 has no October CPI. October 2025 itself is already excluded. December 2016 CPI exists in the raw files; its exclusion here is a planned boundary choice, not unavailable source data.

The 2020 sensitivity samples exclude March and April 2020, the crash and rebound already identified in Phase 2. They do not exclude the whole year. The common-sample comparison uses exactly the lag model's months. All of these choices are saved before the report runs.''')
code('''lag_values = main[["month_index", "headline_yoy_pct"]].copy()
lag_values["month_index"] += 1
lag_values = lag_values.rename(
    columns={"headline_yoy_pct": "previous_headline_yoy_pct"})
with_lag = main.merge(lag_values, on="month_index", how="left",
                      validate="one_to_one")
lag = with_lag.dropna(subset=["previous_headline_yoy_pct"]).copy()
lag_excluded = with_lag.loc[with_lag.previous_headline_yoy_pct.isna(),
                            ["Year", "Month"]].copy()
lag_excluded["reason"] = ["No prior month inside planned sample",
                          "Previous-month CPI missing (October 2025)"]
shock_months = [2020 * 12 + 3, 2020 * 12 + 4]
samples = {
    "main": main,
    "lag": lag,
    "same_common": main.loc[main.month_index.isin(lag.month_index)],
    "main_no_extremes": main.loc[~main.month_index.isin(shock_months)],
    "lag_no_extremes": lag.loc[~lag.month_index.isin(shock_months)],
    "expectations": main.dropna(subset=["expected_inflation_pct"]),
    "interest": main.dropna(subset=["fedfunds_pct"])
}
display(lag_excluded)
display(pd.DataFrame({"Sample": samples.keys(),
                      "Months": [len(x) for x in samples.values()]}))''')
md('''## 6. Validate and export
These checks protect the sample sizes and the calendar alignment. We also verify that the lag really refers to one month earlier, rather than the preceding available row. A source manifest records the raw file hashes. Rerunning this notebook overwrites only the generated files in `data/processed`.''')
code('''expected_sizes = {"main": 116, "lag": 114, "same_common": 114,
                  "main_no_extremes": 114, "lag_no_extremes": 112,
                  "expectations": 115, "interest": 116}
for name, frame in samples.items():
    assert len(frame) == expected_sizes[name], name
    assert not frame.month_index.duplicated().any(), name
    assert frame[required].notna().all().all(), name
    frame.to_csv(OUT / f"{name}.csv", index=False)
lookup = main.set_index("month_index").headline_yoy_pct
assert np.allclose(lag.previous_headline_yoy_pct,
                   lookup.loc[lag.month_index - 1].to_numpy())
assert not lag.month_index.isin([2025 * 12 + 10, 2025 * 12 + 11]).any()
assert excluded[["Year", "Month"]].values.tolist() == [[2025, 10]]
assert lag_excluded[["Year", "Month"]].values.tolist() == [[2017, 1], [2025, 11]]
all_months.to_csv(OUT / "all_months.csv", index=False)
excluded.to_csv(OUT / "excluded_months.csv", index=False)
lag_excluded.to_csv(OUT / "lag_excluded_months.csv", index=False)
pd.DataFrame(audit).to_csv(OUT / "source_audit.csv", index=False)
manifest = {}
for name in series:
    path = RAW / f"{name}.csv"
    manifest[name] = {
        "source": f"https://fred.stlouisfed.org/series/{name}",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "snapshot": "Phase 2 preserved" if name != "FEDFUNDS"
                    else "Phase 3 addition, November 4, 2026"
    }
(OUT / "source_manifest.json").write_text(json.dumps(manifest, indent=2))
print("All checks passed. Seven analysis samples exported.")''')
md('''## Sources and assistance
Raw series: [SP500](https://fred.stlouisfed.org/series/SP500), [CPIAUCNS](https://fred.stlouisfed.org/series/CPIAUCNS), [CPILFENS](https://fred.stlouisfed.org/series/CPILFENS), [MICH](https://fred.stlouisfed.org/series/MICH), and [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS), distributed by FRED. Missing CPI context: [BLS shutdown FAQ](https://www.bls.gov/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi-faq.htm).

This notebook adapts the group's final Phase 2 cleaning workflow. OpenAI Codex assisted with code, documentation, execution, and automated checks. The report explains the analyses and gives the full bibliography. The authors should review the code and interpretations before submitting.''')
nb=nbf.v4.new_notebook(cells=cells,metadata={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"}})
nbf.write(nb,ROOT/'Phase3_Data_Cleaning.ipynb')
print('Built cleaning notebook')
