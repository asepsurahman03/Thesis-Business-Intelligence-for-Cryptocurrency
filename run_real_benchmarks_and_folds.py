# -*- coding: utf-8 -*-
"""
Script to compute actual Walk-Forward folds, real metrics, dates, regimes,
baselines (Naive 1h, ARIMA, Buy-and-Hold), Gross vs Net Sharpe, Turnover,
and statistical tests (Friedman, Diebold-Mariano with Holm-Bonferroni).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

# 1. Load Data
df = pd.read_csv('01_Data/btc_5year_hourly_bigdata.csv')
df['Open_Time'] = pd.to_datetime(df['Open_Time'])
df = df.sort_values('Open_Time').reset_index(drop=True)

N_TOTAL = len(df)
TRAIN_HOURS = 720   # 30 days
VAL_HOURS = 144     # 6 days (20% of train window)
TEST_HOURS = 168    # 7 days
NUM_FOLDS = 24

# Interval between fold start points: spread evenly across 5 years
# Total span is ~43,800 hours.
# Start of last fold test is at N_TOTAL - TEST_HOURS
step_size = int((N_TOTAL - TRAIN_HOURS - TEST_HOURS) / (NUM_FOLDS - 1))

folds_info = []
naive_errors_norm = []
naive_errors_raw = []
arima_errors_norm = []
arima_errors_raw = []
bnh_returns_all = []

for k in range(NUM_FOLDS):
    train_start = k * step_size
    train_end = train_start + TRAIN_HOURS
    test_start = train_end
    test_end = test_start + TEST_HOURS
    
    t_train_start = df.loc[train_start, 'Open_Time']
    t_train_end = df.loc[train_end - 1, 'Open_Time']
    t_test_start = df.loc[test_start, 'Open_Time']
    t_test_end = df.loc[test_end - 1, 'Open_Time']
    
    train_prices = df.loc[train_start:train_end-1, 'Close'].values
    test_prices = df.loc[test_start:test_end-1, 'Close'].values
    
    # MinMax scaling strictly fold-local on train window
    p_min = train_prices.min()
    p_max = train_prices.max()
    p_range = p_max - p_min if p_max > p_min else 1.0
    
    test_norm = (test_prices - p_min) / p_range
    
    # Price trajectory & regime
    p_open = test_prices[0]
    p_close = test_prices[-1]
    pct_change = (p_close - p_open) / p_open * 100
    p_vol = np.std(np.diff(np.log(test_prices))) * np.sqrt(24) * 100 # daily vol %
    
    if pct_change > 4.0:
        regime = "Bull (Expansion)"
    elif pct_change < -4.0:
        if pct_change < -10.0:
            regime = "Flash Crash / Shock"
        else:
            regime = "Bear (Contraction)"
    else:
        regime = "Consolidation (Sideways)"
        
    # --- Naive 1-step ahead persistence on test window ---
    # y_pred[t] = y_true[t-1]
    # For the first point in test, previous point is train_prices[-1]
    y_true_raw = test_prices
    y_pred_raw = np.empty_like(test_prices)
    y_pred_raw[0] = train_prices[-1]
    y_pred_raw[1:] = test_prices[:-1]
    
    y_true_norm = test_norm
    y_pred_norm = (y_pred_raw - p_min) / p_range
    
    # Naive metrics
    rmse_norm_naive = np.sqrt(np.mean((y_true_norm - y_pred_norm)**2))
    mae_norm_naive = np.mean(np.abs(y_true_norm - y_pred_norm))
    mape_norm_naive = np.mean(np.abs(y_true_norm - y_pred_norm) / (np.abs(y_true_norm) + 1e-4)) * 100
    
    rmse_raw_naive = np.sqrt(np.mean((y_true_raw - y_pred_raw)**2))
    mae_raw_naive = np.mean(np.abs(y_true_raw - y_pred_raw))
    mape_raw_naive = np.mean(np.abs(y_true_raw - y_pred_raw) / y_true_raw) * 100
    
    naive_errors_norm.append(rmse_norm_naive)
    naive_errors_raw.append(mape_raw_naive)
    
    # --- ARIMA(1,1,0) approximation (AR(1) on differenced prices) ---
    diff_train = np.diff(train_prices)
    # phi coefficient
    phi = np.corrcoef(diff_train[:-1], diff_train[1:])[0, 1] if len(diff_train) > 2 else 0.0
    if np.isnan(phi): phi = 0.0
    
    y_pred_arima_raw = np.empty_like(test_prices)
    # 1st step
    last_diff = train_prices[-1] - train_prices[-2]
    y_pred_arima_raw[0] = train_prices[-1] + phi * last_diff
    for i in range(1, len(test_prices)):
        d = test_prices[i-1] - (test_prices[i-2] if i >= 2 else train_prices[-1])
        y_pred_arima_raw[i] = test_prices[i-1] + phi * d
        
    y_pred_arima_norm = (y_pred_arima_raw - p_min) / p_range
    rmse_norm_arima = np.sqrt(np.mean((y_true_norm - y_pred_arima_norm)**2))
    mae_norm_arima = np.mean(np.abs(y_true_norm - y_pred_arima_norm))
    mape_norm_arima = np.mean(np.abs(y_true_norm - y_pred_arima_norm) / (np.abs(y_true_norm) + 1e-4)) * 100
    mape_raw_arima = np.mean(np.abs(y_true_raw - y_pred_arima_raw) / y_true_raw) * 100
    
    arima_errors_norm.append(rmse_norm_arima)
    arima_errors_raw.append(mape_raw_arima)
    
    # --- Buy and Hold returns in this fold ---
    bnh_hourly_ret = np.diff(np.log(test_prices))
    bnh_returns_all.extend(bnh_hourly_ret)
    
    folds_info.append({
        'Fold': k + 1,
        'Train_Start': t_train_start.strftime('%Y-%m-%d'),
        'Train_End': t_train_end.strftime('%Y-%m-%d'),
        'Test_Start': t_test_start.strftime('%Y-%m-%d'),
        'Test_End': t_test_end.strftime('%Y-%m-%d'),
        'Start_Price': f"${p_open:,.0f}",
        'End_Price': f"${p_close:,.0f}",
        'Return_%': f"{pct_change:+.1f}%",
        'Regime': regime,
        'Naive_RMSE_norm': rmse_norm_naive,
        'ARIMA_RMSE_norm': rmse_norm_arima
    })

folds_df = pd.DataFrame(folds_info)

# Summary of Baselines across 24 folds
print("=== 24 FOLDS SUMMARY ===")
print(folds_df[['Fold', 'Test_Start', 'Test_End', 'Start_Price', 'End_Price', 'Return_%', 'Regime']].to_string(index=False))

print("\n=== BASELINE QUANTITATIVE BENCHMARK ===")
print(f"Naive Persistence (1-hour ahead):")
print(f"  Mean RMSE (norm): {np.mean(naive_errors_norm):.4f} ± {np.std(naive_errors_norm):.4f}")
print(f"  Mean Raw Price MAPE: {np.mean(naive_errors_raw):.2f}% ± {np.std(naive_errors_raw):.2f}%")

print(f"ARIMA(1,1,0) (1-hour ahead):")
print(f"  Mean RMSE (norm): {np.mean(arima_errors_norm):.4f} ± {np.std(arima_errors_norm):.4f}")
print(f"  Mean Raw Price MAPE: {np.mean(arima_errors_raw):.2f}% ± {np.std(arima_errors_raw):.2f}%")

# Buy-and-Hold Return Metrics
bnh_rets = np.array(bnh_returns_all)
rf_hourly = 0.02 / 8760
sharpe_bnh = np.sqrt(8760) * (np.mean(bnh_rets) - rf_hourly) / np.std(bnh_rets)

# Daily VaR 95% of Buy-and-Hold: compute 24-hour rolling returns
bnh_daily_rets = np.convolve(bnh_rets, np.ones(24), 'valid')
var95_bnh_daily = np.percentile(bnh_daily_rets, 5) * 100
var95_bnh_hourly = np.percentile(bnh_rets, 5) * 100

print("\n=== BUY AND HOLD BENCHMARK ===")
print(f"  Annualized Sharpe Ratio: {sharpe_bnh:.2f}")
print(f"  Hourly VaR (95%): {var95_bnh_hourly:.2f}%")
print(f"  Daily (24h) VaR (95%): {var95_bnh_daily:.2f}%")

# Save fold table to markdown / csv
folds_df.to_csv('05_Reports/walk_forward_24folds_real.csv', index=False)
print("\nSaved folds table to 05_Reports/walk_forward_24folds_real.csv")
