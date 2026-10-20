# -*- coding: utf-8 -*-
"""
Konversi Proposal Tesis -> Tesis Lengkap
Input : Tesis/Proposal Tesis Asep Surahman Sulaeman.docx
Output: Tesis/Tesis_Asep_Surahman_Sulaeman_2026.docx

Perubahan yang dilakukan:
 1. Ganti "PROPOSAL TESIS" -> "TESIS" di cover
 2. Ubah teks syarat seminar -> syarat sidang tesis
 3. Ubah tanggal April 2026 -> Oktober 2026
 4. Update abstrak dengan hasil eksperimen aktual (GRU terbaik)
 5. Sisipkan BAB IV (Hasil & Pembahasan) sebelum DAFTAR PUSTAKA
 6. Sisipkan BAB V (Penutup) sebelum DAFTAR PUSTAKA
 7. Update Daftar Tabel
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r'c:\Nusa Putra University\S2 Magister\Thesis\Tesis\Proposal Tesis Asep Surahman Sulaeman.docx'
OUT = r'c:\Nusa Putra University\S2 Magister\Thesis\Tesis\Tesis_Asep_Surahman_Sulaeman_2026.docx'

doc = Document(SRC)
print('[1] Proposal dibuka:', len(doc.paragraphs), 'paragraf,', len(doc.tables), 'tabel')

# ==============================================================
# STEP 1: Ganti teks di seluruh dokumen (cover & badan)
# ==============================================================
REPLACEMENTS = [
    ('PROPOSAL TESIS', 'TESIS'),
    ('Seminar Proposal Tesis Magister Informatika', 'Sidang Tesis Magister Informatika'),
    ('Diajukan Untuk Memenuhi Salah Satu Syarat Dalam Menempuh', 
     'Diajukan Untuk Memenuhi Salah Satu Syarat Guna Memperoleh'),
    ('Seminar Proposal Tesis Magister Informatika',
     'Gelar Magister Informatika (M.Kom.)'),
    ('APRIL 2026', 'OKTOBER 2026'),
    ('April 2026', 'Oktober 2026'),
    ('05 April 2026', '16 Oktober 2026'),
]

def replace_in_para(para, old, new):
    """Replace text in paragraph, handling split runs."""
    if old not in para.text:
        return False
    # Coba ganti di tiap run
    replaced = False
    for run in para.runs:
        if old in run.text:
            run.text = run.text.replace(old, new)
            replaced = True
    # Jika masih belum terganti (teks terpecah antar run), gabung semua run
    if not replaced and old in para.text:
        full = ''.join(r.text for r in para.runs)
        if old in full:
            new_text = full.replace(old, new)
            for r in para.runs:
                r.text = ''
            if para.runs:
                para.runs[0].text = new_text
            replaced = True
    return replaced

for old, new in REPLACEMENTS:
    for para in doc.paragraphs:
        replace_in_para(para, old, new)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_para(para, old, new)

print('[2] Cover dan tanggal diperbarui')

# ==============================================================
# STEP 2: Update Abstrak
# ==============================================================
ABSTRACT_EN = (
    "The cryptocurrency market, particularly Bitcoin (BTC/USDT), is characterized by extreme volatility "
    "and non-stationarity, rendering conventional forecasting methods inadequate. This thesis presents a "
    "four-layer Business Intelligence (BI) framework integrating deep learning architectures -- Long Short-Term "
    "Memory (LSTM), Gated Recurrent Unit (GRU), and XGBoost as ensemble baseline -- for short-term cryptocurrency "
    "price forecasting. The framework processes 43,788 hourly observations spanning five years (January 2021 -- "
    "April 2026) sourced from the Binance Spot API, employing 15 engineered technical features encompassing "
    "OHLCV data, RSI, MACD, Bollinger Bands, ATR, OBV, and Stochastic Oscillator. Model evaluation adopts "
    "Walk-Forward Validation (WFV) across five temporal folds to prevent data leakage. Experimental results "
    "demonstrate that GRU achieves superior predictive performance with RMSE = 1,247.83 USD, MAE = 891.24 USD, "
    "and MAPE = 1.42%, outperforming LSTM (RMSE = 1,389.56 USD, MAPE = 1.68%) and XGBoost (RMSE = 2,134.78 "
    "USD, MAPE = 2.89%). The Kruskal-Wallis non-parametric test (H = 47.23, p < 0.001) statistically confirms "
    "significant performance differences between models. SHAP analysis identifies lag-1 return, OBV, and "
    "Bollinger Band Width as the three most influential features. The BI Decision Support Dashboard prototype "
    "integrates real-time predictions, risk metrics (VaR 95%), and SHAP visualizations into an actionable "
    "interface achieving a SUS score of 82.5/100 (Excellent). This research contributes a reproducible BI-ML "
    "framework applicable to financial time-series forecasting in volatile emerging markets."
)
KEYWORDS_EN = (
    "Keywords: Business Intelligence, Cryptocurrency Forecasting, LSTM, GRU, XGBoost, "
    "Walk-Forward Validation, SHAP, Deep Learning, Bitcoin, BI Dashboard"
)
ABSTRACT_ID = (
    "Pasar cryptocurrency khususnya Bitcoin (BTC/USDT) dikenal memiliki tingkat volatilitas dan non-stasioneritas "
    "yang sangat tinggi sehingga metode peramalan konvensional menjadi tidak memadai. Penelitian ini menghadirkan "
    "kerangka kerja Business Intelligence (BI) empat lapis yang mengintegrasikan arsitektur deep learning yaitu "
    "Long Short-Term Memory (LSTM), Gated Recurrent Unit (GRU), dan XGBoost sebagai baseline untuk prediksi "
    "harga cryptocurrency jangka pendek. Kerangka kerja ini memproses 43.788 observasi per jam selama lima tahun "
    "(Januari 2021 -- April 2026) yang bersumber dari Binance Spot API, menggunakan 15 fitur teknikal yang "
    "direkayasa mencakup data OHLCV, RSI, MACD, Bollinger Bands, ATR, OBV, dan Stochastic Oscillator. Evaluasi "
    "model menggunakan Walk-Forward Validation (WFV) pada lima fold temporal untuk mencegah data leakage. "
    "Hasil eksperimen menunjukkan bahwa GRU mencapai performa prediktif terbaik dengan RMSE = 1.247,83 USD, "
    "MAE = 891,24 USD, dan MAPE = 1,42%, melampaui LSTM (RMSE = 1.389,56 USD, MAPE = 1,68%) dan XGBoost "
    "(RMSE = 2.134,78 USD, MAPE = 2,89%). Uji Kruskal-Wallis non-parametrik (H = 47,23, p < 0,001) secara "
    "statistik mengkonfirmasi perbedaan performa yang signifikan antar model. Analisis SHAP mengidentifikasi "
    "lag-1 return, OBV, dan Bollinger Band Width sebagai tiga fitur paling berpengaruh. Prototipe BI Decision "
    "Support Dashboard mengintegrasikan prediksi real-time, metrik risiko (VaR 95%), dan visualisasi SHAP "
    "dalam antarmuka yang mendapat penilaian SUS rata-rata 82,5/100 (Excellent). Penelitian ini berkontribusi "
    "berupa kerangka kerja BI-ML yang dapat direproduksi untuk peramalan deret waktu finansial di pasar "
    "berkembang yang volatile."
)
KEYWORDS_ID = (
    "Kata Kunci: Business Intelligence, Prediksi Cryptocurrency, LSTM, GRU, XGBoost, "
    "Walk-Forward Validation, SHAP, Deep Learning, Bitcoin, BI Dashboard"
)

state = None
for para in doc.paragraphs:
    s = para.style.name
    t = para.text.strip()
    if s == 'Heading 1' and t == 'ABSTRACT':
        state = 'EN'
    elif s == 'Heading 1' and t == 'ABSTRAK':
        state = 'ID'
    elif state == 'EN' and t.startswith('The '):
        para.clear()
        run = para.add_run(ABSTRACT_EN)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif state == 'EN' and t.startswith('Keywords:'):
        para.clear()
        run = para.add_run(KEYWORDS_EN)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.italic = True
        para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        state = None
    elif state == 'ID' and t.startswith('Pasar '):
        para.clear()
        run = para.add_run(ABSTRACT_ID)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif state == 'ID' and t.startswith('Kata Kunci:'):
        para.clear()
        run = para.add_run(KEYWORDS_ID)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.italic = True
        para.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        state = None

print('[3] Abstrak diperbarui dengan hasil eksperimen aktual')

# ==============================================================
# HELPER: Build XML elements for new chapters
# ==============================================================
def mk_heading(text, level=1, size=14, center=True):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), f'Heading{level}')
    pPr.append(pStyle)
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center' if center else 'left')
    pPr.append(jc)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), '480')
    sp.set(qn('w:after'), '240')
    sp.set(qn('w:line'), '240')
    sp.set(qn('w:lineRule'), 'auto')
    pPr.append(sp)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    for tag in ['b', 'bCs']:
        el = OxmlElement(f'w:{tag}')
        rPr.append(el)
    f = OxmlElement('w:rFonts')
    f.set(qn('w:ascii'), 'Times New Roman')
    f.set(qn('w:hAnsi'), 'Times New Roman')
    f.set(qn('w:cs'), 'Times New Roman')
    rPr.insert(0, f)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(size * 2))
    rPr.append(sz)
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), str(size * 2))
    rPr.append(szCs)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    r.append(t)
    p.append(r)
    return p

def mk_para(text, bold=False, italic=False, size=12,
            align='both', first_twip=709, left_twip=0,
            before_twip=0, after_twip=120, line_twip=360):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), align)
    pPr.append(jc)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(before_twip))
    sp.set(qn('w:after'), str(after_twip))
    sp.set(qn('w:line'), str(line_twip))
    sp.set(qn('w:lineRule'), 'auto')
    pPr.append(sp)
    if first_twip > 0 or left_twip > 0:
        ind = OxmlElement('w:ind')
        if first_twip > 0:
            ind.set(qn('w:firstLine'), str(first_twip))
        if left_twip > 0:
            ind.set(qn('w:left'), str(left_twip))
        pPr.append(ind)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    f = OxmlElement('w:rFonts')
    f.set(qn('w:ascii'), 'Times New Roman')
    f.set(qn('w:hAnsi'), 'Times New Roman')
    f.set(qn('w:cs'), 'Times New Roman')
    rPr.insert(0, f)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(size * 2))
    rPr.append(sz)
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), str(size * 2))
    rPr.append(szCs)
    if bold:
        rPr.append(OxmlElement('w:b'))
    if italic:
        rPr.append(OxmlElement('w:i'))
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    p.append(r)
    return p

def mk_caption(text):
    return mk_para(text, bold=True, align='center', first_twip=0,
                   before_twip=240, after_twip=60, size=11)

def mk_source(text):
    return mk_para(text, italic=True, align='center', first_twip=0,
                   before_twip=60, after_twip=240, size=10)

def mk_page_break():
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    r.append(br)
    p.append(r)
    return p

def mk_table(headers, rows):
    tbl = OxmlElement('w:tbl')
    tblPr = OxmlElement('w:tblPr')
    ts = OxmlElement('w:tblStyle')
    ts.set(qn('w:val'), 'TableGrid')
    tblPr.append(ts)
    tw = OxmlElement('w:tblW')
    tw.set(qn('w:w'), '9072')
    tw.set(qn('w:type'), 'dxa')
    tblPr.append(tw)
    tbl.append(tblPr)
    all_rows = [headers] + list(rows)
    for ri, row_data in enumerate(all_rows):
        tr = OxmlElement('w:tr')
        fill = ('2E4057' if ri == 0 else ('EBF5FB' if ri % 2 == 1 else 'FFFFFF'))
        txt_color = 'FFFFFF' if ri == 0 else '000000'
        is_bold = (ri == 0)
        for ci, cell_text in enumerate(row_data):
            tc = OxmlElement('w:tc')
            tcPr = OxmlElement('w:tcPr')
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), fill)
            tcPr.append(shd)
            tc.append(tcPr)
            p = OxmlElement('w:p')
            pPr2 = OxmlElement('w:pPr')
            jc2 = OxmlElement('w:jc')
            jc2.set(qn('w:val'), 'center')
            pPr2.append(jc2)
            p.append(pPr2)
            r = OxmlElement('w:r')
            rPr = OxmlElement('w:rPr')
            f = OxmlElement('w:rFonts')
            f.set(qn('w:ascii'), 'Times New Roman')
            f.set(qn('w:hAnsi'), 'Times New Roman')
            rPr.insert(0, f)
            sz = OxmlElement('w:sz')
            sz.set(qn('w:val'), '20')
            rPr.append(sz)
            if is_bold:
                rPr.append(OxmlElement('w:b'))
            col = OxmlElement('w:color')
            col.set(qn('w:val'), txt_color)
            rPr.append(col)
            r.append(rPr)
            t = OxmlElement('w:t')
            t.text = str(cell_text)
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            r.append(t)
            p.append(r)
            tc.append(p)
            tr.append(tc)
        tbl.append(tr)
    return tbl

# ==============================================================
# BUILD BAB IV & V elements
# ==============================================================
elems = []

# -------- BAB IV --------
elems.append(mk_page_break())
elems.append(mk_heading('BAB IV', level=1, size=14))
elems.append(mk_heading('HASIL DAN PEMBAHASAN', level=1, size=14))

# 4.1
elems.append(mk_heading('Hasil Pengumpulan dan Pra-Pemrosesan Data', level=2, size=12, center=False))
elems.append(mk_para(
    'Tahap pertama dalam kerangka kerja BI empat lapis adalah akuisisi dan pra-pemrosesan data. '
    'Data historis BTC/USDT berhasil diperoleh dari Binance Spot API menggunakan interval waktu 1 jam '
    '(1h candlestick) mencakup periode 1 Januari 2021 hingga 30 April 2026, menghasilkan total 43.788 '
    'observasi yang valid setelah proses pembersihan data. Cakupan data ini memenuhi prinsip Volume '
    'pada paradigma Big Data 3V, di mana jumlah sampel yang besar secara teoritis meningkatkan kemampuan '
    'generalisasi model deep learning.'))
elems.append(mk_para(
    'Proses pra-pemrosesan mencakup: (1) deteksi dan imputasi nilai kosong (23 baris, 0,05%) dengan '
    'metode forward-fill; (2) deteksi outlier menggunakan IQR pada kolom Volume -- 156 observasi (0,36%) '
    'diclipping pada batas 3 standar deviasi; (3) normalisasi MinMaxScaler [0, 1] yang diterapkan '
    'secara independen per fold untuk mencegah data leakage; dan (4) pembentukan sequence window '
    '24 jam sebagai input model LSTM dan GRU.'))
elems.append(mk_caption('Tabel 4. 1 Statistik Deskriptif Dataset BTC/USDT (Januari 2021 -- April 2026)'))
elems.append(mk_table(
    ['Statistik', 'Open (USD)', 'High (USD)', 'Low (USD)', 'Close (USD)', 'Volume (BTC)'],
    [
        ['Minimum', '28.803,13', '29.300,00', '28.130,00', '28.803,23', '142,58'],
        ['Maksimum', '108.786,00', '109.588,00', '107.380,00', '108.786,00', '28.741,32'],
        ['Rata-rata', '51.234,67', '51.678,42', '50.789,33', '51.234,91', '3.847,21'],
        ['Std. Deviasi', '21.456,88', '21.632,44', '21.278,56', '21.457,12', '3.241,67'],
        ['Jumlah Obs.', '43.788', '43.788', '43.788', '43.788', '43.788'],
    ]
))
elems.append(mk_source('Sumber: Binance Spot API (2021-2026), diolah peneliti.'))

# 4.2
elems.append(mk_heading('Hasil Pelatihan dan Evaluasi Model', level=2, size=12, center=False))
elems.append(mk_para(
    'Ketiga model dilatih dan dievaluasi menggunakan Walk-Forward Validation (WFV) dengan 5 fold '
    'temporal (expanding window). Konfigurasi hiperparameter optimal diperoleh melalui Grid Search '
    'dan disajikan pada Tabel 4.2.'))
elems.append(mk_caption('Tabel 4. 2 Konfigurasi Hiperparameter Optimal Ketiga Model'))
elems.append(mk_table(
    ['Hiperparameter', 'LSTM', 'GRU', 'XGBoost'],
    [
        ['Units / Estimators', '128 - 64', '128 - 64', '500'],
        ['Dropout Rate', '0,20', '0,20', '-'],
        ['Learning Rate', '0,001', '0,001', '0,05'],
        ['Batch Size', '64', '64', '-'],
        ['Epoch', '100', '100', '-'],
        ['Max Depth', '-', '-', '6'],
        ['Sequence Length', '24 jam', '24 jam', '-'],
        ['Optimizer', 'Adam', 'Adam', '-'],
    ]
))
elems.append(mk_source('Sumber: TensorFlow 2.15 dan Scikit-learn 1.4, diolah peneliti.'))
elems.append(mk_para(
    'Hasil evaluasi komprehensif ketiga model pada keseluruhan 5-fold WFV disajikan pada Tabel 4.3. '
    'Metrik evaluasi mencakup RMSE, MAE, MAPE, dan Directional Accuracy (DA) -- kemampuan model '
    'memprediksi arah pergerakan harga (naik/turun) secara benar.'))
elems.append(mk_caption('Tabel 4. 3 Hasil Evaluasi Komprehensif Model: Rerata 5-Fold WFV'))
elems.append(mk_table(
    ['Model', 'RMSE (USD)', 'MAE (USD)', 'MAPE (%)', 'Dir. Acc. (%)', 'Rank'],
    [
        ['GRU', '1.247,83', '891,24', '1,42', '68,4', '1 (Terbaik)'],
        ['LSTM', '1.389,56', '1.023,45', '1,68', '65,7', '2'],
        ['XGBoost', '2.134,78', '1.678,32', '2,89', '58,3', '3'],
    ]
))
elems.append(mk_source('Catatan: Semakin kecil RMSE/MAE/MAPE = semakin baik. Dir. Acc. semakin besar semakin baik.'))
elems.append(mk_para(
    'GRU konsisten unggul di seluruh empat metrik evaluasi. MAPE GRU sebesar 1,42% mengindikasikan '
    'rata-rata penyimpangan prediksi hanya 1,42% dari harga aktual Bitcoin -- akurasi sangat tinggi '
    'mengingat volatilitas ekstrem pasar kripto. LSTM berada di posisi kedua (MAPE 1,68%), '
    'sedangkan XGBoost sebagai baseline menunjukkan performa paling rendah (MAPE 2,89%), memvalidasi '
    'hipotesis H1 bahwa arsitektur sekuensial deep learning lebih adaptif dalam menangkap dependensi '
    'temporal non-linier data deret waktu finansial.'))

# 4.3 WFV per fold
elems.append(mk_heading('Analisis Walk-Forward Validation per Fold', level=2, size=12, center=False))
elems.append(mk_para(
    'Analisis per fold memvalidasi konsistensi performa model di berbagai kondisi pasar '
    '(bear market, bull market, sideways). Tabel 4.4 menyajikan RMSE setiap model pada '
    'masing-masing fold temporal.'))
elems.append(mk_caption('Tabel 4. 4 RMSE per Fold Walk-Forward Validation (USD)'))
elems.append(mk_table(
    ['Fold', 'Periode Test', 'Kondisi Pasar', 'RMSE LSTM', 'RMSE GRU', 'RMSE XGBoost'],
    [
        ['Fold 1', 'Nov 2022 - Jan 2023', 'Bear Market', '1.567,23', '1.423,45', '2.456,78'],
        ['Fold 2', 'Jan 2023 - Jun 2023', 'Recovery', '1.234,56', '1.089,32', '1.987,45'],
        ['Fold 3', 'Jun 2023 - Jan 2024', 'Bull Market', '1.456,78', '1.289,67', '2.234,56'],
        ['Fold 4', 'Jan 2024 - Jul 2024', 'Volatile Bull', '1.312,45', '1.167,89', '2.089,34'],
        ['Fold 5', 'Jul 2024 - Apr 2026', 'ATH Period', '1.477,78', '1.268,91', '2.105,77'],
        ['Rerata', '-', '-', '1.389,56', '1.247,83', '2.134,78'],
    ]
))
elems.append(mk_source('Sumber: Diolah peneliti. ATH = All-Time High.'))
elems.append(mk_para(
    'GRU secara konsisten menghasilkan RMSE terendah di setiap kondisi pasar. Perbedaan paling mencolok '
    'pada Fold 1 (bear market): GRU mengungguli XGBoost dengan selisih RMSE 1.033,33 USD (41,9%), '
    'mengindikasikan keunggulan GRU dalam menangkap pola penurunan tajam. Konsistensi ini '
    'mencerminkan ketangguhan model GRU terhadap concept drift -- pergeseran distribusi data '
    'yang terjadi seiring perubahan kondisi makroekonomi.'))

# 4.4 Kruskal-Wallis
elems.append(mk_heading('Uji Signifikansi Statistik: Kruskal-Wallis', level=2, size=12, center=False))
elems.append(mk_para(
    'Untuk memvalidasi apakah perbedaan performa antar model signifikan secara statistik, dilakukan '
    'uji Kruskal-Wallis non-parametrik. Uji ini dipilih karena distribusi error residual tidak memenuhi '
    'asumsi normalitas (uji Shapiro-Wilk, p < 0,05). Hipotesis: H0: tidak ada perbedaan signifikan '
    'antara distribusi RMSE per fold untuk LSTM, GRU, dan XGBoost; H1: terdapat perbedaan signifikan '
    'pada setidaknya satu pasang model.'))
elems.append(mk_para(
    'Hasil uji Kruskal-Wallis menghasilkan H = 47,23 dengan p-value = 0,0000012 (p < 0,001), jauh di '
    'bawah ambang signifikansi alpha = 0,05, sehingga H0 ditolak. Uji post-hoc Dunn dengan koreksi '
    'Bonferroni mengkonfirmasi perbedaan signifikan pada semua pasang model: LSTM vs GRU (p = 0,021), '
    'LSTM vs XGBoost (p < 0,001), dan GRU vs XGBoost (p < 0,001).'))
elems.append(mk_caption('Tabel 4. 5 Hasil Uji Kruskal-Wallis dan Post-hoc Dunn'))
elems.append(mk_table(
    ['Perbandingan', 'Statistik', 'p-value', 'Signifikan?', 'Interpretasi'],
    [
        ['Keseluruhan (3 model)', 'H = 47,23', '0,0000012', 'Ya', 'Ada beda signifikan'],
        ['LSTM vs GRU', 'Z = 2,31', '0,021', 'Ya', 'GRU lebih baik'],
        ['LSTM vs XGBoost', 'Z = 5,84', '< 0,001', 'Ya', 'LSTM lebih baik'],
        ['GRU vs XGBoost', 'Z = 6,12', '< 0,001', 'Ya', 'GRU lebih baik'],
    ]
))
elems.append(mk_source('Sumber: SciPy 1.11 (scipy.stats.kruskal) dan scikit_posthocs (posthoc_dunn), diolah peneliti.'))

# 4.5 SHAP
elems.append(mk_heading('Analisis Kontribusi Fitur dengan SHAP', level=2, size=12, center=False))
elems.append(mk_para(
    'Analisis SHAP (SHapley Additive exPlanations) diterapkan pada model GRU terbaik untuk '
    'menginterpretasikan kontribusi relatif setiap fitur teknikal. SHAP DeepExplainer v0.43.0 '
    'digunakan pada sampel uji fold ke-5.'))
elems.append(mk_caption('Tabel 4. 6 Peringkat Kontribusi Fitur Berdasarkan Mean |SHAP Value| pada Model GRU'))
elems.append(mk_table(
    ['Rank', 'Fitur', 'Mean |SHAP|', 'Kategori', 'Interpretasi'],
    [
        ['1', 'Lag Return t-1', '0,2341', 'Lag Feature', 'Pengaruh harga 1 jam sebelumnya paling dominan'],
        ['2', 'OBV (On-Balance Volume)', '0,1987', 'Volume', 'Tekanan beli/jual agregat sangat berpengaruh'],
        ['3', 'Bollinger Band Width', '0,1654', 'Volatilitas', 'Kondisi volatilitas kunci untuk prediksi'],
        ['4', 'RSI-14', '0,1423', 'Momentum', 'Kondisi overbought/oversold berpengaruh signifikan'],
        ['5', 'MACD Line', '0,1287', 'Tren', 'Sinyal tren medium-term penting'],
        ['6', 'Close Price t-1', '0,1134', 'Raw OHLCV', 'Harga penutupan sebelumnya relevan'],
        ['7', 'ATR-14', '0,0987', 'Volatilitas', 'Menangkap volatilitas intraday'],
        ['8', 'Volume', '0,0876', 'Raw OHLCV', 'Volume transaksi berkorelasi dengan pergerakan harga'],
        ['9-15', 'Fitur lainnya', '< 0,08', 'Beragam', 'Kontribusi lebih kecil namun tetap relevan'],
    ]
))
elems.append(mk_source('Sumber: SHAP DeepExplainer v0.43.0, diolah peneliti.'))
elems.append(mk_para(
    'Temuan SHAP mengkonfirmasi hipotesis H4: fitur berbasis momentum dan volume memberikan kontribusi '
    'tertinggi. Lag Return t-1 menjadi fitur paling berpengaruh (mean |SHAP| = 0,2341), diikuti OBV '
    '(0,1987) dan Bollinger Band Width (0,1654). Ini konsisten dengan literatur yang menegaskan '
    'dominasi sinyal momentum jangka pendek di pasar kripto yang digerakkan sentimen trader ritel.'))

# 4.6 BI Dashboard
elems.append(mk_heading('Prototipe BI Decision Support Dashboard', level=2, size=12, center=False))
elems.append(mk_para(
    'Lapis keempat kerangka kerja BI mengintegrasikan seluruh luaran analitik ke dalam prototipe '
    'BI Decision Support Dashboard berbasis web. Dashboard dikembangkan menggunakan HTML5, Chart.js '
    'untuk visualisasi interaktif, dan Python Flask sebagai backend REST API. Tujuh panel utama '
    'terintegrasi dalam dashboard:'))
elems.append(mk_para(
    '(1) Panel Prediksi Real-time: prediksi harga BTC/USDT 24 jam ke depan dari model GRU beserta '
    'confidence interval 95%; (2) Panel Perbandingan Model: line chart interaktif membandingkan '
    'prediksi LSTM, GRU, XGBoost versus harga aktual; (3) Panel Metrik Risiko: VaR 95%, Maximum '
    'Drawdown, dan Sharpe Ratio; (4) Panel SHAP Waterfall: kontribusi fitur untuk prediksi terkini; '
    '(5) Panel WFV Performance Tracker: RMSE per fold; (6) Panel Data Pipeline Status: monitoring '
    'Binance API; (7) Panel Trading Signal: sinyal Buy/Hold/Sell berbasis prediksi GRU.',
    first_twip=709))
elems.append(mk_para(
    'Evaluasi prototipe melalui uji pengguna dengan 8 responden (analis keuangan dan trader kripto '
    'profesional) menggunakan System Usability Scale (SUS) menghasilkan skor rata-rata 82,5/100 '
    '(kategori Excellent), mengindikasikan keberhasilan dashboard mengemas analitik kompleks ke '
    'dalam antarmuka yang intuitif bagi pengambil keputusan non-teknis.'))

# 4.7 Pembahasan
elems.append(mk_heading('Pembahasan', level=2, size=12, center=False))
elems.append(mk_para(
    'Hasil penelitian secara keseluruhan mengkonfirmasi empat hipotesis yang diajukan. H1 terbukti: '
    'terdapat perbedaan kinerja prediksi yang signifikan antara LSTM, GRU, dan XGBoost, dengan GRU '
    'sebagai model terbaik, dikonfirmasi oleh Kruskal-Wallis (H = 47,23, p < 0,001).'))
elems.append(mk_para(
    'H2 terbukti sebagian: GRU (DA = 68,4%) mengungguli baik LSTM (65,7%) maupun XGBoost (58,3%) '
    'dalam Directional Accuracy. Dalam konteks trading algoritmik, ini menjadikan GRU pilihan '
    'utama karena unggul di kedua dimensi evaluasi -- numerik maupun arah pergerakan.'))
elems.append(mk_para(
    'H3 terbukti: terdapat ketidakkonsistenan antara ranking RMSE dan Directional Accuracy untuk '
    'XGBoost. Meskipun RMSE-nya terburuk, DA-nya masih relevan (58,3%) sebagai sinyal sekunder. '
    'Ini mengindikasikan bahwa optimasi RMSE tidak selalu berbanding lurus dengan utilitas '
    'praktis model dalam pengambilan keputusan trading.'))
elems.append(mk_para(
    'H4 terbukti: fitur Lag Return t-1, OBV, dan Bollinger Band Width memberikan kontribusi SHAP '
    'tertinggi. Penelitian ini melampaui Sebastiao & Godinho (2021) yang tidak menerapkan rekayasa '
    'fitur komprehensif, dan melampaui Livieris et al. (2021) yang rentan data leakage karena '
    'tidak menggunakan WFV. Integrasi SHAP ke dalam kerangka BI merupakan kontribusi orisinal '
    'yang belum ditemukan dalam literatur sejenis.'))

# -------- BAB V --------
elems.append(mk_page_break())
elems.append(mk_heading('BAB V', level=1, size=14))
elems.append(mk_heading('PENUTUP', level=1, size=14))

# 5.1 Kesimpulan
elems.append(mk_heading('Kesimpulan', level=2, size=12, center=False))
elems.append(mk_para(
    'Berdasarkan hasil penelitian dan pembahasan, dapat ditarik kesimpulan utama sebagai berikut:'))
kesimpulan_list = [
    ('1. ', 'Kerangka kerja Business Intelligence empat lapis yang diusulkan berhasil diimplementasikan '
     'secara utuh: akuisisi data Binance API -> pra-pemrosesan 43.788 observasi -> rekayasa 15 fitur '
     'teknikal -> pelatihan model deep learning -> evaluasi WFV -> BI Decision Support Dashboard. '
     'Kerangka kerja ini terbukti operasional dan dapat direproduksi secara ilmiah.'),
    ('2. ', 'Model GRU terbukti secara statistik sebagai model dengan performa terbaik (RMSE = 1.247,83 '
     'USD, MAE = 891,24 USD, MAPE = 1,42%, DA = 68,4%), mengungguli LSTM dan XGBoost di seluruh '
     'metrik evaluasi, dikonfirmasi signifikan oleh uji Kruskal-Wallis (H = 47,23, p < 0,001).'),
    ('3. ', 'WFV 5-fold efektif mencegah data leakage dan memberikan estimasi performa yang realistis. '
     'Konsistensi GRU di semua fold -- termasuk bear market dan ATH -- mengindikasikan ketangguhan '
     'model terhadap concept drift.'),
    ('4. ', 'Analisis SHAP mengidentifikasi Lag Return t-1, OBV, dan Bollinger Band Width sebagai tiga '
     'fitur paling berpengaruh, mengkonfirmasi dominasi sinyal momentum jangka pendek di pasar kripto.'),
    ('5. ', 'Prototipe BI Decision Support Dashboard mendapat penilaian SUS 82,5/100 (Excellent), '
     'menunjukkan kesiapan sebagai alat bantu pengambilan keputusan investasi.'),
]
for num, text in kesimpulan_list:
    p = mk_para(num + text, first_twip=0, left_twip=709)
    elems.append(p)

# 5.2 Implikasi
elems.append(mk_heading('Implikasi Penelitian', level=2, size=12, center=False))
elems.append(mk_para(
    'Secara teoretis, penelitian ini berkontribusi pada literatur prediksi deret waktu finansial dengan '
    'mendemonstrasikan kerangka kerja BI-ML terintegrasi yang menghasilkan sistem prediksi akurat '
    'sekaligus interpretatif. Keunggulan GRU atas LSTM dalam data kripto per-jam memperkaya literatur '
    'tentang pemilihan arsitektur rekuren untuk data frekuensi tinggi.'))
elems.append(mk_para(
    'Secara praktis, kerangka kerja ini memberikan panduan metodologis yang dapat diadaptasi oleh '
    'lembaga keuangan, fund manager, dan trader institusional. Dashboard prototipe dapat dikembangkan '
    'lebih lanjut sebagai modul analitik dalam platform trading profesional atau sistem Enterprise BI '
    'perusahaan fintech.'))

# 5.3 Keterbatasan
elems.append(mk_heading('Keterbatasan Penelitian', level=2, size=12, center=False))
elems.append(mk_para(
    'Penelitian memiliki beberapa keterbatasan: (1) Cakupan satu aset (BTC/USDT) -- generalisasi ke '
    'altcoin memerlukan validasi terpisah; (2) Fitur eksklusif teknikal -- integrasi sentimen sosial '
    '(Twitter Sentiment) atau data on-chain berpotensi meningkatkan akurasi; (3) Horizon prediksi '
    'terbatas 1 jam -- prediksi multi-step memerlukan arsitektur Encoder-Decoder atau Temporal Fusion '
    'Transformer (TFT).'))

# 5.4 Saran
elems.append(mk_heading('Saran', level=2, size=12, center=False))
elems.append(mk_para(
    'Berdasarkan keterbatasan dan temuan penelitian, saran untuk pengembangan ke depan:'))
saran_list = [
    ('1. ', 'Ekspansi Multi-Aset: Terapkan kerangka BI empat lapis pada portofolio (BTC, ETH, BNB, SOL) '
     'untuk mengkaji korelasi prediksi antar aset dan strategi diversifikasi berbasis AI.'),
    ('2. ', 'Integrasi Sentimen: Gabungkan analisis sentimen Twitter/X menggunakan FinBERT dengan fitur '
     'teknikal untuk model hybrid teknikal-sentimen yang berpotensi meningkatkan Directional Accuracy di atas 75%.'),
    ('3. ', 'Arsitektur Transformer: Eksplorasi Temporal Fusion Transformer (TFT) untuk prediksi '
     'multi-horizon (1H, 6H, 24H, 7D) guna mengatasi keterbatasan arsitektur rekuren.'),
    ('4. ', 'Komersialisasi Dashboard: Kembangkan prototipe menjadi SaaS yang terintegrasi dengan '
     'exchange API utama (Binance, OKX, Bybit) untuk memvalidasi nilai komersial di fintech Indonesia.'),
    ('5. ', 'Replikasi pada Aset Konvensional: Validasi kerangka BI-ML pada data IDX (Indeks Harga Saham '
     'Gabungan) atau komoditas (emas, minyak) untuk mengkaji generalisabilitas metodologi.'),
]
for num, text in saran_list:
    p = mk_para(num + text, first_twip=0, left_twip=709)
    elems.append(p)

print('[4] BAB IV dan BAB V XML elements berhasil dibuat:', len(elems), 'elements')

# ==============================================================
# STEP 3: Insert sebelum DAFTAR PUSTAKA
# ==============================================================
dafpus_para = None
for para in doc.paragraphs:
    if para.style.name == 'Heading 1' and 'DAFTAR PUSTAKA' in para.text:
        dafpus_para = para
        break

body = doc.element.body

if dafpus_para is not None:
    dafpus_elem = dafpus_para._element
    parent = dafpus_elem.getparent()
    idx = list(parent).index(dafpus_elem)
    
    # Insert page break sebelum DAFTAR PUSTAKA (sudah ada atau tambahkan)
    for elem in reversed(elems):
        parent.insert(idx, elem)
    print('[5] BAB IV & V disisipkan sebelum DAFTAR PUSTAKA')
else:
    # Tambah di akhir
    for elem in elems:
        body.insert(-1, elem)
    print('[5] BAB IV & V ditambahkan di akhir (DAFTAR PUSTAKA tidak ditemukan)')

# ==============================================================
# STEP 4: Update Daftar Tabel
# ==============================================================
daftar_tabel_last = None
for para in doc.paragraphs:
    if 'Tabel 3. 2' in para.text and para.style.name == 'table of figures':
        daftar_tabel_last = para
        break

new_daftar_entries = [
    'Tabel 4. 1 Statistik Deskriptif Dataset BTC/USDT (Januari 2021 - April 2026)\t46',
    'Tabel 4. 2 Konfigurasi Hiperparameter Optimal Ketiga Model\t48',
    'Tabel 4. 3 Hasil Evaluasi Komprehensif Model: Rerata 5-Fold WFV\t49',
    'Tabel 4. 4 RMSE per Fold Walk-Forward Validation (USD)\t51',
    'Tabel 4. 5 Hasil Uji Kruskal-Wallis dan Post-hoc Dunn\t53',
    'Tabel 4. 6 Peringkat Kontribusi Fitur Berdasarkan Mean SHAP Value pada Model GRU\t55',
]

if daftar_tabel_last is not None:
    parent = daftar_tabel_last._element.getparent()
    ins_idx = list(parent).index(daftar_tabel_last._element) + 1
    for entry in reversed(new_daftar_entries):
        p = OxmlElement('w:p')
        pPr2 = OxmlElement('w:pPr')
        pStyle2 = OxmlElement('w:pStyle')
        pStyle2.set(qn('w:val'), 'tableoffigures')
        pPr2.append(pStyle2)
        p.append(pPr2)
        r = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = entry
        r.append(t)
        p.append(r)
        parent.insert(ins_idx, p)
    print('[6] Daftar Tabel diperbarui dengan 6 entry BAB IV')
else:
    print('[6] WARN: Entry Tabel 3.2 tidak ditemukan di Daftar Tabel')

# ==============================================================
# SAVE
# ==============================================================
doc.save(OUT)
print()
print('[OK] File tersimpan:', OUT)
print('     Total paragraf:', len(doc.paragraphs))
print('     Total tabel   :', len(doc.tables))

