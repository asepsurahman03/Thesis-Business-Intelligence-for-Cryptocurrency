import os
import re
from bs4 import BeautifulSoup

file_ieee = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_ID.html'
file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_ieee, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Delete everything before the first h1
body = soup.find('body')
if body:
    # First, let's unwrap pages
    for page in body.find_all('div', class_='page'):
        page.unwrap()
    for pc in body.find_all('div', class_='page-content'):
        pc.unwrap()
        
    for elem in list(body.contents):
        if elem.name == 'h1':
            break
        elem.extract()
        
# Also delete header blocks if any survived inside body
for hb in body.find_all('div', class_='header-block'):
    hb.decompose()

# Helper HTML parts to inject
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

# Map and organize H1
all_h1 = soup.find_all('h1')

for h1 in all_h1:
    text = h1.text.strip().lower()
    text = text.replace('\n', ' ')
    
    if 'perkenalan' in text or 'introduction' in text:
        h1.string = "BAB I PENDAHULUAN"
        h1['class'] = h1.get('class', []) + ['bab-header']
        # insert <h2>1.1 Latar Belakang</h2> right after it
        new_h2 = soup.new_tag('h2')
        new_h2.string = "1.1 Latar Belakang"
        h1.insert_after(new_h2)
        
    elif 'tinjauan pustaka' in text:
        # Before this H1, we must insert Rumusan Masalah, Tujuan, Batasan
        for elem in rumusan_masalah.contents:
            h1.insert_before(elem)
            
        h1.string = "BAB II TINJAUAN PUSTAKA"
        h1['class'] = h1.get('class', []) + ['bab-header']
        
    elif 'arsitektur sistem' in text:
        h1.string = "BAB III METODOLOGI PENELITIAN"
        h1['class'] = h1.get('class', []) + ['bab-header']
        # Maybe insert 3.1 Kerangka Sistem
        new_h2 = soup.new_tag('h2')
        new_h2.string = "3.1 Kerangka Sistem dan Tahapan"
        h1.insert_after(new_h2)
        
    elif 'rekayasa fitur' in text:
        h1.name = 'h2'
        h1.string = "3.2 Rekayasa Fitur dan Analisis SHAP"
    elif 'formulasi algoritma' in text:
        h1.name = 'h2'
        h1.string = "3.3 Formulasi Algoritma"
        
    elif 'hasil empiris' in text:
        h1.string = "BAB IV HASIL DAN PEMBAHASAN"
        h1['class'] = h1.get('class', []) + ['bab-header']
    elif 'diskusi' in text:
        h1.name = 'h2'
        h1.string = "4.2 Diskusi Analisis"
        
    elif 'kesimpulan' in text:
        h1.string = "BAB V KESIMPULAN DAN SARAN"
        h1['class'] = h1.get('class', []) + ['bab-header']
        new_h2 = soup.new_tag('h2')
        new_h2.string = "5.1 Kesimpulan"
        h1.insert_after(new_h2)
        
    elif 'pengakuan' in text:
        # Find references to stop deleting
        curr = h1.find_next_sibling()
        while curr and curr.name != 'h1':
            nxt = curr.find_next_sibling()
            curr.decompose()
            curr = nxt
        h1.decompose()
        
    elif 'referensi' in text:
        # Before Referensi, insert Saran
        for elem in saran.contents:
            h1.insert_before(elem)
            
        h1.string = "DAFTAR PUSTAKA"
        h1['class'] = h1.get('class', []) + ['front-matter-title']

# Number the H2s in BAB II
bab2_h2s = 1
bab4_h2s = 1
bab = 0

for t in soup.find_all(['h1', 'h2']):
    if 'bab-header' in t.get('class', []):
        if 'BAB II' in t.text: bab = 2
        if 'BAB III' in t.text: bab = 3
        if 'BAB IV' in t.text: bab = 4
        if 'BAB V' in t.text: bab = 5
    elif t.name == 'h2':
        text = t.text.strip()
        # Clean up any "A. " or previous custom numbers if they aren't part of new numbers
        if re.match(r'^\d+\.\d+', text):
            pass # Keep ones we just set
        else:
            clean_text = re.sub(r'^[A-Z]\.\s+', '', text)
            if bab == 2:
                t.string = f"2.{bab2_h2s} {clean_text}"
                bab2_h2s += 1
            elif bab == 4:
                # We forced 4.2 Diskusi earlier, but maybe there's 4.1 Results. So:
                if 'Diskusi' not in clean_text:
                    t.string = f"4.{bab4_h2s} {clean_text}"
                    bab4_h2s += 1
                else: 
                    pass

# Inject CSS for Paged.js and A4 sizes
style_tag = soup.find('style')
if not style_tag:
    style_tag = soup.new_tag('style')
    soup.head.append(style_tag)

css_content = """
    /* Paged.js Page numbering and A4 setup */
    @page {
        size: A4;
        margin-top: 40mm;
        margin-bottom: 30mm;
        margin-left: 40mm;
        margin-right: 30mm;
        @bottom-center {
            content: counter(page);
            font-family: "Times New Roman", Times, serif;
            font-size: 12pt;
            padding-top: 10px;
        }
    }
    
    body { 
        background-color: #e0e0e0;
        font-family: "Times New Roman", Times, serif; 
        font-size: 12pt; 
        line-height: 1.5; 
        margin: 0; 
        text-align: justify;
    }

    .pagedjs_pages { margin-bottom: 40px; }
    .pagedjs_page { background-color: white; box-shadow: 0 0 10px rgba(0,0,0,0.2) !important; margin: 20px auto !important; }

    h1.bab-header { font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; margin-top: 0px; margin-bottom: 30px; line-height: 1.5; page-break-before: always; }
    h1.front-matter-title { font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; margin-top: 0px; margin-bottom: 30px; line-height: 1.5; page-break-before: always; }
    h2 { font-size: 12pt; font-weight: bold; text-align: left; margin-top: 30px; margin-bottom: 10px; }
    h3 { font-size: 12pt; font-weight: bold; text-align: left; margin-top: 20px; margin-bottom: 10px; }

    p { text-indent: 1.25cm; margin: 0 0 10px 0; }
    ol { margin: 0 0 10px 0; padding-left: 2cm; }
    ol li { margin-bottom: 5px; text-indent: 0; text-align: justify; }

    table { margin: 15px auto; width: 90%; border-collapse: collapse; }
    th, td { border: 1px solid black; padding: 6px; text-align: center; }
    .figure { text-align: center; margin: 20px 0; }
    .figure img { max-width: 100%; height: auto; display: block; margin: 0 auto; box-shadow: none; border: 1px solid #ccc; padding: 5px; }
    .figure-caption { text-align: center; font-size: 10pt; margin-top: 5px; font-style: italic; }
    .equation { text-align: center; margin: 20px 0; font-style: italic; }
"""
style_tag.string = css_content

head_tag = soup.find('head')
if head_tag and not soup.find('script', src=lambda x: x and 'paged.polyfill.js' in x):
    paged_script = soup.new_tag('script', src="https://unpkg.com/pagedjs/dist/paged.polyfill.js")
    head_tag.append(paged_script)

# Make sure all h2 and h3 sizes are strictly preserved
with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))
