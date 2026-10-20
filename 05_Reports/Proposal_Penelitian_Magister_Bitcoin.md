# PROPOSAL PENELITIAN MAGISTER INFORMATIKA
## Bidang Fokus: Big Data Analysis & Deep Learning

**Judul Penelitian:**  
**"Implementasi Prediksi Bitcoin dalam Analisis Big Data: Studi Komparatif Arsitektur Deep Learning (LSTM vs GRU) untuk Peramalan High-Frequency"**

**Peneliti:** Asep Surahman Sulaeman  
**Program Studi:** Magister Informatika  

---

### 1. Pendahuluan
Bitcoin merupakan aset kripto dengan volatilitas yang sangat tinggi. Penelitian ini menggunakan pendekatan **Big Data Analysis** untuk membandingkan efektivitas dua arsitektur Deep Learning populer, yaitu **Long Short-Term Memory (LSTM)** dan **Gated Recurrent Unit (GRU)**, dalam mengolah 43.000+ baris data per jam guna menemukan model yang paling akurat dan efisien secara komputasi.

### 2. Rumusan Masalah
1. Bagaimana performa akurasi (RMSE & MAE) antara algoritma LSTM dan GRU dalam memprediksi harga Bitcoin pada skala Big Data?
2. Algoritma mana yang lebih efisien dalam hal waktu komputasi (training time) saat menangani dataset High-Frequency?
3. Bagaimana pengaruh indikator teknikal (RSI, Volatilitas) terhadap stabilitas prediksi kedua model tersebut?

### 3. Metodologi Penelitian (Big Data Pipeline)
Penelitian ini mengikuti alur kerja **Big Data Analytics Lifecycle**:
1.  **Data Ingestion**: Akumulasi data mentah dari API Binance (sudah dilakukan, 43k+ rows).
2.  **Data Preprocessing**: Pembersihan data, penanganan outlier, dan normalisasi (Min-Max Scaling).
3.  **Feature Engineering**: Transformasi data mentah menjadi indikator teknikal (RSI, MACD, Bollinger Bands, Moving Averages).
4.  **Modeling**: Implementasi arsitektur **GRU (Gated Recurrent Unit)** yang dipilih karena efisiensinya dalam menangani sekuens data panjang (Big Data) dengan memori yang lebih rendah dibanding LSTM.
5.  **Evaluation**: Pengujian model menggunakan RMSE, MAE, dan MAPE.

### 4. Kebaruan (Novelty) untuk Level Magister
- Penggunaan **High-Frequency Data (Hourly)** selama 5 tahun untuk menangkap dinamika mikro-pasar.
- Integrasi berbagai fitur teknikal sebagai input multi-dimensi pada model GRU.
- Analisis efisiensi komputasi pada pemrosesan dataset dalam skala puluhan ribu baris.

### 5. Hasil yang Diharapkan
- Model prediktif yang dapat memberikan estimasi harga Bitcoin dengan tingkat error yang rendah.
- Dashboard visualisasi interaktif untuk memonitor tren dan prediksi.
- Laporan komprehensif yang memenuhi syarat kelulusan Magister Informatika.

---
*Dokumen ini dibuat otomatis sebagai kerangka awal penelitian.*
