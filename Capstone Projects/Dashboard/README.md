# CryptoPredict AI — DSS Dashboard

### Sistem Pendukung Keputusan Investasi Cryptocurrency Berbasis Deep Learning
**Magister Informatika Konsentrasi Data Science — Universitas Nusa Putra**

> Artefak teknis interaktif sebagai luaran utama **Capstone Project** & **Tesis Magister**:
> *"A Deep Learning Architecture for Cryptocurrency Price Forecasting:*
> *GRU vs LSTM vs Informer vs XGBoost pada Data BTC/USDT Binance 2021–2026"*

---

## Fitur Dashboard (6 Halaman)

| Halaman | Deskripsi |
|---------|-----------|
| **Overview** | KPI real-time, grafik harga historis BTC + SMA, RSI-14, volume |
| **Prediksi AI** | Inferensi langsung GRU/LSTM/Informer/XGBoost, CI 95%, tabel timestep |
| **Benchmark Model** | Tabel komparasi RMSE/MAE/MAPE/DA/Sharpe, Walk-Forward Chart, Radar |
| **Manajemen Risiko** | VaR/CVaR, distribusi return, drawdown chart, kalkulator posisi |
| **Explainability** | SHAP horizontal bar, donat kategori fitur, tabel 15 fitur teknikal |
| **Metodologi** | Arsitektur sistem 4-layer, spesifikasi dataset & model, info PKM |

---

## Cara Menjalankan

### Opsi 1: Double-click (Windows) — Paling Mudah
`
run_dashboard.bat
`
Script akan otomatis install dependensi dan membuka browser ke http://localhost:8051

### Opsi 2: Manual via Terminal
`ash
pip install -r requirements.txt
python api_server.py
`
Buka browser ke: http://localhost:8051

### Opsi 3: Buka HTML langsung (mode offline / mock data)
`
index.html
`
Semua grafik akan menggunakan data simulasi tanpa server.

---

## Hasil Penelitian (Performa Model)

| Model | RMSE | MAE | MAPE | Dir. Acc | Sharpe | Keterangan |
|-------|------|-----|------|----------|--------|------------|
| **GRU** | **0.1058** | **0.0948** | **13.13%** | 69.8% | 1.32 | 🥇 Best Point-Loss |
| **LSTM** | 0.1145 | 0.1008 | 13.96% | **72.3%** | **1.45** | 🥈 Best Trading Utility |
| Informer | 0.1321 | 0.1119 | 14.82% | 64.1% | 1.12 | Transformer baseline |
| XGBoost | 0.1524 | 0.1260 | 16.50% | 58.4% | 0.95 | ML baseline |

**Uji Statistik:** Kruskal-Wallis H=18.4 (p<0.001), Diebold-Mariano p=0.014

---

## Struktur File

`
Dashboard/
├── index.html          # UI dashboard (6 halaman, Chart.js 4)
├── style.css           # Desain dark premium, Inter + JetBrains Mono
├── app.js              # JavaScript controller (navigasi, chart, API)
├── api_server.py       # Flask REST API + model PyTorch (port 8051)
├── server.py           # Lightweight HTTP server alternatif (port 8050)
├── requirements.txt    # Dependensi Python
├── run_dashboard.bat   # Launcher Windows (double-click)
└── README.md           # Dokumentasi ini
`

---

## Endpoint API (Flask — port 8051)

| Endpoint | Deskripsi |
|----------|-----------|
| GET / | Serve index.html |
| GET /api/status | Cek status server & mode (real/mock) |
| GET /api/kpi | KPI metrics semua model |
| GET /api/history?period=7d|30d|90d|180d|1y | Data historis OHLCV+indikator |
| GET /api/predict?model=GRU&steps=24 | Inferensi prediksi AI |
| GET /api/walkforward | Data walk-forward validation |
| GET /api/risk | Metrik risiko (VaR, CVaR, Drawdown, Sharpe) |
| GET /api/shap | SHAP feature importance values |
| GET /api/features | Daftar 15 fitur teknikal |
| GET /api/signals | Riwayat trading signals |

---

## Luaran PKM Kemitraan

Dashboard ini merupakan bagian dari program **Pengabdian Kepada Masyarakat (PKM)** bersama:
- 🤝 **Mitra 1:** Komunitas Trader Kripto Ritel Sukabumi
- 🤝 **Mitra 2:** UMKM Berbasis Ekonomi Digital

Tujuan: meningkatkan literasi risiko finansial berbasis AI melalui workshop dan akses terbuka ke sistem DSS.

---

*Dikembangkan oleh: Asep Muhamad Samsudin | NIM: 222510793*
*Pembimbing: Prof. Dr. Hj. Rina Fiati, ST., M.Cs | Dr. Wahyudi Agustiono, S.T., M.Kom*
*Program Studi Magister Informatika | Universitas Nusa Putra | 2026*
