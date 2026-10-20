# SUITE ARTEFAK CAPSTONE PROJECT & PKM KEMITRAAN
## Program Studi Magister Informatika Konsentrasi Data Science
## Fakultas Teknik, Komputer, dan Desain - Universitas Nusa Putra

Berkas dalam folder ini disusun secara sistematis dan patuh terhadap **Pedoman Capstone Projects.pdf** Universitas Nusa Putra, mengintegrasikan seluruh riset tesis *A Deep Learning Architecture for Cryptocurrency Price Forecasting* serta rencana hilirisasi Pengabdian Kepada Masyarakat (PKM).

---

### DAFTAR DOKUMEN DALAM FOLDER INI:

1. **`Laporan_Capstone_Project_Deep_Learning_Crypto.docx`**
   - Dokumen Word resmi berformat standar pedoman: Ukuran A4, Font Times New Roman 12 pt, Spasi 1.5, Margin Atas & Kiri 4 cm, Bawah & Kanan 3 cm.
   - Memuat lengkap: Cover, Lembar Pengesahan, Ringkasan Eksekutif, BAB I (Pendahuluan), BAB II (Tinjauan Pustaka), BAB III (Metodologi), BAB IV (Hasil & Pembahasan), BAB V (Kesimpulan), Daftar Pustaka IEEE, dan Lampiran.

2. **`Laporan_Capstone_Project_Deep_Learning_Crypto.md`**
   - Versi Markdown lengkap dari Laporan Capstone untuk kemudahan peninjauan kode, version control Git, dan konversi cepat.

3. **`Proposal_PKM_Kemitraan_Aset_Kripto.docx`** & **`.md`**
   - Dokumen rancangan Program Pengabdian Kepada Masyarakat (PKM) Kemitraan bersama Komunitas Trader & UMKM Finansial Digital Sukabumi.
   - Berfungsi sebagai bukti luaran hilirisasi riset nyata, pemenuhan Tridharma Perguruan Tinggi, dan persiapan pengajuan hibah pengabdian (Kemendikbudristek/BIMA atau dana internal universitas).

4. **`Panduan_Presentasi_Sidang_Capstone.md`**
   - Panduan struktur slide per slide (12 slide) untuk presentasi 15 menit sidang capstone project sesuai ketentuan halaman 8 pedoman.

5. **`Pedoman Capstone Projects.pdf`**
   - Dokumen pedoman acuan resmi dari Program Studi Magister Informatika Universitas Nusa Putra.

---

### RINGKASAN DATA & TEMUAN UTAMA PROYEK:
- **Dataset:** 43.786 rekaman hourly OHLCV BTC/USDT (Maret 2021 - Maret 2026) dari Binance Spot API.
- **Model Komparatif:** XGBoost, Informer Transformer, LSTM, GRU.
- **Skema Validasi:** 24-Fold Walk-Forward Validation (Train 720h, Test 168h out-of-sample).
- **Hasil Utama:**
  - *Best Point-Loss:* **GRU** (RMSE = 0.1058 ± 0.0034, MAE = 0.0948, MAPE = 13.13%, Uji DM p = 0.014).
  - *Best Trading Utility:* **LSTM** (Directional Accuracy = 72.3% ± 1.5%, Sharpe Ratio = 1.45 ± 0.10, VaR 95% = -2.34%).
- **Artefak Luaran:** PostgreSQL Data Mart, Microsoft Power BI DirectQuery Live Dashboard, Modul PKM Kemitraan, dan Naskah Publikasi Internasional (IEEE/Scopus).
