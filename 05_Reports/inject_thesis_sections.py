import os
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

rumusan_masalah = BeautifulSoup('''
<h2>1.2 Rumusan Masalah</h2>
<ol>
    <li>Bagaimana mengintegrasikan inferensi deret waktu dari model pembelajaran mendalam ke dalam sebuah sistem antrean Intelijen Bisnis (BI) tingkat perusahaan secara <i>end-to-end</i> yang adaptif?</li>
    <li>Bagaimana perbandingan unjuk kerja komputasi antara algoritma statis (XGBoost), jaringan memori skuensial (LSTM, GRU), dan model mekanisasi atensi probabilistik (Informer Transformer) dalam memfasilitasi prediksi harga pada himpunan data mata uang kripto berfrekuensi tinggi (per jam)?</li>
    <li>Apakah model dengan tingkat kesalahan pengujian terendah mutlak sejalan dengan pencapaian profitabilitas keuangan dan presisi analisis arah pasar?</li>
</ol>
<h2>1.3 Tujuan Penelitian</h2>
<ol>
    <li>Mengusulkan rancang bangun arsitektur operasional 4 lapis (BI-ML Pipeline) yang menjembatani transformasi <i>raw feed/API</i> hingga terkonversi otomatis menjadi matrik terapan pada Sistem Pendukung Keputusan berbasis <i>dashboard</i>.</li>
    <li>Membandingkan fungsionalitas dan akurasi model XGBoost, LSTM, GRU, serta Informer Transformer dalam cakrawala prakiraan (168 jam Walk-Forward) berlandaskan kriteria diagnostik statistik ganda serta rasio profitabilitas finansial.</li>
</ol>
<h2>1.4 Batasan Penelitian</h2>
<ol>
    <li>Data aset transaksi sepenuhnya difokuskan pada nilai Spot satu koin secara eksklusif, yakni Bitcoin (BTC/USDT). Hal ini bertujuan untuk menciptakan kondisi pengukuran analitik dasar (<i>benchmarking</i>) yang paling terkontrol tanpa tumpang tindih dengan gangguan pasar koin sekunder.</li>
    <li>Panjang historis seri temporal diekstraksi dari Binance Spot API yang direntangkan selama periode 1 Januari 2021 hingga 31 Desember 2025 dengan granularitas transaksi per 1 Jam.</li>
    <li>Evaluasi front-end dilakukan hanya menggunakan metodologi SUS (<i>System Usability Scale</i>) via piranti Microsoft Power BI.</li>
</ol>
''', 'html.parser')

saran = BeautifulSoup('''
<h2>5.2 Saran</h2>
<p>Meskipun purwarupa instrumen peramalan mengandalkan pasokan BTC/USDT berhasil memitigasi kesalahan heterogen, riset komprehensif di masa selanjutnya dianjurkan memperluas utilitas lapisan pengujian kepada ekosistem instrumen derivatif berketahanan multi-aset korelasi antar-platform serta melibatkan jaringan dasar yang lebih padat seperti data setingkat Tick (detik per detik).</p>
''', 'html.parser')

body = soup.find('body')

# Find Tinjauan Pustaka H1 and insert rumusan_masalah BEFORE it
bab2_h1 = None
for h1 in body.find_all('h1'):
    if 'TINJAUAN' in h1.text.upper():
        bab2_h1 = h1
        break

if bab2_h1:
    elems = list(rumusan_masalah.contents)
    for elem in elems:
        if elem.name:
            bab2_h1.insert_before(elem)

# Find Daftar Pustaka H1 and insert Saran BEFORE it
ref_h1 = None
for h1 in body.find_all('h1'):
    if 'DAFTAR' in h1.text.upper() or 'REFERENSI' in h1.text.upper():
        ref_h1 = h1
        break

if ref_h1:
    elems = list(saran.contents)
    for elem in elems:
        if elem.name:
            ref_h1.insert_before(elem)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
