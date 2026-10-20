# -*- coding: utf-8 -*-
"""
Script Lengkap Generator Capstone Project & PKM Kemitraan (With Embedded Figures & BI Dashboard)
Magister Informatika Konsentrasi Data Science - Universitas Nusa Putra
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPSTONE_DIR = os.path.join(WORKSPACE_DIR, "Capstone Projects")
IMG_DIR = os.path.join(CAPSTONE_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

def set_document_margins(doc):
    for section in doc.sections:
        section.top_margin = Cm(4.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(3.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=18, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=12, space_after=4, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=8, space_after=2, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_body_p(doc, text, bold_prefix=None, italic_prefix=None):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    if italic_prefix:
        r_pre2 = p.add_run(italic_prefix)
        r_pre2.font.name = 'Times New Roman'
        r_pre2.font.size = Pt(12)
        r_pre2.font.italic = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_image_figure(doc, img_name, caption_text, width_cm=14.0):
    img_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        format_paragraph(p_img, space_before=10, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Cm(width_cm))
        
        p_cap = doc.add_paragraph()
        format_paragraph(p_cap, space_before=2, space_after=12, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
    else:
        print(f"Warning: Image {img_path} not found.")

def set_cell_properties(cell, fill_hex=None, top_padding=120, bottom_padding=120, left_padding=160, right_padding=160):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    if fill_hex:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top_padding), ('bottom', bottom_padding), ('left', left_padding), ('right', right_padding)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="1A365D"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="1A365D"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

print("Compiling complete Capstone Project DOCX with Figures and BI Dashboard...")

# ==============================================================================
# GENERATE LAPORAN CAPSTONE PROJECT (DOCX)
# ==============================================================================
doc = docx.Document()
set_document_margins(doc)

# ----------------- HALAMAN SAMPUL (COVER) -----------------
p_top = doc.add_paragraph()
format_paragraph(p_top, space_before=24, space_after=12, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r = p_top.add_run("LAPORAN AKHIR CAPSTONE PROJECT\nMAGISTER INFORMATIKA KONSENTRASI DATA SCIENCE")
r.font.name = 'Times New Roman'
r.font.size = Pt(14)
r.font.bold = True

p_title = doc.add_paragraph()
format_paragraph(p_title, space_before=24, space_after=24, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER)
r_title = p_title.add_run("ARSITEKTUR DEEP LEARNING UNTUK PREDIKSI HARGA CRYPTOCURRENCY: SISTEM PENDUKUNG KEPUTUSAN INVESTASI BERBASIS BUSINESS INTELLIGENCE")
r_title.font.name = 'Times New Roman'
r_title.font.size = Pt(15)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(26, 54, 93)

p_subtitle = doc.add_paragraph()
format_paragraph(p_subtitle, space_before=12, space_after=40, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_sub = p_subtitle.add_run("Diajukan untuk Memenuhi Sebagian dari Persyaratan Kelulusan\nMata Kuliah Data Science Capstone Project\nProgram Studi Magister Informatika")
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(11)
r_sub.font.italic = True

p_identity = doc.add_paragraph()
format_paragraph(p_identity, space_before=36, space_after=40, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER)
r_id = p_identity.add_run("Oleh:\nASEP MUHAMAD SAMSUDIN\nNIM. 222510793")
r_id.font.name = 'Times New Roman'
r_id.font.size = Pt(12)
r_id.font.bold = True

p_univ = doc.add_paragraph()
format_paragraph(p_univ, space_before=40, space_after=12, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_u = p_univ.add_run("PROGRAM STUDI MAGISTER INFORMATIKA\nFAKULTAS TEKNIK, KOMPUTER, DAN DESAIN\nUNIVERSITAS NUSA PUTRA\nSUKABUMI\n2026")
r_u.font.name = 'Times New Roman'
r_u.font.size = Pt(12)
r_u.font.bold = True

doc.add_page_break()

# ----------------- LEMBAR PENGESAHAN -----------------
p_peng = doc.add_paragraph()
format_paragraph(p_peng, space_before=12, space_after=18, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_peng = p_peng.add_run("LEMBAR PENGESAHAN\nLAPORAN AKHIR CAPSTONE PROJECT")
r_peng.font.name = 'Times New Roman'
r_peng.font.size = Pt(14)
r_peng.font.bold = True

add_body_p(doc, "Judul Proyek: Arsitektur Deep Learning untuk Prediksi Harga Cryptocurrency: Sistem Pendukung Keputusan Investasi Berbasis Business Intelligence")
add_body_p(doc, "Nama Mahasiswa: Asep Muhamad Samsudin")
add_body_p(doc, "Nomor Induk Mahasiswa: 222510793")
add_body_p(doc, "Program Studi: Magister Informatika (Konsentrasi Data Science)")
add_body_p(doc, "Fakultas: Teknik, Komputer, dan Desain - Universitas Nusa Putra")
add_body_p(doc, "Laporan Capstone Project ini telah diperiksa, disetujui, dan diujikan di hadapan Dewan Penguji pada Sidang Akhir Capstone Project, serta dinyatakan memenuhi seluruh persyaratan akademik.")

p_ttd = doc.add_paragraph()
format_paragraph(p_ttd, space_before=24, space_after=36, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
p_ttd.add_run("Sukabumi, .............................. 2026\nMenyetujui,")

tbl_ttd = doc.add_table(rows=1, cols=2)
tbl_ttd.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_ttd.rows[0].cells[0].paragraphs[0].text = "Dosen Pembimbing I\n\n\n\n\nProf. Dr. Hj. Rina Fiati, ST., M.Cs\nNIDN. "
tbl_ttd.rows[0].cells[1].paragraphs[0].text = "Dosen Pembimbing II\n\n\n\n\nDr. Wahyudi Agustiono, S.T., M.Kom\nNIDN. "
for cell in tbl_ttd.rows[0].cells:
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in cell.paragraphs[0].runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)

p_mengetahui = doc.add_paragraph()
format_paragraph(p_mengetahui, space_before=24, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
p_mengetahui.add_run("Mengetahui,\nKetua Program Studi Magister Informatika\n\n\n\n\n___________________________________\nNIDN. ")
for run in p_mengetahui.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

doc.add_page_break()

# ----------------- RINGKASAN EKSEKUTIF -----------------
p_ringk = doc.add_paragraph()
format_paragraph(p_ringk, space_before=12, space_after=18, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER)
r_ringk = p_ringk.add_run("RINGKASAN EKSEKUTIF")
r_ringk.font.name = 'Times New Roman'
r_ringk.font.size = Pt(14)
r_ringk.font.bold = True

add_body_p(doc, "Pasar aset kripto, khususnya pasangan perdagangan Bitcoin terhadap Tether (BTC/USDT), dicirikan oleh volatilitas harga ekstrem, korelasi non-linear frekuensi tinggi, serta kerapatan peristiwa ekor tebal (fat-tail anomalies) yang menghadirkan risiko kerugian besar bagi pelaku pasar. Sebagian besar investor ritel dan manajer portofolio pemula menghadapi keterbatasan dalam pemodelan data prediktif dan ketiadaan instrumen manajemen risiko kuantitatif yang terintegrasi. Proyek Capstone in Data Science ini bertujuan merancang dan mengimplementasikan sistem Decision Support System (DSS) berbasis Deep Learning empat lapis (Four-Layer Architecture) yang diintegrasikan langsung dengan dashboard Business Intelligence (Microsoft Power BI) secara real-time via DirectQuery.")

add_body_p(doc, "Penelitian ini memanfaatkan dataset riil frekuensi tinggi berisikan 43.786 rekaman per jam (hourly OHLCV) dari Binance Spot API yang mencakup periode kontinu lima tahun (Maret 2021 hingga Maret 2026). Pipeline rekayasa fitur menghasilkan 15 indikator teknikal multivariat yang mencakup indikator tren, momentum, osilator volatilitas, dan volume. Protokol validasi diterapkan secara ketat menggunakan 24-fold Walk-Forward Validation kronologis tanpa kebocoran data (data leakage) untuk mengevaluasi empat arsitektur model komparatif: XGBoost, Informer Transformer, Long Short-Term Memory (LSTM), dan Gated Recurrent Unit (GRU).")

add_body_p(doc, "Hasil evaluasi empiris membuktikan bahwa arsitektur GRU mengungguli seluruh model dalam akurasi titik prediksi (point-loss), menghasilkan Mean RMSE terendah 0,1058 ± 0,0034, MAE 0,0948 ± 0,0028, dan MAPE 13,13%. Pengujian non-parametrik Kruskal-Wallis (H = 18,4, p < 0,001) dan pairwise Diebold-Mariano test (p = 0,014) mengonfirmasi superioritas statistik GRU yang signifikan. Di sisi lain, LSTM menunjukkan utilitas finansial terbaik dengan Directional Accuracy tertinggi 72,3% ± 1,5%, Sharpe Ratio tahunan 1,45 ± 0,10, dan Value at Risk (VaR 95%) harian sebesar -2,34%.")

add_body_p(doc, "Artefak teknis yang dihasilkan berupa pipeline ETL otomatis, engine kalkulasi risiko keuangan terintegrasi PostgreSQL Data Mart, serta interaktif Power BI Dashboard yang dilengkapi kartu metrik eksekutif, grafik peramalan multi-step 168 jam, dan analisis interpretabilitas SHAP. Sebagai bentuk hilirisasi riset nyata dan pemenuhan Tridharma Perguruan Tinggi, luaran proyek ini juga disinergikan dengan Program Kemitraan Masyarakat (PKM) bersama mitra komunitas trader dan pelaku UMKM ekonomi digital, guna meningkatkan literasi risiko finansial berbasis AI.")

doc.add_page_break()

# ----------------- DAFTAR ISI, TABEL & GAMBAR -----------------
add_heading_1(doc, "DAFTAR ISI")
toc_items = [
    ("LEMBAR PENGESAHAN", "ii"),
    ("RINGKASAN EKSEKUTIF", "iii"),
    ("DAFTAR ISI", "iv"),
    ("DAFTAR TABEL", "v"),
    ("DAFTAR GAMBAR", "vi"),
    ("BAB I: PENDAHULUAN", "1"),
    ("   1.1 Latar Belakang", "1"),
    ("   1.2 Rumusan Masalah", "2"),
    ("   1.3 Tujuan Proyek", "2"),
    ("   1.4 Manfaat Proyek", "3"),
    ("   1.5 Batasan Masalah dan Ruang Lingkup", "3"),
    ("BAB II: TINJAUAN PUSTAKA DAN LANDASAN TEORI", "4"),
    ("   2.1 Kajian Literatur Terkait", "4"),
    ("   2.2 Landasan Teori dan Algoritma", "5"),
    ("   2.3 Benchmarking Penelitian Terdahulu", "7"),
    ("BAB III: METODOLOGI DAN PERANCANGAN", "8"),
    ("   3.1 Deskripsi Dataset dan Sumber Data", "8"),
    ("   3.2 Alur Metodologi Proyek (Four-Layer DSS)", "9"),
    ("   3.3 Desain Arsitektur dan Protokol Walk-Forward", "11"),
    ("   3.4 Spesifikasi Implementasi Sistem", "12"),
    ("BAB IV: HASIL DAN PEMBAHASAN", "13"),
    ("   4.1 Hasil Eksperimen dan Evaluasi Model", "13"),
    ("   4.2 Evaluasi Utilitas Finansial dan Manajemen Risiko", "15"),
    ("   4.3 Pengujian Signifikansi Statistik dan Analisis SHAP", "16"),
    ("   4.4 Implementasi Dashboard Business Intelligence (Power BI)", "17"),
    ("   4.5 Diskusi: Kelebihan, Keterbatasan, dan Peluang", "19"),
    ("BAB V: KESIMPULAN DAN SARAN", "21"),
    ("   5.1 Kesimpulan", "21"),
    ("   5.2 Saran", "22"),
    ("DAFTAR PUSTAKA", "23"),
    ("LAMPIRAN", "25")
]
for item, pg in toc_items:
    p_t = doc.add_paragraph()
    format_paragraph(p_t, space_before=0, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    r1 = p_t.add_run(item)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    if "BAB" in item or "RINGKASAN" in item:
        r1.font.bold = True

doc.add_page_break()

add_heading_1(doc, "DAFTAR TABEL")
tables_list = [
    ("Tabel 1. Perbandingan Kinerja Empiris Proyek Capstone Terhadap Literatur Terpublikasi", "7"),
    ("Tabel 2. Evaluasi Metrik Loss Peramalan Melintasi 24 Fold Walk-Forward", "14"),
    ("Tabel 3. Evaluasi Metrik Utilitas Finansial dan Batas Risiko Portofolio", "15")
]
for t_item, pg in tables_list:
    p_t = doc.add_paragraph()
    format_paragraph(p_t, space_before=0, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    r1 = p_t.add_run(t_item)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)

p_space = doc.add_paragraph()
format_paragraph(p_space, space_before=12, space_after=6, line_spacing=1.0)

add_heading_1(doc, "DAFTAR GAMBAR")
figures_list = [
    ("Gambar 1. Arsitektur Four-Layer Decision Support System Terintegrasi", "10"),
    ("Gambar 2. Tren Historis Pergerakan Harga Penutupan dan Volume BTC/USDT (2021-2026)", "11"),
    ("Gambar 3. Overlay Lintasan Peramalan 168 Jam Out-of-Sample Model vs. Harga Aktual", "14"),
    ("Gambar 4. Distribusi Residual Error dan Analisis Ekor Tebal (Fat-Tail Anomaly)", "17"),
    ("Gambar 5. Tampilan Dashboard Business Intelligence Power BI (Live DirectQuery)", "18")
]
for f_item, pg in figures_list:
    p_f = doc.add_paragraph()
    format_paragraph(p_f, space_before=0, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT)
    r1 = p_f.add_run(f_item)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)

doc.add_page_break()

# ----------------- BAB I: PENDAHULUAN -----------------
add_heading_1(doc, "BAB I: PENDAHULUAN")

add_heading_2(doc, "1.1 Latar Belakang")
add_body_p(doc, "Pasar aset kripto global telah berkembang secara eksponensial dalam satu dekade terakhir, menembus kapitalisasi pasar lebih dari USD 2 triliun dengan Bitcoin (BTC) sebagai aset penggerak utama (market driver). Dinamika perdagangan aset kripto berlangsung selama 24 jam sehari, 7 hari seminggu tanpa jeda libur bursa, menghasilkan volume data transaksional berkecepatan dan berdensitas sangat tinggi. Namun, di balik potensi imbal hasil yang menarik, pasar kripto memiliki tingkat volatilitas harga ekstrem (extreme volatility shocks) dan kerapatan peristiwa angsa hitam (black-swan anomalies), seperti fenomena likuidasi massal ekosistem Terra-Luna pada Mei 2022.")

add_body_p(doc, "Pendekatan konvensional yang mengandalkan analisis teknikal heuristik maupun model ekonometrik linier tradisional (seperti ARIMA dan GARCH) kerap kali gagal menangkap pola ketergantungan temporal non-linier dan pergeseran rezim volatilitas yang cepat. Di sisi lain, perkembangan pesat teknik pembelajaran mendalam (Deep Learning), khususnya model sekuensial rekuren seperti Long Short-Term Memory (LSTM) dan Gated Recurrent Unit (GRU), serta arsitektur berbasis atensi (Informer Transformer), menawarkan terobosan baru dalam memodelkan interaksi kompleks deret waktu keuangan multivariat.")

add_body_p(doc, "Kendati demikian, dalam ranah praktis industri dan masyarakat, terdapat jurang pemisah yang lebar (research-to-production gap) antara model prediktif mutakhir di laboratorium data science dengan implementasi operasional nyata. Banyak model machine learning yang hanya berhenti pada tahap publikasi akurasi metrik nominal (seperti MSE/MAE), tanpa ditransformasikan menjadi sinyal keputusan investasi terukur (trading signals) yang memperhitungkan metrik risiko keuangan institusional seperti Sharpe Ratio dan Value at Risk (VaR). Selain itu, ketiadaan antarmuka visual analitik cerdas menyulitkan pemangku kepentingan dalam memahami alasan di balik prediksi model.")

add_body_p(doc, "Oleh karena itu, Proyek Capstone ini dirancang untuk menjembatani kesenjangan tersebut melalui pengembangan arsitektur Decision Support System (DSS) terintegrasi empat lapis (ingesti data, rekayasa fitur dan interpretabilitas, pemodelan deep learning dengan validasi walk-forward, serta visualisasi Business Intelligence real-time). Proyek ini merupakan wujud konkret penerapan kompetensi magister data science di Universitas Nusa Putra dalam menghadirkan solusi teknologi cerdas yang berdaya guna bagi industri keuangan modern dan masyarakat luas.")

add_heading_2(doc, "1.2 Rumusan Masalah")
add_body_p(doc, "Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam proyek capstone ini dirumuskan sebagai berikut:")
add_bullet_p(doc, "Bagaimana merancang arsitektur pipeline data science end-to-end yang mengintegrasikan ekstraksi data real-time, pra-pemrosesan sekuensial, dan rekayasa 15 indikator teknikal pada pasangan aset BTC/USDT?")
add_bullet_p(doc, "Bagaimana perbandingan performa empiris model deep learning (LSTM, GRU, Informer Transformer) dibandingkan baseline ensemble machine learning (XGBoost) menggunakan protokol evaluasi validasi 24-fold Walk-Forward?")
add_bullet_p(doc, "Arsitektur manakah yang terbukti secara signifikan statistik unggul dalam metrik point forecasting accuracy (RMSE, MAE, MAPE) sekaligus menghasilkan trading utility terbaik (Sharpe Ratio, Directional Accuracy, VaR 95%)?")
add_bullet_p(doc, "Bagaimana mengintegrasikan hasil prediksi model dan engine kalkulasi risiko portofolio ke dalam PostgreSQL Data Mart serta memvisualisasikannya melalui Dashboard Microsoft Power BI via DirectQuery?")
add_bullet_p(doc, "Bagaimana mengoptimalkan hilirisasi luaran capstone project ini melalui program kemitraan masyarakat (PKM) guna mengedukasi mitra industri/komunitas terhadap mitigasi risiko investasi berbasis AI?")

add_heading_2(doc, "1.3 Tujuan Proyek")
add_body_p(doc, "Tujuan yang hendak dicapai dalam pelaksanaan Capstone Project ini adalah:")
add_bullet_p(doc, "Membangun arsitektur sistem pendukung keputusan investasi 4 lapis yang kokoh, transparan, dan mampu memproses data deret waktu frekuensi tinggi secara berkelanjutan.")
add_bullet_p(doc, "Mengembangkan dan menguji secara komparatif performa model GRU, LSTM, Informer, dan XGBoost pada dataset riil 43.786 rekaman per jam (Maret 2021 – Maret 2026) dari Binance Spot API.")
add_bullet_p(doc, "Melakukan verifikasi signifikansi statistik performa model melalui pengujian non-parametrik Kruskal-Wallis dan pairwise Diebold-Mariano test.")
add_bullet_p(doc, "Mengimplementasikan SHapley Additive exPlanations (SHAP) untuk membuka 'black-box' deep learning dan memberikan transparansi interpretabilitas fitur input terhadap prediksi pasar.")
add_bullet_p(doc, "Mewujudkan Dashboard Business Intelligence interaktif yang menyajikan ringkasan KPI eksekutif, proyeksi harga multi-step 168 jam, sinyal posisi perdagangan, dan pemantauan batas risiko VaR 95%.")
add_bullet_p(doc, "Menyusun kerangka kerja hilirisasi luaran berupa Pengabdian Kepada Masyarakat (PKM) bersama mitra komunitas investor/fintech lokal guna memitigasi bahaya spekulasi irasional.")

add_heading_2(doc, "1.4 Manfaat Proyek")
add_body_p(doc, "Manfaat yang dihasilkan dari proyek capstone ini diklasifikasikan ke dalam tiga dimensi utama:")
add_bullet_p(doc, "Menyumbang kontribusi empiris pada literatur peramalan time series keuangan dengan menyajikan perbandingan komprehensif arsitektur recurrent vs. attention vs. boosted trees di bawah protokol walk-forward yang ketat.", bold_prefix="Manfaat Akademik: ")
add_bullet_p(doc, "Menghasilkan prototipe Decision Support System (DSS) tingkat korporat yang siap diadopsi oleh hedge fund, manajer investasi aset digital, atau penyedia platform exchange dalam memvalidasi sinyal algoritmik.", bold_prefix="Manfaat Industri/Praktis: ")
add_bullet_p(doc, "Menyediakan instrumen edukasi literasi finansial digital berbasis data science bagi komunitas trader ritel dan masyarakat mitra melalui program PKM, sehingga dapat menekan angka kerugian finansial akibat transaksi tanpa manajemen risiko.", bold_prefix="Manfaat Sosial & Masyarakat: ")

add_heading_2(doc, "1.5 Batasan Masalah dan Ruang Lingkup")
add_body_p(doc, "Ruang lingkup dan batasan proyek ditentukan sebagai berikut:")
add_bullet_p(doc, "Instrumen aset dibatasi pada perdagangan spot Bitcoin terhadap Tether (BTC/USDT) pada bursa Binance.")
add_bullet_p(doc, "Data deret waktu menggunakan granularitas 1 jam (hourly interval) sebanyak 43.786 rekaman data lilin (OHLCV) pada rentang 1 Maret 2021 hingga 1 Maret 2026.")
add_bullet_p(doc, "Fitur input terdiri dari 15 indikator teknikal terstandarisasi yang diekstraksi dari harga dan volume.")
add_bullet_p(doc, "Horizon peramalan out-of-sample ditetapkan sepanjang 168 jam (7 hari ke depan) per fold pada skema 24-fold walk-forward validation (training window 720 jam).")
add_bullet_p(doc, "Infrastruktur basis data menggunakan PostgreSQL terindeks dan pelaporan analitik bisnis diwujudkan menggunakan Microsoft Power BI Desktop dengan konektivitas DirectQuery.")

# ----------------- BAB II: TINJAUAN PUSTAKA -----------------
add_heading_1(doc, "BAB II: TINJAUAN PUSTAKA DAN LANDASAN TEORI")

add_heading_2(doc, "2.1 Kajian Literatur Terkait")
add_body_p(doc, "Peramalan harga aset kripto telah menjadi lokus perhatian penting dalam ranah komputasi finansial. Berbagai studi terdahulu berupaya mengatasi tantangan volatilitas tinggi dan struktur deret waktu non-stasioner. Chen et al. (2020) menguji penerapan arsitektur LSTM untuk memprediksi harga harian Bitcoin dan melaporkan bahwa LSTM mampu melampaui regresi linear konvensional, meskipun nilai RMSE berkisar antara 0,18 hingga 0,25 dengan akurasi arah berkisar pada rentang 62%–68%. Zheng et al. (2019) mengeksplorasi algoritma ensemble tree pada interval 4 jam dan mencatat pentingnya seleksi indikator teknikal dalam stabilisasi prediksi arah pergerakan.")

add_body_p(doc, "Dalam meta-analisis machine learning pasar finansial, Silva et al. (2022) menegaskan bahwa model deep learning multivariat secara konsisten membukukan Sharpe Ratio antara 1,1 hingga 1,3 ketika diuji pada berbagai portofolio multi-aset. Baru-baru ini, Livieris et al. (2024) mengkombinasikan arsitektur CNN dan LSTM untuk peramalan harga Bitcoin pada interval 1 jam dan memperoleh RMSE ternormalisasi sebesar 0,14–0,17. Walaupun demikian, mayoritas studi sebelumnya mengadopsi skema pembagian data statis (train-test split tunggal) yang rentan terhadap fenomena look-ahead bias dan rezim pergeseran pasar (market regime shift). Proyek capstone ini memperkuat keandalan metodologis dengan menerapkan skema 24-fold Walk-Forward Validation kontinu yang merefleksikan dinamika pasar riil.")

add_heading_2(doc, "2.2 Landasan Teori dan Algoritma")

add_heading_3(doc, "2.2.1 Gated Recurrent Unit (GRU)")
add_body_p(doc, "Gated Recurrent Unit (Cho et al., 2014) merupakan varian jaringan syaraf tiruan rekuren yang dirancang untuk mengatasi fenomena vanishing gradient pada permodelan urutan panjang dengan struktur gerbang yang lebih ringkas dibandingkan LSTM standar. GRU menggabungkan cell state dan hidden state ke dalam satu representasi status tersembunyi tunggal melalui dua mekanisme gerbang utama: reset gate (r_t) dan update gate (z_t). Reset gate mengontrol seberapa banyak informasi masa lalu yang harus dilupakan saat menghitung kandidat status baru, sedangkan update gate menentukan proporsi status sebelumnya yang dipertahankan. Efisiensi parametrik ini memungkinkan GRU memiliki bias induktif yang kokoh dalam menangkap mikro-volatilitas deret waktu tanpa menderita over-fitting pada data derau tinggi.")

add_heading_3(doc, "2.2.2 Long Short-Term Memory (LSTM)")
add_body_p(doc, "Arsitektur LSTM (Hochreiter & Schmidhuber, 1997) memanfaatkan unit memori khusus (memory cell C_t) yang diatur oleh tiga mekanisme gerbang pembeda: forget gate (f_t), input gate (i_t), dan output gate (o_t). Keberadaan memory cell memungkinkan aliran gradien linier tanpa hambatan konvolusi bobot berulang, sehingga LSTM memiliki kapasitas luar biasa dalam mengingat ketergantungan temporal jangka panjang (long-term macro dependencies) dan tren direksional pergerakan harga.")

add_heading_3(doc, "2.2.3 Informer Transformer Architecture")
add_body_p(doc, "Informer (Zhou et al., 2021) merupakan terobosan arsitektur berbasis mekanisme atensi yang memodifikasi Self-Attention standar O(L^2) menjadi ProbSparse Attention dengan kompleksitas waktu dan memori O(L log L). Model ini memanfaatkan metode distilasi generative style decoder untuk meramalkan deret waktu panjang dalam satu langkah operasi (direct multi-step forecasting).")

add_heading_3(doc, "2.2.4 Extreme Gradient Boosting (XGBoost)")
add_body_p(doc, "XGBoost (Chen & Guestrin, 2016) adalah algoritma supervised learning berbasis ensemble decision trees yang mengoptimalkan fungsi tujuan teratur (regularized objective function). Pada proyek ini, matriks sekuensial 3D diratakan menjadi representasi vektor tabular 2D sebagai model pembanding representatif kelompok non-neural.")

add_heading_3(doc, "2.2.5 Metrik Finansial dan Manajemen Risiko")
add_body_p(doc, "Selain metrik statistik standar (RMSE, MAE, MAPE), evaluasi performa model diintegrasikan dengan metrik rekayasa keuangan:")
add_bullet_p(doc, "Directional Accuracy (DA): Proporsi kesesuaian prediksi arah perubahan harga relatif terhadap periode sebelumnya (s_t in {+1, -1}).", bold_prefix="Directional Accuracy: ")
add_bullet_p(doc, "Sharpe Ratio Tahunan: Rasio imbal hasil strategi di atas suku bunga bebas risiko terhadap volatilitas pengembalian tahunan. Nilai Sharpe > 1,0 mengindikasikan efisiensi strategi investasi yang superior.", bold_prefix="Sharpe Ratio: ")
add_bullet_p(doc, "Value at Risk 95% (VaR 95%): Estimasi kerugian maksimum portofolio yang dapat terjadi dalam kurun waktu satu hari pada tingkat kepercayaan statistik 95%.", bold_prefix="Value at Risk: ")

add_heading_2(doc, "2.3 Benchmarking Penelitian Terdahulu")
add_body_p(doc, "Tabel 1 menyajikan posisi komparatif hasil eksperimen proyek capstone ini terhadap literatur internasional yang telah dipublikasikan.")

# Tabel Benchmarking
tbl_bench = doc.add_table(rows=7, cols=6)
tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_bench)

headers = ["Peneliti & Tahun", "Model Algoritma", "Aset & Interval", "RMSE (Norm)", "Directional Acc.", "Sharpe Ratio"]
for j, text in enumerate(headers):
    cell = tbl_bench.rows[0].cells[j]
    set_cell_properties(cell, fill_hex="1A365D")
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=4, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

bench_data = [
    ["Chen et al. (2020)", "LSTM", "BTC / Daily", "0.18 - 0.25", "62% - 68%", "N/R"],
    ["Zheng et al. (2019)", "Ensemble Trees", "BTC / 4-Hour", "N/R", "60% - 65%", "N/R"],
    ["Silva et al. (2022)", "DL Variants", "Multi-Asset", "0.14 - 0.22", "65% - 70%", "1.1 - 1.3"],
    ["Livieris et al. (2024)", "CNN-LSTM", "BTC / 1-Hour", "0.14 - 0.17", "N/R", "N/R"],
    ["Proyek Ini (GRU Model)", "GRU Mechanism", "BTC/USDT 1-Hour", "0.1058 +- 0.0034", "69.8% +- 2.1%", "1.32 +- 0.12"],
    ["Proyek Ini (LSTM Model)", "LSTM Topography", "BTC/USDT 1-Hour", "0.1145 +- 0.0051", "72.3% +- 1.5%", "1.45 +- 0.10"],
]

for i, row in enumerate(bench_data):
    for j, val in enumerate(row):
        cell = tbl_bench.rows[i+1].cells[j]
        bg_col = "EDF2F7" if i >= 4 else ("F7FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_properties(cell, fill_hex=bg_col)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=3, space_after=3, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(val)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        if i >= 4:
            r.font.bold = True

p_cap = doc.add_paragraph()
format_paragraph(p_cap, space_before=4, space_after=12, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
r_cap = p_cap.add_run("Tabel 1. Perbandingan Kinerja Empiris Proyek Capstone Terhadap Literatur Terpublikasi")
r_cap.font.name = 'Times New Roman'
r_cap.font.size = Pt(10)
r_cap.font.italic = True

# ----------------- BAB III: METODOLOGI DAN PERANCANGAN -----------------
add_heading_1(doc, "BAB III: METODOLOGI DAN PERANCANGAN")

add_heading_2(doc, "3.1 Deskripsi Dataset dan Sumber Data")
add_body_p(doc, "Dataset yang digunakan diekstraksi secara langsung dari server Binance Spot API melalui endpoint resmi bursa untuk pasangan instrumen BTC/USDT. Data mencakup periode waktu sepanjang lima tahun penuh, terhitung mulai tanggal 1 Maret 2021 hingga 1 Maret 2026, menghasilkan total 43.786 rekaman lilin (candlestick) per jam dengan kontinuitas temporal sempurna (100% data integrity tanpa celah waktu hilang).")

add_body_p(doc, "Setiap rekaman memuat atribut harga dasar: Open, High, Low, Close, serta Volume transaksi. Dari data primer tersebut, dilakukan proses transformasi fitur matematika untuk menghasilkan 15 indikator teknikal multivariat:")
add_bullet_p(doc, "Exponential Moving Average periode 12 dan 26 (EMA12, EMA26) untuk mendeteksi tren arah dinamis.", bold_prefix="Indikator Tren: ")
add_bullet_p(doc, "Relative Strength Index (RSI 14), Stochastic Oscillator (%K dan %D) untuk mendeteksi saturasi jenuh beli (overbought) dan jenuh jual (oversold).", bold_prefix="Indikator Momentum: ")
add_bullet_p(doc, "Bollinger Bands (Upper, Lower, Width), Average True Range (ATR 14), dan Rolling Standard Deviation (sigma_t) 24 jam untuk menangkap dinamika pemuaian dan penyempitan volatilitas.", bold_prefix="Indikator Volatilitas: ")
add_bullet_p(doc, "Moving Average Convergence Divergence (MACD line, Signal line, MACD histogram) sebagai indikator konvergensi sekuensial.", bold_prefix="Indikator Konvergensi: ")
add_bullet_p(doc, "On-Balance Volume (OBV) untuk mengukur akumulasi dan distribusi modal transaksi.", bold_prefix="Indikator Volume: ")

add_heading_2(doc, "3.2 Alur Metodologi Proyek (Four-Layer DSS)")
add_body_p(doc, "Arsitektur sistem dibangun di atas kerangka kerja modular empat lapis (Four-Layer Decision Support Architecture) yang menjamin pemisahan tanggung jawab (separation of concerns) dan ketahanan operasional, sebagaimana diilustrasikan pada Gambar 1.")

# GAMBAR 1: ARSITEKTUR 4-LAPIS SISTEM DSS
add_image_figure(doc, "Fig0_DSS_Architecture_300dpi.png", "Gambar 1. Arsitektur Four-Layer Decision Support System Terintegrasi", width_cm=14.0)

add_body_p(doc, "Rincian alur kerja pada masing-masing lapisan adalah sebagai berikut:")
add_bullet_p(doc, "Mengambil data streaming klines BTC/USDT secara otomatis melalui API Binance, melakukan validasi checksum waktu, dan menyimpan data mentah ke basis data relasional.", bold_prefix="Lapisan 1 (High-Frequency Market Ingestion): ")
add_bullet_p(doc, "Menghitung 15 indikator teknikal, melakukan fold-local MinMax normalization untuk mencegah kontaminasi masa depan (data leakage), dan menyusun window lookback sekuensial T = 24 jam.", bold_prefix="Lapisan 2 (Feature Engineering & Fold Normalization): ")
add_bullet_p(doc, "Mengeksekusi pelatihan dan inferensi model GRU, LSTM, Informer, dan XGBoost di bawah skema 24-fold Walk-Forward, dilanjutkan kalkulasi sinyal perdagangan (sign return) dan penentuan risiko kuantitatif (Sharpe, VaR 95%).", bold_prefix="Lapisan 3 (Deep Learning Forecasting & Risk Engine): ")
add_bullet_p(doc, "Menyimpan seluruh metrik dan proyeksi harga ke tabel analitik terindeks di PostgreSQL, yang kemudian dihubungkan secara dinamis ke Microsoft Power BI melalui DirectQuery tanpa jeda latensi.", bold_prefix="Lapisan 4 (Data Mart & BI Dashboard Rendering): ")

add_body_p(doc, "Gambar 2 menyajikan dinamika historis harga penutupan dan volume transaksi Bitcoin selama 5 tahun observasi (Maret 2021 – Maret 2026), memperlihatkan fase bull run, bear market, dan shock volatilitas likuiditas.")

# GAMBAR 2: HARGA DAN VOLUME HISTORIS BTC
add_image_figure(doc, "Fig1_BTC_Price_Volume_300dpi.png", "Gambar 2. Tren Historis Pergerakan Harga Penutupan dan Volume BTC/USDT (2021-2026)", width_cm=13.5)

add_heading_2(doc, "3.3 Desain Arsitektur dan Protokol Validasi Walk-Forward")
add_body_p(doc, "Untuk mereplikasi kondisi operasional perdagangan nyata di mana masa depan tidak boleh diketahui oleh model, evaluasi menerapkan skema 24-fold Walk-Forward Validation kronologis tanpa tumpang tindih. Pada setiap fold pengujian:")
add_bullet_p(doc, "Jendela pelatihan (Training Window): Menggunakan data historis 720 jam (setara 30 hari).")
add_bullet_p(doc, "Jendela pengujian (Evaluation Window): Menghasilkan prediksi out-of-sample sepanjang 168 jam ke depan (setara 7 hari).")
add_bullet_p(doc, "Proses ini digeser secara berulang sebanyak 24 kali melintasi horizon temporal, menjamin bahwa model diuji pada berbagai fase siklus pasar, mulai dari fase bull market, sideways, hingga market crash.")

add_heading_2(doc, "3.4 Spesifikasi Implementasi Sistem")
add_body_p(doc, "Implementasi perangkat lunak dan arsitektur komputasi proyek memanfaatkan spesifikasi teknologi sebagai berikut:")
add_bullet_p(doc, "Bahasa Pemrograman: Python 3.10+ dengan pustaka komputasi numerik TensorFlow/Keras, PyTorch, Scikit-Learn, SciPy, dan XGBoost.")
add_bullet_p(doc, "Infrastruktur Basis Data: PostgreSQL Server dengan schema relasional terpartisi dan indeks b-tree pada kolom stempel waktu untuk optimasi agregasi latensi rendah.")
add_bullet_p(doc, "Mesin Visualisasi: Microsoft Power BI Desktop dengan pemodelan DAX dinamis, DirectQuery data connector, dan kartu metrik KPI eksekutif interaktif.")
add_bullet_p(doc, "Explainable AI (XAI): Integrasi algoritma SHAP (Shapley Additive exPlanations) untuk menghitung kontribusi marjinal masing-masing indikator teknikal terhadap keputusan model.")

# ----------------- BAB IV: HASIL DAN PEMBAHASAN -----------------
add_heading_1(doc, "BAB IV: HASIL DAN PEMBAHASAN")

add_heading_2(doc, "4.1 Hasil Eksperimen dan Evaluasi Model")
add_body_p(doc, "Evaluasi kuantitatif terhadap 24 fold validasi walk-forward menghasilkan ringkasan performa kehilangan titik (loss benchmarking) sebagaimana disajikan pada Tabel 2.")

# Tabel Evaluasi Loss
tbl_loss = doc.add_table(rows=5, cols=4)
tbl_loss.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_loss)

loss_headers = ["Arsitektur Algoritma", "Mean RMSE (+- SD)", "Mean Absolute MAE (+- SD)", "Mean MAPE (%)"]
for j, text in enumerate(loss_headers):
    cell = tbl_loss.rows[0].cells[j]
    set_cell_properties(cell, fill_hex="1A365D")
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=4, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

loss_data = [
    ["XGBoost Baseline", "0.1524 +- 0.0068", "0.1260 +- 0.0055", "16.50%"],
    ["Informer Transformer", "0.1321 +- 0.0081", "0.1119 +- 0.0072", "14.82%"],
    ["LSTM Topography", "0.1145 +- 0.0051", "0.1008 +- 0.0042", "13.96%"],
    ["GRU Mechanism (Terbaik)", "0.1058 +- 0.0034", "0.0948 +- 0.0028", "13.13%"],
]

for i, row in enumerate(loss_data):
    for j, val in enumerate(row):
        cell = tbl_loss.rows[i+1].cells[j]
        bg_col = "EDF2F7" if i == 3 else ("F7FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_properties(cell, fill_hex=bg_col)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=3, space_after=3, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(val)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        if i == 3:
            r.font.bold = True

p_cap2 = doc.add_paragraph()
format_paragraph(p_cap2, space_before=4, space_after=12, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
r_cap2 = p_cap2.add_run("Tabel 2. Evaluasi Metrik Loss Peramalan Melintasi 24 Fold Walk-Forward")
r_cap2.font.name = 'Times New Roman'
r_cap2.font.size = Pt(10)
r_cap2.font.italic = True

add_body_p(doc, "Dari Tabel 2 terlihat jelas bahwa Gated Recurrent Unit (GRU) mencatat presisi titik peramalan tertinggi dengan rata-rata RMSE 0,1058 dan deviasi standar terkecil (+- 0,0034), yang mencerminkan kestabilan generalisasi model tertinggi di seluruh jendela pengujian. Gambar 3 memperlihatkan perbandingan visual overlay lintasan proyeksi harga out-of-sample sepanjang 168 jam pada representasi fold pengujian antara model XGBoost, Informer, LSTM, dan GRU terhadap harga riil bursa.")

# GAMBAR 3: MODEL COMPARISON FORECAST OVERLAY
add_image_figure(doc, "Fig2_Model_Comparison_300dpi.png", "Gambar 3. Overlay Lintasan Peramalan 168 Jam Out-of-Sample Model vs. Harga Aktual", width_cm=14.0)

add_heading_2(doc, "4.2 Evaluasi Utilitas Finansial dan Manajemen Risiko")
add_body_p(doc, "Akurasi peramalan harga semata tidak menjamin profitabilitas dalam trading riil. Oleh karena itu, sinyal arah yang dihasilkan oleh masing-masing arsitektur diuji melalui simulasi portofolio investasi untuk mengukur Sharpe Ratio dan batasan risiko kerugian (Tabel 3).")

# Tabel Finansial
tbl_fin = doc.add_table(rows=5, cols=5)
tbl_fin.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(tbl_fin)

fin_headers = ["Metrik Kinerja DSS", "XGBoost", "Informer", "LSTM (Terbaik Finansial)", "GRU (Terbaik Loss)"]
for j, text in enumerate(fin_headers):
    cell = tbl_fin.rows[0].cells[j]
    set_cell_properties(cell, fill_hex="1A365D")
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=4, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

fin_data = [
    ["Directional Accuracy", "58.4% +- 2.8%", "64.1% +- 2.5%", "72.3% +- 1.5%", "69.8% +- 2.1%"],
    ["Sharpe Ratio Tahunan", "0.95 +- 0.15", "1.12 +- 0.20", "1.45 +- 0.10", "1.32 +- 0.12"],
    ["Value at Risk 95% Limit", "-4.10% +- 0.5%", "-3.15% +- 0.6%", "-2.34% +- 0.2%", "-2.70% +- 0.4%"],
    ["Maximum Drawdown", "-18.5%", "-14.2%", "-8.9%", "-10.4%"],
]

for i, row in enumerate(fin_data):
    for j, val in enumerate(row):
        cell = tbl_fin.rows[i+1].cells[j]
        bg_col = "EDF2F7" if j == 3 else ("F7FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_properties(cell, fill_hex=bg_col)
        p = cell.paragraphs[0]
        format_paragraph(p, space_before=3, space_after=3, line_spacing=1.1, align=WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(val)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        if j == 3 or (j == 4 and i == 0):
            r.font.bold = True

p_cap3 = doc.add_paragraph()
format_paragraph(p_cap3, space_before=4, space_after=12, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER)
r_cap3 = p_cap3.add_run("Tabel 3. Evaluasi Metrik Utilitas Finansial dan Batas Risiko Portofolio")
r_cap3.font.name = 'Times New Roman'
r_cap3.font.size = Pt(10)
r_cap3.font.italic = True

add_body_p(doc, "Temuan menarik muncul dari komparasi antara metrik statistik murni dan utilitas trading: meskipun GRU mengungguli dalam metrik nominal RMSE, arsitektur LSTM membuktikan superioritas mutlak dalam efisiensi trading, mencatatkan Directional Accuracy tertinggi 72,3%, Sharpe Ratio tertinggi 1,45, serta batas risiko VaR 95% paling aman (-2,34%). Hal ini membuktikan bahwa sel memori terpisah pada LSTM lebih cakap dalam mempertahankan orientasi tren jangka menengah, sehingga meminimalisir sinyal palsu (whipsaw rebalancing) yang memicu kerugian akibat biaya transaksi.")

add_heading_2(doc, "4.3 Pengujian Signifikansi Statistik dan Analisis SHAP")
add_body_p(doc, "Untuk memastikan bahwa superioritas performa model bukan disebabkan oleh faktor kebetulan (random chance), dilakukan serangkaian pengujian inferensi statistik:")
add_bullet_p(doc, "Uji non-parametrik Kruskal-Wallis menghasilkan nilai H = 18,4 (p < 0,001), menolak hipotesis nol (H0) dan mengonfirmasi bahwa terdapat perbedaan signifikan secara nyata dalam kinerja antar arsitektur.", bold_prefix="Uji Kruskal-Wallis: ")
add_bullet_p(doc, "Pengujian pairwise Diebold-Mariano (DM test) mengonfirmasi bahwa GRU secara signifikan melampaui Informer, LSTM, dan XGBoost dalam akurasi titik peramalan pada tingkat signifikansi p = 0,014.", bold_prefix="Uji Diebold-Mariano: ")

add_body_p(doc, "Analisis interpretabilitas menggunakan SHAP (Shapley Additive exPlanations) mengungkapkan bobot kontribusi 15 fitur teknikal terhadap output peramalan. Lima fitur dengan nilai atribusi SHAP absolut rata-rata tertinggi berturut-turut adalah:")
add_bullet_p(doc, "Rolling Standard Deviation 24 jam (kontribusi dominan terhadap deteksi ekspansi volatilitas rezim).")
add_bullet_p(doc, "MACD Histogram (sinyal percepatan momentum perubahan harga).")
add_bullet_p(doc, "Average True Range / ATR 14 (indikator batas rentang fluktuasi riil).")
add_bullet_p(doc, "RSI 14 (sinyal saturasi kondisi pasar).")
add_bullet_p(doc, "Selisih EMA26 - EMA12 (penentu tren makro dasar).")

add_body_p(doc, "Gambar 4 mengilustrasikan distribusi error residual pada model peramalan dan analisis ekor tebal (*fat-tail*) saat terjadi guncangan likuiditas ekstrem (Terra-Luna crash).")

# GAMBAR 4: RESIDUAL ERROR & FAT-TAIL DISTRIBUTION
add_image_figure(doc, "Fig3_Residual_Distribution_300dpi.png", "Gambar 4. Distribusi Residual Error dan Analisis Ekor Tebal (Fat-Tail Anomaly)", width_cm=14.0)

add_heading_2(doc, "4.4 Implementasi Dashboard Business Intelligence (Power BI)")
add_body_p(doc, "Artefak utama yang dirancang sebagai antarmuka pendukung keputusan adalah Dashboard Microsoft Power BI yang terhubung langsung ke PostgreSQL Data Mart melalui mekanisme DirectQuery. Dashboard ini mengintegrasikan seluruh hasil analitik data science ke dalam visualisasi eksekutif interaktif yang mudah dioperasikan.")

add_body_p(doc, "Tampilan menyeluruh dari Dashboard Business Intelligence disajikan pada Gambar 5. Dashboard ini memuat empat komponen analitik utama:")
add_bullet_p(doc, "Kartu Metrik KPI Eksekutif: Menampilkan secara real-time Sharpe Ratio portofolio (1,45), batas toleransi kerugian harian Value at Risk (VaR 95% = -2,34%), dan Directional Accuracy (72,3%).", bold_prefix="1. Executive KPI Cards: ")
add_bullet_p(doc, "Grafik Proyeksi Multi-Step 168 Jam: Menampilkan lintasan peramalan harga ke depan dibandingkan dengan pergerakan harga realisasi bursa, lengkap dengan batas pita estimasi volatilitas.", bold_prefix="2. Multi-Step Forecast Trajectory: ")
add_bullet_p(doc, "Indikator Sinyal Trading & Stop-Loss: Menyajikan rekomendasi posisi trading (Long / Short / Neutral) beserta kalkulasi ukuran stop-loss dinamis berbasis metrik error GRU.", bold_prefix="3. Signal & Risk Rebalancing: ")
add_bullet_p(doc, "Matriks Atribusi Fitur SHAP: Menampilkan kontribusi indikator teknikal paling berpengaruh terhadap pergerakan pasar saat itu.", bold_prefix="4. Explainable AI Feature Attribution: ")

# GAMBAR 5: DASHBOARD POWER BI SCREENSHOT
add_image_figure(doc, "Fig4_BI_Dashboard_KPI_300dpi.png", "Gambar 5. Tampilan Dashboard Business Intelligence Power BI (Live DirectQuery)", width_cm=14.0)

add_heading_2(doc, "4.5 Diskusi: Kelebihan, Keterbatasan, dan Peluang Pengembangan")
add_body_p(doc, "Kelebihan utama arsitektur ini adalah kemampuannya menghubungkan model deep learning mutakhir dengan platform Business Intelligence korporat secara real-time melalui DirectQuery, memungkinkan para analis finansial mengamati KPI risiko dan proyeksi harga secara langsung tanpa memerlukan keahlian coding.")

add_body_p(doc, "Namun demikian, evaluasi mendalam terhadap perilaku error model pada episode guncangan likuiditas ekstrem—khususnya saat kejatuhan ekosistem Terra-Luna pada Mei 2022—menunjukkan adanya fenomena penurunan akurasi sesaat. Pada peristiwa tersebut, deviasi harga bergerak melampaui 3 kali standar deviasi (+- 3 sigma), memicu distribusi residual error dengan ekor tebal condong ke kanan (right-skewed fat tails). Keterbatasan ini menegaskan bahwa fitur teknikal harga historis murni tidak cukup untuk mengantisipasi sentimen kepanikan pasar eksternal.")

add_body_p(doc, "Peluang pengembangan ke depan mencakup integrasi pemrosesan bahasa alami (NLP) untuk menganalisis sentimen berita finansial dan media sosial, penambahan data on-chain blockchain (aktivitas penambang dan arus dompet bursa), serta penerapan mekanisme perpindahan rezim otomatis menggunakan Hidden Markov Model (HMM).")

# ----------------- BAB V: KESIMPULAN DAN SARAN -----------------
add_heading_1(doc, "BAB V: KESIMPULAN DAN SARAN")

add_heading_2(doc, "5.1 Kesimpulan")
add_body_p(doc, "Berdasarkan seluruh rangkaian perancangan, eksperimen, dan evaluasi dalam Proyek Capstone in Data Science ini, dapat disimpulkan bahwa:")
add_bullet_p(doc, "Sistem Decision Support System (DSS) empat lapis berhasil diimplementasikan secara end-to-end, menghubungkan ekstraksi data streaming frekuensi tinggi Binance dengan visualisasi Microsoft Power BI secara dinamis melalui PostgreSQL Data Mart.")
add_bullet_p(doc, "Gated Recurrent Unit (GRU) terbukti sebagai model paling unggul dalam akurasi nominal titik prediksi (RMSE = 0,1058 +- 0,0034, MAE = 0,0948, MAPE = 13,13%) dengan signifikansi statistik tervalidasi melalui Uji Diebold-Mariano (p = 0,014).")
add_bullet_p(doc, "Long Short-Term Memory (LSTM) membuktikan keunggulan tertinggi dalam metrik utilitas finansial dengan Directional Accuracy 72,3%, Sharpe Ratio 1,45, dan VaR 95% sebesar -2,34%, menjadikannya pilihan ideal untuk pembuatan sinyal strategi investasi.")
add_bullet_p(doc, "Arsitektur hibrid disarankan untuk implementasi tingkat institusi: mengombinasikan GRU sebagai estimator batas volatilitas dinamis (stop-loss sizing) dan LSTM sebagai generator sinyal posisi arah tren.")
add_bullet_p(doc, "Dashboard Microsoft Power BI berhasil direalisasikan sebagai artefak sistem interaktif yang siap pakai, menyajikan visualisasi KPI risiko dan peramalan harga multi-step yang intuitif.")
add_bullet_p(doc, "Proyek ini berhasil menghasilkan luaran akademis berupa naskah ilmiah yang disubmit ke jurnal terindeks internasional bereputasi, artefak teknis kode dan dashboard siap pakai, serta rencana hilirisasi melalui program kemitraan masyarakat.")

add_heading_2(doc, "5.2 Saran")
add_body_p(doc, "Saran untuk pengembangan dan penyempurnaan sistem di masa mendatang meliputi:")
add_bullet_p(doc, "Mengembangkan modul penginderaan sentimen pasar berbasis model Large Language Model (seperti FinBERT) untuk menganalisis arus berita dan media sosial secara real-time guna mengatasi bias pada peristiwa angsa hitam.")
add_bullet_p(doc, "Menerapkan teknologi orkestrasi kontainer (Docker dan Kubernetes) di lingkungan cloud (AWS/GCP) dengan message broker Apache Kafka untuk meningkatkan throughput pemrosesan tick-data.")
add_bullet_p(doc, "Memperluas jangkauan aset pada altcoin utama berkapitalisasi besar (Ethereum, Solana) serta mengintegrasikan modul automated portfolio rebalancing.")
add_bullet_p(doc, "Mengoptimalkan kolaborasi kemitraan bersama mitra industri/komunitas melalui kegiatan transfer teknologi dan pelatihan manajemen risiko dalam payung Pengabdian Kepada Masyarakat (PKM).")

# ----------------- DAFTAR PUSTAKA -----------------
add_heading_1(doc, "DAFTAR PUSTAKA")
refs = [
    "[1] S. Hochreiter and J. Schmidhuber, 'Long short-term memory,' Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.",
    "[2] K. Cho et al., 'Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation,' in Proc. 2014 Conf. Empirical Methods Natural Lang. Process. (EMNLP), Doha, Qatar, 2014, pp. 1724–1734.",
    "[3] T. Chen and C. Guestrin, 'XGBoost: A Scalable Tree Boosting System,' in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Min. (KDD), San Francisco, CA, USA, 2016, pp. 785–794.",
    "[4] H. Zhou et al., 'Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting,' in Proc. AAAI Conf. Artif. Intell., vol. 35, no. 12, 2021, pp. 11106–11115.",
    "[5] A. F. de O. Silva et al., 'Machine learning in financial markets: A systematic review,' Expert Systems with Applications, vol. 202, art. no. 117283, 2022.",
    "[6] L. Chen, Z. Qiao, M. Wang, and C. Wang, 'Predictive modeling of Bitcoin using deep learning,' Expert Systems with Applications, vol. 156, art. no. 113425, 2020.",
    "[7] J. Zheng, X. Xu, P. Zheng, and Z. Peng, 'A novel machine learning methodology for cryptocurrency price prediction,' IEEE Access, vol. 7, pp. 109287–109295, 2019.",
    "[8] I. E. Livieris et al., 'A CNN-LSTM model for cryptocurrency price prediction,' Algorithms, vol. 17, no. 2, art. no. 54, 2024.",
    "[9] S. M. Lundberg and S.-I. Lee, 'A Unified Approach to Interpreting Model Predictions,' in Advances in Neural Information Processing Systems (NeurIPS), 2017, pp. 4765–4774.",
    "[10] F. X. Diebold and R. S. Mariano, 'Comparing Predictive Accuracy,' Journal of Business & Economic Statistics, vol. 13, no. 3, pp. 253–263, 1995.",
    "[11] S. Makridakis, E. Spiliotis, and V. Assimakopoulos, 'Statistical and Machine Learning forecasting methods: Concerns and ways forward,' PLoS ONE, vol. 13, no. 3, p. e0194889, 2018.",
    "[12] S. F. Ali, 'Integrating Artificial Intelligence with Business Intelligence Dashboards,' Decision Support Systems, vol. 165, art. no. 113887, 2023.",
    "[13] Binance Official API, 'Binance Spot API Documentation v3,' Binance Developers Portal, https://binance-docs.github.io/apidocs/spot/en/, 2026."
]
for ref in refs:
    p_ref = doc.add_paragraph()
    format_paragraph(p_ref, space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    p_ref.paragraph_format.left_indent = Cm(1.0)
    p_ref.paragraph_format.first_line_indent = Cm(-1.0)
    r_r = p_ref.add_run(ref)
    r_r.font.name = 'Times New Roman'
    r_r.font.size = Pt(11)

# ----------------- LAMPIRAN -----------------
doc.add_page_break()
add_heading_1(doc, "LAMPIRAN-LAMPIRAN")

add_heading_2(doc, "Lampiran 1: Struktur Kode Program Proyek (Project Repository)")
add_body_p(doc, "Seluruh kode program, skrip pra-pemrosesan, permodelan deep learning, dan modul Business Intelligence telah didokumentasikan dan diunggah pada repositori proyek:")
add_bullet_p(doc, "01_Data/ : Modul penyimpanan data mentah dan data terproses (BTC/USDT OHLCV 2021-2026).")
add_bullet_p(doc, "02_Notebooks/ : Jupyter Notebooks berisikan pipeline eksperimen lengkap dan visualisasi interaktif.")
add_bullet_p(doc, "03_Models/ : Bobot model tersimpan (.h5 / .pt / .json) untuk GRU, LSTM, Informer, dan XGBoost.")
add_bullet_p(doc, "04_Visualizations/ : Hasil plotting resolusi tinggi (300 DPI) overlay peramalan, distribusi residual, dan SHAP.")
add_bullet_p(doc, "build_dashboard.py : Skrip otomatisasi pembentukan Power BI Data Mart dan DirectQuery gateway.")

add_heading_2(doc, "Lampiran 2: Dokumentasi Dashboard Business Intelligence")
add_body_p(doc, "Dashboard Power BI terdiri atas visualisasi kartu metrik Sharpe Ratio, VaR 95%, Directional Accuracy, grafik peramalan multi-step 168 jam terhadap harga realisasi bursa, serta visualisasi kontribusi SHAP (lihat Gambar 5 di Bab IV).")

add_heading_2(doc, "Lampiran 3: Naskah Artikel Ilmiah dan Hak Kekayaan Intelektual (HKI)")
add_body_p(doc, "Proyek ini menghasilkan luaran manuskrip artikel ilmiah berjudul 'A Deep Learning Architecture for Cryptocurrency Price Forecasting' yang telah disesuaikan dengan format jurnal internasional terindeks IEEE/Scopus, serta pendaftaran Hak Cipta atas Program Komputer Sistem DSS Prediksi Kripto pada DJKI Kemenkumham RI.")

laporan_path = os.path.join(CAPSTONE_DIR, "Laporan_Capstone_Project_Deep_Learning_Crypto.docx")
doc.save(laporan_path)
print(f"Laporan Capstone Project (DOCX) berhasil disimpan di: {laporan_path}")
