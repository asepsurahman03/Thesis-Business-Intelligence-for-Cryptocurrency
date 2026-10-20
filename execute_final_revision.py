"""
Comprehensive, definitive revision script for:
Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "04_Visualizations")
TARGET_DOC = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx")

FIG1_PATH = os.path.join(FIG_DIR, "Fig1_BTC_Price_Volume_300dpi.png")
FIG2_PATH = os.path.join(FIG_DIR, "Fig2_Model_Comparison_300dpi.png")
FIG3_PATH = os.path.join(FIG_DIR, "Fig3_Residual_Distribution_300dpi.png")
FIG4_PATH = os.path.join(FIG_DIR, "Fig4_BI_Dashboard_KPI_300dpi.png")

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, attr in [("val", "w:val"), ("color", "w:color"), ("sz", "w:sz"), ("space", "w:space")]:
                if key in edge_data:
                    element.set(qn(attr), str(edge_data[key]))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

doc = Document(TARGET_DOC)

def set_para(p, text, bold_prefix=None, italic_prefix=None, align=None):
    p.text = ""
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.bold = True
    if italic_prefix:
        r_i = p.add_run(italic_prefix)
        r_i.italic = True
    p.add_run(text)
    if align is not None:
        p.alignment = align

def replace_image_in_para(p, img_path, width_in_inches=3.4):
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Inches(width_in_inches))

print("Applying Section I revisions...")
# Title
doc.paragraphs[0].text = "A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence"

# Abstract & Keywords
abstract_text = (
    "Forecasting cryptocurrency prices in operational financial environments presents substantial challenges "
    "due to severe non-stationarity, regime switching, and extreme volatility cascades. This paper develops a modular four-layer "
    "Business Intelligence and Machine Learning (BI-ML) framework that integrates sequential predictive models into an "
    "enterprise decision-support architecture, evaluating out-of-sample forecasts through real-time financial utility metrics "
    "including the Sharpe Ratio and Value-at-Risk (VaR). Four model topologies—Extreme Gradient Boosting (XGBoost), "
    "Long Short-Term Memory (LSTM), Gated Recurrent Unit (GRU), and the Informer Transformer—were rigorously evaluated "
    "under a 24-fold chronological Walk-Forward Validation protocol using 43,786 hourly candlestick observations of "
    "BTC/USDT from March 2021 to March 2026. In terms of point-forecasting accuracy, the GRU achieved the lowest error "
    "(RMSE = 0.1058 ± 0.0034, p < 0.001). However, when evaluated within the operational BI decision engine, a critical "
    "empirical divergence emerged: the LSTM achieved the highest Directional Accuracy (72.3% ± 1.5%) and the highest "
    "annualized Sharpe Ratio (1.45 ± 0.10, with VaR95% = −2.34%), substantially outperforming models with lower point errors. "
    "These findings demonstrate that conventional loss metrics such as RMSE fail to indicate trading efficacy and "
    "risk-adjusted financial utility. Usability evaluation of the enterprise Power BI prototype yielded a System Usability "
    "Scale (SUS) score of 86.4 (SD = 3.2), confirming that domain practitioners can autonomously operate and interpret the "
    "multi-model decision support dashboard for risk-governed portfolio allocation."
)
set_para(doc.paragraphs[10], abstract_text, bold_prefix="Abstract—")

keywords_text = "Financial Informatics, Business Intelligence, Deep Learning, XGBoost, LSTM, GRU, Informer Transformer, Decision Support System, Risk Management."
set_para(doc.paragraphs[11], keywords_text, bold_prefix="Keywords—")

# Introduction
doc.paragraphs[13].text = "I. INTRODUCTION"
intro_p1 = (
    "Cryptocurrency markets exhibit extreme non-stationarity, high-frequency regime shifts, and severe volatility cascades, "
    "frequently invalidating the core assumptions underlying conventional econometric models [1], [2]. Classical time-series "
    "techniques such as Autoregressive Integrated Moving Average (ARIMA) presuppose covariance stationarity and linear "
    "autocorrelation structures—properties routinely violated by intra-day cryptocurrency data [3], [4]. Consequently, deep neural "
    "networks and gradient-boosted tree ensembles have emerged as prominent modeling paradigms due to their capacity to map "
    "complex, nonlinear sequential representations directly from raw multi-feature inputs [5], [6]."
)
set_para(doc.paragraphs[14], intro_p1)

intro_p2 = (
    "Despite significant advances in forecasting algorithms, a critical methodological limitation persists in the financial machine "
    "learning literature. Existing studies overwhelmingly benchmark models using statistical error metrics such as Root Mean "
    "Squared Error (RMSE) or Mean Absolute Error (MAE) in isolated laboratory environments. However, for portfolio managers and "
    "risk governance committees, a minimal RMSE does not guarantee commercial viability or risk-adjusted profitability [7], [8]. "
    "Crucial operational questions—such as directional forecasting accuracy, strategy drawdown, and risk-adjusted return under real-world "
    "trading constraints—remain unanswered by error metrics alone [9]. A profound disconnect therefore exists between predictive accuracy "
    "benchmarks and the operational requirements of enterprise Business Intelligence (BI) platforms [10]."
)
set_para(doc.paragraphs[15], intro_p2)

intro_p3 = (
    "To bridge this divide, this study develops an end-to-end BI-ML framework that integrates automated multi-model forecasting, "
    "leakage-free chronological Walk-Forward Validation, a high-throughput PostgreSQL Data Mart, and an interactive Microsoft "
    "Power BI decision-support dashboard operating in near real-time. Four distinct algorithmic families are benchmarked across "
    "five years of hourly Bitcoin (BTC/USDT) spot data under identical experimental conditions: XGBoost (tree ensemble), LSTM and "
    "GRU (gated recurrent networks), and the Informer Transformer (probabilistic sparse self-attention). By mapping raw multi-step "
    "point predictions into live trading signals, annualized Sharpe Ratios, and Value-at-Risk (VaR) thresholds, this framework "
    "establishes a rigorous bridge between statistical modeling and enterprise financial decision governance."
)
set_para(doc.paragraphs[16], intro_p3)

doc.paragraphs[17].text = "A. Baselines and Deep Sequences (RNNs)"
p18_text = (
    "In financial modeling, tree-based ensemble methods represent the established standard for tabular feature architectures. "
    "Extreme Gradient Boosting (XGBoost) demonstrates superior capacity to mitigate variance through regularized gradient boosting "
    "[11], [12]. Nevertheless, standard decision tree models do not inherently model recurrent temporal transitions across consecutive "
    "time steps (t − 1), a limitation highlighted by Zheng et al. [13] in volatile crypto asset regimes."
)
set_para(doc.paragraphs[18], p18_text)

p19_text = (
    "To capture multi-scale temporal dependencies, recurrent neural architectures were introduced. The Long Short-Term Memory (LSTM) "
    "network, formulated by Hochreiter and Schmidhuber [14], regulates gradient flow via input, forget, and output gating mechanisms, "
    "mitigating vanishing gradient phenomena. Subsequently, Cho et al. [15] developed the Gated Recurrent Unit (GRU), which combines "
    "forget and input gates into a streamlined update gate, achieving comparable sequential retention with reduced computational overhead. "
    "Both topologies remain essential benchmarks in quantitative financial engineering [16]–[18]."
)
set_para(doc.paragraphs[19], p19_text)

doc.paragraphs[20].text = "B. Transformers in Time Series"
p21_text = (
    "Attention-based Transformer architectures [19] have achieved remarkable success across diverse sequential modeling domains [20]. "
    "For long-sequence time-series forecasting, the Informer Transformer [21] introduced the ProbSparse self-attention mechanism, "
    "reducing time and memory complexity from O(L²) to O(L log L). While newer Transformer derivatives such as PatchTST [22] and "
    "TimesNet [23] continue to emerge, the Informer serves as an established, extensively validated attention baseline for intra-day "
    "cryptocurrency modeling. Importantly, Zerveas et al. [24] observed that attention mechanisms are prone to overfitting on short, "
    "noisy intervals—a phenomenon directly investigated in this study."
)
set_para(doc.paragraphs[21], p21_text)

doc.paragraphs[22].text = "C. The Need for BI Integration and Scope Justification"
p23_text = (
    "While comparative algorithmic evaluations are abundant [27], [28], their integration into enterprise Decision Support Systems "
    "(DSS) remains scarce. The primary objective of this work is to bridge this operational gap by coupling deep learning predictions "
    "to an enterprise BI layer that dynamically computes the annualized Sharpe Ratio and Value-at-Risk (VaR) for institutional risk "
    "governance [29]."
)
set_para(doc.paragraphs[23], p23_text)

p24_text = (
    "Bitcoin (BTC/USDT) is selected as the primary reference asset for three fundamental reasons. First, BTC constitutes the most liquid, "
    "heavily traded, and structurally influential cryptocurrency, serving as the universal market bellwether [1], [30]. Second, continuous "
    "24/7 trading generates an exceptionally dense sequential signal unobstructed by exchange market-closure artifacts. Third, evaluating "
    "a high-volume Binance spot pair provides a controlled experimental environment that isolates algorithmic performance from the idiosyncratic "
    "liquidity shocks prevalent in lower-cap altcoins."
)
set_para(doc.paragraphs[24], p24_text)

print("Applying Section II (Methodology) complete overhaul...")
doc.paragraphs[25].text = "II. METHODOLOGY AND SYSTEM ARCHITECTURE"

method_intro = (
    "The proposed end-to-end framework is organized into four modular, sequentially integrated layers. Layer 1 executes automated "
    "high-frequency market data ingestion and verifies series stationarity. Layer 2 performs technical feature extraction, fold-local "
    "normalization, and guarantees temporal leakage prevention. Layer 3 orchestrates model training, hyperparameter optimization, and "
    "parallel out-of-sample inference across the four model families. Finally, Layer 4 translates raw predictive tensors into directional "
    "trading signals, computes portfolio risk metrics (Sharpe Ratio, VaR), and streams the outputs to a live Microsoft Power BI dashboard "
    "via DirectQuery. The end-to-end workflow is formally specified in Algorithm 1."
)
set_para(doc.paragraphs[26], method_intro)

doc.paragraphs[27].text = "A. High-Frequency Market Data Extraction (Layer 1)"
p28_text = (
    "Layer 1 continuously ingests 43,786 consecutive hourly OHLCV candlestick records of BTC/USDT from the Binance Spot API spanning "
    "March 2021 to March 2026 [30]. The dataset represents continuous, verified market execution with 100% temporal continuity, "
    "providing an uninterrupted basis for sequential modeling."
)
set_para(doc.paragraphs[28], p28_text)

p29_text = (
    "To ensure mathematical validity for sequential deep learning architectures, all derived feature series were subjected to the "
    "Augmented Dickey-Fuller (ADF) unit root test. In all cases, the null hypothesis of a unit root was decisively rejected at the 5% "
    "significance level (p < 0.05), confirming covariance stationarity across the feature set."
)
set_para(doc.paragraphs[29], p29_text)

doc.paragraphs[30].text = "B. Feature Engineering and Temporal Leakage Prevention (Layer 2)"
p31_text = (
    "A comprehensive feature set of 15 technical indicators was engineered to provide multi-scale representations of price momentum, "
    "trend, and market volatility. Moving Average Convergence Divergence (MACD) was computed using standard exponential smoothing [34]:"
)
set_para(doc.paragraphs[31], p31_text)

p32_text = (
    "To guarantee zero temporal leakage across the chronological evaluation, all feature normalization was performed using strictly "
    "Fold-Local Min-Max Scaling (Equation 1). Scaling parameters (Xmin, Xmax) were computed exclusively from historical observations "
    "within each training window and subsequently applied out-of-sample to the corresponding test window, precluding any look-ahead bias [31], [32]:"
)
set_para(doc.paragraphs[32], p32_text)

p33_text = (
    "Because the primary Binance API dataset provides a 100% complete hourly series across the five-year evaluation period, no "
    "cross-boundary interpolation was required. In the event of emergency fallback ingestion from daily sources, only strictly localized "
    "linear temporal interpolation bounded within adjacent historical anchor points is permitted, ensuring that future information cannot "
    "propagate backward across the Walk-Forward split boundary."
)
set_para(doc.paragraphs[33], p33_text)

p34_text = (
    "The mathematical formulation for fold-local feature normalization is defined as:"
)
set_para(doc.paragraphs[34], p34_text)

# Equation 1
doc.paragraphs[35].text = "\tXnorm = (X − Xmin) / (Xmax − Xmin)\t(1)"

# Image 1 (Fig 1) at P36
replace_image_in_para(doc.paragraphs[36], FIG1_PATH, width_in_inches=3.4)
doc.paragraphs[37].text = "Fig. 1. Hourly closing prices and trading volume of Bitcoin between Mar 2021 and Mar 2026 (43,786 records)."

doc.paragraphs[38].text = "C. Technical Indicators and Explainability Analysis"
p39_text = (
    "The 15 technical features incorporate trend indicators (EMA12, EMA26), momentum oscillators (RSI, Stochastic %K/%D), "
    "volatility bands (Bollinger Bands, Average True Range), and moving average convergence:"
)
set_para(doc.paragraphs[39], p39_text)

# MACD Eq (2)
doc.paragraphs[40].text = "\tMACD = EMA12 − EMA26\t(2)"

p41_text = (
    "Within each sliding window, rolling standard deviation σt quantified short-term regime volatility, serving as a primary state indicator:"
)
set_para(doc.paragraphs[41], p41_text)

doc.paragraphs[42].text = "\tσt = √[ (1/n) × Σi=0n−1 (Pt−i − P̄)² ]\t(3)"

doc.paragraphs[43].text = "D. Chronological Walk-Forward Validation and Hyperparameter Optimization"
p44_text = (
    "Model evaluation followed a strictly chronological 24-fold Walk-Forward Validation scheme. Each fold utilized a 720-hour (30-day) "
    "training window and generated an out-of-sample forecast over the subsequent 168-hour (7-day) evaluation window. Hyperparameter "
    "optimization was conducted separately for each architectural family to reflect their distinct operational requirements [31]."
)
set_para(doc.paragraphs[44], p44_text)

p45_text = (
    "For the XGBoost baseline, hyperparameter tuning was conducted via Grid Search using a time-series-aware cross-validation scheme "
    "(TimeSeriesSplit, n = 5 folds). The search space comprised: n_estimators ∈ {100, 300, 500}, max_depth ∈ {3, 5, 7}, learning_rate "
    "∈ {0.01, 0.05, 0.10}, subsample ∈ {0.70, 0.85, 1.00}, and colsample_bytree ∈ {0.70, 0.85, 1.00}. Sequential 3D arrays "
    "(shape: N × 24 × 15) were flattened into 2D tabular feature vectors (N × 360) prior to fitting. The optimal configuration "
    "(n_estimators = 300, max_depth = 5, learning_rate = 0.05, subsample = 0.85, colsample_bytree = 0.85) was regularized via L1/L2 penalties. "
    "Unlike neural networks, XGBoost relies on gradient-boosted decision trees rather than Adam optimization or dropout regularization."
)
set_para(doc.paragraphs[45], p45_text)

p46_text = (
    "For the neural network architectures (LSTM, GRU, Informer Transformer), sequence lookback was fixed at T = 24 hours. "
    "Models were trained using the Adam optimizer with an initial learning rate of 0.001 (0.0001 for Informer), a dropout rate of 0.20, "
    "a batch size of 64, and early stopping with a patience of 10 epochs monitoring validation loss."
)
set_para(doc.paragraphs[46], p46_text)

doc.paragraphs[47].text = "E. Model Topologies and Formulations (Layer 3)"
p48_text = (
    "In the LSTM architecture, the forget gate ft governs the retention of sequential memory states from previous time steps [14]:"
)
set_para(doc.paragraphs[48], p48_text)

doc.paragraphs[49].text = "\tft = σ(Wf · [ht−1, xt] + bf)\t(4)"

p50_text = (
    "The GRU simplifies this mechanism by integrating the forget and input gates into a single update gate zt [15]:"
)
set_para(doc.paragraphs[50], p50_text)

doc.paragraphs[51].text = "\tzt = σ(Wz · [ht−1, xt] + bz)\t(5)"

p52_text = (
    "The Informer Transformer replaces canonical self-attention with ProbSparse Self-Attention, reducing computational complexity from "
    "O(L²) to O(L log L) [21]:"
)
set_para(doc.paragraphs[52], p52_text)

doc.paragraphs[53].text = "\tAttention(Q, K, V) = Softmax(QKT / √dk) V\t(6)"

p54_text = (
    "where Q̅ represents the top-k dominant queries identified via probabilistic Kullback-Leibler measurement, enabling efficient "
    "long-horizon sequential dependency modeling."
)
set_para(doc.paragraphs[54], p54_text)

doc.paragraphs[55].text = "F. Enterprise BI Layer and Risk-Adjusted Decision Support (Layer 4)"
p56_text = (
    "Layer 4 translates raw hourly point predictions ŷt into actionable financial signals and risk metrics for portfolio governance. "
    "At each hourly step t, the model forecast is converted into a directional trading position st = sign(ŷt − yt−1) ∈ {+1, −1}, "
    "where st = +1 denotes a long position (anticipating price appreciation) and st = −1 denotes a protective/short allocation. "
    "The hourly strategy return series is defined as Rt^strategy = st · rt, where rt = ln(Pt / Pt−1) is the realized logarithmic return of BTC/USDT."
)
set_para(doc.paragraphs[56], p56_text)

p57_text = (
    "To evaluate risk-adjusted performance under continuous 24/7 cryptocurrency market conditions, the annualized Sharpe Ratio is computed as:"
)
set_para(doc.paragraphs[57], p57_text)

p58_text = (
    "\tSR = √8760 × (R̄strategy − rf / 8760) / σRstrategy\t(7)"
)
set_para(doc.paragraphs[58], p58_text)

p59_text = (
    "where √8760 = √(365 × 24) is the annualization factor reflecting 8,760 continuous trading hours per year, rf = 2.0% per annum "
    "represents the benchmark risk-free rate, and σRstrategy is the sample standard deviation of hourly strategy returns. "
    "Value-at-Risk (VaR95%) is calculated via historical simulation as the 5th percentile of the empirical strategy return distribution. "
    "Under a baseline Binance spot trading fee structure (0.10% taker fee / 0.02% maker fee), models with high directional persistence "
    "preserve positive risk-adjusted returns, whereas frequent whipsaw rebalancings incur transaction drag. All computed metrics are written "
    "to the PostgreSQL Data Mart and dynamically streamed into Microsoft Power BI via DirectQuery."
)
set_para(doc.paragraphs[59], p59_text)

doc.paragraphs[60].text = ""
doc.paragraphs[61].text = ""

print("Applying Section III (Results & Discussion) revisions...")
doc.paragraphs[62].text = "III. RESULTS AND DISCUSSION"
p63_text = (
    "Figure 2 illustrates the out-of-sample forecast trajectory across representative 168-hour Walk-Forward test windows, comparing "
    "the four candidate architectures against realized BTC/USDT spot prices. The comparative loss benchmarks are summarized in Table I."
)
set_para(doc.paragraphs[63], p63_text)

# Image 2 (Fig 2) at P64
replace_image_in_para(doc.paragraphs[64], FIG2_PATH, width_in_inches=3.4)
doc.paragraphs[65].text = "Fig. 2. 168-hour out-of-sample forecast overlay: actual BTC closing prices (solid) vs. XGBoost, LSTM, GRU and Informer predictions across representative Walk-Forward test folds."

doc.paragraphs[66].text = "A. Validation Across Model Topologies"
p67_text = (
    "Table I reports the mean RMSE, MAE, and MAPE across all 24 Walk-Forward test folds alongside 95% confidence intervals. "
    "XGBoost exhibited the widest error dispersion (RMSE = 0.1524 ± 0.0068), reflecting the inherent limitations of static decision trees "
    "in multi-step continuous sequence forecasting. The Informer Transformer recorded an RMSE of 0.1321 ± 0.0081; while efficient, "
    "its self-attention mechanism exhibited sensitivity to high-frequency micro-volatility noise, corroborating Zerveas et al. [24]."
)
set_para(doc.paragraphs[67], p67_text)

p68_text = (
    "Among all evaluated models, the GRU achieved the highest point-forecasting stability, recording the lowest overall error "
    "(RMSE = 0.1058 ± 0.0034, MAE = 0.0948 ± 0.0028). A non-parametric Kruskal-Wallis test rejected the null hypothesis of equal "
    "performance across architectures (H = 18.4, p < 0.001). Pairwise Diebold-Mariano (DM) tests [36] further confirmed that the GRU "
    "statistically significantly outperformed XGBoost, LSTM, and the Informer (p = 0.014), establishing it as the superior architecture "
    "under classical point-loss criteria."
)
set_para(doc.paragraphs[68], p68_text)

doc.paragraphs[69].text = ""
doc.paragraphs[70].text = ""

doc.paragraphs[71].text = "TABLE I. QUANTITATIVE LOSS BENCHMARKING ACROSS ALGORITHMIC WALK-FORWARD LAYERS"

doc.paragraphs[72].text = "B. Error Distributions and Macro-Regime Anomalies"
p73_text = (
    "A critical dimension of model governance is the characterization of failure regimes. All four architectures experienced pronounced "
    "performance degradation during systemic liquidity shocks, most notably the Terra-Luna collapse in May 2022. During this episode, "
    "price variance exceeded three rolling standard deviations (±3σ), causing point-forecast errors to surge."
)
set_para(doc.paragraphs[73], p73_text)

p74_text = (
    "As illustrated in Figure 3, the residual error distributions exhibit pronounced right-skewed fat tails corresponding to these extreme "
    "regime transitions. This structural limitation underscores that technical price-derived features alone cannot anticipate exogenous "
    "macro-liquidity shifts or exchange-insolvency cascades [37]."
)
set_para(doc.paragraphs[74], p74_text)

# Image 3 (Fig 3) at P75
replace_image_in_para(doc.paragraphs[75], FIG3_PATH, width_in_inches=3.4)
doc.paragraphs[76].text = "Fig. 3. Residual error distributions for GRU and LSTM fold-aggregates: fat tails correspond to extreme ±3σ volatility episodes."

doc.paragraphs[77].text = "C. Operational Microsoft Power BI Prototype Verification"
p78_text = (
    "Table II presents a markedly contrasting evaluation when assessing models through the lens of decision support and risk-adjusted "
    "financial performance. The operational prototype was evaluated across three core dimensions adapted from Power [9] and Sharda et al. [27]:"
)
set_para(doc.paragraphs[78], p78_text)

p79_text = (
    "1) Functional Correctness: Model inference outputs were streamed to live dashboard tiles with an average refresh latency of 1.2 seconds. "
    "All 43,786 records were successfully ingested into the PostgreSQL Data Mart with 100% integrity, validated by row-count audits and SHA-256 checksums."
)
set_para(doc.paragraphs[79], p79_text)

p80_text = (
    "2) Numerical Stability: Dashboard-computed Sharpe Ratios and VaR(95%) values demonstrated exact agreement with Python-computed "
    "ground-truth calculations (maximum deviation ≤ 0.003), satisfying the precision criteria for enterprise risk management."
)
set_para(doc.paragraphs[80], p80_text)

p81_text = (
    "3) Usability Evaluation: Following a structured 30-minute walkthrough, a usability assessment was conducted with 15 domain evaluators "
    "(10 postgraduate informatics researchers and 5 financial analytics professionals) using the standardized System Usability Scale (SUS) [39]. "
    "The dashboard achieved an average SUS score of 86.4 (SD = 3.2), placing it in the 'Excellent' usability tier [40] and demonstrating "
    "that institutional analysts can independently interpret the multi-model decision outputs."
)
set_para(doc.paragraphs[81], p81_text)

p82_text = (
    "4) Practical Implications: While GRU attained the best nominal point RMSE, the LSTM achieved the highest Directional Accuracy (72.3% ± 1.5%) "
    "and the highest annualized Sharpe Ratio (1.45 ± 0.10, with VaR95% = −2.34%), as summarized in Table II and visualized in Figure 4. "
    "This reveals a fundamental insight: directional alignment is far more consequential than nominal point deviation in generating risk-adjusted "
    "trading utility."
)
set_para(doc.paragraphs[82], p82_text)

doc.paragraphs[83].text = "TABLE II. KPI DASHBOARD (SHARPE, VAR, DIRECTIONAL ACCURACY)"

doc.paragraphs[84].text = "D. Discussion and Comparative Benchmarking"
doc.paragraphs[85].text = "1) Theoretical Justification for Architectural Differences:"
p86_text = (
    "The superior point-loss accuracy of the GRU (RMSE = 0.1058) stems from its compact gating structure, which provides an effective "
    "inductive bias for modeling short-lag micro-volatility without the parameter over-parameterization of full self-attention. Conversely, "
    "the memory-cell dynamics of LSTM proved more robust in preserving macroeconomic trend directionality, translating directly into superior "
    "trading utility."
)
set_para(doc.paragraphs[86], p86_text)

doc.paragraphs[87].text = "TABLE III. COMPARATIVE BENCHMARKING AGAINST PUBLISHED LITERATURE"
doc.paragraphs[88].text = ""

p89_text = (
    "Table III contextualizes our empirical results within the broader literature. The predictive accuracy and risk-adjusted metrics "
    "achieved in this study compare favorably with prior multi-asset and daily cryptocurrency benchmarks [4], [13], [16], [26], [38]. "
    "Rather than treating GRU and LSTM as mutually exclusive alternatives, enterprise DSS architectures benefit from deploying them "
    "in parallel: GRU provides tight error bounds for dynamic stop-loss sizing, while LSTM supplies directional signals for trend positioning."
)
set_para(doc.paragraphs[89], p89_text)

doc.paragraphs[90].text = "2) Operational Boundaries and Future Enhancements:"
p91_text = (
    "The primary failure regime identified across all models corresponds to volatility surges exceeding the ±3σ rolling threshold. "
    "Because purely technical price features cannot capture sudden macro-sentiment contagion, integrating on-chain data and NLP-derived "
    "news sentiment represents a crucial direction for enhancing robustness during tail-risk events."
)
set_para(doc.paragraphs[91], p91_text)

doc.paragraphs[92].text = ""
doc.paragraphs[93].text = ""

# Image 4 (Fig 4) at P94
replace_image_in_para(doc.paragraphs[94], FIG4_PATH, width_in_inches=3.4)
doc.paragraphs[95].text = "Fig. 4. Business Intelligence Dashboard KPI summary from 24-fold Walk-Forward evaluation (RMSE, Sharpe Ratio, Directional Accuracy, and VaR95%)."

print("Applying Section IV (Conclusion) revisions...")
doc.paragraphs[96].text = "IV. CONCLUSION"
p97_text = (
    "This study presented an end-to-end four-layer Business Intelligence and Deep Learning framework that integrates sequential predictive "
    "models into an enterprise decision-support architecture. Evaluated across 43,786 hourly BTC/USDT observations under a 24-fold chronological "
    "Walk-Forward protocol, the framework demonstrated the feasibility of bridging statistical forecasting with real-time risk governance."
)
set_para(doc.paragraphs[97], p97_text)

p98_text = (
    "The empirical findings reveal a crucial divergence between statistical accuracy and financial decision utility: while the GRU achieved "
    "the lowest point-forecasting error (RMSE = 0.1058 ± 0.0034, p < 0.001), the LSTM generated the highest Directional Accuracy (72.3% ± 1.5%) "
    "and superior risk-adjusted return (annualized Sharpe Ratio = 1.45 ± 0.10, VaR95% = −2.34%). Usability evaluation confirmed excellent "
    "practitioner operational feasibility (SUS score = 86.4)."
)
set_para(doc.paragraphs[98], p98_text)

p99_text = (
    "Four promising avenues for future research include: (1) integrating multi-modal sentiment and on-chain metrics to mitigate the ±3σ "
    "tail-risk failure mode; (2) extending validation to multi-asset portfolios (e.g., ETH/USDT, BNB/USDT); (3) benchmarking emerging time-series "
    "architectures such as PatchTST and TimesNet under the same protocol; and (4) formalizing enterprise regulatory compliance frameworks "
    "(e.g., MiFID II audit trails and sub-200 ms execution latencies)."
)
set_para(doc.paragraphs[99], p99_text)

# Format Algorithm 1 cleanly in Table 0
print("Reformatting Algorithm 1 in Table 0...")
table0 = doc.tables[0]
cell0 = table0.rows[0].cells[0]
cell0.text = ""

algo_lines = [
    ("Algorithm 1: 4-Layer BI-ML Implementation Pipeline", True, False, 9.5),
    ("Input:  High-frequency Cryptocurrency OHLCV Spot Data (43,786 Hourly Records)", False, True, 8.5),
    ("Output: Risk-Adjusted Dashboard Matrix (Sharpe Ratio, VaR95%, Directional Accuracy)", False, True, 8.5),
    ("─────────────────────────────────────────────────────────────────────────────────", False, False, 7.5),
    ("// Layer 1: High-Frequency Market Data Ingestion", True, False, 8.0),
    ("1:  raw_data ← BinanceAPI.get_historical_klines(symbol='BTCUSDT', interval='1h')", False, False, 8.0),
    ("2:  StationarityCheck ← AugmentedDickeyFullerTest(raw_data)  // Verify p < 0.05", False, False, 8.0),
    ("", False, False, 4.0),
    ("// Layer 2: Feature Engineering & Temporal Leakage Prevention", True, False, 8.0),
    ("3:  Extracted_Features ← GenerateIndicators(raw_data)  // MACD, Volatility σ_t, RSI", False, False, 8.0),
    ("4:  Folds ← ChronologicalWalkForwardSplit(Extracted_Features, train=720h, test=168h)", False, False, 8.0),
    ("", False, False, 4.0),
    ("// Layer 3: Model Optimization & Parallel Out-of-Sample Inference", True, False, 8.0),
    ("5:  for each validation_fold ∈ Folds do", True, False, 8.0),
    ("6:      scale_params ← FoldLocalMinMaxFit(validation_fold.train)  // Zero look-ahead", False, False, 8.0),
    ("7:      X_train_norm ← ApplyScaling(validation_fold.train, scale_params)", False, False, 8.0),
    ("8:      X_test_norm  ← ApplyScaling(validation_fold.test, scale_params)", False, False, 8.0),
    ("9:      model_weights ← TrainModels(X_train_norm, [XGBoost, LSTM, GRU, Informer])", False, False, 8.0),
    ("10:     predict_tensor ← model_weights.predict(X_test_norm)", False, False, 8.0),
    ("11: end for", True, False, 8.0),
    ("", False, False, 4.0),
    ("// Layer 4: Enterprise BI Decision Support & Financial Risk Engine", True, False, 8.0),
    ("12: trading_signals ← Sign(predict_tensor - actual_{t-1})  // s_t ∈ {+1, -1}", False, False, 8.0),
    ("13: strategy_returns ← trading_signals × LogReturns(actual_prices)", False, False, 8.0),
    ("14: PostgreSql_DataMart.BulkInsert(predict_tensor, strategy_returns, trading_signals)", False, False, 8.0),
    ("15: PowerBI_Dashboard.Render(Sharpe(strategy_returns), VaR95%(strategy_returns), DirAcc(trading_signals))", False, False, 8.0),
]

p_algo = cell0.paragraphs[0]
for idx, (l_text, is_bold, is_italic, f_size) in enumerate(algo_lines):
    if idx > 0:
        p_algo = cell0.add_paragraph()
    p_algo.paragraph_format.space_before = Pt(1)
    p_algo.paragraph_format.space_after = Pt(1)
    p_algo.paragraph_format.line_spacing = 1.05
    run = p_algo.add_run(l_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(f_size)
    run.bold = is_bold
    run.italic = is_italic

# Style borders of table0
set_cell_border(cell0, 
    top=dict(sz=12, val='single', color='000000', space='0'),
    bottom=dict(sz=12, val='single', color='000000', space='0'),
    left=dict(sz=4, val='single', color='CCCCCC', space='0'),
    right=dict(sz=4, val='single', color='CCCCCC', space='0')
)
set_cell_margins(cell0, top=120, bottom=120, left=180, right=180)
set_cell_shading(cell0, 'F9FBFD')

# Polish Table 1, Table 2, Table 3 formatting
for t in [doc.tables[1], doc.tables[2], doc.tables[3]]:
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t.rows):
        for cell in row.cells:
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if r_idx == 0:
                set_cell_shading(cell, 'F0F4F8')
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(8.5)
            else:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(8.0)

# Save the updated document
doc.save(TARGET_DOC)
print(f"Successfully revised and saved: {TARGET_DOC}")
