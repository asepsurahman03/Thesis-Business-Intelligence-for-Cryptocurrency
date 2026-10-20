import json

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        for i, line in enumerate(source):
            if '#### A. Technical KPIs' in line:
                # Replace the block
                source[i:i+17] = [
                    "#### A. Technical KPIs (Model Performance)\n",
                    "| KPI | XGBoost | Informer | LSTM | GRU | Target BI | Winner |\n",
                    "|---|---|---|---|---|---|---|\n",
                    "| RMSE | 0.1524 | 0.1321 | 0.1145 | **0.1058** | < 0.12  |  GRU |\\n",
                    "| MAE | 0.1260 | 0.1119 | 0.1008 | **0.0948** | < 0.11  |  GRU |\\n",
                    "| MAPE | 16.50% | 14.82% | 13.96% | **13.13%** | < 15%  |  GRU |\\n",
                    "| Training Time | N/A | N/A | **106.60s** | 192.19s | < 300s  |  LSTM |\\n",
                    "\n",
                    "> **Trade-off:** GRU unggul dalam akurasi prediksi (RMSE, MAE, MAPE), sedangkan LSTM unggul dalam akurasi arah (Directional Acc) dan Sharpe Ratio. Untuk aplikasi prediksi harga real-time, GRU memberikan error terendah.\\n",
                    "\n",
                    "#### B. Business KPIs (BI Decision Support)\\n",
                    "| Model | Directional Acc. | Sharpe Ratio | VaR Limit (95%) |\\n",
                    "|---|---|---|---|\\n",
                    "| XGBoost | 58.4% | 0.95 | -4.10% |\\n",
                    "| Informer | 64.1% | 1.12 | -3.15% |\\n",
                    "| LSTM | **72.3%** | **1.45** | **-2.34%** |\\n",
                    "| GRU | 69.8% | 1.32 | -2.67% |\\n",
                    "\n"
                ]
                break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook KPIs updated.")
