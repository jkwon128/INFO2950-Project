# Phase 3 analysis additions

This method record is dated November 4, 2026 and was reviewed November 5, 2026 (Eastern time). The draft already contained fitted results at review. The record's timing relative to the first fit could not be verified, so these additions are exploratory or supplemental to the Phase 2 preregistration.

## Final Phase 2 plan

The final Phase 2 submission specifies the same-month headline inflation model (116 months) and the previous-calendar-month headline inflation model (114 months). It supersedes an earlier plan that used core inflation for the second model. Core inflation and consumer expectations remain descriptive comparisons. Phase 2 exploratory analysis already revealed the same-month correlation, which determines the slope direction and R² for that model.

## Significance and diagnostics

For each main model, test H₀: slope ≥ 0 against Hₐ: slope < 0 at the zero boundary. The primary inference uses calendar-aware Newey–West HAC covariance with Bartlett weights, three monthly lags, the n/(n−k) correction, and approximate normal-reference p-values and two-sided 95% confidence intervals. Months without observations contribute zero to the score sequence. The underlying CPI and returns remain missing. Compare six and twelve monthly lags and ordinary OLS uncertainty. Apply Holm correction across the two one-sided tests at a family-wise 5% level. Inference remains approximate in this short, potentially nonstationary series.

The report plots residuals against fitted values and calendar time and gives residual correlations and pair counts at lags of 1, 3, 6, and 12 months. These diagnostics describe the observed residuals and leave independence unestablished.

## Exploratory comparisons

1. Refit both models without March and April 2020, the crash and rebound identified in Phase 2. Compare the slopes and R² with the full-sample fits.
2. Refit the same-month model on the lagged model's 114 months to compare the two timings on a common sample.
3. Add the same-month monthly-average effective federal funds rate (FEDFUNDS) to the same-month model on the original 116 months. The extension uses the rate level and reports descriptive coefficients and R². It does not identify a causal effect or evaluate forecasting performance.

Phase 3 uses the original snapshots and study window, with the archived FEDFUNDS series added for the third comparison.
