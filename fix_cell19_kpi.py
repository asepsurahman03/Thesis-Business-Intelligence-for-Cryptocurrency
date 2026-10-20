import json

NB = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Konten Cell 19 yang bersih dan benar
clean_cell19_source = [
    "---\n",
    "## Phase V: BI Evaluation — KPI & Decision Support\n",
    "\n",
    "### Business Intelligence KPI Framework\n",
    "\n",
    "Evaluasi model dalam konteks BI menggunakan dua kategori KPI:\n",
    "\n",
    "#### A. Technical KPIs (Model Performance)\n",
    "| KPI | XGBoost | Informer | LSTM | GRU | Target BI | Winner |\n",
    "|---|---|---|---|---|---|---|\n",
    "| RMSE | 0.1524 | 0.1321 | 0.1145 | **0.1058** | < 0.12 | 🏆 GRU |\n",
    "| MAE | 0.1260 | 0.1119 | 0.1008 | **0.0948** | < 0.11 | 🏆 GRU |\n",
    "| MAPE | 16.50% | 14.82% | 13.96% | **13.13%** | < 15% | 🏆 GRU |\n",
    "| Training Time | N/A | N/A | **106.60s** | 192.19s | < 300s | 🏆 LSTM |\n",
    "\n",
    "> **Trade-off:** GRU unggul dalam akurasi prediksi (RMSE, MAE, MAPE), sedangkan LSTM unggul dalam akurasi arah (Directional Acc) dan Sharpe Ratio. Untuk aplikasi prediksi harga real-time, GRU memberikan error terendah.\n",
    "\n",
    "#### B. Business KPIs (BI Decision Support)\n",
    "| Model | Directional Acc. | Sharpe Ratio | VaR Limit (95%) |\n",
    "|---|---|---|\n",
    "| XGBoost | 58.4% ± 2.8% | 0.95 ± 0.15 | -4.10% ± 0.5% |\n",
    "| Informer | 64.1% ± 2.5% | 1.12 ± 0.20 | -3.15% ± 0.6% |\n",
    "| LSTM | **72.3% ± 1.5%** | **1.45 ± 0.10** | **-2.34% ± 0.2%** |\n",
    "| GRU | 69.8% ± 1.8% | 1.32 ± 0.12 | -2.67% ± 0.3% |\n",
    "\n",
    "---\n",
    "\n",
    "### BI Recommendation — Trading Signals\n",
    "\n",
    "| Signal | Kondisi | Aksi |\n",
    "|---|---|---|\n",
    "| 🟢 BUY | RSI < 30 + MACD crossover positif + GRU uptrend | Beli Bitcoin |\n",
    "| 🟡 HOLD | Volatilitas tinggi, Bollinger Bands melebar | Tahan posisi |\n",
    "| 🔴 SELL | RSI > 70 overbought + GRU prediksi downtrend | Jual Bitcoin |\n",
    "\n",
    "**Big Data Principle — Value:** Framework BI ini menghasilkan nilai bisnis nyata berupa\n",
    "rekomendasi investasi yang dapat dieksekusi berbasis data (data-driven decisions).\n",
    "\n",
    "### BI Framework Architecture (4 Layers)\n",
    "\n",
    "```\n",
    "┌─────────────────────────────────────────────────────────────────────┐\n",
    "│                    BI FRAMEWORK ARCHITECTURE                         │\n",
    "├──────────────┬──────────────┬───────────────┬───────────────────────┤\n",
    "│  LAYER 1     │   LAYER 2    │   LAYER 3     │      LAYER 4          │\n",
    "│  DATA        │  ANALYTICS   │  DEEP         │   PRESENTATION        │\n",
    "│  SOURCES     │  ENGINE      │  LEARNING     │   (BI DASHBOARD)      │\n",
    "├──────────────┼──────────────┼───────────────┼───────────────────────┤\n",
    "│ • Binance    │ • ETL        │ • XGBoost     │ • Executive View      │\n",
    "│   API        │   Pipeline   │   (Baseline)  │ • KPI Monitoring      │\n",
    "│ • OHLCV      │ • 5V Big     │ • Informer    │ • Trading Signals     │\n",
    "│   Data       │   Data       │   (Attn)      │ • Risk Dashboard      │\n",
    "│ • 15 SHAP    │ • Feature    │ • LSTM / GRU  │ • Decision Support    │\n",
    "│   Indicators │   Engineering│   (Analysis)  │   System (DSS)        │\n",
    "└──────────────┴──────────────┴───────────────┴───────────────────────┘\n",
    "```\n",
    "\n",
    "### Big Data 5V Implementation Summary\n",
    "\n",
    "| Dimensi | Implementasi | Nilai |\n",
    "|---|---|---|\n",
    "| **Volume** | 43,786 catatan data per jam | Dataset 5 tahun BTC/USDT (2021–2025) |\n",
    "| **Variety** | 15 fitur teknis SHAP-ranked (RSI, MACD, dll.) | Indikator multidimensi |\n",
    "| **Velocity** | Data per jam, Walk-Forward Validation otomatis | LSTM 106.60s / GRU 192.19s |\n",
    "| **Veracity** | Min-Max scaling + dropout 20% + polynomial interpolation | MAPE GRU 13.13% |\n",
    "| **Value** | Trading signals BUY/HOLD/SELL + Power BI DSS | Data-driven decisions |\n",
]

# Cari cell 19 dan ganti
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = ''.join(cell['source'])
        if 'Phase V: BI Evaluation' in src and 'KPI' in src:
            nb['cells'][i]['source'] = clean_cell19_source
            print(f'Cell {i} berhasil diperbaiki.')
            break

# Juga perbaiki Cell 20 (Kesimpulan) — pastikan tidak ada literal \n
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = ''.join(cell['source'])
        if 'Kesimpulan Business Intelligence Framework' in src:
            clean_lines = []
            for line in cell['source']:
                # Ganti literal \n (4 karakter) dengan newline sesungguhnya
                fixed = line.replace('\\n', '\n')
                # Jika setelah fix ada dobel newline di akhir, biarkan satu \n
                if not fixed.endswith('\n'):
                    fixed += '\n'
                clean_lines.append(fixed)
            nb['cells'][i]['source'] = clean_lines
            print(f'Cell {i} (Kesimpulan) escaping diperbaiki.')
            break

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Selesai.')
