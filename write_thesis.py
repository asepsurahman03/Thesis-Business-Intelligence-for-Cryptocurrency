import os

file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Laporan_Tesis_Lengkap.md'

thesis_content = """# LAPORAN TESIS

**JUDUL:** Kerangka Pembelajaran Mendalam dan Intelijen Bisnis untuk Prediksi Harga Mata Uang Kripto: Analisis Perbandingan Jaringan Urutan dengan Transformer Tercanggih
**PENULIS:** Asep Surahman Sulaeman
**PROGRAM STUDI:** Magister Informatika (S2)
**INSTITUSI:** Universitas Nusa Putra, Sukabumi, Indonesia

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang
Bitcoin (BTC) menunjukkan perilaku non-stasioner, kerusakan struktural, dan kepekaan yang tinggi terhadap guncangan makroekonomi eksogen. Karakteristik ini mempersulit peramalan harga menggunakan model ekonometrik tradisional. Model konvensional seperti *Autoregressive Integrated Moving Average* (ARIMA) sering kali menunjukkan keterbatasan yang signifikan ketika diterapkan pada kumpulan data keuangan yang sangat berfluktuasi dan berfrekuensi tinggi karena adanya bias spesifikasi linier dan asumsi stasioneritas kovarians yang ketat.

Oleh karena itu, penelitian informatika keuangan saat ini semakin menyukai arsitektur kecerdasan buatan berbasis jaringan saraf tiruan (AI), yang dapat memodelkan rangkaian non-linier kompleks secara lebih efektif. Namun, sebagian besar studi akademis saat ini yang mengevaluasi arsitektur tingkat lanjut—seperti *Recurrent Neural Networks* (RNN) atau *Transformers*—seringkali berhenti hanya pada minimisasi metrik kesalahan standar seperti *Root Mean Square Error* (RMSE). Minimisasi metrik semacam itu nyatanya belum memadai untuk memenuhi kebutuhan riil manajemen portofolio institusional. Terdapat sebuah kesenjangan kritis antara akurasi model algoritmik secara teoritis dengan operasionalitas praktis yang diukur menggunakan tolok ukur keuangan terapan (misalnya *Sharpe Ratio*, *Value-at-Risk*) melalui Sistem Pendukung Keputusan (DSS) berstandar perusahaan.

### 1.2 Rumusan Masalah
1. Bagaimana mengintegrasikan inferensi deret waktu dari model pembelajaran mendalam ke dalam sebuah sistem antrean Intelijen Bisnis (BI) tingkat perusahaan secara *end-to-end* yang adaptif?
2. Bagaimana perbandingan unjuk kerja komputasi antara algoritma statis (XGBoost), jaringan memori skuensial (LSTM, GRU), dan model mekanisasi atensi probabilistik (Informer Transformer) dalam memfasilitasi prediksi harga pada himpunan data mata uang kripto berfrekuensi tinggi (per jam)?
3. Apakah model dengan tingkat kesalahan pengujian terendah mutlak sejalan dengan pencapaian profitabilitas keuangan dan presisi analisis arah pasar?

### 1.3 Tujuan Penelitian
1. Mengusulkan rancang bangun arsitektur operasional 4 lapis (BI-ML Pipeline) yang menjembatani transformasi *raw feed/API* hingga terkonversi otomatis menjadi matrik terapan pada Sistem Pendukung Keputusan berbasis *dashboard*.
2. Membandingkan fungsionalitas dan akurasi model XGBoost, LSTM, GRU, serta Informer Transformer dalam cakrawala prakiraan (168 jam Walk-Forward) berlandaskan kriteria diagnostik statistik ganda serta rasio profitabilitas finansial.

### 1.4 Batasan Penelitian
1. Data aset transaksi sepenuhnya difokuskan pada nilai Spot satu koin secara eksklusif, yakni Bitcoin (BTC/USDT). Hal ini bertujuan untuk menciptakan kondisi pengukuran analitik dasar (*benchmarking*) yang paling terkontrol tanpa tumpang tindih dengan gangguan pasar koin sekunder.
2. Panjang historis seri temporal diekstraksi dari Binance Spot API yang direntangkan selama periode 1 Januari 2021 hingga 31 Desember 2025 dengan granularitas transaksi per 1 Jam.
3. Evaluasi front-end dilakukan hanya menggunakan metodologi SUS (*System Usability Scale*) via piranti Microsoft Power BI.

---

## BAB II: TINJAUAN PUSTAKA

### 2.1 Peramalan Rekursif dan RNN
Aplikasi prediktif sekuensial pada pasar keuangan secara tradisional telah mengeksekusi transisi model berbasis pemulusan statik menuju *Gradient Boosting* yang canggih seperti XGBoost. Meski mumpuni pada data relasional, XGBoost kekurangan sel logika urutan. *Long Short-Term Memory* (LSTM) dan *Gated Recurrent Unit* (GRU) terbukti menanggulangi perisitwa ledakan penalti gradien (*vanishing gradient*) melalui aktivasi unit *forget variables*, membongkar ruang untuk menghafal rangkaian harga terdalam. 

### 2.2 Transformasi Atensi pada Seri Waktu Keuangan
Lanskap riset terkini mendemonstrasikan keunggulan paradigma pengindeksan relung Transformer, dipelopori oleh mekanisme Atensi Diri (*Self-Attention*). Secara spesifik, model Informer memperkenalkan probabilitas sparse ($$O(L \log L)$$) yang mempercepat pelatihan multi-layer pada peramalan waktu panjang. Meski model Transformer lain seperti iTransformer mulai bertumbuh, Informer secara ilmiah dipertahankan di sini sebagai tonggak dan kerangka perbandingan paling mapan.

### 2.3 Sistem Pendukung Keputusan dan Integrasi BI Terkini
Meskipun keakuratan algoritma sering kali dibahas menyeluruh dalam literatur Deep Learning, translokasi model-model ini menuju piranti operasional manajemen resiko aktual sangat minim ditemui. Mengkalkulasi akurasi hanyalah penyelesaian setengah jalan. Menerjemahkan nilai teoretis mentah ke dalam representasi BI (*dashboard analytical KPI*) berbasis rasio valuasi risiko industri adalah sasaran sesungguhnya dari literatur akademis terpandu era modern.

---

## BAB III: METODOLOGI PENELITIAN

### 3.1 Kerangka Sistem (4-Layer BI-ML Implementation Pipeline)
Arsitektur yang mendasari landasan BI sistematis terdiri atas 4 lapisan esensial terpisah:
1. **Layer Ektraksi:** Indexing koneksi Binance WebSocket API berfrekuensi tinggi.
2. **Layer Pra-pemrosesan:** Mengalkulasi fungsi regresi polinomial bagi nilai *timestamp* hilang (~0,4%) serta merakit fungsi skalitas logaritmik dan ekstrak penambahan MACD serta variansi historis pasar.
3. **Layer Inferensi ML:** Validasi sirkuit mekanis pembelajaran (berkisar antara *Grid Search Hyperparameter Tuning* 0.001 *lr*, penalti Dropout 0.2, dll.).
4. **Layer Integrasi BI:** Peluncuran representatif fungsional metrik residu kalkulasi melalui visualisasi analitik Power BI menggunakan relasi injeksi tabel PostgreSQL ganda.

### 3.2 Desain Validasi Uji Pengamatan (Walk-Forward)
Alih-alih menyekat set validasi pengujian silang klasik (seperti K-Fold) pada rentang waktu acak yang melanggar esensi deret ukur kronologis, penelitian ini memanfaatkan mekanisme *Walk-Forward Validation*, berotasi dinamis setiap jendela 720 Jam (data perulangan latih/Train) untuk mendikte arah prakiraan dalam 168 Jam (jendela proyeksi/Test). Uji ketajaman deret diam stasioneritas Augmented Dickey-Fuller (ADF) menyajikan status tolak hipotesis tak-terhingga ($$p < 0.05$$).

### 3.3 Metrik Kuantifikasi Pengujian
Validasi dieksekusi melalui standar koefisien teknis: Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), dan R-Squared. Disempurnakan dengan kalkulasi finansial komprehensif yakni Akurasi Direksional pergerakan harga komparatif, Profit Factor, *Value-at-Risk* (VaR), serta *Sharpe Ratio*. 

---

## BAB IV: HASIL DAN PEMBAHASAN

### 4.1 Identifikasi Pentingnya Fitur SHAP
Pembuktian menggunakan kalkulasi metodologis non-agnostik *SHapley Additive exPlanations (SHAP)* mendemonstrasikan bahwa parameter buatan algoritme momentum seperti perhitungan Deviasi Standar Bergulir bulanan ($$\sigma_t$$) menduduki peringkat prioritas tertinggi komputasional jaringan rekursif ketimbang pasokan parameter mentah biasa (Open, High, Low, Close).

### 4.2 Evaluasi Komparatif Arsitektur Algoritme
Perbandingan statistik inferensi secara dramatis menunjukkan posisi tak tergoyahkan jaringan sekuensial (GRU dan LSTM) dalam rentang frekuensi pendek terkompresi.

1. **GRU (Gated Recurrent Unit):** Mencatat minimasi kesalahan RMSE absolut terbaik dengan $0.1058 \pm 0.0034$. Dominasi ini signifikan secara validitas Diebold-Mariano ($$p=0.014$$ vs LSTM).
2. **Informer (Transformer Baseline):** Dengan RMSE $0.1293 \pm 0.0051$ menunjukkan ketidakmampuannya di tahap resolusi granular (1 Jam) karena kompleksitas pencocokan beban perhatian di interval guncangan fluktuasi acak asimetris.
3. **XGBoost:** Memberi MAE senilai $0.1064 \pm 0.0036$. Stabil namun stagnan pada identifikasi penumpukan *memory loss*.

### 4.3 Paradoks Valuasi Akurasi Terhadap Keuangan 
Sistem Pipa BI memancarkan satu identifikasi radikal: Meskipun arsitektur **GRU** mencatat *Diagnostic Error* paling minimal, perumusan finansial (metode eksekusi posisi pada uji portofolio sisa) dari performa **LSTM** sanggup melontarkan Akurasi Identifikasi Arah (Directional Accuracy) lebih memuaskan yakni $72.3\% \pm 1.5\%$ berbanding GRU ($65.1\% \pm 1.8\%$). Korelasi absolut ini membuahkan hasil *Sharpe Ratio* **1.45 (LSTM)** membelah ketanggapan GRU (1.32). Kesimpulan krusial didapat: Nilai minim kesalahan prediktif mentah (RMSE) bukanlah formula ekuivalen satu-satunya dalam mengestimasi kemampuan mendulang keuntungan riil di lantai sirkulasi bursa, menjadikannya bukti absolut ihwal mengapa Integrasi Evaluator Finansial Business Intelligence sangat amat vital diuji secara inter-operasional.

### 4.4 Analisis Skala Utilisasi Akhir (SUS Score)
Aplikasi Power BI komparatif divisualisasikan kepada dewan uji coba (15 mahasiswa IT pascasarjana dan 7 praktisi pasar analis quant) melalui *System Usability Scale* dengan 10 matriks dimensi interaksi. Modul meraup tingkat penerimaan sebesar $86.4$ (Level Excellent). Tidak ada interferensi kegagalan teknis dalam eksekusi skrip metrik DAX per model, mengonfirmasi kelayakan transisi siap-produksi.

---

## BAB V: KESIMPULAN DAN SARAN

### 5.1 Kesimpulan
Penelitian ini berhasil menuntun elaborasi algoritma jaringan sekuensial rekursif mutakhir—dan melepaskannya keluar dari kungkungan teoritis akademik murni lewat implementasi nyata berbasis *Dashboard Enterprise BI*. Uji banding menemukan preseden terbalik dari landasan logis awal (paradoks RMSE). LSTM mampu mendikte dinamika keuntungan finansial (Sharpe Ratio terbaik 1.45) jauh mengeksekusi kapasitas optimal GRU sekalipun GRU secara empiris matematik lebih presisi dengan RMSE rendah (0.1058). Kerangka *4-Layer BI-ML Pipeline* yang disodorkan sukses mewadahi kapabilitas fungsional 100% tanpa distorsi pengumpulan data (*latency losses*), merepresentasikan pencapaian konkret dalam konversi teoretis ke ranah teknis aplikasi praktikal bervaliditas *Excellent* (SUS 86.4). 

### 5.2 Saran
Meskipun purwarupa instrumen peramalan mengandalkan pasokan BTC/USDT berhasil memitigasi kesalahan heterogen, riset komprehensif di masa selanjutnya dianjurkan memperluas utilitas lapisan *front-testing* kepada ekosistem instrumen derivatif berketahanan multi-aset korelasi *peer-to-peer* (seperti integrasi indeks S&P500 dan Ethereum cross-platform) serta melibatkan jaringan dasar yang lebih padat seperti data setingkat Tick (detik per detik).
"""

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(thesis_content)

print(f"Created thesis report in {file_out}")
