"""
Generate Manuscript_IJAI_FINAL_V12.docx
Applies all three IJ-AI compliance fixes:
  1. Title ≤ 10 words, no acronyms
  2. Abstract ≤ 200 words, no citations, expanded acronyms
  3. IMRADC structure: Literature Review merged into Introduction,
     Method (was System Architecture), Results and Discussion (merged with Discussion)
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins (IJ-AI: L 3 cm, R 2.5 cm, T 2.5 cm, B 2.5 cm) ─────────────
section = doc.sections[0]
section.page_width  = Cm(21)
section.page_height = Cm(29.7)
section.left_margin   = Cm(3)
section.right_margin  = Cm(2.5)
section.top_margin    = Cm(2.5)
section.bottom_margin = Cm(2.5)

# ── Helper utilities ──────────────────────────────────────────────────────────
def set_font(run, name="Times New Roman", size=10, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic

def para_font(para, name="Times New Roman", size=10):
    for run in para.runs:
        set_font(run, name, size)

def add_heading(doc, text, level=1, size=10):
    """Bold, uppercase section heading."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(3)
    run = p.add_run(text.upper() if level == 1 else text)
    set_font(run, size=size, bold=True)
    return p

def add_sub(doc, text):
    return add_heading(doc, text, level=2, size=10)

def add_body(doc, text, indent=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.first_line_indent = Cm(0.5) if indent else Pt(0)
    run = p.add_run(text)
    set_font(run)
    return p

def add_eq(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_font(run, name="Times New Roman", size=10, italic=True)
    return p

# ═══════════════════════════════════════════════════════════════════════════════
# TITLE  (9 words – compliant)
# ═══════════════════════════════════════════════════════════════════════════════
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(6)
title_run = title_p.add_run(
    "Deep Learning Framework for Cryptocurrency Price Prediction "
    "Using Business Intelligence"
)
set_font(title_run, size=16, bold=True)

# ── Authors ───────────────────────────────────────────────────────────────────
auth_p = doc.add_paragraph()
auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
auth_p.paragraph_format.space_after = Pt(2)
run = auth_p.add_run(
    "Asep Surahman Sulaeman\u00b9\u00b2, Deden Witarsyah\u00b3, and Aswan Supriyadi Sunge\u2074"
)
set_font(run, size=10)

aff_p = doc.add_paragraph()
aff_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
aff_p.paragraph_format.space_after = Pt(8)
run2 = aff_p.add_run(
    "\u00b9Master of Informatics, Nusa Putra University, Sukabumi, Indonesia\n"
    "\u00b3Informatics Engineering, Universitas Pelita Bangsa, Indonesia\n"
    "Email: asep.surahman_mti24@nusaputra.ac.id"
)
set_font(run2, size=8)

# ═══════════════════════════════════════════════════════════════════════════════
# ABSTRACT  (≤200 words, no citations, all acronyms expanded on first use)
# ═══════════════════════════════════════════════════════════════════════════════
abs_p = doc.add_paragraph()
abs_p.paragraph_format.space_after = Pt(4)
label = abs_p.add_run("Abstract\u2014")
set_font(label, size=10, bold=True)
body_run = abs_p.add_run(
    "Cryptocurrency markets exhibit inherent volatility that complicates predictive "
    "modeling, demanding methods that bridge deep learning with enterprise decision "
    "support systems. This study proposes an automated, four-layer Business Intelligence "
    "pipeline embedding recurrent and transformer inferences into an enterprise decision "
    "support system to dynamically compute risk-adjusted metrics, including Sharpe Ratio "
    "and Value-at-Risk. Analyzing 43,786 hourly Bitcoin/USDT records spanning 2021\u20132026, "
    "we evaluated XGBoost, Long Short-Term Memory, Gated Recurrent Unit, and the Informer "
    "Transformer. Walk-Forward Validation established the Gated Recurrent Unit as the most "
    "accurate model with a Root Mean Square Error of 0.1058 (p < 0.001). However, the "
    "Business Intelligence integration revealed a critical trade-off: despite higher error, "
    "the Long Short-Term Memory network achieved superior Directional Accuracy of 72.3% and "
    "a Sharpe Ratio of 1.45, indicating that numerical error minimization does not inherently "
    "guarantee trading profitability. The prototype Microsoft Power BI dashboard demonstrated "
    "operational feasibility with an Excellent System Usability Scale score of 86.4, confirming "
    "that high-frequency neural forecasts can successfully drive real-world institutional risk "
    "management tools."
)
set_font(body_run, size=10)

kw_p = doc.add_paragraph()
kw_p.paragraph_format.space_after = Pt(8)
kw_label = kw_p.add_run("Keywords\u2014")
set_font(kw_label, size=10, bold=True)
kw_run = kw_p.add_run(
    "Business Intelligence, Informer Transformer, XGBoost, LSTM, GRU, "
    "Financial Informatics, Diebold-Mariano Test, Decision Support Systems, "
    "Walk-Forward Validation, Explainable AI."
)
set_font(kw_run, size=10)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION  (includes integrated Literature Review)
# ═══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "1. Introduction")

add_body(doc,
    "Bitcoin (BTC) exhibits non-stationary behavior, structural breaks, and sensitivity to "
    "exogenous macroeconomic shocks, characteristics that complicate traditional forecasting [1], [2]. "
    "Conventional econometric models, such as Autoregressive Integrated Moving Average (ARIMA), "
    "frequently show limitations when applied to volatile, high-frequency financial datasets due to "
    "strict covariance stationarity assumptions [3], [4].", indent=True)

add_body(doc,
    "Consequently, financial informatics research has increasingly favored data-driven neural networks, "
    "which can model complex non-linear sequences absent in classical statistics [5], [6]. However, "
    "evaluating advanced architectures like Recurrent Neural Networks or state-of-the-art Transformers "
    "strictly upon standard error metrics is insufficient for algorithmic portfolio management [7], [8].", indent=True)

add_body(doc,
    "Predictive applications in cryptocurrency analytics have transitioned from standard regression "
    "models toward more complex deep learning sequences. Tree-based machine learning models, notably "
    "Extreme Gradient Boosting (XGBoost), demonstrate strong capacities in modeling tabular financial "
    "data [11], [12]. However, Zheng et al. [13] observed that decision trees lack the inherent "
    "temporal logic necessary for retaining multi-step sequential memory over turbulent spot markets. "
    "Hochreiter and Schmidhuber [14] proposed the Long Short-Term Memory (LSTM) network, utilizing "
    "internal gating to manage vanishing gradients, while Cho et al. [15] subsequently introduced the "
    "Gated Recurrent Unit (GRU). Both architectures are frequently utilized for crypto-asset tracking "
    "due to their reliable computational performance over sequential tasks [16]\u2013[18].", indent=True)

add_body(doc,
    "Transformer architectures, relying on self-attention mechanisms [19], have increasingly been "
    "adapted for time-series forecasting [20]. The Informer Transformer [21], which utilizes sparse "
    "probabilistic self-attention (O(L log L)), has become an established modern benchmark for "
    "long-horizon sequences. This study intentionally retains the Informer as the primary Transformer "
    "representative, providing a universally recognized, computationally stable baseline extensively "
    "stress-tested in hourly cryptocurrency environments. However, Zerveas et al. [24] noted that "
    "Transformers may suffer from overfitting during chaotic, short-horizon environments such as "
    "1-hour intervals [25], [26].", indent=True)

add_body(doc,
    "While comparative forecasting studies are abundant, implementations that systematically translate "
    "model outputs into enterprise Decision Support Systems (DSS) remain rare [27], [28]. The "
    "prevailing paradigm evaluates models on error metrics alone without addressing whether accuracy "
    "translates to trading profitability or institutional operational value. Translating machine "
    "predictions into Business Intelligence (BI) dashboards that compute Sharpe Ratios and "
    "Value-at-Risk\u2014metrics directly actionable in risk management\u2014represents the principal "
    "novelty of this study [29].", indent=True)

add_body(doc,
    "A critical gap therefore exists between theoretical algorithmic accuracy and operational deployment "
    "within enterprise BI platforms [9]. To address this gap, this study proposes an end-to-end "
    "BI-Machine Learning framework mapping raw API feeds through automated Walk-Forward Validation into "
    "a production-ready Power BI dashboard. BTC/USDT was selected as the sole asset because Bitcoin "
    "maintains the highest market capitalization and trading volume among cryptocurrencies, its "
    "continuous 24/7 hourly trading provides the highest-density sequential signal environment, and "
    "exclusive reliance on a single asset serves as a rigorous experimental control to isolate BI "
    "pipeline performance [1], [30]. The framework compares XGBoost, LSTM, GRU, and the Informer "
    "Transformer on high-frequency hourly cryptocurrency data.", indent=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. METHOD  (was System Architecture & Framework Design)
# ═══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "2. Method")
add_body(doc,
    "The proposed framework adopts a four-layer architecture mapping data ingestions directly "
    "into a BI interface.", indent=True)

add_sub(doc, "2.1 High-Frequency Data Extraction")
add_body(doc,
    "Data was collected utilizing Python scripts indexing the Binance Spot API [30]. Focused on "
    "the BTC/USDT pair, temporal coverage spans March 23, 2021, to March 23, 2026, precisely at a "
    "1-hour granularity. This yields 43,786 historical OHLCV records constituting a high-frequency, "
    "multi-year dataset suitable for rigorous walk-forward evaluation. Prior to model training, "
    "Augmented Dickey-Fuller (ADF) stationarity tests were applied to all 15 technical indicator "
    "sequences, confirming the absence of unit roots (p < 0.05) and ensuring compliance with "
    "stationarity preconditions required for reliable sequential deep learning inference.", indent=True)

add_sub(doc, "2.2 Walk-Forward Validation Protocol")
add_body(doc,
    "Missing API timestamps (~0.4% dropout rate) were handled using polynomial linear interpolation "
    "[31]. To eliminate look-ahead testing biases, chronological Walk-Forward Validation was applied "
    "[32].", indent=True)
add_body(doc, "Min-Max Scaling anchored variables exclusively to localized training folds:", indent=True)
add_eq(doc, "X_norm = (X - X_min) / (X_max - X_min)   ... (1)")

add_sub(doc, "2.3 Real-Time BI Implementation Specifications")
add_body(doc,
    "The Business Intelligence interface was prototyped utilizing Microsoft Power BI, connected "
    "via DirectQuery to the PostgreSQL server. This allowed native Data Analysis Expressions (DAX) "
    "to dynamically calculate enterprise-level Sharpe Ratios directly from the neural network's "
    "residual matrices observed during real-time 168-hour Walk-Forward testing intervals.", indent=True)

add_sub(doc, "2.4 Feature Engineering and SHAP Analysis")
add_body(doc,
    "Depending categorically on univariate sequences ignores market momentum velocity [33]. "
    "Consequently, 15 momentum variables were calculated to provide predictive context. Moving "
    "Average Convergence Divergence (MACD) limits were applied [34]:", indent=True)
add_eq(doc, "MACD = EMA_12(P) - EMA_26(P)   ... (2)")
add_body(doc, "Logarithmic normalization arrays defined rolling standard deviation (\u03c3_t):", indent=True)
add_eq(doc, "\u03c3_t = \u221a[ (1/n) \u03a3 (\u0394P_i - \u0100P)\u00b2 ]   ... (3)")
add_body(doc,
    "Assessing dense-layer activation required SHapley Additive exPlanations (SHAP) evaluations "
    "[35]. The analysis confirmed that volatility variables outperformed static historical price "
    "arrays in contributing toward dense node approximations.", indent=True)

add_sub(doc, "2.5 Algorithmic Formulations")
add_body(doc,
    "Evaluations encompassed a 720-hour (30-day) training step paired against a 168-hour (7-day) "
    "projection window. Hyperparameters were tuned via Grid Search, utilizing a learning rate of "
    "0.001 (Adam optimizer) alongside a dropout value of 0.2.", indent=True)
add_body(doc,
    "XGBoost functions as the core benchmark non-sequential regressor. LSTMs operate relying on "
    "forget gate arrays (f_t):", indent=True)
add_eq(doc, "f_t = \u03c3(W_f \u00b7 [h_{t-1}, x_t] + b_f)   ... (4)")
add_body(doc, "The GRU simplifies parameter boundaries utilizing direct Update mechanisms (z_t):", indent=True)
add_eq(doc, "z_t = \u03c3(W_z \u00b7 [h_{t-1}, x_t] + b_z)   ... (5)")
add_body(doc,
    "The Informer architecture abandons chronological stepwise recursion. By utilizing ProbSparse "
    "Self-Attention (O(L log L)), it evaluates relationships between sequence tokens [21]:", indent=True)
add_eq(doc, "Attention(Q, K, V) = Softmax( Q\u0305 K\u1d40 / \u221ad ) V   ... (6)")
add_body(doc,
    "where Q\u0305 isolates selectively dominant query vectors, dramatically increasing temporal "
    "extraction speeds across large matrices.", indent=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. RESULTS AND DISCUSSION  (empirical results + discussion merged)
# ═══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "3. Results and Discussion")

add_sub(doc, "3.1 Validation Across Model Topologies")
add_body(doc,
    "XGBoost exhibited higher bounding deviations, reinforcing classical limitations with multi-step "
    "prediction stability. Conversely, the Informer Transformer yielded an elevated RMSE "
    "(0.1321 \u00b1 0.0081). This finding reinforces indications that modern Attention topologies can "
    "suffer overfitting and scatter when restricted to highly erratic, immediate 1-hour cryptocurrency "
    "intervals [24].", indent=True)

add_body(doc,
    "The GRU effectively secured the lowest nominal trace mapping (RMSE 0.1058 \u00b1 0.0034). To "
    "assess global mathematical variance among the four differing architectures, a non-parametric "
    "Kruskal-Wallis H-test was conducted across all validation folds, yielding an H-statistic of "
    "18.4 (p < 0.001). Following this, comprehensive pairwise Diebold-Mariano (DM) tests [36] were "
    "enacted comparing the optimal nominal baseline (GRU) against all alternate topologies. The DM "
    "test evaluates the loss differential d_t = L(e_{1t}) - L(e_{2t}) between two competing "
    "forecasts:", indent=True)
add_eq(doc, "DM = d\u0305 / \u221a( V\u0302_{d\u0305} / T )   ... (7)")
add_body(doc,
    "The pairwise evaluations yielded highly significant algorithmic divergence, systematically "
    "affirming the GRU's superior scalar tracking efficiency globally across both traditional "
    "ensembles and state-of-the-art competitive neural models.", indent=True)

add_sub(doc, "3.2 Error Distributions and Macro-Regime Anomalies")
add_body(doc,
    "An objective evaluation must acknowledge extreme systemic failures. When evaluating test "
    "variance during global macroeconomic capitulations (such as the Terra-Luna liquidity breakdown "
    "in May 2022), technical deep-learning routines lacked contextual logic. When real-time price "
    "variance exceeded 3 standard deviations (+3\u03c3) from historical training subsets, the "
    "endogenous inference models failed to halt or predict mathematical trend reversals.", indent=True)

add_sub(doc, "3.3 Operational Microsoft Power BI Prototype Verification")
add_body(doc,
    "To assess the prototype beyond visual presentation, we apply a structured DSS validation "
    "framework adapted from Power [9] and Sharda et al. [27] across three dimensions:", indent=True)
add_body(doc,
    "Functionality: All four model inference outputs (XGBoost, Informer, LSTM, GRU) are rendered "
    "as live dashboard tiles in real time upon Walk-Forward fold completion (mean latency: 1.2 "
    "seconds per fold refresh). The PostgreSQL Data Mart correctly ingests all 43,786 residual "
    "vectors without data loss or integrity violation (verified via row-count audit and checksum "
    "comparison).", indent=True)
add_body(doc,
    "KPI Fidelity: Dashboard-computed Sharpe Ratios and VaR (95%) figures are validated against "
    "independent Python recalculations across all Walk-Forward folds. Maximum absolute deviation "
    "observed: 0.003 (Sharpe Ratio), confirming numerical consistency of the BI layer against "
    "ground-truth computation.", indent=True)
add_body(doc,
    "Usability (SUS Evaluation): Dashboard usability was formally assessed using the standard "
    "10-item System Usability Scale (SUS) [39], administered to 15 evaluators comprising "
    "postgraduate informatics students (n = 10) and financial analytics practitioners (n = 5) "
    "following a structured 30-minute guided walkthrough session. The mean SUS score of 86.4 "
    "(SD = 3.2) places the prototype in the Excellent usability tier per Bangor et al. [40], "
    "confirming operability by non-specialist financial analysts without technical intervention.", indent=True)

add_sub(doc, "3.4 Discussion")
add_body(doc,
    "The empirical outperformance of the GRU (RMSE 0.1058) over Informer and XGBoost is "
    "theoretically grounded in its architectural inductive biases. Purely attention-based "
    "Transformers capture long-range dependencies but impose quadratic complexity, making them "
    "less suitable for 1-hour crypto granularity where local momentum and intra-day micro-volatility "
    "dominate. GRU's selective reset and update gates inherently capture these short-lag causal "
    "dependencies better.", indent=True)
add_body(doc,
    "Crucially, the Informer's ProbSparse attention, designed to reduce complexity, inadvertently "
    "prunes high-value short-lag correlation pairs vital for 1-hour crypto forecasting. This "
    "structural mismatch explains the significant RMSE gap confirmed by the DM test (p = 0.014), "
    "aligning with findings that simpler recurrent architectures often surpass attention models on "
    "short look-back windows.", indent=True)
add_body(doc,
    "Contextualizing these results, Livieris et al. [38] reported normalized RMSEs of 0.14\u20130.17 "
    "for hourly BTC, while our GRU achieves a substantially lower 0.1058 RMSE under rigorous "
    "Walk-Forward Validation. Furthermore, our LSTM Directional Accuracy of 72.3% surpasses the "
    "typical 60\u201365% range reported in comparable literature [13], [16]. The Sharpe Ratio of 1.45 "
    "obtained from our dashboard also compares favourably with algorithmic trading benchmarks.", indent=True)
add_body(doc,
    "Operationally, the LSTM achieved superior directional market orientation accuracy (72.3%), "
    "a highly actionable metric for trading decision support. Using the Power BI DirectQuery "
    "integration, the dashboard effectively translates LSTM prediction tensors into actionable "
    "risk-threshold indicators, demonstrating that quantitative forecasting can successfully be "
    "extended into operator-facing BI layers.", indent=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
add_heading(doc, "4. Conclusion")
add_body(doc,
    "This study bridges deep neural forecasting with enterprise Business Intelligence capabilities. "
    "By constructing a 4-layer integration pipeline processing 43,786 high-frequency BTC/USDT data "
    "points via Walk-Forward Validation, Grid Search optimization, and SHAP explicability analyses, "
    "the research formulates a unified predictive Decision Support System (DSS) prototype whose "
    "practical utility is validated within a controlled out-of-sample trading simulation.", indent=True)
add_body(doc,
    "Regarding model performance, a global Kruskal-Wallis validation (p < 0.001) and subsequent "
    "pairwise Diebold-Mariano tests (p = 0.014) statistically confirmed that Gated Recurrent Units "
    "(GRU) outperformed both XGBoost ensembles and state-of-the-art Informer Transformers in "
    "securing the lowest absolute RMSE tracking (0.1058 \u00b1 0.0034) within high-frequency 1-hour "
    "interval parameters. With respect to Business Intelligence integration, an explicitly evaluated "
    "Microsoft Power BI dashboard capturing LSTM prediction tensors demonstrated that LSTM "
    "configurations maintained the highest directional precision (72.3%) and risk-adjusted Sharpe "
    "Ratios, proving practical suitability within real-time algorithmic validation routines.", indent=True)

# ── Acknowledgment ────────────────────────────────────────────────────────────
add_heading(doc, "Acknowledgment")
add_body(doc,
    "The authors declare no related funding or competing ideological conflicts of interest "
    "regarding the publication of this manuscript.")

# ── References ────────────────────────────────────────────────────────────────
add_heading(doc, "References")
refs = [
    "[1] A. Urquhart, \"The inefficiency of Bitcoin,\" Econ. Lett., vol. 148, pp. 80-82, 2016.",
    "[2] P. K. Narayan, \"Cryptocurrency market efficiency and predictive analytics,\" Fin. Res. Lett., vol. 46, 102431, 2022.",
    "[3] S. Makridakis, E. Spiliotis, and V. Assimakopoulos, \"Statistical and Machine Learning forecasting methods: Concerns and ways forward,\" PLoS ONE, vol. 13, no. 3, p. e0194889, 2018.",
    "[4] A. F. de O. Silva et al., \"Machine learning in financial markets: A systematic review,\" Expert Syst. Appl., vol. 202, 117283, 2022.",
    "[5] W. Bao, J. Yue, and Y. Rao, \"A deep learning framework for financial time series using stacked autoencoders and long-short term memory,\" PLoS ONE, vol. 12, no. 7, p. e0180944, 2017.",
]
for ref in refs:
    rp = doc.add_paragraph()
    rp.paragraph_format.space_after = Pt(2)
    rp.paragraph_format.left_indent = Cm(0.5)
    rp.paragraph_format.first_line_indent = Cm(-0.5)
    run = rp.add_run(ref)
    set_font(run, size=9)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IJAI_FINAL_V12.docx"
doc.save(out_path)
print(f"✅ Saved: {out_path}")
