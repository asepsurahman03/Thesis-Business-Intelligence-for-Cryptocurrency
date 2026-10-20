# BUSINESS INTELLIGENCE FRAMEWORK FOR CRYPTOCURRENCY PREDICTION
## A Comparative Study of LSTM vs GRU Architectures Using Big Data Analytics with Deep Learning Integration

**Peneliti:** Asep Surahman Sulaeman  
**Program:** Magister Informatika — Nusa Putra University  
**Mata Kuliah:** Business Intelligence  
**Tahun:** 2026

---

## 1. JUDUL PENELITIAN (RESMI)

**"Business Intelligence Framework for Cryptocurrency Prediction: A Comparative Study of LSTM vs GRU Architectures Using Big Data Analytics with Deep Learning Integration"**

### Justifikasi Pemilihan Judul

| Komponen Judul | Implementasi dalam Penelitian |
|---|---|
| **Business Intelligence Framework** | Arsitektur BI 4-layer: Data → Analytics → Deep Learning → Dashboard |
| **Cryptocurrency Prediction** | Prediksi harga Bitcoin (BTC/USDT) dengan data 5 tahun |
| **LSTM vs GRU** | Perbandingan komparatif 2 arsitektur gated RNN |
| **Big Data Analytics** | Implementasi 5V Principles: Volume, Velocity, Variety, Veracity, Value |
| **Deep Learning Integration** | Integrasi DL dalam pipeline BI sebagai analytics engine |

---

## 2. BUSINESS INTELLIGENCE FRAMEWORK

### 2.1 Arsitektur BI 4-Layer

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BI FRAMEWORK ARCHITECTURE                         │
├──────────────┬──────────────┬───────────────┬───────────────────────┤
│  LAYER 1     │   LAYER 2    │   LAYER 3     │      LAYER 4          │
│  DATA        │  ANALYTICS   │  DEEP         │   PRESENTATION        │
│  SOURCES     │  ENGINE      │  LEARNING     │   (BI DASHBOARD)      │
├──────────────┼──────────────┼───────────────┼───────────────────────┤
│ • Binance    │ • ETL        │ • LSTM Model  │ • Executive View      │
│   API        │   Pipeline   │   (4 Gates)   │ • KPI Monitoring      │
│ • OHLCV      │ • 5V Big     │ • GRU Model   │ • Trading Signals     │
│   Data       │   Data       │   (2 Gates)   │ • Risk Dashboard      │
│ • Technical  │ • Feature    │ • Comparative │ • Decision Support    │
│   Indicators │   Engineering│   Analysis    │   System (DSS)        │
└──────────────┴──────────────┴───────────────┴───────────────────────┘
```

### 2.2 BI Research Pipeline (5 Phases)

| Phase | Aktivitas | Big Data Dimension | Output |
|---|---|---|---|
| **I. Data Ingestion** | Binance API Mining | **Volume** (43,786 records) | Raw Dataset |
| **II. Preprocessing** | Min-Max Scaling, Chronological Split | **Veracity** | Normalized Data |
| **III. Feature Engineering** | 7 Technical Indicators | **Variety** | Feature Matrix |
| **IV. Deep Learning** | LSTM & GRU Training (10 Epochs) | **Velocity** | Trained Models |
| **V. BI Evaluation** | RMSE, MAE, MAPE + BI KPIs | **Value** | BI Dashboard |

---

## 3. BIG DATA 5V IMPLEMENTATION

### Volume
- Dataset: **43,786 hourly records** Bitcoin BTC/USDT
- Rentang waktu: 5 tahun (2021-2026)
- Features: 7 kolom OHLCV + 15 kolom technical indicators

### Velocity
- Frekuensi data: **Hourly** (high-frequency)
- Simulasi real-time trading environment
- Processing pipeline otomatis

### Variety
- **Raw Features:** Open, High, Low, Close, Volume
- **Technical Indicators:** MA7, MA25, RSI, MACD, Signal Line, Log Returns, Volatility, BB_Mid, BB_Upper, BB_Lower
- **BI Metrics:** Sharpe Ratio, VaR, Win Rate, Profit Factor

### Veracity
- Data cleaning: dropna() setelah feature engineering
- Normalization: Min-Max Scaler [0,1]
- Split: 80% training / 20% testing (chronological)

### Value
- Prediksi harga Bitcoin 24 jam ke depan
- Trading signals: BUY / HOLD / SELL
- Business Decision Support System

---

## 4. MODEL COMPARISON RESULTS

### 4.1 Technical Metrics

| Metric | LSTM | GRU | Winner | Significance |
|---|---|---|---|---|
| RMSE | 0.1145 | **0.1058** | ✅ GRU | Margin kesalahan lebih kecil |
| MAE | 0.1008 | **0.0948** | ✅ GRU | Error absolut lebih rendah |
| MAPE | 13.96% | **13.13%** | ✅ GRU | Persentase error lebih minimal |
| Training Time | **106.6s** | 192.2s | ✅ LSTM | 44% (~85 detik) lebih cepat |
| Parameters | 4 gates | **3 gates** | ✅ GRU | Komputasi lebih presisi dan efisien |

### 4.2 BI Business Metrics

| BI KPI | LSTM | GRU | Benchmark |
|---|---|---|---|
| Directional Accuracy | **72.3%** | 69.8% | >60% (Good) |
| Sharpe Ratio (Est.) | 1.45 | 1.32 | >1.0 (Acceptable) |
| Win Rate | **72.3%** | 69.8% | >65% (Good) |
| VaR (95%) | -2.34% | -2.67% | <-5% (Risk Limit) |

### 4.3 BI Recommendation

```
RECOMMENDATION:
┌─────────────────────────────────────────────────────┐
│ GRU  → Rekomendasi untuk akurasi maksimal           │
│         (Production BI System, Investment Decisions)│
│                                                     │
│ LSTM → Rekomendasi untuk real-time processing cepat │
│         (Lightweight BI, High-Frequency Refresh)    │
└─────────────────────────────────────────────────────┘
```

---

## 5. BI DASHBOARD COMPONENTS

### 5.1 Executive View (Level C-Suite)
- Total Dataset Volume: 43,786 records
- Best Model Accuracy: GRU MAPE 13.13%
- Current Trading Signal: Based on latest prediction
- Portfolio Risk Level: VaR -2.34%

### 5.2 Analyst View (Technical)
- LSTM vs GRU Performance Charts
- RMSE/MAE/MAPE Comparison
- Training Loss Curves (10 Epochs)
- Feature Importance Analysis

### 5.3 Risk Management View
- Value at Risk (VaR 95%): -2.34%
- Conditional VaR (CVaR): -4.12%
- Maximum Drawdown: -8.56%
- Sharpe Ratio: 1.45
- Beta: 1.08

### 5.4 Decision Support View
- 🟢 BUY Signal: RSI < 30 + MACD crossover positif
- 🟡 HOLD Signal: Volatilitas tinggi, Bollinger Bands melebar
- 🔴 SELL Alert: RSI > 70 overbought + prediksi downtrend

---

## 6. MATHEMATICAL FOUNDATIONS (BI Analytics)

### Deep Learning Models

**LSTM Cell Operations:**
- Forget Gate: ft = σ(Wf·[ht-1, xt] + bf)
- Input Gate: it = σ(Wi·[ht-1, xt] + bi)
- Cell State: Ct = ft * Ct-1 + it * C̃t
- Output Gate: ot = σ(Wo·[ht-1, xt] + bo)

**GRU Cell Operations:**
- Update Gate: zt = σ(Wz·[ht-1, xt] + bz)
- Reset Gate: rt = σ(Wr·[ht-1, xt] + br)
- Hidden State: ht = (1-zt) * ht-1 + zt * h̃t

### Financial BI Metrics

**Sharpe Ratio:**
> SR = (Rp - Rf) / σp

**Value at Risk:**
> VaR = μ - z * σ (untuk confidence level tertentu)

**Win Rate:**
> WR = (Jumlah prediksi benar) / (Total prediksi) × 100%

---

## 7. CONTRIBUTION TO BI KNOWLEDGE

### Theoretical Contributions:
1. **Novel BI-ML Framework** — Integrasi unik Business Intelligence dengan Deep Learning untuk cryptocurrency
2. **Comparative BI Analytics** — Metodologi perbandingan sistematis LSTM vs GRU dalam konteks BI
3. **5V Big Data for Finance** — Penerapan prinsip Big Data dalam financial informatics
4. **BI KPI Definition** — Kerangka KPI bisnis untuk evaluasi sistem prediksi aset digital

### Practical Contributions:
1. **Production-Ready BI Dashboard** — Dashboard interaktif siap digunakan investor
2. **Risk Management Tools** — VaR, CVaR, Sharpe Ratio terintegrasi
3. **Automated Trading Signals** — Sistem rekomendasi BUY/HOLD/SELL otomatis
4. **Replicable Pipeline** — Framework dapat direplikasi untuk aset kripto lain

---

## 8. CONCLUSION

Penelitian ini berhasil membangun **Business Intelligence Framework** yang komprehensif untuk prediksi harga Bitcoin menggunakan perbandingan arsitektur deep learning LSTM dan GRU.

**Temuan Utama:**
- **GRU** terbukti unggul secara keseluruhan dalam presisi akurasi teknis prediksi harga (MAPE: 13.13% vs 13.96%)
- **LSTM** jauh lebih efisien dalam hal waktu eksekusi / *training time* (106.6 detik vs 192.2 detik)
- Framework BI 4-layer berhasil mengintegrasikan Big Data, Deep Learning, dan Decision Support
- Sistem menghasilkan trading signals yang dapat digunakan sebagai alat bantu investasi

**Rekomendasi untuk Penelitian Lanjutan:**
- Integrasi sentiment analysis dari media sosial (Twitter, Reddit)
- Implementasi Transformer/BERT untuk time-series prediction
- Real-time deployment dengan Apache Kafka + Apache Spark
- Perluasan ke multi-cryptocurrency portfolio optimization

---

*Dokumen ini adalah bagian dari penelitian Business Intelligence Magister Informatika*  
*Nusa Putra University | 2026 | Asep Surahman Sulaeman*
