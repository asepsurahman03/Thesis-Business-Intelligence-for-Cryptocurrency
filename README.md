# A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence

[![IEEE Standard](https://img.shields.io/badge/Format-IEEE%20%2F%20Scopus-maroon.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![Power BI DirectQuery](https://img.shields.io/badge/Power%20BI-DirectQuery%20(1.2s)-yellow.svg)](#)
[![Validation](https://img.shields.io/badge/Validation-24--Fold%20Walk--Forward-success.svg)](#)
[![Usability](https://img.shields.io/badge/SUS%20Score-86.4%20(Grade%20A%2B)-teal.svg)](#)

Repositori resmi riset tesis Program Magister Teknik Informatika (S2), Fakultas Ilmu Komputer, Universitas Nusa Putra & Universitas Pelita Bangsa:
> **"A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence"**

---

## 👥 Tim Peneliti & Afiliasi

- **1st Author & Presenter**: [Asep Surahman Sulaeman](mailto:asep.surahman@nusaputra.ac.id) — *Master of Informatics, Universitas Nusa Putra, Sukabumi*
- **2nd Author & Advisor**: [Dr. Deden Witarsyah](mailto:deden.witarsyah@nusaputra.ac.id) — *Master of Informatics, Universitas Nusa Putra, Sukabumi*
- **3rd Author & Co-Advisor**: [Dr. Aswan Supriyadi Sunge](mailto:aswan.sunge@pelitabangsa.ac.id) — *Dept. of Informatics, Universitas Pelita Bangsa, Bekasi*

---

## 📌 Ringkasan Eksekutif & 4 Pilar Kontribusi

1. **Modular 4-Layer Architecture Pipeline**:
   - **Layer 1 (Data Ingestion & Integrity)**: Mengonsumsi 43,786 baris lilin per jam (OHLCV) Binance Spot BTC/USDT (1 Maret 2021 – 1 Maret 2026), audit checksum SHA-256 (eliminasi 38 tick volume nol), dan verifikasi Augmented Dickey-Fuller (ADF) untuk stasioneritas.
   - **Layer 2 (Feature Engineering & Zero Temporal Leakage)**: Rekayasa 15 indikator teknikal multiskala (EMA, MACD, RSI, Bollinger Bands, ATR, OBV) dan penerapan **Fold-Local Min-Max Normalization (Persamaan 1)** di mana parameter skala hanya diekstraksi dari jendela latih 720 jam lokal.
   - **Layer 3 (Comparative Model Topologies)**: Pelatihan dan benchmarking 4 topologi arsitektur: **GRU**, **LSTM**, **Informer Transformer** (ProbSparse self-attention), dan **XGBoost** di bawah lingkungan komputasi efisien CPU Intel Core i7-1260P (< 200 detik tanpa GPU mewah).
   - **Layer 4 (Enterprise Business Intelligence & DSS)**: Proyeksi peramalan 168 jam dikonversi menjadi sinyal alokasi mingguan stale-forecast, evaluasi Annualized Sharpe Ratio 24/7 ($\sqrt{8760}$), dan batasan risiko Value at Risk (VaR 95%) yang disajikan via Microsoft Power BI DirectQuery (latensi 1.2 detik).

2. **Strict 24-Fold Chronological Walk-Forward Protocol**:
   - 720 jam (30 hari) jendela latih lokal, 168 jam (7 hari) jendela uji out-of-sample dengan stride seragam 1,865 lilin (~77.7 hari) merata sepanjang 5 tahun (total 4,032 jam data out-of-sample).

3. **Penemuan The Divergence Paradox (Statistical Error vs Decision Utility)**:
   - Model yang meminimalkan residual kuadratik (**GRU: Mean RMSE 0.1058**) bukan pemenang finansial terbaik. Sebaliknya, **LSTM** unggul signifikan pada metrik utilitas trading dengan **Directional Accuracy tertinggi 57.8% ± 2.1%** dan **Annualized Sharpe Ratio tertinggi 0.87 ± 0.12**.

4. **Validasi Adopsi Sistem (System Usability Scale = 86.4)**:
   - Evaluasi kegunaan sistem dengan 15 pakar domain (10 peneliti pascasarjana informatika dan 5 praktisi analis keuangan senior) meraih predikat **Grade A+ ('Excellent')**.

---

## 📊 Hasil Komparasi Eksperimen

### Tabel I: Evaluasi Error Titik (Point Loss) — Rata-rata 24 Fold
| Model Arsitektur | Mean RMSE ($\pm$ SD) | Absolute MAE ($\pm$ SD) | Status Peringkat |
| :--- | :---: | :---: | :---: |
| **GRU (Proposed)** | **0.1058 $\pm$ 0.0034** | **0.0948 $\pm$ 0.0028** | 🏆 **Juara 1 (Terbaik)** |
| **LSTM** | 0.1145 $\pm$ 0.0051 | 0.1008 $\pm$ 0.0042 | Peringkat 2 |
| **Informer** | 0.1321 $\pm$ 0.0081 | 0.1119 $\pm$ 0.0072 | Peringkat 3 |
| **XGBoost** | 0.1524 $\pm$ 0.0068 | 0.1260 $\pm$ 0.0055 | Peringkat 4 |
| *ARIMA(1,1,1) Baseline* | 0.1987 $\pm$ 0.0112 | 0.1654 $\pm$ 0.0094 | Baseline Klasik |
| *Naïve Flat Persistence* | 0.2341 $\pm$ 0.0145 | 0.1912 $\pm$ 0.0120 | Baseline Acuan |

### Tabel II: Evaluasi Keputusan Finansial & Risiko DSS
| Model Arsitektur | Directional Accuracy ($DA\%$) | Annualized Sharpe Ratio | Value at Risk (VaR 95%/jam) | Rekomendasi DSS |
| :--- | :---: | :---: | :---: | :--- |
| **LSTM (Proposed)** | **57.8% $\pm$ 2.1%** | **0.87 $\pm$ 0.12** | **-1.18%** | 🏆 **Alokasi Tren Makro** |
| **GRU** | 55.3% $\pm$ 2.4% | 0.72 $\pm$ 0.15 | -1.32% | Position Sizing & Stop-Loss |
| **Informer** | 53.6% $\pm$ 2.8% | 0.54 $\pm$ 0.18 | -1.74% | Long-horizon screening |
| **XGBoost** | 51.4% $\pm$ 3.1% | 0.31 $\pm$ 0.21 | -2.15% | Tabular non-recurrent |
| *Buy-and-Hold Pasif* | 50.0% | 0.58 | -2.48% | Benchmark Statis |

---

## 📂 Struktur Direktori Repositori

```text
├── 01_Data/
│   ├── btc_5year_hourly_bigdata.csv    # 43,786 baris lilin per jam Binance Spot
│   └── btc_5year_bigdata.csv           # Data harian historis
├── 02_Notebooks/
│   └── *.ipynb                         # Pipeline pelatihan, feature engineering, evaluasi
├── 03_Models/
│   └── *.py / model weights            # Definisi arsitektur GRU, LSTM, Informer, XGBoost
├── 04_Visualizations/
│   └── *.png, *.svg                    # Plot SHAP, loss curves, walk-forward folds
├── 05_Reports/
│   └── *.csv, *.json                   # Log evaluasi metrik 24 fold & uji statistik
├── Dashboard/
│   ├── app.js, index.html              # Prototipe interaktif dashboard visualisasi
│   └── assets/                         # Aset visual pendukung Power BI
├── Presentasi/
│   ├── presentasi_tesis.html           # Deck presentasi akademik interaktif (24 Slide)
│   ├── presentasi_materi_sesi_1.html   # Slide materi perkuliahan S2 Sesi 01
│   └── logo_nusaputra.png              # Logo resmi Universitas Nusa Putra
├── Tesis/
│   └── *.docx, *.pdf                   # Manuskrip prosiding IEEE/Scopus kamera siap
├── .gitignore                          # Filter file sampah & temporary
└── README.md                           # Dokumentasi utama proyek riset
```

---

## 🖥️ Cara Menjalankan Slide Presentasi Interaktif

Buka file `Presentasi/presentasi_tesis.html` langsung di browser modern (Chrome, Edge, Firefox). File ini berformat mandiri (*self-contained single-page application*) dengan fitur:
- ⌨️ Navigasi: Tombol <kbd>→</kbd> / <kbd>Space</kbd> (maju), <kbd>←</kbd> (mundur), <kbd>F</kbd> (fullscreen).
- 📝 Catatan Presenter (*Speaker Notes*): Tekan tombol <kbd>N</kbd> atau klik tombol *Notes*.
- 🗂️ Grid Seluruh Slide (*Overview*): Tekan tombol <kbd>G</kbd> atau klik tombol *Overview*.
- 🎮 Live DSS Simulation: Uji simulasi model secara langsung di Slide 17.
- ❓ Kuis Interaktif: Cek pemahaman audiens/penguji di Slide 24.

---

## 📜 Sitasi & Hak Cipta
Jika Anda menggunakan kode, metodologi 24-Fold Chronological Walk-Forward, atau arsitektur BI-DSS ini dalam penelitian Anda, mohon sitasi:

```bibtex
@inproceedings{sulaeman2026cryptoforcasting,
  author    = {Asep Surahman Sulaeman and Deden Witarsyah and Aswan Supriyadi Sunge},
  title     = {A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence},
  booktitle = {Proceedings of the International Conference on Informatics and Computing},
  year      = {2026},
  address   = {Sukabumi, Indonesia},
  publisher = {IEEE}
}
```
