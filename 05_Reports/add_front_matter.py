import os
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

front_matter_html = """
<!-- PERNYATAAN ORISINALITAS -->
<div class="page">
    <h1 style="counter-increment: none;">PERNYATAAN ORISINALITAS</h1>
    <p style="text-indent: 0; text-align: justify; margin-top: 40px;">Tesis dengan judul <b>"Kerangka Pembelajaran Mendalam dan Intelijen Bisnis untuk Prediksi Harga Mata Uang Kripto: Analisis Perbandingan Jaringan Urutan dengan Transformer Tercanggih"</b> adalah hasil karya saya sendiri, dan seluruh sumber yang dikutip maupun dirujuk telah saya nyatakan dengan benar.</p>
    <p style="text-indent: 0; text-align: justify;">Apabila di kemudian hari terbukti atau dapat dibuktikan bahwa sebagian atau keseluruhan Tesis ini merupakan hasil karya orang lain atau bentuk ketidakjujuran akademis secara parsial, saya bersedia menerima sanksi pencabutan gelar atas perbuatan tersebut sesuai dengan ketentuan yang berlaku dalam statuta etika Universitas Nusa Putra.</p>
    <div style="margin-top: 80px; text-align: right; margin-right: 50px;">
        Sukabumi, _________ 2026<br>
        Yang membuat pernyataan,<br><br><br>
        <span style="font-size: 8pt; color: #555;">[Materai Rp 10.000]</span><br><br>
        <b>Asep Surahman Sulaeman</b><br>
        NIM: ________________
    </div>
</div>

<!-- HALAMAN PENGESAHAN -->
<div class="page">
    <h1 style="counter-increment: none;">HALAMAN PENGESAHAN</h1>
    <p style="text-indent: 0; text-align: center; margin-top: 40px; margin-bottom: 30px;">Tesis ini diajukan oleh:<br>
    Nama: <b>Asep Surahman Sulaeman</b><br>
    Program Studi: <b>Magister Informatika</b><br>
    Judul Tesis: <b>Kerangka Pembelajaran Mendalam dan Intelijen Bisnis untuk Prediksi Harga Mata Uang Kripto: Analisis Perbandingan Jaringan Urutan dengan Transformer Tercanggih</b></p>
    <p style="text-indent: 0; text-align: center; margin-top: 30px;">Telah berhasil dipertahankan di hadapan Dewan Penguji dan diterima sebagai bagian persyaratan yang diperlukan untuk memperoleh gelar Magister Komputer (M.Kom) pada Program Studi Magister Informatika, Universitas Nusa Putra.</p>
    <div style="margin-top: 50px; text-align: center;">
        <b>DEWAN PENGUJI</b>
    </div>
    <div style="margin-top: 30px; display: flex; justify-content: space-between;">
        <div style="text-align: left; width: 45%;">Pembimbing Utama<br><br><br><br><b>____________________</b><br>NIDN. </div>
        <div style="text-align: left; width: 45%;">Pembimbing Pendamping<br><br><br><br><b>____________________</b><br>NIDN. </div>
    </div>
    <div style="margin-top: 50px; display: flex; justify-content: space-between;">
        <div style="text-align: left; width: 45%;">Penguji 1<br><br><br><br><b>____________________</b><br>NIDN. </div>
        <div style="text-align: left; width: 45%;">Penguji 2<br><br><br><br><b>____________________</b><br>NIDN. </div>
    </div>
    <div style="margin-top: 60px; text-align: center;">
        Ditetapkan di: Sukabumi<br>
        Tanggal Ujian Tesis: _________ 2026<br><br>
        Ketua Program Studi Magister Informatika<br><br><br><br><br>
        <b>_________________________</b><br>
        NIDN. ___________________
    </div>
</div>

<!-- KATA PENGANTAR -->
<div class="page">
    <h1 style="counter-increment: none;">KATA PENGANTAR</h1>
    <p style="margin-top: 20px;">Puji syukur penulis panjatkan ke hadirat Allah SWT, karena atas berkat dan rahmat-Nya, penulis dapat menyelesaikan penyusunan Tesis yang dijudulkan <i>"Kerangka Pembelajaran Mendalam dan Intelijen Bisnis untuk Prediksi Harga Mata Uang Kripto: Analisis Perbandingan Jaringan Urutan dengan Transformer Tercanggih"</i>. Penulisan naskah laporan penelitian Tesis ini dilakukan secara penuh sebagai komitmen guna memenuhi salah satu syarat imperatif akademis untuk mencapai gelar Magister Komputer di Program Pascasarjana Informatika Universitas Nusa Putra.</p>
    <p>Penulis menyadari bahwa tanpa bantuan dan bimbingan dari berbagai pihak institusional dan personal, dari masa perkuliahan sampai pada penyusunan Tesis ini, sangatlah sulit bagi penulis untuk dapat menyentuh titik kesimpulan akhir dari seluruh proses riset. Oleh karena itu, pada kesempatan khusus yang berharga ini, penulis mengucapkan beribu terima kasih dan atensi tinggi utamanya kepada:</p>
    <ol>
        <li>Rektor Universitas Nusa Putra atas segala penyediaan sarana pendidikan di dalam kampus.</li>
        <li>Ketua Program Studi Magister Informatika S2, Universitas Nusa Putra.</li>
        <li>Bapak Dr. Deden Witarsyah, S.T., M.Kom. dan Bapak Aswan Supriyadi Sunge, M.Kom. selaku dosen pembimbing yang senantiasa melimpahkan waktu, kebijaksanaan, pandangan logis kritis, serta bimbingan dedikatif bagi penulis.</li>
        <li>Rekan-rekan setingkat Pascasarjana Informatika Batch Terkait, serta tim pakar analisis kuantiatif <i>Crypto</i> eksternal yang telah membantu sebagai subjek validasi pengujian akhir <i>dashboard intelligence</i> ini.</li>
    </ol>
    <p>Akhir kata, penulis sangat berharap agar skripsi / tesis laporan terapan ini dapat memberikan faedah literatur referensi komputasional yang meluas bagi penggiat *Fintech Analytics*. Kritik dan saran pemutakhiran selanjutnya sangat kami hargai.</p>
    <div style="margin-top: 50px; text-align: right; margin-right: 50px;">
        Sukabumi, _________ 2026<br><br><br>
        <b>Penulis</b>
    </div>
</div>

<!-- ABSTRAK -->
<div class="page">
    <h1 style="counter-increment: none;">ABSTRAK</h1>
    <p style="text-indent: 0; margin-top: 20px;"><b>Nama:</b> Asep Surahman Sulaeman<br>
    <b>Program Studi:</b> Magister Informatika<br>
    <b>Judul:</b> Kerangka Pembelajaran Mendalam dan Intelijen Bisnis untuk Prediksi Harga Mata Uang Kripto: Analisis Perbandingan Jaringan Urutan dengan Transformer Tercanggih</p>
    <p>Penelitian ini memecahkan masalah prediktif rentang harga non-stasioner instrumen *Bitcoin* dengan mengusulkan kerangka operasional (<i>Pipeline BI-ML</i>) terintegrasi <i>end-to-end</i> tingkat instansi fungsionalis. Analisis kinerja model diukur melalui pendekatan struktural regresi berurutan <i>Walk-Forward Validation</i> (perancangan jendela interval pengujian periode 168 jam dan pelatihan 720 jam) yang secara presisi membandingkan kinerja utilitas jaringan rekursif ingatan GRU, jala LSTM klasik, algoritma *Statis Tree-Boosting* XGBoost, hingga paradigma atensi terkompresi canggih pada struktur asli model *Informer Transformer* generasi terbaru. Catatan validitas hasil demonstrasi komputasi dengan keras menyoroti krisis pembuktian *Diagnostic Error* linear konvensional manakala diformulasikan ke dalam probabilitas finansial kuantitatif (sebuah fenomena pergeseran nilai kemapanan atau "Paradoks RMSE"). Kendati arsitektur GRU dieksekusi dengan dominasi *Diagnostic Error* absolut paling minimal lewat unjuk koefisien <i>Root Mean Square Error</i> senilai 0.1058, konfrontasinya dalam parameter efektivitas perputaran rasio valuasi resiko (realisasi keuangan portofolio simulasi sisa), secara mutlak dikuasai oleh model sekuensial LSTM yang mampu menorehkan rasio <i>Sharpe Ratio</i> terunggul senilai 1.45 (berkat sokongan sinkronitas analisis presisi kepekaan parameter nilai <i>Directional Accuracy</i> memuaskan di persentil tinggi). Temuan penelitian menanamkan fakta vital empiris bahwasanya seluruh rantai indikasi algoritme AI (buatan mesin) sama sekali tiada bernilai terapan esensial jikalau prediktif numeriknya tidak otomatis divisualisasikan pada arsitektur penyambung visual metrik KPI. Dasbor integrasi Pipa *Decision Support System* Power BI terapan SQL di eksperimen ini disimulasikan bebas kompromi data lambat <i>(latency free metrics propagation)</i>, mencetak angka *satisfaction level score* yang berada di klaster utilitas <i>Excellent Scale</i> lewat standar dimensi penerimaan SUS (*System Usability Scale*) terverifikasi final 86.4.</p>
    <p style="text-indent: 0; margin-top: 20px;"><b>Kata Kunci:</b> Intelijen Bisnis, Informer Transformer, LSTM, Deep Learning, DSS Finansial, Dasbor Harga Kripto.</p>
</div>

<!-- ABSTRACT -->
<div class="page">
    <h1 style="counter-increment: none;">ABSTRACT</h1>
    <p style="text-indent: 0; margin-top: 20px;"><b>Name:</b> Asep Surahman Sulaeman<br>
    <b>Study Program:</b> Master of Informatics<br>
    <b>Title:</b> Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction: Comparative Analysis of Sequence Networks against State-of-the-Art Transformers</p>
    <p>This research solves the non-stationary predictive problem of Bitcoin prices by proposing an institution-grade end-to-end integrated operational framework (BI-ML Pipeline). Multi-model performance analysis was measured via a Walk-Forward validation structural sequential regression validation approach (designing an interval window of 168 hours of testing and 720 continuous hours of training memory blocks) measuring and specifically comparing GRU network dynamics, LSTM configurations, XGBoost Tree-Boosting methodologies, and the newest paradigm-shifting state-of-the-art baseline standard from the natively compressed sparse self-attention <i>Informer Transformer</i>. Validated demonstration results robustly highlighted the severity of the standard linear diagnostic convention crisis evaluated against financial realities (a phenomenon known as the "RMSE Error-Paradox"). Though the GRU algorithms natively executed with significantly better absolute minimal coefficients reaching an empiric <i>Root Mean Square Error</i> evaluation of 0.1058, actual testing metrics over simulated residual portfolio financial risk turnover valences confirmed LSTM to be far more profitable in terms of financial return direction, dominating the charts with a superior 1.45 <i>Sharpe Ratio</i> metrics value (backed specifically by far better, consistently higher synchronous values of <i>Directional Accuracy</i>). Further findings reinforce the reality that an entire pipeline of raw machine-generated arrays serves minimal essential utility outside of automation metric visualizations. This research successfully built its own automated metric KPI dashboard via Power BI SQL Data Mart mechanisms without metric delay losses (latency-free metrics propagations) and officially recorded a fully established satisfaction level marking an exceptional "Excellent Scale" ranking validation per its finalized standard SUS (System Usability Scale) usability dimension findings equal to 86.4 final score validation matrices.</p>
    <p style="text-indent: 0; margin-top: 20px;"><b>Keywords:</b> Business Intelligence, Informer Transformer, LSTM, Deep Learning, Crypto Prediction, Financial DSS Dashboard.</p>
</div>

<!-- DAFTAR ISI -->
<div class="page">
    <h1 style="counter-increment: none;">DAFTAR ISI</h1>
    <div style="margin-top: 30px; font-size: 12pt; line-height: 2;">
        HALAMAN SAMPUL .............................................................. i<br>
        HALAMAN PERNYATAAN ORISINALITAS ........................................... ii<br>
        HALAMAN PENGESAHAN .......................................................... iii<br>
        KATA PENGANTAR .............................................................. iv<br>
        ABSTRAK ..................................................................... v<br>
        ABSTRACT .................................................................... vi<br>
        DAFTAR ISI .................................................................. vii<br>
        DAFTAR TABEL ................................................................ viii<br>
        DAFTAR GAMBAR ............................................................... ix<br>
        BAB I PENDAHULUAN ........................................................... 1<br>
        BAB II TINJAUAN PUSTAKA ..................................................... 6<br>
        BAB III METODOLOGI PENELITIAN ............................................... 15<br>
        BAB IV HASIL DAN PEMBAHASAN ................................................. 28<br>
        BAB V KESIMPULAN DAN SARAN .................................................. 45<br>
        DAFTAR PUSTAKA .............................................................. 49<br>
        LAMPIRAN .................................................................... 54
    </div>
</div>
"""

lampiran_html = """
<!-- LAMPIRAN -->
<div class="page">
    <h1 style="counter-increment: none;">LAMPIRAN</h1>
    <h2>Lampiran A: Cuplikan Kode Program Model Evaluasi LSTM dan GRU</h2>
    <p style="text-indent: 0;">Berikut merupakan contoh instansiasi sebagian struktur kelas fungsi <i>neural network model</i> dengan *Tensorflow/Keras Backend* yang didesain ke dalam struktur Pipa evaluatorial berjalan.</p>
    <pre style="background: #f4f4f4; padding: 15px; font-family: monospace; font-size: 9pt; border: 1px solid #ddd; overflow-x: auto; margin-top: 20px;">
def build_rnn_model(X_train, unit_type='LSTM'):
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, LSTM, GRU
    
    model = Sequential()
    if unit_type == 'LSTM':
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
    elif unit_type == 'GRU':
        model.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model
    </pre>

    <h2>Lampiran B: Dokumentasi Prototipe Arsitektur Dashboard Intelegensi Bisnis</h2>
    <p style="text-indent: 0;">Layar dasbor integrasi grafikal terapan visualisasi Microsoft Power BI untuk *Decision Support System* disimulasikan sesuai struktur berikut (<i>Mockup Screenshot</i>).</p>
    <div style="text-align: center; border: 1px dashed #ccc; padding: 50px; background: #fafafa; color: #777; margin-top: 20px;">
        [Tangkapan Layar Modul PowerBI Disisipkan di Sini]
    </div>
</div>
"""

cover_page = soup.find('div', class_='cover-page')
if cover_page:
    fm_soup = BeautifulSoup(front_matter_html, 'html.parser')
    for elem in reversed(fm_soup.contents):
        if elem.name:
            cover_page.insert_after(elem)

body = soup.find('body')
if body:
    lamp_soup = BeautifulSoup(lampiran_html, 'html.parser')
    for elem in lamp_soup.contents:
        if elem.name:
            body.append(elem)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
