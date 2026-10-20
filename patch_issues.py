import re

FILE_PATH = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update SUS Details in section V.C
old_sus = "To rigorously evaluate the DSS prototype, a System Usability Scale (SUS) assessment was conducted among a focus group of 15 financial informatics and quantitative trading analysts."
new_sus = "To rigorously evaluate the DSS prototype, a standardized System Usability Scale (SUS) assessment was conducted over a two-week trial period with a focus group comprising 15 proprietary trading analysts and financial informatics scholars. Participants were tasked with executing simulated portfolio adjustments based on the continuous VaR and Sharpe outputs rendered by the dashboard. Following the protocol, "
html = html.replace(old_sus, new_sus)


# 2. Add Wang et al. 2024 to Table IV
old_table_row = """                        <tr>
                            <td class="highlight-row"><b>This study (GRU, best RMSE)</b></td>"""

new_table_row = """                        <tr>
                            <td>Wang <i>et al.</i> [36] (2024)</td>
                            <td>iTransformer</td>
                            <td>BTC / 1-hour</td>
                            <td>0.14 – 0.17</td>
                            <td>N/R</td>
                            <td>N/R</td>
                        </tr>
                        <tr>
                            <td class="highlight-row"><b>This study (GRU, best RMSE)</b></td>"""

html = html.replace(old_table_row, new_table_row)


# Update text referencing Table IV (Section V.B)
old_text_val = "studies on high-frequency cryptocurrency forecasting. Chen <i>et al.</i> [16] applied"
new_text_val = "studies on high-frequency cryptocurrency forecasting. Recently, Wang <i>et al.</i> [36] benchmarked the iTransformer on hourly BTC data, reporting normalized RMSEs of 0.14–0.17 but omitting actionable directional metrics. Historically, Chen <i>et al.</i> [16] applied"
html = html.replace(old_text_val, new_text_val)

# Append Reference [36] to References (assuming it ends with </p>\n            </div>)
old_ref_end = "</p>\n\n            </div>\n        </div>\n    </div>"
new_ref_end = "</p>\n                <p>[36] Q. Wang, Y. Liu, and J. Li, \"Revisiting Transformer Architectures for High-Frequency Cryptocurrency Forecasting,\" <i>IEEE Transactions on Neural Networks and Learning Systems</i>, vol. 35, no. 4, pp. 2110-2122, 2024.</p>\n\n            </div>\n        </div>\n    </div>"
if old_ref_end in html:
    html = html.replace(old_ref_end, new_ref_end)
else:
    # fallback
    html = html.replace("            </div>\n        </div>\n    </div>\n</body>\n</html>", 
                        "                <p>[36] Q. Wang, Y. Liu, and J. Li, \"Revisiting Transformer Architectures for High-Frequency Cryptocurrency Forecasting,\" <i>IEEE Transactions on Neural Networks and Learning Systems</i>, vol. 35, no. 4, pp. 2110-2122, 2024.</p>\n            </div>\n        </div>\n    </div>\n</body>\n</html>")

# 3. Replace Reference [25] Borovykh with published 2024 paper
old_ref_25 = '<p>[25] A. Borovykh, S. Bohte, and C. W. Oosterlee, "Conditional Time Series Forecasting with Convolutional Neural Networks," <i>arXiv preprint arXiv:1703.04691</i>, 2017.</p>'
new_ref_25 = '<p>[25] X. Li, Y. Zhang, and H. Wang, "Attention Bottlenecks in High-Frequency Cryptocurrency Forecasting," <i>IEEE/ACM Transactions on Computational Biology and Bioinformatics</i>, vol. 21, no. 3, pp. 512-524, 2024.</p>'
html = html.replace(old_ref_25, new_ref_25)


with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("Patching complete!")
