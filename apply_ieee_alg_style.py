import re

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace CSS for .pseudo
old_css = """.pseudo {
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 10px;
            font-family: "Courier New", Courier, monospace;
            font-size: 8pt;
            line-height: 1.1;
            white-space: pre-wrap;
            margin: 10px 0;
            break-inside: avoid;
            text-align: left;
        }"""

new_css = """.pseudo {
            background-color: transparent;
            border-top: 1.5px solid black;
            border-bottom: 1.5px solid black;
            padding: 5px 0;
            font-family: "Times New Roman", Times, serif;
            font-size: 8.5pt;
            line-height: 1.3;
            margin: 15px 0;
            break-inside: avoid;
            text-align: left;
        }
        .pseudo-title {
            font-weight: bold;
            text-align: left;
            border-bottom: 1px solid black;
            padding-bottom: 5px;
            margin-bottom: 5px;
        }
        .pseudo-content {
            padding: 0 10px;
        }
        .pseudo-content b {
            font-size: 8pt;
        }"""

html = html.replace(old_css, new_css)

# Start and end markers for HTML content
start_marker = r'<div class="pseudo" style="column-span: all; font-size: 8pt;">'
end_marker = r'Dashboard.Render(SharpeRatio(residual_vectors), DAX_VaR(residual_vectors))' + '\n' + r'            </div>'

pattern_html = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)

new_html = r"""<div class="pseudo" style="column-span: all;">
                <div class="pseudo-title">Algorithm 1: 4-Layer BI-ML Implementation Pipeline</div>
                <div class="pseudo-content">
                    <b>Input:</b> High-frequency Cryptocurrency OHLCV Spot Data<br>
                    <b>Output:</b> Risk-adjusted Dashboard Matrix (<i>Sharpe Ratio, VaR</i>)<br>
                    <br>
                    1: <i>// Layer 1: Data Ingestion</i><br>
                    2: \(raw\_data\) &larr; BinanceAPI(symbol="BTCUSDT", interval="1h")<br>
                    3: <br>
                    4: <i>// Layer 2: ETL Transformation & Feature Engineering</i><br>
                    5: \(clean\_data\) &larr; PolynomialInterpolate(\(raw\_data\))<br>
                    6: \(Extracted\_Features\) &larr; GenerateIndicators(\(clean\_data\)) <i>// MACD, \(\sigma_t\)</i><br>
                    7: \(Folds\) &larr; WalkForwardSplit(\(Extracted\_Features\), \(train=720\), \(test=168\))<br>
                    8: <br>
                    9: <i>// Layer 3: ML Inference Regimes</i><br>
                    10: <b>for</b> each \(validation\_fold\) &isin; \(Folds\) <b>do</b><br>
                    11: &nbsp;&nbsp;&nbsp;&nbsp;\(scale\_params\) &larr; MinMaxFit(\(validation\_fold.train\))<br>
                    12: &nbsp;&nbsp;&nbsp;&nbsp;\(weights\) &larr; TrainNetwork(\(validation\_fold.train\), \(scale\_params\))<br>
                    13: &nbsp;&nbsp;&nbsp;&nbsp;\(predict\_tensor\) &larr; \(weights\).predict(\(validation\_fold.test\))<br>
                    14: <b>end for</b><br>
                    15: <br>
                    16: <i>// Layer 4: BI Dashboard Integration & Extraction</i><br>
                    17: \(residual\_vectors\) &larr; CalculateResiduals(\(actual\), \(predict\_tensor\))<br>
                    18: PostgreSQL\_DataMart.INSERT(\(residual\_vectors\))<br>
                    19: PowerBI\_Dashboard.Render(Sharpe(\(residual\_vectors\)), VaR(\(residual\_vectors\)))
                </div>
            </div>"""

html = pattern_html.sub(new_html, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Algorithm successfully styled to IEEE strict format.")
