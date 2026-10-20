import re

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Fig. 4 Caption to be honest and highly academic "Proposed Architecture..."
html = html.replace('Fig. 4. Evaluated Microsoft Power BI operational prototype of the proposed Business Intelligence monitoring dashboard. Live data connections map LSTM prediction traces directly into computed directional probability scores and real-time Sharpe Ratio limits for DSS evaluation.',
                    'Fig. 4. Proposed architecture of the Business Intelligence monitoring dashboard. The prototype design maps LSTM prediction traces directly into computed directional probability scores and theoretical Sharpe Ratio limits for DSS evaluation.')

# Replace Fake Reference [27] (Ali - BI Bottleneck) with R. Sharda
html = html.replace('[27] S. F. Ali and M. T. T. Lee, "The Business Intelligence bottleneck in predictive Deep Learning," <i>Int. J. Inf. Manage.</i>, vol. 68, 102555, 2023.',
                    '[27] R. Sharda, D. Delen, and E. Turban, <i>Business Intelligence, Analytics, and Data Science: A Managerial Perspective</i>, 4th ed. Pearson, 2017.')

# Replace Fake Reference [28] (J. He - DSS Bridging ML in Banking) with D. Arnott
html = html.replace('[28] J. He, S. Zhao, and L. Huang, "Decision Support Systems bridging modern machine learning in banking," <i>J. Risk Fin. Manag.</i>, vol. 16, no. 4, p. 288, 2023.',
                    '[28] D. Arnott and G. Pervan, "A critical analysis of decision support systems research revisited: The rise of design science," <i>J. Inf. Technol.</i>, vol. 29, no. 4, pp. 269-293, 2014.')

# Replace Irrelevant Reference [29] (Bengio - Rep Learning) with P. Jorion (Value at Risk)
html = html.replace('[29] Y. Bengio, A. Courville, and P. Vincent, "Representation Learning: A Review and New Perspectives," <i>IEEE Trans. Pattern Anal. Mach. Intell.</i>, vol. 35, no. 8, pp. 1798-1828, 2013.',
                    '[29] P. Jorion, <i>Value at Risk: The New Benchmark for Managing Financial Risk</i>, 3rd ed. New York, NY, USA: McGraw-Hill Education, 2006.')

# Replace Fake Reference [32] (Y. Peng - Walk-Forward in DL Finance) with R. J. Hyndman (Forecasting Textbook)
html = html.replace('[32] Y. Peng et al., "Walk-Forward testing dynamics in deep learning finance," <i>J. Fin. Data Sci.</i>, vol. 5, pp. 45-60, 2023.',
                    '[32] R. J. Hyndman and G. Athanasopoulos, <i>Forecasting: Principles and Practice</i>, 3rd ed. Melbourne, Australia: OTexts, 2021.')

# Replace Irrelevant Reference [37] (Krizhevsky - ImageNet CNN) with J. Bollen (Twitter Mood NLP in Finance)
html = html.replace('[37] A. Krizhevsky, I. Sutskever, and G. E. Hinton, "ImageNet Classification with Deep Convolutional Neural Networks," in <i>Advances in Neural Information Processing Systems</i>, 2012, pp. 1097-1105.',
                    '[37] J. Bollen, H. Mao, and X. Zeng, "Twitter mood predicts the stock market," <i>J. Comput. Sci.</i>, vol. 2, no. 1, pp. 1-8, 2011.')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Manuscript finalized. Replaced all 5 flagged references with hyper-accurate, verifiable classic literature. Adjusted Fig 4 caption.")
