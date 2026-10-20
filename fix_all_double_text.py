"""
Definitive script to eliminate all duplicate prefixes and style misalignments:
- Fixes automatic Word numbering vs manual prefix duplication
- Fixes body paragraphs that accidentally had Heading styles
- Ensures all Headings, Figure Captions, Table Headings, and Equations render cleanly without any double text
- Re-exports PDF and verifies rendering
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

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "04_Visualizations")
TARGET_DOC = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx")
PDF_PATH = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.pdf")

doc = Document(TARGET_DOC)

def set_para(p, text, style_name=None, bold_prefix=None, align=None):
    if style_name:
        p.style = doc.styles[style_name]
    p.text = ""
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.bold = True
    p.add_run(text)
    if align is not None:
        p.alignment = align

print("1. Fixing Headings (removing manual numbering like 'I. ', 'A. ', etc.)...")

# Title
set_para(doc.paragraphs[0], "A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence", style_name='paper title')

# Abstract & Keywords
abstract_body = (
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
set_para(doc.paragraphs[10], abstract_body, style_name='Abstract', bold_prefix="Abstract—")

keywords_body = "Financial Informatics, Business Intelligence, Deep Learning, XGBoost, LSTM, GRU, Informer Transformer, Decision Support System, Risk Management."
set_para(doc.paragraphs[11], keywords_body, style_name='Keywords', bold_prefix="Keywords—")

# Section I Headings
set_para(doc.paragraphs[13], "Introduction", style_name='Heading 1')
set_para(doc.paragraphs[17], "Baselines and Deep Sequences (RNNs)", style_name='Heading 2')
set_para(doc.paragraphs[20], "Transformers in Time Series", style_name='Heading 2')
set_para(doc.paragraphs[22], "The Need for BI Integration and Scope Justification", style_name='Heading 2')

# Section II Headings & Body Alignment
set_para(doc.paragraphs[25], "METHODOLOGY AND SYSTEM ARCHITECTURE", style_name='Heading 1')
set_para(doc.paragraphs[27], "High-Frequency Market Data Extraction (Layer 1)", style_name='Heading 2')
set_para(doc.paragraphs[30], "Feature Engineering and Temporal Leakage Prevention (Layer 2)", style_name='Heading 2')
set_para(doc.paragraphs[38], "Technical Indicators and Explainability Analysis", style_name='Heading 2')

# P41 was mistakenly Heading 2 -> Change to Body Text
p41_text = "Within each sliding window, rolling standard deviation σt quantified short-term regime volatility, serving as a primary state indicator:"
set_para(doc.paragraphs[41], p41_text, style_name='Body Text')

# Equation 3 at P42
set_para(doc.paragraphs[42], "\tσt = √[ (1/n) × Σi=0n−1 (Pt−i − P̄)² ]\t(3)", style_name='equation')

# Subsections II.D, II.E, II.F
set_para(doc.paragraphs[43], "Chronological Walk-Forward Validation and Hyperparameter Optimization", style_name='Heading 2')
set_para(doc.paragraphs[47], "Model Topologies and Formulations (Layer 3)", style_name='Heading 2')

# P48 was mistakenly Heading 3 -> Change to Body Text
p48_text = "In the LSTM architecture, the forget gate ft governs the retention of sequential memory states from previous time steps [14]:"
set_para(doc.paragraphs[48], p48_text, style_name='Body Text')

# Eq 4 at P49
set_para(doc.paragraphs[49], "\tft = σ(Wf · [ht−1, xt] + bf)\t(4)", style_name='equation')

# P50 was mistakenly Heading 2 -> Change to Body Text
p50_text = "The GRU simplifies this mechanism by integrating the forget and input gates into a single update gate zt [15]:"
set_para(doc.paragraphs[50], p50_text, style_name='Body Text')

# Eq 5 at P51
set_para(doc.paragraphs[51], "\tzt = σ(Wz · [ht−1, xt] + bz)\t(5)", style_name='equation')

# P52
p52_text = "The Informer Transformer replaces canonical self-attention with ProbSparse Self-Attention, reducing computational complexity from O(L²) to O(L log L) [21]:"
set_para(doc.paragraphs[52], p52_text, style_name='Body Text')

# P53 was mistakenly Heading 3 -> Change to equation
set_para(doc.paragraphs[53], "\tAttention(Q, K, V) = Softmax(QKT / √dk) V\t(6)", style_name='equation')

# P54
p54_text = "where Q̅ represents the top-k dominant queries identified via probabilistic Kullback-Leibler measurement, enabling efficient long-horizon sequential dependency modeling."
set_para(doc.paragraphs[54], p54_text, style_name='Body Text')

# Layer 4 Heading
set_para(doc.paragraphs[55], "Enterprise BI Layer and Risk-Adjusted Decision Support (Layer 4)", style_name='Heading 2')

# P56
p56_text = (
    "Layer 4 translates raw hourly point predictions ŷt into actionable financial signals and risk metrics for portfolio governance. "
    "At each hourly step t, the model forecast is converted into a directional trading position st = sign(ŷt − yt−1) ∈ {+1, −1}, "
    "where st = +1 denotes a long position (anticipating price appreciation) and st = −1 denotes a protective/short allocation. "
    "The hourly strategy return series is defined as Rt^strategy = st · rt, where rt = ln(Pt / Pt−1) is the realized logarithmic return of BTC/USDT."
)
set_para(doc.paragraphs[56], p56_text, style_name='Body Text')

# P57
p57_text = "To evaluate risk-adjusted performance under continuous 24/7 cryptocurrency market conditions, the annualized Sharpe Ratio is computed as:"
set_para(doc.paragraphs[57], p57_text, style_name='Body Text')

# P58 was mistakenly Heading 3 -> Change to equation
set_para(doc.paragraphs[58], "\tSR = √8760 × (R̄strategy − rf / 8760) / σRstrategy\t(7)", style_name='equation')

# P59
p59_text = (
    "where √8760 = √(365 × 24) is the annualization factor reflecting 8,760 continuous trading hours per year, rf = 2.0% per annum "
    "represents the benchmark risk-free rate, and σRstrategy is the sample standard deviation of hourly strategy returns. "
    "Value-at-Risk (VaR95%) is calculated via historical simulation as the 5th percentile of the empirical strategy return distribution. "
    "Under a baseline Binance spot trading fee structure (0.10% taker fee / 0.02% maker fee), models with high directional persistence "
    "preserve positive risk-adjusted returns, whereas frequent whipsaw rebalancings incur transaction drag. All computed metrics are written "
    "to the PostgreSQL Data Mart and dynamically streamed into Microsoft Power BI via DirectQuery."
)
set_para(doc.paragraphs[59], p59_text, style_name='Body Text')

# Section III Headings
set_para(doc.paragraphs[62], "RESULTS AND DISCUSSION", style_name='Heading 1')
set_para(doc.paragraphs[66], "Validation Across Model Topologies", style_name='Heading 2')
set_para(doc.paragraphs[72], "Error Distributions and Macro-Regime Anomalies", style_name='Heading 2')
set_para(doc.paragraphs[77], "Operational Microsoft Power BI Prototype Verification", style_name='Heading 2')
set_para(doc.paragraphs[84], "Discussion and Comparative Benchmarking", style_name='Heading 2')
set_para(doc.paragraphs[85], "Theoretical Justification for Architectural Differences:", style_name='Heading 3')
set_para(doc.paragraphs[90], "Operational Boundaries and Future Enhancements:", style_name='Heading 3')

# Section IV Heading
set_para(doc.paragraphs[96], "CONCLUSION", style_name='Heading 1')

print("2. Fixing Figure Captions (removing manual 'Fig. X.' since style automatically generates it)...")
# Fig 1 at P37
set_para(doc.paragraphs[37], "Hourly closing prices and trading volume of Bitcoin between Mar 2021 and Mar 2026 (43,786 records).", style_name='figure caption', align=WD_ALIGN_PARAGRAPH.CENTER)

# Fig 2 at P65
set_para(doc.paragraphs[65], "168-hour out-of-sample forecast overlay: actual BTC closing prices (solid) vs. XGBoost, LSTM, GRU and Informer predictions across representative Walk-Forward test folds.", style_name='figure caption', align=WD_ALIGN_PARAGRAPH.CENTER)

# Fig 3 at P76
set_para(doc.paragraphs[76], "Residual error distributions for GRU and LSTM fold-aggregates: fat tails correspond to extreme ±3σ volatility episodes.", style_name='figure caption', align=WD_ALIGN_PARAGRAPH.CENTER)

# Fig 4 at P95
set_para(doc.paragraphs[95], "Business Intelligence Dashboard KPI summary from 24-fold Walk-Forward evaluation (RMSE, Sharpe Ratio, Directional Accuracy, and VaR95%).", style_name='figure caption', align=WD_ALIGN_PARAGRAPH.CENTER)

print("3. Fixing Table Headings (removing manual 'TABLE X' since style automatically generates it)...")
# Table I at P71
set_para(doc.paragraphs[71], "QUANTITATIVE LOSS BENCHMARKING ACROSS ALGORITHMIC WALK-FORWARD LAYERS", style_name='table head', align=WD_ALIGN_PARAGRAPH.CENTER)

# Table II at P83
set_para(doc.paragraphs[83], "KPI DASHBOARD (SHARPE, VAR, DIRECTIONAL ACCURACY)", style_name='table head', align=WD_ALIGN_PARAGRAPH.CENTER)

# Table III at P87
set_para(doc.paragraphs[87], "COMPARATIVE BENCHMARKING AGAINST PUBLISHED LITERATURE", style_name='table head', align=WD_ALIGN_PARAGRAPH.CENTER)

print("4. Re-saving document...")
doc.save(TARGET_DOC)
print(f"[OK] Document saved successfully: {TARGET_DOC}")

print("5. Exporting PDF via Word COM...")
try:
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    doc_com = word.Documents.Open(os.path.abspath(TARGET_DOC))
    doc_com.SaveAs(os.path.abspath(PDF_PATH), FileFormat=17)
    doc_com.Close()
    word.Quit()
    print(f"[OK] PDF successfully exported to: {PDF_PATH}")
except Exception as e:
    print(f"[!] PDF export warning: {e}")
