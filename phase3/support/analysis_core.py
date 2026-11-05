import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import norm

def fit_line(frame, predictors):
    model = LinearRegression().fit(frame[predictors], frame.sp500_return_pct)
    return model

def calendar_hac(frame, predictors, max_lag=3):
    """OLS covariance with Bartlett weights at actual calendar-month lags."""
    X = np.column_stack([np.ones(len(frame)), frame[predictors].to_numpy()])
    y = frame.sp500_return_pct.to_numpy()
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    residual = y - X @ beta
    scores = X * residual[:, None]
    months = frame.month_index.to_numpy(dtype=int)
    # Zero score contributions preserve gaps; no missing data values are filled.
    grid = np.zeros((months.max() - months.min() + 1, X.shape[1]))
    grid[months - months.min()] = scores
    meat = grid.T @ grid
    for lag in range(1, max_lag + 1):
        weight = 1 - lag / (max_lag + 1)
        cross = grid[lag:].T @ grid[:-lag]
        meat += weight * (cross + cross.T)
    bread = np.linalg.inv(X.T @ X)
    n, k = X.shape
    covariance = n / (n - k) * bread @ meat @ bread
    se = np.sqrt(np.diag(covariance))
    return beta, se, covariance

def residual_pairs(frame, residual, lag):
    series = pd.Series(np.asarray(residual), index=frame.month_index)
    earlier = series.copy()
    earlier.index = earlier.index + lag
    pairs = pd.concat([series, earlier], axis=1).dropna()
    return pairs.iloc[:, 0].corr(pairs.iloc[:, 1]), len(pairs)
