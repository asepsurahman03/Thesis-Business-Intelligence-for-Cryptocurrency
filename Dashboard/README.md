# CryptoPredict AI | Executive BI DSS Dashboard

### Sistem Pendukung Keputusan Investasi Cryptocurrency Berbasis Deep Learning & Business Intelligence
**Program Studi Magister Informatika Konsentrasi Data Science - Universitas Nusa Putra**

Dashboard ini merupakan artefak teknis interaktif tingkat produksi yang dikembangkan sebagai luaran utama dari **Capstone Project** dan **Tesis Magister**:
*"A Deep Learning Architecture for Cryptocurrency Price Forecasting"*.

---

## 🚀 Fitur Unggulan Dashboard

1. **Executive KPI Cards Real-Time:**
   - **Best Point-Loss (GRU):** RMSE 0.1058 ± 0.0034, MAE 0.0948, MAPE 13.13%.
   - **Best Trading Direction (LSTM):** Directional Accuracy 72.3%, Sharpe Ratio 1.45, VaR 95% -2.34%.
   - **Uji Statistik Inferensial:** Kruskal-Wallis $H = 18.4$ ($p < 0.001$), Diebold-Mariano $p = 0.014$.

2. **Visualisasi Multi-Step Forecast 168 Jam (Out-of-Sample):**
   - Menampilkan lintasan peramalan 7 hari ke depan terhadap harga realisasi bursa Binance Spot.
   - Filter dinamis per model (*Toggle*: GRU, LSTM, Informer Transformer, XGBoost, atau Semua Model).
   - Pemilih Siklus Validasi (*Walk-Forward Fold Selector* dari Fold 1 hingga Fold 24).

3. **Explainable AI (XAI) - Atribusi Fitur SHAP:**
   - Grafik batang horizontal interaktif yang memvisualisasikan pengaruh 15 indikator teknikal.
   - Mengungkapkan peran dominan *Rolling Volatility 24h* dan *MACD Histogram*.

4. **Interactive Risk & Portfolio Engine:**
   - Kalkulator simulasi alokasi modal dan leverage dinamis (1x - 5x).
   - Menghitung secara otomatis ukuran posisi ideal (*position sizing*), batasan *stop-loss* dinamis berbasis deviasi GRU, dan estimasi potensi kerugian harian maksimum (*Value at Risk* 95%).

5. **Live Trading Signals Feed:**
   - Tabel riwayat sinyal *LONG / SHORT / NEUTRAL* beserta tingkat keyakinan (*confidence level*) dan harga eksekusi.

6. **Hilirisasi Riset PKM Kemitraan:**
   - Terintegrasi dengan program pengabdian bersama mitra **Komunitas Trader Ritel & Pelaku UMKM Finansial Sukabumi**.

---

## 💻 Cara Menjalankan Dashboard

Anda memiliki 2 opsi mudah untuk membuka dan menjalankan dashboard ini:

### Opsi 1: Menjalankan Server Python Lokal (Direkomendasikan)
Buka terminal / PowerShell di root proyek dan jalankan:
```bash
py -3 Dashboard/server.py
```
Server akan aktif di `http://localhost:8050` dan browser Anda akan otomatis terbuka.

### Opsi 2: Buka Langsung File HTML di Browser
Cukup buka berkas berikut di browser apa saja (Google Chrome, Microsoft Edge, Mozilla Firefox):
`Dashboard/index.html`

---

## 📁 Struktur Berkas

```
Dashboard/
├── index.html        # Antarmuka web semantik modern dengan komponen interaktif
├── style.css         # Desain glassmorphism gelap modern, Outfit & Inter typography
├── app.js            # Engine visualisasi Chart.js, simulasi data 168h, dan kalkulator risiko
├── server.py         # Web server Python ringan + REST API endpoints (/api/kpi, /api/models)
└── README.md         # Dokumentasi panduan teknis
```
