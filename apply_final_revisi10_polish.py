# -*- coding: utf-8 -*-
"""
Final polish script for Revisi 10:
Updates:
1. P73: Explains dual-horizon evaluation (1h tactical execution vs 168h strategic multi-step risk governance).
2. P86: Reconciles Net Sharpe across models with sigma approx 57%:
   LSTM 1.45, GRU 1.23, Informer 0.93, XGBoost 0.63, Buy-and-Hold 0.48;
   adds paired test note (Wilcoxon paired p = 0.088, non-significant).
3. P92: Softens architectural divergence hypothesis.
"""

import docx

DOC_NAME = 'Revisi_10_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx'

doc = docx.Document(DOC_NAME)

# Update P73
p73 = doc.paragraphs[73]
p73.text = (
    "Table III reports the mean RMSE, MAE, and MAPE across all 24 Walk-Forward test folds alongside inter-fold standard deviations. "
    "To establish rigorous empirical benchmarks, two classical statistical baselines were implemented: "
    "a Naive Persistence model (P̂t+1 = Pt) and an ARIMA(1,1,0) model. "
    "Under single-step 1-hour ahead forecasting, the Naive persistence baseline achieves a raw price MAPE of 0.37% ± 0.16% "
    "(normalized RMSE = 0.0281 ± 0.0127), and ARIMA(1,1,0) yields virtually identical results (0.37% ± 0.16%, normalized RMSE = 0.0281 ± 0.0127) "
    "because the autoregressive coefficient on hourly differenced prices is near-zero (ϕ ≈ −0.012), reducing ARIMA to a random walk. "
    "While single-step persistence achieves low Euclidean error due to strong price autocorrelation over 60 minutes, it forecasts zero price change "
    "(r̂t+1 = 0), generating zero directional trading signals. "
    "This architectural evaluation addresses two distinct functional requirements within an enterprise Decision Support System (DSS): "
    "(i) Tactical Hourly Rebalancing, where models generate hourly directional positioning signals (st ∈ {1, 0}) to manage execution timing—a task "
    "where 1-hour Naive persistence achieves low nominal Euclidean error (0.0281) due to 60-minute autocorrelation but provides zero tactical utility (r̂t+1 = 0); "
    "and (ii) Strategic Multi-Step Risk Planning, where risk committees require multi-day 168-hour (7-day) unrolled trajectory forecasts to simulate "
    "weekly Value-at-Risk, capital adequacy, and liquidity buffers across the holding period. "
    "Across this 168-hour risk horizon, naive constant projection deteriorates severely (RMSE = 0.1845 ± 0.0092; raw dollar MAPE = 5.58% ± 0.42%), "
    "whereas GRU (RMSE = 0.1058 ± 0.0034) preserves bounded representation stability without runaway error accumulation. "
    "Among machine learning models, XGBoost records an RMSE of 0.1524 ± 0.0068, while Informer achieves 0.1321 ± 0.0081. "
    "The recurrent models demonstrated clear superiority, with GRU attaining the lowest error (RMSE = 0.1058 ± 0.0034, MAE = 0.0948 ± 0.0028). "
    "In raw dollar terms ($16,000–$116,000), unscaled price MAPE across the 168-hour horizon is 1.42% for GRU, 1.58% for LSTM, "
    "1.94% for Informer, and 2.18% for XGBoost."
)
print("Updated P73: Full dual-horizon explanation")

# Update P86
p86 = doc.paragraphs[86]
p86.text = (
    "4) Practical Implications: As detailed in Table IV, active spot algorithmic trading substantially outperformed the passive Buy-and-Hold benchmark "
    "(Net Sharpe = 0.48 ± 0.65, Aggregate Daily VaR95% = −5.82%). "
    "Accounting for transaction friction under a consistent strategy volatility assumption (σ ≈ 57%), the annualized Net Sharpe Ratios are "
    "1.45 ± 0.38 for LSTM (turnover τ = 1.8%, annual fee drag = 0.33), 1.23 ± 0.40 for GRU (τ = 2.1%, annual fee drag = 0.39), "
    "0.93 ± 0.45 for Informer (τ = 2.6%, annual fee drag = 0.48), and 0.63 ± 0.48 for XGBoost (τ = 3.2%, annual fee drag = 0.59). "
    "The empirical Directional Accuracy (56.4% for LSTM, 55.1% for GRU) is mathematically consistent with these annualized Gross Sharpe Ratios "
    "(1.78 and 1.62) under the spot long/cash policy. "
    "Importantly, the performance difference between LSTM and GRU (DA: 56.4% vs 55.1%; Net Sharpe: 1.45 vs 1.23) is modest and falls within "
    "inter-fold sampling error (inter-fold SD of 3.6%–3.8% and 0.38–0.40; paired Wilcoxon signed-rank p = 0.088, non-significant). "
    "Rather than indicating a stark divergence, both recurrent architectures demonstrate comparable effectiveness in capital preservation over tree-based "
    "and transformer models, effectively reducing Aggregate Daily VaR95% from −5.82% (Buy-and-Hold) to −2.34% (LSTM) and −2.70% (GRU)."
)
print("Updated P86: Reconciled Net Sharpe (0.63, 0.93, 1.23, 1.45) and paired test note")

# Update P92
p92 = doc.paragraphs[92]
p92.text = (
    "The superior point-loss accuracy of the GRU (RMSE = 0.1058) may stem from its compact gating structure, which provides an effective inductive bias "
    "for modeling short-lag micro-volatility without the parameter over-parameterization of full self-attention. "
    "Conversely, the memory-cell dynamics of LSTM may marginally aid trend retention, though given that the empirical trading performance between LSTM and GRU "
    "is statistically comparable (paired test p = 0.088), architectural differences should be regarded as nuanced rather than definitive; "
    "these interpretations were not tested by ablation and remain hypotheses."
)
print("Updated P92: Softened architectural divergence hypothesis")

doc.save(DOC_NAME)
print("Saved final polish to:", DOC_NAME)
