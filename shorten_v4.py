import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import shutil

# Start from V2 which has native OMML equations intact
shutil.copy('05_Reports/Manuscript_IJAI_FINAL_V2.docx', '05_Reports/Manuscript_IJAI_FINAL_V4.docx')

doc = docx.Document('05_Reports/Manuscript_IJAI_FINAL_V4.docx')

short_abstract = (
    "Abstract—Cryptocurrency markets' inherent volatility complicates predictive modeling, "
    "demanding methods that link deep learning with enterprise Decision Support Systems (DSS). "
    "This study proposes an automated, four-layer Business Intelligence (BI) pipeline embedding Recurrent "
    "and Transformer inferences into an enterprise DSS to dynamically compute Risk-adjusted metrics "
    "like Sharpe Ratio and Value-at-Risk. Analyzing 43,786 hourly BTC/USDT records (2021–2026), "
    "we evaluated XGBoost, LSTM, GRU, and the Informer Transformer. Walk-Forward Validation established GRU "
    "as the most accurate model (RMSE: 0.1058; p < 0.001). However, the BI integration revealed a critical "
    "trade-off: despite higher RMSE, LSTM achieved superior Directional Accuracy (72.3%) and Sharpe Ratio (1.45), "
    "indicating that numerical error minimization does not inherently guarantee trading profitability. "
    "The prototype Microsoft Power BI dashboard demonstrated operational feasibility with an Excellent 86.4 "
    "System Usability Scale (SUS) score, verifying that high-frequency neural forecasts can successfully "
    "drive real-world institutional risk management tools."
)

for p in doc.paragraphs:
    text = p.text.strip()
    
    # 1. Replace abstract
    if text.startswith("Abstract—"):
        p.text = short_abstract
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        continue
        
    # 3. Shorten text in Discussion
    if "The empirical outperformance of the Gated Recurrent Unit (GRU)" in text:
        p.text = (
            "The empirical outperformance of the GRU (RMSE 0.1058) over Informer and XGBoost is theoretically grounded "
            "in its architectural inductive biases. Purely attention-based Transformers capture long-range dependencies "
            "but impose quadratic complexity, making them less suitable for 1-hour crypto granularity where local momentum "
            "and intra-day micro-volatility dominate. GRU's selective reset and update gates inherently capture these "
            "short-lag causal dependencies better."
        )
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
    if "Crucially, the Informer's ProbSparse attention" in text:
        p.text = (
            "Crucially, the Informer's ProbSparse attention, designed to reduce complexity, inadvertently prunes "
            "high-value short-lag correlation pairs vital for 1-hour crypto forecasting. This structural mismatch explains "
            "the significant RMSE gap confirmed by the DM test (p = 0.014), aligning with findings that simpler recurrent "
            "architectures often surpass attention models on short look-back windows."
        )
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
    if "To contextualise our results within the existing literature" in text:
        p.text = (
            "Contextualizing these results, Livieris et al. [38] reported normalized RMSEs of 0.14–0.17 for hourly BTC, "
            "while our GRU achieves a substantially lower 0.1058 RMSE under rigorous Walk-Forward Validation. "
            "Furthermore, our LSTM's DA of 72.3% surpasses the typical 60-65% range reported in comparable literature [13], [16]. "
            "The Sharpe Ratio of 1.45 obtained from our dashboard also compares favourably with algorithmic trading benchmarks."
        )
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
    if "While the GRU exhibited lower numerical RMSE, operational analysis" in text:
        p.text = (
            "Operationally, the LSTM achieved superior directional market orientation accuracy (72.3%), a highly actionable "
            "metric for trading decision support. Using our explicitly formulated Power BI DirectQuery integration, the "
            "dashboard effectively translates LSTM prediction tensors into actionable risk-threshold indicators, demonstrating "
            "that quantitative forecasting can successfully be extended into operator-facing BI layers."
        )
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)

doc.save('05_Reports/Manuscript_IJAI_FINAL_V4.docx')
print("Successfully shortened text and preserved original Word OMML equations.")
