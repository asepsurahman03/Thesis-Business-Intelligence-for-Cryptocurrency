<div align="center">

<img src="https://img.shields.io/badge/Universitas%20Nusa%20Putra-S2%20Magister%20Informatika-8B0000?style=for-the-badge&logoColor=white" alt="Universitas Nusa Putra"/>

# 🔮 Cryptocurrency Price Forecasting with Business Intelligence

### *A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence*

[![IEEE Format](https://img.shields.io/badge/📄%20Format-IEEE%20%2F%20Scopus-8B0000?style=flat-square)](https://ieee.org)
[![Python](https://img.shields.io/badge/🐍%20Python-3.10%2B-3776AB?style=flat-square)](https://python.org)
[![Power BI](https://img.shields.io/badge/📊%20Power%20BI-DirectQuery%201.2s-F2C811?style=flat-square)](https://powerbi.microsoft.com)
[![Walk-Forward](https://img.shields.io/badge/🔄%20Validation-24--Fold%20Walk--Forward-22C55E?style=flat-square)](#)
[![SUS Score](https://img.shields.io/badge/✅%20SUS%20Score-86.4%20Grade%20A%2B-06B6D4?style=flat-square)](#)
[![License](https://img.shields.io/badge/📜%20License-Academic%20Research-purple?style=flat-square)](#)

<br/>

> **Program Magister Teknik Informatika (S2)**
> **Fakultas Ilmu Komputer — Universitas Nusa Putra, Sukabumi**

---

</div>

## 📋 Daftar Isi

| Bagian | Deskripsi |
|--------|-----------|
| [🎯 Tentang Penelitian](#-tentang-penelitian) | Latar belakang & tujuan |
| [👥 Tim Peneliti](#-tim-peneliti--afiliasi) | Penulis & pembimbing |
| [🏗️ Arsitektur 4-Layer](#️-arsitektur-4-layer-pipeline) | Pipeline metodologi |
| [📊 Hasil Eksperimen](#-hasil-eksperimen) | Tabel perbandingan model |
| [💡 Temuan Utama](#-temuan-utama-the-divergence-paradox) | The Divergence Paradox |
| [📂 Struktur Repositori](#-struktur-repositori) | Organisasi file |
| [🚀 Cara Menjalankan](#-cara-menjalankan) | Panduan penggunaan |
| [📜 Sitasi](#-sitasi) | BibTeX |

---

## 🎯 Tentang Penelitian

Penelitian ini mengembangkan **arsitektur deep learning modular 4-layer** untuk peramalan harga Bitcoin (BTC/USDT) yang diintegrasikan dengan **Business Intelligence (BI)** berbasis Microsoft Power BI sebagai *Decision Support System (DSS)* bagi investor kripto.

**❓ Mengapa Penelitian Ini Penting?**

Pasar kripto beroperasi **24/7 tanpa henti**, sangat volatil, dan mengandung pola non-linear yang sulit diprediksi oleh model statistik konvensional. Investor membutuhkan sistem cerdas yang tidak hanya akurat secara statistik, tetapi juga **menghasilkan sinyal keputusan finansial yang dapat diandalkan**.

**🔑 Kata Kunci:**
`Deep Learning` · `GRU` · `LSTM` · `Informer Transformer` · `XGBoost` · `Walk-Forward Validation` · `Business Intelligence` · `Power BI` · `Cryptocurrency` · `Bitcoin` · `Time Series Forecasting`

---

## 👥 Tim Peneliti & Afiliasi

| Peran | Nama | Email | Institusi |
|-------|------|-------|-----------|
| 🎓 **1st Author & Presenter** | Asep Surahman Sulaeman | asep.surahman@nusaputra.ac.id | Master of Informatics, Universitas Nusa Putra |
| 🏛️ **2nd Author & Advisor** | Dr. Deden Witarsyah | deden.witarsyah@nusaputra.ac.id | Master of Informatics, Universitas Nusa Putra |
| 🏛️ **3rd Author & Co-Advisor** | Dr. Aswan Supriyadi Sunge | aswan.sunge@pelitabangsa.ac.id | Dept. of Informatics, Universitas Pelita Bangsa |

---

## 🏗️ Arsitektur 4-Layer Pipeline

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     MODULAR 4-LAYER ARCHITECTURE PIPELINE                    │
├──────────────┬───────────────────┬─────────────────┬────────────────────────┤
│   LAYER 1    │      LAYER 2      │     LAYER 3     │        LAYER 4         │
│ Data Ingestion│Feature Engineering│  Model Training │  Business Intelligence  │
├──────────────┼───────────────────┼─────────────────┼────────────────────────┤
│ • Binance API │ • 15 Indikator   │ • GRU 🏆        │ • Power BI DirectQuery  │
│ • 43,786 brs  │   Teknikal       │ • LSTM          │   (Latensi: 1.2s)      │
│ • OHLCV/jam   │ • EMA, MACD, RSI │ • Informer      │ • Sharpe Ratio DSS      │
│ • SHA-256     │ • Bollinger, ATR │   Transformer   │ • VaR 95% Risk Mgmt     │
│   Checksum    │ • OBV            │ • XGBoost       │ • Sinyal Alokasi 168h   │
│ • ADF Test ✅ │ • Fold-Local     │ 24-Fold WFV     │ • SUS = 86.4 (A+) ✅   │
│               │   Min-Max Norm   │ < 200s CPU      │                         │
└──────────────┴───────────────────┴─────────────────┴────────────────────────┘
```

<details>
<summary><b>🔍 Layer 1 — Data Ingestion & Integrity</b></summary>

- **Sumber Data**: Binance Spot API — BTC/USDT (1 Maret 2021 – 1 Maret 2026)
- **Volume**: **43,786 baris** candlestick per jam (OHLCV)
- **Audit**: Checksum SHA-256 — eliminasi **38 tick volume nol**
- **Uji Stasioneritas**: Augmented Dickey-Fuller (ADF Test) ✅

</details>

<details>
<summary><b>🔍 Layer 2 — Feature Engineering & Zero Temporal Leakage</b></summary>

- **15 Indikator Teknikal Multi-Skala**: EMA (9, 21), MACD, RSI, Bollinger Bands, ATR, OBV
- **Fold-Local Min-Max Normalization** (Persamaan 1): Parameter skala hanya diekstraksi dari **jendela latih lokal 720 jam** — nol kebocoran data masa depan

</details>

<details>
<summary><b>🔍 Layer 3 — Comparative Model Topologies (24-Fold Walk-Forward)</b></summary>

- **Jendela Latih**: 720 jam (30 hari) per fold
- **Jendela Uji**: 168 jam (7 hari) out-of-sample
- **Stride**: Seragam 1,865 candle (~77.7 hari) — total **4,032 jam data uji**
- **Komputasi**: CPU Intel Core i7-1260P — **< 200 detik** tanpa GPU mahal

</details>

<details>
<summary><b>🔍 Layer 4 — Enterprise Business Intelligence & DSS</b></summary>

- **Dashboard**: Microsoft Power BI dengan DirectQuery (latensi 1.2 detik)
- **Sinyal DSS**: Alokasi mingguan berdasarkan proyeksi 168 jam ke depan
- **Metrik Risiko**: Annualized Sharpe Ratio (√8760) + VaR 95%

</details>

---

## 📊 Hasil Eksperimen

### 🎯 Tabel I — Evaluasi Error Statistik (Point Loss) — Rata-rata 24 Fold

| # | Model Arsitektur | Mean RMSE (± SD) | MAE (± SD) | Status |
|:-:|:---|:---:|:---:|:---:|
| 🥇 | **GRU (Proposed)** | **0.1058 ± 0.0034** | **0.0948 ± 0.0028** | 🏆 **Terbaik** |
| 🥈 | **LSTM** | 0.1145 ± 0.0051 | 0.1008 ± 0.0042 | Peringkat 2 |
| 🥉 | **Informer Transformer** | 0.1321 ± 0.0081 | 0.1119 ± 0.0072 | Peringkat 3 |
| 4️⃣ | **XGBoost** | 0.1524 ± 0.0068 | 0.1260 ± 0.0055 | Peringkat 4 |
| — | *ARIMA(1,1,1) Baseline* | 0.1987 ± 0.0112 | 0.1654 ± 0.0094 | Baseline Klasik |
| — | *Naïve Persistence* | 0.2341 ± 0.0145 | 0.1912 ± 0.0120 | Baseline Acuan |

### 💰 Tabel II — Evaluasi Keputusan Finansial & Risiko DSS

| # | Model Arsitektur | Dir. Accuracy | Sharpe Ratio | VaR 95%/jam | Rekomendasi DSS |
|:-:|:---|:---:|:---:|:---:|:---|
| 🥇 | **LSTM** | **57.8% ± 2.1%** | **0.87 ± 0.12** | **-1.18%** | 🏆 **Alokasi Tren Makro** |
| 🥈 | **GRU** | 55.3% ± 2.4% | 0.72 ± 0.15 | -1.32% | Position Sizing & Stop-Loss |
| 🥉 | **Informer** | 53.6% ± 2.8% | 0.54 ± 0.18 | -1.74% | Long-horizon Screening |
| 4️⃣ | **XGBoost** | 51.4% ± 3.1% | 0.31 ± 0.21 | -2.15% | Tabular Non-recurrent |
| — | *Buy-and-Hold Pasif* | 50.0% | 0.58 | -2.48% | Benchmark Statis |

---

## 💡 Temuan Utama: The Divergence Paradox

> **⚠️ The Divergence Paradox** adalah temuan kritis penelitian ini:
>
> Model yang **meminimalkan residual kuadratik** (GRU: RMSE terbaik = **0.1058**) **bukan** model terbaik untuk pengambilan keputusan finansial.
>
> Sebaliknya, **LSTM** — meski RMSE-nya lebih tinggi — unggul signifikan pada:
> - 📈 **Directional Accuracy**: **57.8% ± 2.1%** (tertinggi)
> - 📊 **Annualized Sharpe Ratio**: **0.87 ± 0.12** (tertinggi)
>
> **💡 Implikasi**: Evaluasi model peramalan kripto tidak boleh hanya bergantung pada metrik statistik (RMSE/MAE), tetapi **wajib menggunakan metrik utilitas keputusan finansial** seperti Directional Accuracy dan Sharpe Ratio.

```
STATISTIK vs KEPUTUSAN FINANSIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RMSE Terbaik  → GRU  🥇 (0.1058)
Sharpe Terbaik → LSTM 🥇 (0.87)

        "Akurat ≠ Menguntungkan"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📂 Struktur Repositori

```
Thesis-Business-Intelligence-for-Cryptocurrency/
│
├── 📁 01_Data/
│   ├── btc_5year_hourly_bigdata.csv    # 43,786 baris candlestick/jam Binance Spot
│   └── btc_5year_bigdata.csv           # Data harian historis BTC
│
├── 📁 02_Notebooks/
│   └── *.ipynb                         # Pipeline: training, feature engineering, evaluasi
│
├── 📁 03_Models/
│   └── *.py / weights                  # Arsitektur GRU, LSTM, Informer, XGBoost
│
├── 📁 04_Visualizations/
│   └── *.png, *.svg                    # Plot SHAP, loss curves, walk-forward folds
│
├── 📁 05_Reports/
│   └── *.csv, *.json                   # Log evaluasi metrik 24 fold & uji statistik
│
├── 📁 Dashboard/
│   ├── index.html                      # Dashboard interaktif visualisasi
│   ├── app.js                          # Logika dashboard JavaScript
│   └── assets/                         # Aset visual Power BI
│
├── 📁 Presentasi/
│   ├── presentasi_tesis.html           # 🎯 Deck presentasi akademik (24 Slide interaktif)
│   ├── presentasi_materi_sesi_1.html   # 📚 Slide materi perkuliahan S2 Sesi 01
│   └── logo_nusaputra.png              # Logo resmi Universitas Nusa Putra
│
├── 📁 Tesis/
│   └── Manuscript_IEEE_*.docx          # Manuskrip prosiding IEEE/Scopus — kamera siap
│
├── 📁 Template/                        # Template IEEE & IJAI
├── 📁 Capstone Projects/               # Proyek capstone terkait
├── 📄 .gitignore                       # Filter file sementara & data besar
├── 📄 requirements.txt                 # Dependensi Python
└── 📄 README.md                        # 📖 Dokumentasi ini
```

---

## 🚀 Cara Menjalankan

### 1️⃣ Clone Repositori

```bash
git clone https://github.com/asepsurahman03/Thesis-Business-Intelligence-for-Cryptocurrency.git
cd Thesis-Business-Intelligence-for-Cryptocurrency
```

### 2️⃣ Install Dependensi

```bash
pip install -r requirements.txt
```

### 3️⃣ Buka Presentasi Interaktif

Buka langsung di browser modern (Chrome, Edge, Firefox):

```
Presentasi/presentasi_tesis.html
```

| Tombol | Fungsi |
|--------|--------|
| `→` / `Space` | Slide berikutnya |
| `←` | Slide sebelumnya |
| `F` | Fullscreen mode |
| `N` | Speaker Notes (Catatan Presenter) |
| `G` | Overview Grid (Semua Slide) |
| Slide 17 | 🎮 Live DSS Simulation |
| Slide 24 | ❓ Kuis Interaktif |

### 4️⃣ Jalankan Pipeline Notebook

```bash
cd 02_Notebooks
jupyter notebook
```

---

## 📜 Sitasi

Jika Anda menggunakan kode, metodologi **24-Fold Chronological Walk-Forward**, atau arsitektur **BI-DSS** ini dalam penelitian Anda, mohon sitasi sebagai berikut:

```bibtex
@inproceedings{sulaeman2026cryptoforecasting,
  author    = {Asep Surahman Sulaeman and Deden Witarsyah and Aswan Supriyadi Sunge},
  title     = {A Deep Learning Architecture for Cryptocurrency Price Forecasting
               Utilizing Business Intelligence},
  booktitle = {Proceedings of the International Conference on Informatics and Computing},
  year      = {2026},
  address   = {Sukabumi, Indonesia},
  publisher = {IEEE}
}
```

---

<div align="center">

**⭐ Jika penelitian ini bermanfaat, berikan bintang pada repositori ini! ⭐**

---

*© 2026 Asep Surahman Sulaeman · Universitas Nusa Putra · All Rights Reserved*
*Research conducted under supervision of Dr. Deden Witarsyah & Dr. Aswan Supriyadi Sunge*

[![GitHub](https://img.shields.io/badge/GitHub-asepsurahman03-181717?style=flat-square&logo=github)](https://github.com/asepsurahman03)

</div>
