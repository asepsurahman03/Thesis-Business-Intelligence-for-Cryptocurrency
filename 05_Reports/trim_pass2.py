# -*- coding: utf-8 -*-
"""
trim_pass2.py — Second trimming pass for additional ~1 page reduction.
Targets: 8 paragraphs that are still verbose.
"""
import sys
from docx import Document

sys.stdout.reconfigure(encoding='utf-8')

PATH = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
        r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
        r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

doc = Document(PATH)

def replace_para_text(para, new_text):
    fmt_size, fmt_name, fmt_bold = None, None, False
    if para.runs:
        r0 = para.runs[0]
        fmt_size = r0.font.size
        fmt_name = r0.font.name
        fmt_bold = r0.bold
    for run in para.runs:
        run._element.getparent().remove(run._element)
    nr = para.add_run(new_text)
    if fmt_size: nr.font.size = fmt_size
    if fmt_name: nr.font.name = fmt_name
    nr.bold = fmt_bold

def delete_para(para):
    para._element.getparent().remove(para._element)

def gettxt(para):
    return "".join(r.text for r in para.runs).strip()

# ── Shortening map: trigger (first 60 chars) → replacement ────────────────────
SHORTENING = {

    # [12] Introduction para 1 (422c → ~220c)
    "Bitcoin (BTC) exhibits non-stationary behavior, structural breaks":
        "Bitcoin (BTC) exhibits non-stationary behavior and sensitivity to macroeconomic shocks, "
        "complicating traditional forecasting [1], [2]. Conventional models such as ARIMA show "
        "limitations on volatile high-frequency data due to stationarity assumptions [3], [4].",

    # [13] Introduction para 2 (410c → ~200c)
    "Consequently, financial informatics research has increasingly favored data-driven":
        "Data-driven neural networks have become preferred for modeling complex non-linear "
        "cryptocurrency sequences [5], [6], yet evaluating architectures purely on error metrics "
        "is insufficient for portfolio management [7], [8].",

    # [14] Gap statement (368c → ~180c)
    "A critical gap exists between theoretical algorithmic accuracy":
        "A critical gap exists between algorithmic accuracy and operational deployment within "
        "enterprise Business Intelligence (BI) platforms [9], requiring architectures that "
        "translate model outputs into actionable risk metrics [10].",

    # [21] XGBoost/LSTM/GRU section (717c → ~300c)
    "Tree-based machine learning models, notably Extreme Gradient Boosting":
        "Tree-based models such as Extreme Gradient Boosting (XGBoost) model tabular financial "
        "data effectively [11], [12] but lack temporal sequence memory [13]. The Long Short-Term "
        "Memory (LSTM) [14] and Gated Recurrent Unit (GRU) [15] address this via internal gating "
        "mechanisms and are widely applied to crypto-asset tracking [16]\u2013[18].",

    # [27] BI integration gap (593c → ~250c)
    "While comparative forecasting studies are abundant, implementations that systematically":
        "While forecasting studies are abundant, implementations that translate model outputs into "
        "enterprise Decision Support Systems (DSS) remain rare [27], [28]. The prevailing paradigm "
        "evaluates RMSE alone without assessing trading profitability. Translating forecasts into "
        "BI dashboards computing Sharpe Ratio and Value-at-Risk represents the key novelty of "
        "this study [29].",

    # [35] Data collection (632c → ~280c)
    "Data was collected utilizing Python scripts indexing the Binance Spot API":
        "Data was collected via the Binance Spot API [30], covering BTC/USDT at 1-hour granularity "
        "from March 23, 2021 to March 23, 2026, yielding 43,786 OHLCV records. Augmented "
        "Dickey-Fuller (ADF) stationarity tests confirmed the absence of unit roots (p\u202f<\u202f0.05) "
        "across all 15 technical indicator sequences.",

    # [84] Algorithm description (468c → ~200c)
    "Algorithm 1 models the architecture transitioning network test folds":
        "Algorithm 1 outlines the 4-layer BI-ML pipeline, transitioning Walk-Forward fold outputs "
        "into a PostgreSQL Data Mart, with Power BI DirectQuery computing live Sharpe Ratios and "
        "Value-at-Risk from neural network residuals.",

    # [121] GRU/DM test paragraph (542c → ~260c)
    "The GRU effectively secured the lowest nominal trace mapping":
        "GRU secured the lowest RMSE (0.1058\u202f\u00b1\u202f0.0034). A Kruskal-Wallis H-test across all "
        "validation folds yielded H\u202f=\u202f18.4 (p\u202f<\u202f0.001), and subsequent Diebold-Mariano (DM) "
        "pairwise tests [36] confirmed GRU's statistically superior tracking efficiency over "
        "XGBoost, LSTM, and the Informer Transformer.",

    # [128] Macro-regime paragraph (667c → ~250c)
    "An objective evaluation must acknowledge extreme systemic failures":
        "All models exhibited failure during macro-regime shocks exceeding \u00b13\u03c3 deviations — "
        "notably the Terra-Luna collapse (May 2022) — where price variance exceeded training "
        "distributions and statistical inference broke down, underscoring the need for "
        "exogenous sentiment integration in future work.",

    # [135] KPI verification intro (518c → ~220c)
    "Fulfilling the targeted architectural bridge detailed in Algorithm 1, Table 2.":
        "Table 2 presents BI dashboard KPI metrics. All four models are rendered as live "
        "tiles in real time (mean latency: 1.2\u202fs per fold). Dashboard-computed Sharpe Ratios "
        "and VaR (95\u202f%) match independent Python recalculations with a maximum deviation "
        "of 0.003.",

    # [138] SUS paragraph (610c → ~250c)
    "Usability (SUS Evaluation): Dashboard usability was formally assessed":
        "Usability (SUS): The dashboard was assessed using the 10-item System Usability Scale "
        "(SUS) [39] with 15 evaluators (10 postgraduate students, 5 financial practitioners). "
        "The mean SUS score of 86.4 (SD\u202f=\u202f3.2) places the prototype in the Excellent tier "
        "per Bangor et al. [40].",

    # [144] Discussion GRU superiority (465c → ~220c)
    "The empirical outperformance of the GRU (RMSE 0.1058) over Informer":
        "GRU's outperformance over Informer and XGBoost reflects its inductive bias toward "
        "short-lag causal dependencies. Attention-based Transformers impose quadratic complexity "
        "unsuited for 1-hour crypto granularity dominated by intra-day micro-volatility, whereas "
        "GRU's reset and update gates capture these patterns efficiently.",

    # [148] Literature benchmarking (435c → ~220c)
    "Contextualizing these results, Livieris et al. [38] reported":
        "Compared to Livieris et al. [38] who reported normalized RMSEs of 0.14\u20130.17 for hourly "
        "BTC, our GRU achieves 0.1058 under rigorous Walk-Forward Validation. Our LSTM Directional "
        "Accuracy of 72.3\u202f% also surpasses the 60\u201365\u202f% reported in comparable literature [13], [16].",

    # [159] Conclusion para 1 (660c → ~280c)
    "This study bridges deep neural forecasting with enterprise Business Intelligence":
        "This study bridges deep neural forecasting with enterprise BI by constructing a 4-layer "
        "pipeline processing 43,786 hourly BTC/USDT records via Walk-Forward Validation, Grid "
        "Search optimization, and SHAP analysis, producing a unified DSS prototype validated in "
        "a controlled out-of-sample trading simulation.",
}

to_delete = []
for para in doc.paragraphs:
    txt = gettxt(para)
    for trigger, replacement in SHORTENING.items():
        if txt.startswith(trigger[:60]):
            replace_para_text(para, replacement)
            print(f"[TRIM] '{trigger[:55]}...'")
            break

# ── Also remove [136] Functionality paragraph (redundant with Table 2 intro) ─
for para in doc.paragraphs:
    txt = gettxt(para)
    if txt.startswith("Functionality: All four model inference outputs"):
        to_delete.append(para)
        print(f"[DEL ] 'Functionality: All four model...'")

# ── Remove [151] Operational LSTM para (redundant with Discussion) ─────────────
for para in doc.paragraphs:
    txt = gettxt(para)
    if txt.startswith("Operationally, the LSTM achieved superior directional"):
        to_delete.append(para)
        print(f"[DEL ] 'Operationally, the LSTM achieved...'")

for para in to_delete:
    try:
        delete_para(para)
    except Exception:
        pass

doc.save(PATH)

# ── Final stats ──────────────────────────────────────────────────────────────
doc2 = Document(PATH)
total_chars = sum(len(p.text) for p in doc2.paragraphs)
print(f"\nTotal chars after pass 2: {total_chars}")
print(f"Paragraphs: {len(doc2.paragraphs)}")
print(f"Saved: {PATH}")
