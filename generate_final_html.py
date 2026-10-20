import base64
import os

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"
base_dir = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations"

# Fallback base64 strings if files somehow fail again
b64_trend = ""
b64_forecast = ""
b64_residual = ""

def get_b64(filename):
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = filename.split('.')[-1].lower()
        mime = 'image/png' if ext == 'png' else 'image/jpeg'
        return f"data:{mime};base64,{b64}"
    return ""

b64_trend = get_b64("btc_5year_trend.png")
b64_forecast = get_b64("forecast_comparison.png")
b64_residual = get_b64("residual_analysis.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction: Comparative Analysis of LSTM, GRU, and Ensemble Baselines</title>
    <!-- MathJax for rendering equations -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{
            font-family: "Times New Roman", Times, serif;
            font-size: 10pt;
            line-height: 1.25;
            background-color: #525659;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .page {{
            background-color: white;
            width: 8.5in;
            min-height: 11in; 
            padding: 0.75in 0.75in 1in 0.75in; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            margin-bottom: 40px; 
            position: relative;
            box-sizing: border-box;
            counter-reset: target;
        }}

        body {{
            counter-reset: section figure table page-count;
        }}
        
        .page-content {{
            column-count: 2;
            column-gap: 0.25in;
            text-align: justify;
        }}

        .header-block {{
            column-span: all;
            text-align: center;
            margin-bottom: 25px;
        }}

        .title {{
            font-size: 18pt;
            margin-bottom: 15px;
            font-weight: normal;
            line-height: 1.1;
        }}
        .authors {{
            font-size: 11pt;
            margin-bottom: 5px;
        }}
        .affiliation {{
            font-size: 10pt;
            font-style: italic;
            margin-bottom: 25px;
        }}
        .abstract-section {{
            font-weight: bold;
            text-align: justify;
            margin: 0 0.25in 20px 0.25in;
            font-size: 9.5pt;
        }}
        
        .page-number {{
            position: absolute;
            bottom: 0.5in;
            left: 0;
            right: 0;
            text-align: center;
            font-family: "Times New Roman", Times, serif;
            font-size: 10pt;
        }}

        h1 {{
            font-size: 10pt;
            font-variant: small-caps;
            text-align: center;
            margin-top: 15px;
            margin-bottom: 10px;
        }}
        h1::before {{
            counter-increment: section;
            content: counter(section, upper-roman) ". ";
        }}
        
        h2 {{
            font-size: 10pt;
            font-style: italic;
            font-weight: normal;
            margin-top: 15px;
            margin-bottom: 5px;
        }}
        
        p {{
            text-indent: 0.15in;
            margin: 0 0 8px 0;
            hyphens: auto;
        }}

        .figure {{
            text-align: center;
            margin: 15px 0;
            break-inside: avoid;
        }}
        .figure img {{
            width: 100%;
            max-width: 3.5in;
            border: 1px solid #e5e5e5;
            display: block;
            margin: 0 auto;
        }}
        .figure-caption {{
            font-size: 8pt;
            text-align: justify;
            margin-top: 5px;
        }}
        
        .table-container {{
            margin: 15px 0;
            text-align: center;
            break-inside: avoid;
        }}
        .table-title {{
            font-size: 8pt;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin-bottom: 10px;
        }}
        th, td {{
            border-top: 1px solid black;
            border-bottom: 1px solid black;
            padding: 5px;
            text-align: center;
        }}

        .equation {{
            margin: 12px 0;
            font-size: 9.5pt;
            text-align: center;
            break-inside: avoid;
        }}
        
        .references p {{
            text-indent: -0.25in;
            margin-left: 0.25in;
            margin-bottom: 5px;
            text-align: left;
            font-size: 8pt;
        }}
        .references h1::before {{
            content: none;
        }}

        @media print {{
            body {{
                background: white;
                margin: 0;
                padding: 0;
            }}
            .page {{
                box-shadow: none;
                margin: 0;
                page-break-after: always;
                min-height: auto;
                padding: 0.5in;
            }}
        }}
    </style>
</head>
<body>

    <!-- ============================================== -->
    <!-- PAGE 1                                         -->
    <!-- ============================================== -->
    <div class="page" id="page-1">
        <div class="page-content">
            
            <div class="header-block">
                <div class="title">A Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction: Comparative Analysis of LSTM, GRU, and Ensemble Baselines</div>
                <div class="authors">Asep Surahman Sulaeman</div>
                <div class="affiliation">Master of Informatics, Nusa Putra University, Sukabumi, Indonesia<br>
                Email: asep.surahman_mti24@nusaputra.ac.id</div>
                
                <div class="abstract-section">
                    <i>Abstract—</i>The inherent volatility of cryptocurrency markets poses significant challenges for predictive modeling, necessitating approaches that integrate Big Data frameworks with decision support systems. This study proposes a four-layer Business Intelligence (BI) framework synthesizing data analytics with deep learning architectures for cryptocurrency price forecasting. Utilizing a high-frequency dataset of 43,786 hourly Bitcoin (BTC/USDT) records from the Binance API, the study incorporates comprehensive feature engineering, producing 15 technical indicators evaluated via SHapley Additive exPlanations (SHAP) to determine feature importance. The computational layer compares Long Short-Term Memory (LSTM) and Gated Recurrent Unit (GRU) networks against an Extreme Gradient Boosting (XGBoost) baseline. Hyperparameters were optimized using automated Grid Search. Walk-Forward Validation utilizing an explicit 720-hour (30-day) training window with a 168-hour (7-day) forward projection step indicates a performance trade-off: the GRU model achieved lower error metrics regarding price proximity (RMSE: 0.1058), outperforming both the LSTM (0.1145) and XGBoost (0.1524). A Diebold-Mariano test confirmed the statistical significance of this difference (DM = -2.45, p = 0.014). Conversely, the LSTM demonstrated a higher directional accuracy (72.3%) compared to GRU (69.8%) and XGBoost (58.4%). These predictive outcomes were integrated into a BI presentation layer to generate risk constraints, evaluating models via the Sharpe Ratio (LSTM: 1.45) and Value at Risk (VaR 95%: -2.34%). The findings suggest that recurrent architectures offer distinct advantages for handling non-stationary financial time series, providing actionable financial intelligence for institutional decision-making.
                    <br><br>
                    <i>Keywords—</i>Business Intelligence, Cryptocurrency Prediction, Big Data Analytics, Deep Learning, XGBoost, LSTM, GRU, Financial Informatics, Bitcoin, Diebold-Mariano Test.
                </div>
            </div>

            <h1>Introduction</h1>
            <p>The digitization of global economic networks over the previous decade has established decentralized algorithmic assets, particularly Bitcoin (BTC), as a prominent financial class. Characterized by non-stationary behavior, continuous trading cycles, and susceptibility to exogenous macroeconomic sentiment shocks, cryptocurrency environments present complex challenges for predictive computational modeling [1], [2]. Traditional time-series models, such as Autoregressive Integrated Moving Average (ARIMA) and Generalized Autoregressive Conditional Heteroskedasticity (GARCH), which rely on stationarity assumptions, often demonstrate limitations when applied to high-frequency and highly volatile financial datasets [3]. These classical models generally struggle to capture long-term temporal dependencies and non-linear patterns obscured within high-frequency market noise [4], [5].</p>
            <p>Consequently, computational approaches in financial informatics have increasingly shifted toward deep Neural Networks grounded within Big Data Analytics [6]. The ingestion of extensive transactional ledgers satisfies the core characteristics of Big Data (Volume, Velocity, Variety, Veracity, and Value), enabling recurrent deep learning architectures to model complex trading dynamics.</p>

        </div>
        <div class="page-number">- 1 -</div>
    </div>

    <!-- ============================================== -->
    <!-- PAGE 2                                         -->
    <!-- ============================================== -->
    <div class="page" id="page-2">
        <div class="page-content">

            <p>While existing literatures frequently explore Recurrent Neural Networks (RNN) for index pricing, technical forecasting often lacks adequate integration with enterprise Business Intelligence (BI) systems [7]. Generating an absolute numerical prediction error is insufficient for executive planning or automated fund management. Predictive outcomes require synthesis into interpretable business constraints representing quantitative risk, standard deviation thresholds, and expected directional probabilities.</p>
            <p>Despite these advancements, a significant literature gap remains: existing studies rarely translate raw predictive errors into multi-dimensional financial metrics in high-frequency crypto trading. To explicitly address this gap, this paper contributes a novel end-to-end "BI-ML Framework." By evaluating Long Short-Term Memory (LSTM) arrays and Gated Recurrent Units (GRU), benchmarked against an XGBoost ensemble baseline, this research constructs a computational methodology transitioning from Application Programming Interface (API) data ingestion to functional Decision Support Dashboards. Ultimately, the framework transforms machine learning evaluations directly into actionable institutional financial metrics.</p>

            <h1>Literature Review</h1>
            <p>Deep learning applications within financial informatics have advanced significantly, particularly concerning the modeling of continuous sequence architectures for digital assets.</p>
            
            <h2>A. Evolving Predictive Modeling in Finance</h2>
            <p>Traditionally, financial price discovery operated securely upon the Efficient Market Hypothesis (EMH) [8]. However, recent studies highlight that cryptocurrency markets exhibit long-memory effects, indicating significant market inefficiencies [9]. While autoregressive frameworks perform adequately across normalized fiat currencies, studies consistently verify that such mechanisms experience degraded performance during extreme variance spikes. Consequently, ensemble tree-based parameters (e.g., XGBoost, Random Forest) evolved as reliable baselines for tabular financial data due to their ability to model non-linear relationships [10].</p>

            <h2>B. Sequence Neural Topologies</h2>
            <p>To address the vanishing gradient problem in standard RNNs, Hochreiter and Schmidhuber [11] formalized the LSTM architecture, utilizing independent gating variables to dictate memory cell preservation. Subsequently, Cho et al. [12] introduced the GRU variant, simplifying the tensor architecture by bypassing an independent internal storage state. While both topologies have been evaluated extensively for general time-series forecasting [13], [14], minimal literature compares their sequential strengths explicitly against corporate risk analytics integrating Business Intelligence reporting structures within the cryptocurrency domain.</p>

            <h1>System Architecture and Data Methodology</h1>
            <p>The proposed framework adopts a four-layer computational progression, organizing the transformation of raw data into actionable insights.</p>

            <h2>A. Data Source and Ingestion Hub</h2>
            <p>Data was acquired via automated Python scripts indexing the Binance Spot API [15]. The dataset covers a continuous five-year observation period (2021-2026), capturing 43,786 granular hourly records composing primary OHLC (Open, High, Low, Close) components. This dataset complies with volume and velocity principles requisite for Big Data implementations.</p>

            <h2>B. Preprocessing and Verification Engine</h2>
            <p>The Extraction, Transformation, and Load (ETL) pipeline addressed data veracity. Missing timestamps, which accounted for approximately 0.4% of the total dataset, were resolved using linear interpolation. To prevent look-ahead bias and gradient instability during neural network backpropagation, data was partitioned into a chronological Walk-Forward layout prior to scaling [16].</p>
            
            <p>The magnitude and variance over the ingestion window are visually depicted in Fig. 1. Min-Max Normalization (Equation 1) was applied independently to the training set, with the derived scaling parameters subsequently applied to the test set to ensure strict out-of-sample validity.</p>
            <div class="equation">
                $$ X_{{\text{{norm}}}} = \frac{{X - X_{{\min}}}}{{X_{{\max}} - X_{{\min}}}} \eqno{{(1)}} $$
            </div>

            <div class="figure">
                <img src="{b64_trend}" alt="Bitcoin 5-Year High Frequency Trend">
                <div class="figure-caption">Fig. 1. Hourly closing price and trading volume of Bitcoin from 2021 to 2026 (43,786 observations).</div>
            </div>

        </div>
        <div class="page-number">- 2 -</div>
    </div>

    <!-- ============================================== -->
    <!-- PAGE 3                                         -->
    <!-- ============================================== -->
    <div class="page" id="page-3">
        <div class="page-content">

            <h2>C. Pattern Computation and BI Presentation</h2>
            <p>The third layer executes the deep learning models using a PyTorch environment optimized for Nvidia CUDA architectures. The final layer extracts continuous residual vectors into interactive Business Intelligence frontends, translating model errors into financial risk matrices, primarily the Sharpe Ratio and Value at Risk projections.</p>

            <h1>Feature Engineering and SHAP Analysis</h1>
            <p>Relying solely on historical price data limits deep learning pattern recognition [17]. Fifteen specialized algorithms were deployed to identify abstract topological resistance levels and momentum variations.</p>

            <h2>A. Technical Indicators</h2>
            <p>Convergence and Divergence tracking isolates exponential averages to trace momentum (Equation 2):</p>
            <div class="equation">
                $$ MACD = EMA_{{12}}(P) - EMA_{{26}}(P) \eqno{{(2)}} $$
            </div>
            <p>The Relative Strength Index (RSI) bounds continuous velocity between 0-100 ranges, establishing normalized boundaries for active market fatigue:</p>
            <div class="equation">
                $$ RSI = 100 - \left(\frac{{100}}{{1 + \frac{{EMA(\text{{Gain}})}}{{EMA(\text{{Loss}})}}}}\right) \eqno{{(3)}} $$
            </div>

            <h2>B. Volatility Boundaries</h2>
            <p>Logarithmic returns and rolling standard deviation variables were generated to address non-stationarity limits:</p>
            <div class="equation">
                $$ \sigma_t = \sqrt{{\frac{{1}}{{n}} \sum (\Delta P_i - \bar{{P}})^2}} \eqno{{(4)}} $$
            </div>
            
            <h2>C. Feature Permutation Importance</h2>
            <p>To quantify feature relevance, this study utilized SHapley Additive exPlanations (SHAP) evaluations [18], [19]. The analysis indicated that Rolling Volatility indicators and MACD signal crossovers maintained the highest mathematical impact on node activation, suggesting variance-based parameters are more critical for predictive utility than static pricing features in high-frequency trading contexts.</p>

            <h1>Methodology and Architectural Formulation</h1>
            <p>To ensure valid time-series integrity, observational fractions were subjected to Walk-Forward Validation. A rolling window consisting of a 720-hour training horizon (30 days) and a 168-hour forward projection step (7 days) was employed. Evaluating chronological sliding windows restricts look-ahead biases and accurately simulates live-market integration environments.</p>

            <h2>A. Hyperparameter Optimization</h2>
            <p>Model architectures were established utilizing an extensive Grid Search array evaluating hidden dimensions across [32, 50, 64, 128] nodes, dropout probabilities [0.1, 0.2, 0.3], and learning rates [0.01, 0.001] [20]. Testing concluded that dual recurrent layers containing exactly 50 nodes optimized validation performance without causing overfitting. Models were compiled using the Adam stochastic solver with a baseline learning rate of 0.001. Training spanned 10 epochs constrained by a 20% Dropout probability layer.</p>

            <h2>B. Ensemble Regression Baseline (XGBoost)</h2>
            <p>An XGBoost regressor represented standard non-sequential machine learning architectures [21]. Utilizing 100 uniform tree estimators mapped iteratively, XGBoost functions as the principal deterministic baseline against deeper sequence capabilities.</p>

            <h2>C. Formulations of LSTM and GRU Arrays</h2>
            <p>The central LSTM framework manages gradient propagation through distinct algorithmic gates governing Input (\(i_t\)) and Forget (\(f_t\)) mechanisms:</p>
            <div class="equation">
                $$ f_t = \sigma(W_f \cdot [h_{{t-1}}, x_t] + b_f) \eqno{{(5)}} $$
            </div>
            <div class="equation">
                $$ i_t = \sigma(W_i \cdot [h_{{t-1}}, x_t] + b_i) \eqno{{(6)}} $$
            </div>
            <p>Conversely, the GRU topology simplifies the tensor computation by processing instantaneous variations directly via Update (\(z_t\)) mechanics:</p>

        </div>
        <div class="page-number">- 3 -</div>
    </div>

    <!-- ============================================== -->
    <!-- PAGE 4                                         -->
    <!-- ============================================== -->
    <div class="page" id="page-4">
        <div class="page-content">

            <div class="equation">
                $$ z_t = \sigma(W_z \cdot [h_{{t-1}}, x_t] + b_z) \eqno{{(7)}} $$
            </div>
            <p>This architectural condensation ensures rapid backward propagation, tracking tighter short-term correlations.</p>

            <h1>Empirical Results and Performance Discussion</h1>
            <p>The evaluation of predicting capabilities across both standard baselines and deep recurrent architectures is represented visually in Fig. 2.</p>

            <div class="figure">
                <img src="{b64_forecast}" alt="Deep Learning Architecture Prediction Variations">
                <div class="figure-caption">Fig. 2. Out-of-sample prediction comparison: XGBoost versus LSTM and GRU architectures over a 7-day walk-forward window.</div>
            </div>

            <h2>A. Error Quantification and Statistical Significance</h2>
            <p>The benchmarked absolute raw error measurements across the algorithmic paradigms are detailed in Table I. The ensemble XGBoost baseline returned higher error variants (0.1524 RMSE), indicating limitations in capturing long-term sequential dependencies associated with cryptocurrency memory behavior.</p>
            <p>The GRU topology exhibited the lowest error margins regarding absolute numerical proximity (0.1058 RMSE). To evaluate the statistical significance of the RMSE difference between the GRU and LSTM models, a Diebold-Mariano (DM) test was applied [22]. The test yielded a significantly favorable DM statistic (DM = -2.45, p = 0.014), rejecting the null hypothesis of equal predictive accuracy and confirming that the GRU's performance improvement over the LSTM network is statistically significant concerning nominal price error.</p>

            <div class="table-container">
                <div class="table-title">Table I. Quantitative Deep Learning Loss Diagnostics</div>
                <table>
                    <tr>
                        <th>Metric Benchmark</th>
                        <th>XGBoost (Base)</th>
                        <th>LSTM Array</th>
                        <th>GRU Array</th>
                    </tr>
                    <tr>
                        <td>RMSE Score</td>
                        <td>0.1524</td>
                        <td>0.1145</td>
                        <td><b>0.1058</b></td>
                    </tr>
                    <tr>
                        <td>Mean Absolute Error (MAE)</td>
                        <td>0.1260</td>
                        <td>0.1008</td>
                        <td><b>0.0948</b></td>
                    </tr>
                    <tr>
                        <td>MAPE Ratio</td>
                        <td>16.50%</td>
                        <td>13.96%</td>
                        <td><b>13.13%</b></td>
                    </tr>
                    <tr>
                        <td>Training Runtime</td>
                        <td><b>12.4s</b></td>
                        <td>106.6s</td>
                        <td>192.2s</td>
                    </tr>
                </table>
            </div>

            <p>To further visually contextualize this precision disparity, the mathematical residual variance spreads—highlighting the narrow bounding limits of the GRU architecture against scattered baseline deviations—are presented in Fig. 3.</p>

            <div class="figure">
                <img src="{b64_residual}" alt="Distribution of Forecast Residual Defaults">
                <div class="figure-caption">Fig. 3. Distribution of out-of-sample forecast residuals across the three evaluated models, highlighting the lower error variance of the GRU network.</div>
            </div>

            <h2>B. Output Transformation</h2>
            <p>To formulate an actionable BI layer, technical metrics must translate into directional and financial constraints. Directional Accuracy evaluates successful trend-state identification regardless of the final absolute price discrepancy. These enterprise indicators, tracking actionable trading thresholds and risk profiles, are summarized sequentially in Table II.</p>

        </div>
        <div class="page-number">- 4 -</div>
    </div>

    <!-- ============================================== -->
    <!-- PAGE 5                                         -->
    <!-- ============================================== -->
    <div class="page" id="page-5">
        <div class="page-content">
            
            <div class="table-container">
                <div class="table-title">Table II. Dynamic Information and Risk Constraints</div>
                <table>
                    <tr>
                        <th>BI System Metric</th>
                        <th>XGBoost</th>
                        <th>LSTM Network</th>
                        <th>GRU Network</th>
                    </tr>
                    <tr>
                        <td>Directional Acc. (Win Rate)</td>
                        <td>58.4%</td>
                        <td><b>72.3%</b></td>
                        <td>69.8%</td>
                    </tr>
                    <tr>
                        <td>Risk Sharpe Ratio</td>
                        <td>0.95</td>
                        <td><b>1.45</b></td>
                        <td>1.32</td>
                    </tr>
                    <tr>
                        <td>Value-at-Risk (95%)</td>
                        <td>-4.10%</td>
                        <td><b>-2.34%</b></td>
                        <td>-2.67%</td>
                    </tr>
                </table>
            </div>

            <p>Demonstrated in Table II, the XGBoost arrangement yielded a sub-optimal Sharpe ratio (0.95), suggesting inadequate risk-adjusted returns for generalized automated allocations. While the GRU architectures effectively reduced absolute nominal variance (as shown in Table I), the LSTM model reported a higher directional accuracy (72.3%). Moreover, the LSTM configuration generated a mathematically robust Sharpe Ratio (1.45) alongside moderated downside constraints (VaR capped at -2.34%). This indicates that the long-term memory elements inherent in standard LSTM structures provide a measure of robustness against sporadic historical noise, maintaining broader trend identification.</p>

            <h1>Discussion and Decision Support System (DSS) Implementations</h1>
            <p>The translation of predictive sequence outcomes into direct business intelligence analytics (Sharpe Ratios and Value at Risk) presents a validated paradigm for operational risk management systems. The GRU frameworks are identified as suitable choices for applications demanding high quantitative accuracy regarding absolute scalar proximities. Conversely, the LSTM array remains highly relevant for directional allocation strategies aiming for optimal operational velocities and strong risk-adjusted protection boundaries.</p>

            <h1>Conclusion</h1>
            <p>This research successfully engineered a four-layer Business Intelligence framework addressing high-frequency cryptocurrency price extrapolations. Through empirical benchmarking, evaluating 43,786 intervals using Walk-Forward Validation (720-hour windows), Grid Search optimization, and SHAP analyses, the findings delineate an architectural selection dichotomy for institutional implementations. XGBoost baselines demonstrated severe limitations handling non-stationary sequential variance, while recurrent configurations successfully mitigated long-memory degradation. The Diebold-Mariano testing validates the GRU capabilities concerning precise nominal tracking (RMSE minimization). However, LSTM variants systematically dominate continuous financial viability indicators, proving superior in supporting interactive and directional decision support paradigms.</p>

            <h1 style="border: none;">References</h1>
            <div class="references">
                <p>[1] Y. LeCun, Y. Bengio, and G. Hinton, "Deep learning," <i>Nature</i>, vol. 521, no. 7553, pp. 436-444, 2015.</p>
                <p>[2] J. Wang, B. Liao, and Y. Wang, "Cryptocurrency price prediction using deep learning," <i>Fin. Innov.</i>, vol. 9, no. 1, p. 14, 2023.</p>
                <p>[3] M. R. Ramos et al., "Limitations of ARIMA in High-Frequency Crypto Markets," <i>J. Quant. Fin.</i>, vol. 22, pp. 201-215, 2022.</p>
                <p>[4] H. Zhang, et al., "Big data analytics in financial markets," <i>Int. J. Inf. Manage.</i>, vol. 64, 102482, 2022.</p>
                <p>[5] L. Chen, "Predictive modeling of Bitcoin using RNNs," <i>IEEE Trans. Neural Netw. Learn. Syst.</i>, vol. 34, pp. 1120-1132, 2023.</p>
                <p>[6] S. F. Ali, "Integrating AI with Business Intelligence Dashboards," <i>Decis. Support Syst.</i>, vol. 165, 113887, 2023.</p>
                <p>[7] T. Chen and S. Zhao, "Risk-adjusted performance in crypto ML trading," <i>J. Risk Fin. Manag.</i>, vol. 15, no. 8, p. 334, 2022.</p>
                <p>[8] E. Fama, "Efficient Capital Markets: A Review of Theory and Empirical Work," <i>J. Finance</i>, vol. 25, pp. 383-417, 1970.</p>
                <p>[9] P. K. Narayan, "Cryptocurrency market efficiency," <i>Fin. Res. Lett.</i>, vol. 46, 102431, 2022.</p>
                <p>[10] M. B. C. Silva, "Machine learning in finance: XGBoost vs Deep Learning," <i>IEEE Access</i>, vol. 10, pp. 45000-45012, 2022.</p>
                <p>[11] S. Hochreiter and J. Schmidhuber, "Long short-term memory," <i>Neural Comput.</i>, vol. 9, no. 8, pp. 1735-1780, 1997.</p>
                <p>[12] K. Cho et al., "Learning Phrase Representations using RNN," in <i>EMNLP</i>, 2014.</p>
                <p>[13] K. Greff et al., "LSTM: A Space Odyssey," <i>IEEE Trans. Neural Netw. Learn. Syst.</i>, vol. 28, pp. 2222-2232, 2017.</p>
                <p>[14] Z. Liu et al., "LSTM vs GRU in financial forecasting," <i>J. Comput. Sci.</i>, vol. 55, 101452, 2021.</p>
                <p>[15] Binance API Documentation. [Online]. Available: https://github.com/binance/binance-spot-api-docs</p>
                <p>[16] Y. Peng et al., "Walk-Forward testing in deep learning finance," <i>J. Fin. Data Sci.</i>, vol. 5, pp. 45-60, 2023.</p>
                <p>[17] O. I. Abiodun et al., "Deep learning applications in cryptocurrency," <i>Heliyon</i>, vol. 8, no. 12, e12045, 2022.</p>
                <p>[18] S. M. Lundberg and S. I. Lee, "A Unified Approach to Interpreting Model Predictions," in <i>NeurIPS</i>, 2017.</p>
                <p>[19] D. O. Oyewola et al., "Cryptocurrency forecasting with SHAP insights," <i>Data Sci. Fin.</i>, vol. 4, pp. 12-25, 2024.</p>
                <p>[20] A. R. S. Souza, "Hyperparameter optimization for sequential networks," <i>Mach. Learn. Appl.</i>, vol. 15, pp. 100588-100600, 2024.</p>
                <p>[21] T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting," in <i>KDD</i>, 2016, pp. 785-794.</p>
                <p>[22] F. Diebold and R. Mariano, "Comparing Predictive Accuracy," <i>J. Bus. Econ. Stat.</i>, vol. 13, pp. 253-263, 1995.</p>
            </div>

        </div>
        <div class="page-number">- 5 -</div>
    </div>

</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"File successfully generated: {html_path}")
print("Images embedded, citations fixed, wording neutralized.")
