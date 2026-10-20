import os
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Function to cleanly insert HTML before a specific h2
def insert_html_before_h2(soup_obj, match_text, new_html):
    target = None
    for h2 in soup_obj.find_all('h2'):
        if match_text.lower() in h2.text.lower():
            target = h2
            break
    if target:
        new_soup = BeautifulSoup(new_html, 'html.parser')
        for elem in list(new_soup.contents):
            if elem.name:
                target.insert_before(elem)

def insert_html_after_h2_block(soup_obj, match_text, new_html):
    # Inserts after the target h2 and its immediately following elements (p, ul, ol, table) 
    # until the next heading is reached.
    target = None
    for h2 in soup_obj.find_all('h2'):
        if match_text.lower() in h2.text.lower():
            target = h2
            break
    if target:
        curr = target.find_next_sibling()
        while curr and curr.name not in ['h1', 'h2', 'h3']:
            target = curr
            curr = curr.find_next_sibling()
        
        new_soup = BeautifulSoup(new_html, 'html.parser')
        for elem in reversed(list(new_soup.contents)):
            if elem.name:
                target.insert_after(elem)

# 1. Add Manfaat Penelitian and Sistematika Penulisan to BAB I
manfaat_sistematika = """
<h2>1.4 Manfaat Penelitian</h2>
<p>Penelitian ini diharapkan dapat memberikan kontribusi dan manfaat pada dua aspek utama, yaitu:</p>
<ol>
    <li><b>Manfaat Teoritis:</b> Memperkaya khazanah keilmuan Informatika khususnya pada implementasi algoritma <i>Deep Learning</i> (LSTM, GRU, dan Informer Transformer) dalam pemrosesan data deret waktu yang non-stasioner. Penelitian ini memberikan landasan empiris baru mengenai komparasi kinerja <i>Transformer</i> melawan RNN klasik pada rentang data frekuensi tinggi, serta mempertegas fenomena "Paradoks RMSE" dalam evaluasi model finansial.</li>
    <li><b>Manfaat Praktis:</b> Menghasilkan purwarupa <i>Pipeline BI-ML</i> (kerangka kerja hulu ke hilir) terintegrasi yang dapat diadopsi secara langsung oleh praktisi kuantitatif, manajer portofolio, maupun analis data di bursa kripto. Dasbor evaluatorial berbasis <i>Decision Support System</i> yang dihasilkan berguna sebagai instrumen mitigasi risiko finansial yang andal secara <i>real-time</i>.</li>
</ol>

<h2>1.6 Sistematika Penulisan</h2>
<p>Untuk memberikan gambaran yang jelas mengenai isi dari Tesis ini, maka penyusunan laporan dibagi menjadi lima bab dengan sistematika sebagai berikut:</p>
<p><b>BAB I PENDAHULUAN</b><br>Bab ini menguraikan latar belakang masalah, rumusan masalah, tujuan penelitian, batasan penelitian, manfaat penelitian, dan sistematika penulisan tesis.</p>
<p><b>BAB II TINJAUAN PUSTAKA</b><br>Bab ini merangkum kajian studi terdahulu (<i>State of the Art</i>) serta landasan teori yang relevan meliputi konsep peramalan harga kripto, jaringan saraf tiruan (RNN, LSTM, GRU), mekanisme Atensi, dan konsep <i>Business Intelligence</i>.</p>
<p><b>BAB III METODOLOGI PENELITIAN</b><br>Bab ini memaparkan secara rinci tahapan-tahapan penelitian, kerangka arsitektur sistem (<i>4-Layer BI-ML Pipeline</i>), teknik pengumpulan dan prapemrosesan data, serta skenario desain validasi <i>Walk-Forward</i> dan metrik pengujian kuantifikasi finansial.</p>
<p><b>BAB IV HASIL DAN PEMBAHASAN</b><br>Bab ini mendeskripsikan secara komprehensif implementasi model, hasil evaluasi komparatif dari setiap algoritma (RMSE, MAE, <i>Directional Accuracy</i>, <i>Sharpe Ratio</i>), temuan terkait analisis <i>SHAP feature importance</i>, serta diakhiri dengan hasil uji validasi <i>front-end dashboard</i> menggunakan metode SUS.</p>
<p><b>BAB V KESIMPULAN DAN SARAN</b><br>Bab ini berisi rangkuman konklusi yang menjawab seluruh rumusan masalah dari hasil penelitian dan memberikan saran atau rekomendasi untuk pengembangan penelitian di masa yang akan datang.</p>
"""

tinjauan_studi_terdahulu = """
<h2>2.1 Tinjauan Studi Terdahulu (<i>State of the Art</i>)</h2>
<p>Sebagai pijakan pengembangan landasan model ini, beberapa literatur utama dikomparasikan. Sebagian besar penelitian peramalan harga aset keuangan beberapa tahun silam bertumpu pada teknik parametrik konvensional seperti ARIMA dan GARCH. Kendala utama pada pendekatan tersebut adalah ketidakmampuannya di dalam merekam ledakan volatilitas sisa pada seri waktu kripto. Evolusi berlanjut ketika jurnal-jurnal modern memperkenalkan efektivitas arsitektur XGBoost dalam klasifikasi prediksi harian, yang kemudian tak lama digeser oleh kehadiran teknik <i>Deep Sequence</i> (LSTM/GRU) akibat kemahiran jaringan saraf mendelegasikan beban ingatan waktu panjang. Transisi mutakhir saat ini mengacu pada jurnal primer yang membahas aplikasi mekanisme atensi murni, yakni arsitektur <i>Informer</i>. Penelitian ini memposisikan pembaruan keilmuannya (<i>Novelty</i>) dengan mengevaluasi langsung titik lemah model <i>Informer</i> pada bursa spot intra-hari (<i>intra-day granularities</i>) dan mendedahkan integrasinya ke dalam panel <i>Business Intelligence</i>, sebuah aspek eksekusi produksi yang luput pada mayoritas literatur AI terdahulu.</p>
"""

tahapan_penelitian = """
<h2>3.1 Tahapan Penelitian</h2>
<p>Penelitian ini disusun melalui beberapa tahapan prosedural yang terstruktur agar penelitian dapat dipertanggungjawabkan secara saintifik. Langkah-langkah tersebut terbagi atas:</p>
<ol>
    <li><b>Pengumpulan Data (<i>Data Crawling</i>):</b> Mengekstrak data deret waktu harga <i>Cryptocurrency</i> (BTC/USDT) secara historis melalui antarmuka Binance API.</li>
    <li><b>Prapemrosesan Data (<i>Data Pre-processing</i>):</b> Melakukan normalisasi skala logaritmik, penanganan nilai hilang berbasis polinomial, dan ekstraksi fitur buatan (<i>Feature Engineering</i>) teknikal (seperti MACD, deviasi standar bergulir \(\sigma_t\)).</li>
    <li><b>Desain Arsitektur Pembelajaran Mendalam (<i>Deep Learning</i>):</b> Mengompilasi dan menyeleksi <i>hyperparameter</i> model prediksi mencakup XGBoost, LSTM, GRU, dan Informer Transformer pada panggung komputasi <i>backend</i>.</li>
    <li><b>Evaluasi Teknis (<i>Walk-Forward Validation</i>):</b> Melaksanakan pelatihan jaringan mesin prediksi melalui metode validasi jendela statis maju untuk merekam akurasi absolut (RMSE, MAE).</li>
    <li><b>Integrasi dan Pengujian Operasional (<i>BI-ML Dashboard</i>):</b> Memvisualisasikan parameter probabilitas untung/rugi (<i>Sharpe Ratio</i>, <i>Directional Accuracy</i>) ke dalam <i>Virtual Dashboard Business Intelligence</i> untuk divalidasi oleh dewan uji pakar menggunakan skala kelayakan aplikasi (SUS).</li>
</ol>
"""

# Insert Batasan Before 1.6
target_batasan = None
for h2 in soup.find_all('h2'):
    if '1.4 batasan penelitian' in h2.text.lower():
        h2.string = h2.text.replace('1.4', '1.5')
        target_batasan = h2
        break

if target_batasan:
    # Insert Manfaat before Batasan (so Manfaat becomes 1.4)
    new_manfaat_soup = BeautifulSoup(manfaat_sistematika.split('<h2>1.6')[0], 'html.parser')
    for elem in list(new_manfaat_soup.contents):
        if elem.name:
            target_batasan.insert_before(elem)
            
    # Insert Sistematika after Batasan (and its list) block
    new_sist = BeautifulSoup('<h2>1.6' + manfaat_sistematika.split('<h2>1.6')[1], 'html.parser')
    curr = target_batasan.find_next_sibling()
    while curr and curr.name not in ['h1', 'h2']:
        target_batasan = curr
        curr = curr.find_next_sibling()
        
    for elem in reversed(list(new_sist.contents)):
        if elem.name:
            target_batasan.insert_after(elem)

# BAB 2: Insert Tinjauan Studi Terdahulu immediately after BAB II h1
bab2_h1 = None
for h1 in soup.find_all('h1', class_='bab-header'):
    if 'BAB II' in h1.text:
        bab2_h1 = h1
        break
        
if bab2_h1:
    old_h2_21 = bab2_h1.find_next_sibling('h2')
    if old_h2_21 and '2.1' in old_h2_21.text:
       old_h2_21.string = old_h2_21.text.replace('2.1', '2.2')
       
       # Next h2: 2.2 -> 2.3
       curr = old_h2_21.find_next_sibling('h2')
       if curr and '2.2' in curr.text:
           curr.string = curr.text.replace('2.2', '2.3')
           
       # Next h2: 2.3 -> 2.4
       curr = curr.find_next_sibling('h2') if curr else None
       if curr and '2.3' in curr.text:
           curr.string = curr.text.replace('2.3', '2.4')
           if 'sistem pendukung' in curr.text.lower():
               curr.string = "2.4 Sistem Pendukung Keputusan dan Integrasi BI Terkini"
               
    # Insert new 2.1
    new_21_soup = BeautifulSoup(tinjauan_studi_terdahulu, 'html.parser')
    for elem in reversed(list(new_21_soup.contents)):
        if elem.name:
            bab2_h1.insert_after(elem)

# BAB 3: Insert Tahapan Penelitian immediately after BAB III h1
bab3_h1 = None
for h1 in soup.find_all('h1', class_='bab-header'):
    if 'BAB III' in h1.text:
        bab3_h1 = h1
        break

if bab3_h1:
    h2_runner = bab3_h1.find_next_sibling('h2')
    while h2_runner and '3.' in h2_runner.text:
        # Increment index 3.x to 3.(x+1)
        try:
            num = int(h2_runner.text.split()[0].split('.')[1])
            h2_runner.string = h2_runner.text.replace(f'3.{num}', f'3.{num+1}')
        except:
            pass
        h2_runner = h2_runner.find_next_sibling('h2')

    new_31_soup = BeautifulSoup(tahapan_penelitian, 'html.parser')
    for elem in reversed(list(new_31_soup.contents)):
        if elem.name:
            bab3_h1.insert_after(elem)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
