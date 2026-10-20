# PANDUAN DAN STRUKTUR SLIDE PRESENTASI SIDANG CAPSTONE PROJECT
## SESUAI PEDOMAN CAPSTONE PROJECTS UNIVERSITAS NUSA PUTRA (HALAMAN 8)
### Alokasi Waktu: 15 Menit Presentasi + 15 Menit Tanya Jawab

---

### SLIDE 1: JUDUL DAN IDENTITAS PROYEK
- **Judul:** Arsitektur Deep Learning untuk Prediksi Harga Cryptocurrency: Sistem Pendukung Keputusan Investasi Berbasis Business Intelligence
- **Identitas Mahasiswa:** Asep Muhamad Samsudin (NIM. 222510793)
- **Program Studi:** Magister Informatika - Konsentrasi Data Science
- **Dosen Pembimbing:** Prof. Dr. Hj. Rina Fiati, ST., M.Cs & Dr. Wahyudi Agustiono, S.T., M.Kom
- **Institusi:** Universitas Nusa Putra

### SLIDE 2: LATAR BELAKANG DAN URGENSI MASALAH
- Pasar Kripto beroperasi 24/7 dengan kapitalisasi > USD 2 Triliun, sarat volatilitas ekstrem (contoh: crash Terra-Luna Mei 2022).
- Masalah: Investor ritel & manajer investasi menghadapi kerugian akibat tidak adanya sistem prediktif yang dilengkapi manajemen risiko kuantitatif (Sharpe, VaR).
- Solusi: Membangun Decision Support System (DSS) 4 lapis yang mengintegrasikan Deep Learning canggih dengan Power BI Dashboard real-time.

### SLIDE 3: TUJUAN DAN BATASAN PROYEK
- Tujuan: Mengembangkan pipeline end-to-end, menguji model komparatif (GRU, LSTM, Informer, XGBoost), memvalidasi secara statistik, dan memvisualisasikan ke Power BI.
- Batasan: Pasangan BTC/USDT di Binance Spot API, granularitas 1 jam (43.786 data points, 2021-2026), 15 indikator teknikal, horizon prediksi 168 jam (7 hari).

### SLIDE 4: METODOLOGI & ARSITEKTUR SISTEM (FOUR-LAYER DSS)
- Diagram Alir 4 Lapis:
  1. Layer 1: Ingesti Data Otomatis via Binance REST API ke PostgreSQL.
  2. Layer 2: Rekayasa 15 Fitur Teknikal & Fold-Local Normalization (bebas data leakage).
  3. Layer 3: Pemodelan Deep Learning & Financial Risk Engine (Sharpe Ratio, VaR 95%, Sinyal Posisi).
  4. Layer 4: PostgreSQL Data Mart & Visualisasi Live Power BI via DirectQuery.

### SLIDE 5: PROTOKOL VALIDASI BERJALAN (24-FOLD WALK-FORWARD)
- Mengapa Walk-Forward? Menghindari look-ahead bias yang sering terjadi pada train-test split statis.
- Konfigurasi per Fold: 720 Jam Pelatihan (30 hari) -> 168 Jam Uji Out-of-sample (7 hari).
- Dilakukan berulang sebanyak 24 siklus fold tanpa jeda waktu.

### SLIDE 6: HASIL EVALUASI MODEL (POINT-LOSS BENCHMARK)
- Tabel Perbandingan 4 Model:
  - **GRU (Terbaik Loss):** RMSE = 0.1058 ± 0.0034 | MAE = 0.0948 ± 0.0028 | MAPE = 13.13%
  - LSTM: RMSE = 0.1145 ± 0.0051 | MAE = 0.1008 | MAPE = 13.96%
  - Informer: RMSE = 0.1321 ± 0.0081 | MAE = 0.1119 | MAPE = 14.82%
  - XGBoost: RMSE = 0.1524 ± 0.0068 | MAE = 0.1260 | MAPE = 16.50%
- Signifikansi: Uji Kruskal-Wallis H=18.4 (p < 0.001) dan Diebold-Mariano test p=0.014 mengonfirmasi GRU unggul signifikan.

### SLIDE 7: HASIL UTILITAS FINANSIAL & MANAJEMEN RISIKO
- Analisis Utility Finansial:
  - **LSTM (Terbaik Finansial):** Directional Accuracy = **72.3%** | Sharpe Ratio = **1.45** | VaR 95% = **-2.34%** | Max Drawdown = -8.9%
  - GRU: Directional Accuracy = 69.8% | Sharpe Ratio = 1.32 | VaR 95% = -2.70%
- Insight Kunci: LSTM lebih unggul dalam menjaga tren arah (memori jangka panjang), sehingga menghasilkan profitabilitas strategi trading lebih stabil.

### SLIDE 8: INTERPRETABILITAS FITUR (SHAP EXPLAINABILITY)
- Membuka kotak hitam deep learning dengan SHAP:
  - Fitur #1: Rolling Standard Deviation (deteksi pergantian rezim volatilitas pasar).
  - Fitur #2: MACD Histogram (akselerasi momentum harga).
  - Fitur #3: Average True Range (ATR 14).
  - Fitur #4: Relative Strength Index (RSI 14).

### SLIDE 9: DEMONSTRASI DASHBOARD BUSINESS INTELLIGENCE (POWER BI)
- Tampilkan tangkapan layar (screenshot) Live Dashboard Power BI:
  - Kartu KPI Eksekutif: Sharpe Ratio live, batas risiko VaR 95%, Directional Accuracy.
  - Grafik Multi-Step Forecast 168 jam terhadap harga realisasi bursa.
  - Sinyal Trading Eksekusi (Long/Short) dan Matriks Korelasi Indikator.

### SLIDE 10: RENCANA HILIRISASI: PROGRAM KEMITRAAN MASYARAKAT (PKM)
- Menjawab Luaran Pengabdian Masyarakat:
  - Mitra: Komunitas Trader Ritel & Pelaku UMKM Finansial Sukabumi.
  - Masalah: Kerugian modal akibat minimnya pemahaman risiko dan jebakan FOMO.
  - Aksi Nyata: Workshop edukasi literasi risiko AI, pemberian akses dashboard Power BI, dan penyusunan SOP trading terukur.
  - Target Luaran PKM: Buku Panduan ber-ISBN, HKI Modul, dan Publikasi di Jurnal SINTA Abdimas.

### SLIDE 11: KESIMPULAN DAN REKOMENDASI PENGEMBANGAN
- Kesimpulan: Model GRU terbukti terbaik untuk estimasi volatilitas nominal, sedangkan LSTM terbaik untuk arah sinyal trading; arsitektur hibrid direkomendasikan untuk implementasi institusional.
- Rekomendasi: Penambahan sentimen NLP berita finansial (FinBERT) dan integrasi on-chain blockchain.
- Publikasi Ilmiah: Naskah disubmit ke jurnal internasional terindeks IEEE/Scopus.

### SLIDE 12: SESI TANYA JAWAB (Q&A)
- Ucapan terima kasih kepada Dewan Penguji dan Dosen Pembimbing.
- Kesiapan mendemonstrasikan kode program dan dashboard Power BI.
