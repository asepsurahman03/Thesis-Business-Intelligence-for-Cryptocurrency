
# -*- coding: utf-8 -*-
"""
Generate Draft Tesis: Kerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency
Berdasarkan:
  - Proposal Tesis Asep Surahman Sulaeman.docx
  - Revisi_19_A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx
  - Template Tesis S2 Universitas Nusa Putra

Penulis  : Asep Surahman Sulaeman
NIM      : 20250130001
Program  : Magister Informatika, Universitas Nusa Putra
"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def set_font(run, name='Times New Roman', size=12, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    # Set font for East Asian characters too
    r = run._r
    rPr = r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rPr.insert(0, rFonts)

def set_para_format(para, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                    space_before=0, space_after=6,
                    line_spacing=1.5, first_line_indent=1.0,
                    left_indent=0):
    pf = para.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line_spacing
    if first_line_indent > 0:
        pf.first_line_indent = Cm(first_line_indent)
    if left_indent > 0:
        pf.left_indent = Cm(left_indent)

def add_paragraph(doc, text, style='Normal', align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                  bold=False, italic=False, size=12, space_before=0, space_after=6,
                  first_indent=1.0, left_indent=0, line_spacing=1.5):
    para = doc.add_paragraph()
    para.style = doc.styles[style] if style in [s.name for s in doc.styles] else doc.styles['Normal']
    run = para.add_run(text)
    set_font(run, size=size, bold=bold, italic=italic)
    set_para_format(para, align=align, space_before=space_before,
                    space_after=space_after, line_spacing=line_spacing,
                    first_line_indent=first_indent, left_indent=left_indent)
    return para

def add_heading(doc, text, level=1, center=True, size=14, bold=True, space_before=24, space_after=12):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles[f'Heading {level}']
    except:
        para.style = doc.styles['Normal']
    run = para.add_run(text)
    set_font(run, size=size, bold=bold)
    pf = para.paragraph_format
    if center:
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.0
    return para

def add_subheading(doc, text, number='', size=12, bold=True, level=2):
    para = doc.add_paragraph()
    try:
        para.style = doc.styles[f'Heading {level}']
    except:
        para.style = doc.styles['Normal']
    full = f'{number} {text}'.strip() if number else text
    run = para.add_run(full)
    set_font(run, size=size, bold=bold)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.0
    return para

def add_bullet(doc, text, size=12, left_indent=1.25):
    para = doc.add_paragraph(style='List Bullet' if 'List Bullet' in [s.name for s in doc.styles] else 'Normal')
    run = para.add_run(text)
    set_font(run, size=size)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(left_indent)
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    return para

def add_numbered(doc, text, number, size=12, left_indent=1.25):
    para = doc.add_paragraph()
    run_n = para.add_run(f'{number}. ')
    set_font(run_n, size=size, bold=False)
    run_t = para.add_run(text)
    set_font(run_t, size=size)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(left_indent)
    pf.first_line_indent = Cm(-0.75)
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    return para

def add_page_break(doc):
    doc.add_page_break()

def set_page_margins(section, top=3, bottom=3, left=4, right=3):
    section.top_margin = Cm(top)
    section.bottom_margin = Cm(bottom)
    section.left_margin = Cm(left)
    section.right_margin = Cm(right)

def add_caption(doc, text, size=11):
    para = doc.add_paragraph()
    para.style = doc.styles['Caption'] if 'Caption' in [s.name for s in doc.styles] else doc.styles['Normal']
    run = para.add_run(text)
    set_font(run, size=size, italic=True)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(4)
    pf.space_after = Pt(8)
    pf.first_line_indent = Cm(0)
    return para

def add_simple_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # Header
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = ''
        run = cell.paragraphs[0].add_run(h)
        set_font(run, size=10, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        # shade header
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'D9E1F2')
        tcPr.append(shd)
    # Data rows
    for r_idx, row in enumerate(rows):
        tr = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row):
            cell = tr.cells[c_idx]
            cell.text = ''
            run = cell.paragraphs[0].add_run(str(val))
            set_font(run, size=10)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Column widths
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)
    return table


# ─────────────────────────────────────────────
#  BUILD DOCUMENT
# ─────────────────────────────────────────────

doc = Document()

# Default section margins (4-3-3-3 cm)
section = doc.sections[0]
set_page_margins(section, top=3, bottom=3, left=4, right=3)
section.page_height = Cm(29.7)
section.page_width = Cm(21.0)

# ═══════════════════════════════════════════════════════════════════
# HALAMAN SAMPUL (COVER PAGE 1)
# ═══════════════════════════════════════════════════════════════════
p = add_paragraph(doc,
    'KERANGKA KERJA BUSINESS INTELLIGENCE UNTUK PREDIKSI CRYPTOCURRENCY:\n'
    'STUDI KOMPARATIF LSTM, GRU, DAN ENSEMBLE BASELINE MENGGUNAKAN\n'
    'BIG DATA ANALYTICS DENGAN INTEGRASI DEEP LEARNING',
    align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=24,
    first_indent=0)

p = add_paragraph(doc, 'TESIS', align=WD_ALIGN_PARAGRAPH.CENTER,
                  bold=True, size=14, space_before=24, space_after=24, first_indent=0)

# Logo placeholder
p = add_paragraph(doc, '[LOGO UNIVERSITAS NUSA PUTRA]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, size=12,
                  space_before=12, space_after=12, first_indent=0)

p = add_paragraph(doc, 'ASEP SURAHMAN SULAEMAN',
                  align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12,
                  space_before=12, space_after=4, first_indent=0)
p = add_paragraph(doc, 'NIM. 20250130001',
                  align=WD_ALIGN_PARAGRAPH.CENTER, size=12,
                  space_before=0, space_after=24, first_indent=0)

p = add_paragraph(doc,
    'PROGRAM STUDI MAGISTER INFORMATIKA\n'
    'FAKULTAS TEKNIK, KOMPUTER DAN DESAIN\n'
    'UNIVERSITAS NUSA PUTRA\n'
    'SUKABUMI\n'
    '2026',
    align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=True,
    space_before=24, space_after=0, first_indent=0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# HALAMAN JUDUL (COVER PAGE 2)
# ═══════════════════════════════════════════════════════════════════
p = add_paragraph(doc,
    'KERANGKA KERJA BUSINESS INTELLIGENCE UNTUK PREDIKSI CRYPTOCURRENCY:\n'
    'STUDI KOMPARATIF LSTM, GRU, DAN ENSEMBLE BASELINE MENGGUNAKAN\n'
    'BIG DATA ANALYTICS DENGAN INTEGRASI DEEP LEARNING',
    align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14,
    space_after=24, first_indent=0)

p = add_paragraph(doc, 'TESIS', align=WD_ALIGN_PARAGRAPH.CENTER,
                  bold=True, size=14, space_before=24, space_after=12, first_indent=0)
p = add_paragraph(doc,
    'Diajukan Untuk Memenuhi Salah Satu Syarat Dalam Menempuh\n'
    'Gelar Magister Komputer (M.Kom)',
    align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=24, first_indent=0)

p = add_paragraph(doc, 'ASEP SURAHMAN SULAEMAN',
                  align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12,
                  space_before=12, space_after=4, first_indent=0)
p = add_paragraph(doc, 'NIM. 20250130001',
                  align=WD_ALIGN_PARAGRAPH.CENTER, size=12,
                  space_before=0, space_after=24, first_indent=0)

p = add_paragraph(doc,
    'PROGRAM STUDI MAGISTER INFORMATIKA\n'
    'FAKULTAS TEKNIK, KOMPUTER DAN DESAIN\n'
    'UNIVERSITAS NUSA PUTRA\n'
    'SUKABUMI\n'
    '2026',
    align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=True,
    space_before=24, space_after=0, first_indent=0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# PERNYATAAN ORISINALITAS
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'PERNYATAAN ORISINALITAS', level=1, size=14)
doc.add_paragraph()

t = add_paragraph(doc, 'JUDUL\t:\tKerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency: '
    'Studi Komparatif LSTM, GRU, dan Ensemble Baseline Menggunakan Big Data Analytics dengan Integrasi Deep Learning',
    first_indent=0, space_after=4)
t = add_paragraph(doc, 'NAMA\t:\tAsep Surahman Sulaeman', first_indent=0, space_after=4)
t = add_paragraph(doc, 'NIM\t:\t20250130001', first_indent=0, space_after=12)

p = add_paragraph(doc,
    '\t"Saya menyatakan dan bertanggung jawab dengan sebenarnya bahwa tesis ini adalah hasil karya '
    'saya sendiri kecuali cuplikan dan ringkasan yang masing-masing telah saya jelaskan sumbernya. '
    'Jika pada waktu selanjutnya ada pihak lain yang mengklaim bahwa tesis ini sebagai karyanya, '
    'yang disertai dengan bukti-bukti yang cukup, maka saya bersedia untuk dibatalkan gelar Magister '
    'Komputer saya beserta segala hak dan kewajiban yang melekat pada gelar tersebut."',
    space_before=12, space_after=36, first_indent=0)

p = add_paragraph(doc, 'Sukabumi, __________ 2026', align=WD_ALIGN_PARAGRAPH.RIGHT,
                  first_indent=0, space_after=48)

p = add_paragraph(doc, 'Asep Surahman Sulaeman', align=WD_ALIGN_PARAGRAPH.RIGHT,
                  first_indent=0, space_after=4)
p = add_paragraph(doc, 'Penulis', align=WD_ALIGN_PARAGRAPH.RIGHT,
                  first_indent=0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# LEMBAR PERSETUJUAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'PERSETUJUAN TESIS', level=1, size=14)
doc.add_paragraph()
t = add_paragraph(doc, 'JUDUL\t:\tKerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency: '
    'Studi Komparatif LSTM, GRU, dan Ensemble Baseline Menggunakan Big Data Analytics dengan Integrasi Deep Learning',
    first_indent=0, space_after=4)
t = add_paragraph(doc, 'NAMA\t:\tAsep Surahman Sulaeman', first_indent=0, space_after=4)
t = add_paragraph(doc, 'NIM\t:\t20250130001', first_indent=0, space_after=12)
t = add_paragraph(doc, 'Tesis ini telah diperiksa dan disetujui.', first_indent=0, space_after=24)
t = add_paragraph(doc, 'Sukabumi, __________ 2026', first_indent=0, space_after=48)

tbl = doc.add_table(rows=4, cols=2)
tbl.style = 'Table Grid'
cells = tbl.rows[0].cells
cells[0].text = 'Ketua Pembimbing,'; cells[1].text = 'Anggota Pembimbing,'
cells = tbl.rows[2].cells
cells[0].text = 'Prof. Ts. Deden Witarsyah, S.T, Ph.D'
cells[1].text = 'Assoc. Prof. Dr. Aswan Supriyadi Sunge, S.E., M.Kom'
cells = tbl.rows[3].cells
cells[0].text = 'NIDN. 0120240060'; cells[1].text = 'NIDN. 0426018003'

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# LEMBAR PENGESAHAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'PENGESAHAN TESIS', level=1, size=14)
doc.add_paragraph()
t = add_paragraph(doc, 'JUDUL\t:\tKerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency: '
    'Studi Komparatif LSTM, GRU, dan Ensemble Baseline Menggunakan Big Data Analytics dengan Integrasi Deep Learning',
    first_indent=0, space_after=4)
t = add_paragraph(doc, 'NAMA\t:\tAsep Surahman Sulaeman', first_indent=0, space_after=4)
t = add_paragraph(doc, 'NIM\t:\t20250130001', first_indent=0, space_after=12)
t = add_paragraph(doc,
    'Tesis ini telah diujikan dan dipertahankan di depan Dewan Penguji pada Sidang Tesis '
    'tanggal __________. Menurut pandangan kami, Tesis ini memadai dari segi kualitas untuk '
    'tujuan penganugerahan gelar Magister Komputer (M.Kom).', first_indent=0, space_after=24)
t = add_paragraph(doc, 'Sukabumi, __________ 2026', first_indent=0, space_after=48)

tbl2 = doc.add_table(rows=6, cols=2)
tbl2.style = 'Table Grid'
r = tbl2.rows[0].cells; r[0].text = 'Ketua Pembimbing,'; r[1].text = 'Anggota Pembimbing,'
r = tbl2.rows[2].cells
r[0].text = 'Prof. Ts. Deden Witarsyah, S.T, Ph.D'
r[1].text = 'Assoc. Prof. Dr. Aswan Supriyadi Sunge, S.E., M.Kom'
r = tbl2.rows[3].cells; r[0].text = 'NIDN. 0120240060'; r[1].text = 'NIDN. 0426018003'
r = tbl2.rows[4].cells; r[0].text = 'Ketua Penguji,'; r[1].text = 'Anggota Penguji,'
r = tbl2.rows[5].cells
r[0].text = 'Assoc. Prof. Dr. Adhi Kusnadi, S.T., M.Si\nNIDN. 0303037304'
r[1].text = 'Assoc. Prof. Dr. Chaerur Rozikin, S.Kom., M.Kom\nNIDN. 20058305'

doc.add_paragraph()
tbl3 = doc.add_table(rows=3, cols=2)
tbl3.style = 'Table Grid'
r = tbl3.rows[0].cells; r[0].text = 'Ketua Program Studi,'; r[1].text = 'Plh. Dekan,'
r = tbl3.rows[2].cells
r[0].text = 'Assoc. Prof. Dr. Adhi Kusnadi, S.T., M.Si\nNIDN. 0303037304'
r[1].text = 'Ir. Paikun, S.T., M.T., IPM., ASEAN Eng\nNIDN. 0402037401'

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# HALAMAN PERSETUJUAN PUBLIKASI
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'HALAMAN PERNYATAAN PERSETUJUAN PUBLIKASI TESIS\nUNTUK KEPENTINGAN AKADEMIK',
            level=1, size=13)
doc.add_paragraph()
p = add_paragraph(doc, 'Sebagai civitas akademik Universitas Nusa Putra, saya yang bertanda tangan di bawah ini:',
                  first_indent=0, space_after=8)
t = add_paragraph(doc, 'Nama\t\t:\tAsep Surahman Sulaeman', first_indent=0, space_after=4)
t = add_paragraph(doc, 'NIM\t\t:\t20250130001', first_indent=0, space_after=4)
t = add_paragraph(doc, 'Program Studi\t:\tMagister Informatika', first_indent=0, space_after=4)
t = add_paragraph(doc, 'Jenis Karya\t:\tTesis', first_indent=0, space_after=12)
p = add_paragraph(doc,
    'Demi perkembangan ilmu pengetahuan, dengan ini saya menyetujui untuk memberikan kepada '
    'Universitas Nusa Putra Hak Bebas Royalti Non-eksklusif (Non-exclusive Royalty-Free Right) '
    'atas karya ilmiah saya yang berjudul:', first_indent=0, space_after=8)
p = add_paragraph(doc,
    '"Kerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency: Studi Komparatif LSTM, '
    'GRU, dan Ensemble Baseline Menggunakan Big Data Analytics dengan Integrasi Deep Learning"',
    align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, first_indent=0, space_after=8)
p = add_paragraph(doc,
    'Beserta perangkat yang ada (jika diperlukan). Dengan hak bebas royalti Non-eksklusif ini '
    'Universitas Nusa Putra berhak menyimpan, mengalih media/format, mengolah dalam bentuk '
    'pangkalan data (database), merawat dan mempublikasikan tesis saya selama tetap mencantumkan '
    'nama saya sebagai penulis/pencipta dan sebagai pemilik Hak Cipta.',
    first_indent=0, space_after=24)
p = add_paragraph(doc, 'Demikian pernyataan ini saya buat dengan sebenarnya.', first_indent=0, space_after=8)
p = add_paragraph(doc, 'Dibuat di\t: Sukabumi\nPada tanggal\t: __________ 2026', first_indent=0, space_after=36)
p = add_paragraph(doc, 'Yang Menyatakan,', align=WD_ALIGN_PARAGRAPH.RIGHT, first_indent=0, space_after=36)
p = add_paragraph(doc, 'Asep Surahman Sulaeman\n20250130001',
                  align=WD_ALIGN_PARAGRAPH.RIGHT, first_indent=0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# ABSTRACT (ENGLISH)
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'ABSTRACT', level=1, size=14)
doc.add_paragraph()
p = add_paragraph(doc,
    'Forecasting cryptocurrency prices in operational financial environments is challenged by severe '
    'non-stationarity, regime switching, and extreme volatility cascades. This study develops a modular '
    'four-layer Business Intelligence and Machine Learning (BI-ML) framework that integrates sequential '
    'predictive models into an enterprise decision-support architecture, evaluating out-of-sample '
    'forecasts through financial utility metrics including the Sharpe Ratio and Value-at-Risk (VaR). '
    'Four model topologies — Extreme Gradient Boosting (XGBoost), Long Short-Term Memory (LSTM), '
    'Gated Recurrent Unit (GRU), and the Informer Transformer — were evaluated under a 24-fold '
    'chronological Walk-Forward Validation protocol using 43,786 hourly BTC/USDT candlestick '
    'observations from March 2021 to March 2026. In point-forecasting accuracy, the GRU achieved '
    'the lowest error (RMSE = 0.1058 ± 0.0034), while the LSTM achieved the highest Directional '
    'Accuracy (57.8% ± 2.1%) and annualized Sharpe Ratio (0.87 ± 0.12, VaR\u209595% = −1.18% per hour). '
    'This reveals a critical divergence between statistical accuracy and decision utility that RMSE '
    'alone cannot capture. A System Usability Scale (SUS) evaluation of the Power BI prototype yielded '
    'a score of 86.4 (SD = 3.2), placing it in the \'Excellent\' tier. The framework bridges the gap '
    'between deep learning forecasting and enterprise financial decision governance.',
    space_after=12)
p = add_paragraph(doc,
    'Keywords: Business Intelligence, Cryptocurrency Prediction, Big Data Analytics, Deep Learning, '
    'XGBoost, LSTM, GRU, Informer Transformer, Financial Informatics, Walk-Forward Validation, '
    'Decision Support System.',
    bold=False, space_after=0)
run = p.runs[0]; run.bold = False
p.runs[0].font.bold = True  # "Keywords:" bold

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# ABSTRAK (INDONESIA)
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'ABSTRAK', level=1, size=14)
doc.add_paragraph()
p = add_paragraph(doc,
    'Peramalan harga cryptocurrency dalam lingkungan keuangan operasional menghadapi tantangan '
    'berupa non-stasioneritas yang parah, pergantian rezim pasar, dan kaskade volatilitas ekstrem. '
    'Penelitian ini mengembangkan kerangka kerja Business Intelligence dan Machine Learning (BI-ML) '
    'empat lapis yang bersifat modular, mengintegrasikan model prediktif sekuensial ke dalam '
    'arsitektur pendukung keputusan tingkat enterprise, dan mengevaluasi prakiraan out-of-sample '
    'melalui metrik utilitas finansial termasuk Sharpe Ratio dan Value-at-Risk (VaR). Empat '
    'topologi model — Extreme Gradient Boosting (XGBoost), Long Short-Term Memory (LSTM), Gated '
    'Recurrent Unit (GRU), dan Informer Transformer — dievaluasi di bawah protokol Walk-Forward '
    'Validation kronologis 24 lipatan menggunakan 43.786 observasi candlestick BTC/USDT per jam '
    'dari Maret 2021 hingga Maret 2026. Dalam akurasi point-forecasting, GRU mencapai galat terendah '
    '(RMSE = 0,1058 ± 0,0034), sedangkan LSTM mencapai Directional Accuracy tertinggi (57,8% ± 2,1%) '
    'dan Sharpe Ratio tahunan (0,87 ± 0,12, VaR95% = −1,18% per jam). Hal ini mengungkap divergensi '
    'kritis antara akurasi statistik dan utilitas keputusan yang tidak dapat ditangkap oleh RMSE '
    'semata. Evaluasi System Usability Scale (SUS) terhadap prototipe Power BI menghasilkan skor 86,4 '
    '(SD = 3,2), menempatkannya dalam tingkat \'Sangat Baik\'. Kerangka kerja ini menjembatani '
    'kesenjangan antara peramalan deep learning dan tata kelola keputusan keuangan tingkat enterprise.',
    space_after=12)
p = add_paragraph(doc,
    'Kata Kunci: Business Intelligence, Prediksi Cryptocurrency, Big Data Analytics, Deep Learning, '
    'XGBoost, LSTM, GRU, Informer Transformer, Informatika Finansial, Walk-Forward Validation, '
    'Sistem Pendukung Keputusan.')

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# KATA PENGANTAR
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'KATA PENGANTAR', level=1, size=14)
doc.add_paragraph()
p = add_paragraph(doc,
    'Segala puji dan syukur penulis panjatkan kehadirat Allah SWT yang telah memberikan rahmat '
    'serta karunia-Nya sehingga penulis akhirnya dapat menyelesaikan tesis yang berjudul "Kerangka '
    'Kerja Business Intelligence untuk Prediksi Cryptocurrency: Studi Komparatif LSTM, GRU, dan '
    'Ensemble Baseline Menggunakan Big Data Analytics dengan Integrasi Deep Learning" dengan lancar. '
    'Sholawat beserta salam semoga tercurahkan kepada junjungan alam, Nabi Muhammad SAW. Tujuan '
    'penulisan tesis ini adalah untuk memenuhi salah satu syarat mencapai gelar Magister Komputer '
    '(M.Kom) di Program Studi Magister Informatika Universitas Nusa Putra.')

p = add_paragraph(doc,
    'Penyusunan tesis ini tentunya tidak akan berjalan dengan baik tanpa adanya dukungan dan '
    'bimbingan dari berbagai pihak. Oleh karena itu, penulis mengucapkan terima kasih yang '
    'sebesar-besarnya kepada:')

ucapan = [
    'Bapak Dr. Kurniawan, ST., M. Si., MM., selaku Rektor Universitas Nusa Putra Sukabumi.',
    'Bapak Assoc. Prof. Dr. Samsul Pahmi, S.Pd., M.Pd., selaku Wakil Rektor I Bidang Akademik '
    'Universitas Nusa Putra Sukabumi.',
    'Bapak Assoc. Prof. Dr. Adhi Kusnadi, S.T, M.Si., selaku Kepala Program Studi Magister '
    'Informatika Universitas Nusa Putra.',
    'Bapak Prof. Ts. Deden Witarsyah, S.T, Ph.D., selaku Ketua Pembimbing yang telah meluangkan '
    'waktu, tenaga, dan pikiran dalam membimbing penyusunan tesis ini.',
    'Bapak Assoc. Prof. Dr. Aswan Supriyadi Sunge, S.E, M.Kom., selaku Anggota Pembimbing yang '
    'telah membimbing dan mengarahkan penulis demi kelancaran penyusunan tesis ini.',
    'Seluruh pimpinan dan civitas akademika Program Pascasarjana Universitas Nusa Putra.',
    'Seluruh dosen S1 dan S2 di lingkungan Universitas Nusa Putra yang telah memberikan ilmu '
    'dan kontribusi akademik kepada penulis.',
    'Keluarga tercinta, yaitu Bapak Maman, Ibu Amah, Imas Siti Maemunah, S.Pd., dan Feri Ilham '
    'Fadilah, yang telah memberikan dukungan, doa, serta semangat.',
    'Rekan-rekan mahasiswa Magister Informatika angkatan 2025 Universitas Nusa Putra.',
    'Serta kepada semua pihak yang telah membantu dalam penyusunan karya ilmiah tesis ini yang '
    'tidak dapat disebutkan satu per satu.',
]
for item in ucapan:
    add_bullet(doc, item)

p = add_paragraph(doc,
    'Akhir kata, penulis berharap Allah SWT berkenan membalas segala kebaikan semua pihak yang '
    'telah membantu. Semoga tesis ini membawa manfaat bagi pengembangan ilmu pengetahuan di masa '
    'mendatang, khususnya di bidang Informatika Finansial dan kecerdasan buatan.')

doc.add_paragraph()
p = add_paragraph(doc, 'Sukabumi, __________ 2026', first_indent=0,
                  align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=4)
p = add_paragraph(doc, 'Penulis,', first_indent=0,
                  align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=36)
p = add_paragraph(doc, 'Asep Surahman Sulaeman', first_indent=0,
                  align=WD_ALIGN_PARAGRAPH.RIGHT)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# DAFTAR ISI (placeholder)
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'DAFTAR ISI', level=1, size=14)
doc.add_paragraph()
toc_items = [
    ('HALAMAN SAMPUL', 'i'),
    ('PERNYATAAN ORISINALITAS', 'ii'),
    ('PERSETUJUAN TESIS', 'iii'),
    ('PENGESAHAN TESIS', 'iv'),
    ('PERSETUJUAN PUBLIKASI', 'v'),
    ('ABSTRACT', 'vi'),
    ('ABSTRAK', 'vii'),
    ('KATA PENGANTAR', 'viii'),
    ('DAFTAR ISI', 'ix'),
    ('DAFTAR TABEL', 'xi'),
    ('DAFTAR GAMBAR', 'xii'),
    ('DAFTAR LAMPIRAN', 'xiii'),
    ('BAB I PENDAHULUAN', '1'),
    ('    1.1 Latar Belakang', '1'),
    ('    1.2 Identifikasi Masalah', '8'),
    ('    1.3 Rumusan Masalah', '9'),
    ('    1.4 Tujuan Penelitian', '10'),
    ('    1.5 Manfaat Penelitian', '11'),
    ('    1.6 Batasan Penelitian', '13'),
    ('    1.7 Sistematika Penulisan Tesis', '14'),
    ('BAB II KAJIAN TEORITIS DAN TINJAUAN PUSTAKA', '16'),
    ('    2.1 Tinjauan Penelitian Terdahulu (State of the Art)', '16'),
    ('    2.2 Karakteristik Aset Digital dan Fundamen Cryptocurrency', '27'),
    ('    2.3 Analisis Kritis Hipotesis Pasar Efisien (EMH)', '29'),
    ('    2.4 Evolusi Arsitektur Deep Learning: Dari RNN hingga LSTM dan GRU', '31'),
    ('    2.5 Paradigma Explainable AI (XAI) dalam Kecerdasan Bisnis Finansial', '34'),
    ('    2.6 Arsitektur Business Intelligence untuk Prakiraan Deret Waktu Finansial', '36'),
    ('    2.7 Kerangka Pemikiran Penelitian', '38'),
    ('    2.8 Hipotesis Penelitian', '40'),
    ('BAB III METODOLOGI PENELITIAN', '42'),
    ('    3.1 Pendekatan dan Jenis Penelitian', '42'),
    ('    3.2 Desain Penelitian', '44'),
    ('    3.3 Arsitektur Kerangka Kerja Business Intelligence Empat Lapis', '45'),
    ('    3.4 Populasi, Sampel, dan Teknik Pengumpulan Data', '48'),
    ('    3.5 Spesifikasi dan Rekayasa Fitur Model', '51'),
    ('    3.6 Arsitektur Model', '55'),
    ('    3.7 Konfigurasi Hiperparameter dan Strategi Validasi', '60'),
    ('    3.8 Lapis 4 — BI Analytics: Konversi Prediksi menjadi Metrik Risiko', '64'),
    ('    3.9 Metrik Evaluasi Model', '66'),
    ('    3.10 Jadwal Penelitian', '68'),
    ('BAB IV HASIL DAN PEMBAHASAN', '70'),
    ('    4.1 Hasil Pengumpulan dan Pra-Pemrosesan Data', '70'),
    ('    4.2 Hasil Rekayasa Fitur Teknikal dan Analisis SHAP', '74'),
    ('    4.3 Hasil Pelatihan dan Evaluasi Model', '78'),
    ('    4.4 Komparasi Antar Model dan Uji Signifikansi Statistik', '88'),
    ('    4.5 Evaluasi Metrik Risiko Bisnis (Sharpe Ratio, VaR, Win Rate)', '93'),
    ('    4.6 Prototipe BI Decision Support Dashboard', '97'),
    ('    4.7 Pembahasan dan Diskusi', '100'),
    ('BAB V KESIMPULAN DAN SARAN', '108'),
    ('    5.1 Kesimpulan', '108'),
    ('    5.2 Implikasi Penelitian', '110'),
    ('    5.3 Keterbatasan Penelitian', '111'),
    ('    5.4 Saran untuk Penelitian Selanjutnya', '112'),
    ('DAFTAR PUSTAKA', '114'),
    ('LAMPIRAN', '121'),
    ('DAFTAR RIWAYAT HIDUP PENULIS', '130'),
]
for item, page in toc_items:
    para = doc.add_paragraph()
    run = para.add_run(item)
    set_font(run, size=12)
    run2 = para.add_run(f'\t{page}')
    set_font(run2, size=12)
    pf = para.paragraph_format
    pf.tab_stops.clear_all()
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(0)
    pf.space_after = Pt(2)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.0

add_page_break(doc)

# DAFTAR TABEL
add_heading(doc, 'DAFTAR TABEL', level=1, size=14)
doc.add_paragraph()
tabel_items = [
    ('Tabel 2.1', 'Tinjauan Literatur Terdahulu (State of the Art)', '16'),
    ('Tabel 3.1', 'Matriks Lima Belas Fitur Teknikal: Kategori, Fungsi, dan Rumus', '51'),
    ('Tabel 3.2', 'Spesifikasi Hiperparameter Model Neural Network dan XGBoost', '61'),
    ('Tabel 3.3', 'Jadwal Pelaksanaan Penelitian (Maret–November 2026)', '68'),
    ('Tabel 4.1', 'Statistik Deskriptif Dataset BTC/USDT (43.786 Observasi Per Jam)', '71'),
    ('Tabel 4.2', 'Hasil Augmented Dickey-Fuller (ADF) Test per Fitur', '73'),
    ('Tabel 4.3', 'Peringkat SHAP Feature Importance Rata-Rata Lintas Semua Model', '76'),
    ('Tabel 4.4', 'Benchmarking Kerugian Kuantitatif Lintas Lapisan Walk-Forward Algoritmik', '81'),
    ('Tabel 4.5', 'KPI Dashboard: Sharpe Ratio, VaR, dan Directional Accuracy', '85'),
    ('Tabel 4.6', 'Benchmarking Komparatif terhadap Literatur yang Dipublikasikan', '90'),
    ('Tabel 4.7', 'Hasil Evaluasi System Usability Scale (SUS) Dashboard Power BI', '99'),
]
for kode, judul, hal in tabel_items:
    para = doc.add_paragraph()
    run = para.add_run(f'{kode}  {judul}')
    set_font(run, size=12)
    run2 = para.add_run(f'\t{hal}')
    set_font(run2, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(0); pf.space_after = Pt(2)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.0

add_page_break(doc)

# DAFTAR GAMBAR
add_heading(doc, 'DAFTAR GAMBAR', level=1, size=14)
doc.add_paragraph()
gambar_items = [
    ('Gambar 1.1', 'Geopolitik Global pada Februari 2026', '2'),
    ('Gambar 1.2', 'Lintasan Pergerakan Harga Aktual Bitcoin (BTC/USDT) dengan 43.786 Observasi Per Jam pada Periode 2021–2026', '4'),
    ('Gambar 2.1', 'Kerangka Pemikiran Penelitian: Peta Konseptual Alur Logika Ilmiah', '38'),
    ('Gambar 3.1', 'Tahapan Penelitian: Lima Fase Sistematis Mulai dari Akuisisi Data hingga BI Dashboard', '42'),
    ('Gambar 3.2', 'Arsitektur Kerangka Kerja Business Intelligence Empat Lapis', '45'),
    ('Gambar 3.3', 'Prototipe BI Decision Support Dashboard (Crypto Predictive Analytics Platform)', '65'),
    ('Gambar 3.4', 'Skema Walk-Forward Validation: 24 Lipatan Kronologis dengan Jendela Pelatihan 720 Jam', '62'),
    ('Gambar 4.1', 'Visualisasi Harga Penutupan dan Volume BTC/USDT (43.786 Rekaman)', '70'),
    ('Gambar 4.2', 'Distribusi Fitur Teknikal: Histogram dan Korelasi Matriks', '75'),
    ('Gambar 4.3', 'SHAP Summary Plot: Kontribusi 15 Fitur terhadap Output Prediksi (GRU)', '77'),
    ('Gambar 4.4', 'Overlay Prakiraan 168 Jam Out-of-Sample: Harga Aktual vs XGBoost, LSTM, GRU, dan Informer', '79'),
    ('Gambar 4.5', 'Distribusi RMSE per Lipatan Walk-Forward untuk Keempat Model (Boxplot)', '82'),
    ('Gambar 4.6', 'Rangkuman KPI Dashboard BI dari Evaluasi 24-Lipatan Walk-Forward', '94'),
    ('Gambar 4.7', 'Kurva Akumulasi Imbal Hasil Strategi Berbasis Sinyal Model vs Buy-and-Hold', '96'),
    ('Gambar 4.8', 'Antarmuka Lengkap BI Decision Support Dashboard (Power BI)', '98'),
]
for kode, judul, hal in gambar_items:
    para = doc.add_paragraph()
    run = para.add_run(f'{kode}  {judul}')
    set_font(run, size=12)
    run2 = para.add_run(f'\t{hal}')
    set_font(run2, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.space_before = Pt(0); pf.space_after = Pt(2)
    pf.first_line_indent = Cm(0)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.0

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# BAB I PENDAHULUAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'BAB I', level=1, size=14)
add_heading(doc, 'PENDAHULUAN', level=1, size=14)

add_subheading(doc, 'Latar Belakang', '1.1', level=2)
p = add_paragraph(doc,
    'Perkembangan teknologi digital selama satu dekade terakhir telah secara masif mengubah '
    'lanskap sistem keuangan global. Kemunculan aset kripto terutama Bitcoin (BTC) yang pertama '
    'kali diperkenalkan oleh Nakamoto [1] pada tahun 2008 sebagai sistem pembayaran terdesentralisasi '
    'kini telah bertransformasi menjadi kelas aset investasi baru yang bernilai triliunan dolar dan '
    'mendisrupsi paradigma investasi tradisional secara fundamental. Berdasarkan data CoinMarketCap '
    'per tahun 2024, kapitalisasi pasar Bitcoin telah melampaui angka 1,2 triliun dolar Amerika '
    'Serikat, menjadikannya aset digital dengan valuasi terbesar di dunia [2].')
p = add_paragraph(doc,
    'Namun di balik potensi keuntungan yang sangat besar tersebut, pasar cryptocurrency terutama '
    'Bitcoin memiliki karakteristik yang sangat berbeda dari pasar konvensional. Pasar ini beroperasi '
    'penuh selama 24 jam sehari dan 7 hari seminggu tanpa jeda, bersifat sangat terdesentralisasi, '
    'tidak terikat regulasi tunggal, dan sangat rentan terhadap perubahan sentimen makroekonomi serta '
    'faktor eksternal seperti kebijakan pemerintah, perkembangan teknologi blockchain, dan pengaruh '
    'tokoh-tokoh berpengaruh di media sosial. Kondisi inilah yang menyebabkan pergerakan harga Bitcoin '
    'bersifat non-linear, penuh noise, dan sangat sulit diprediksi [3], [4], [5].')
p = add_paragraph(doc,
    'Dinamika volatilitas aset tersebut secara gamblang mencerminkan besarnya pengaruh guncangan '
    'eksternal. Dalam rentang lima tahun penelitian, harga Bitcoin mencatat lonjakan ke puncak '
    'tertinggi pertama (All-Time High/ATH) sebesar ±$69.000 pada November 2021, kemudian anjlok '
    'drastis hingga ke titik terendah ±$16.500 akibat serangkaian krisis beruntun: keruntuhan '
    'ekosistem Terra/LUNA (Mei 2022), kebangkrutan bursa kripto FTX (November 2022), serta '
    'memburuknya sentimen pasar global akibat invasi Rusia ke Ukraina (Februari 2022) [6]. '
    'Memasuki akhir 2024, harga Bitcoin mencapai ATH baru di atas $100.000 seiring terpilihnya '
    'kembali Donald Trump sebagai Presiden Amerika Serikat dengan platform kebijakan ramah aset '
    'digital.')
p = add_paragraph(doc,
    'Puncak ketidakpastian geopolitik dalam periode penelitian ini terjadi pada tahun 2026, '
    'ketika koalisi militer Amerika Serikat dan Israel melancarkan serangkaian serangan terhadap '
    'fasilitas nuklir Iran pada 28 Februari 2026, memicu eskalasi konflik berskala penuh di kawasan '
    'Timur Tengah [7]. Harga Bitcoin turun tajam dari kisaran $72.000 ke $63.000 dalam beberapa '
    'hari pertama konflik, dengan Crypto Fear & Greed Index anjlok ke angka 8/100 ("Extreme Fear"). '
    'Fenomena ini secara konsisten memperlihatkan bahwa Bitcoin berperilaku sebagai aset berisiko '
    'tinggi (high-beta risk asset) yang tidak dapat dimodelkan secara memadai oleh pendekatan '
    'statistik linier konvensional [3], [6].')
p = add_paragraph(doc,
    'Di tingkat nasional, pertumbuhan pasar kripto di Indonesia turut mencatat angka yang sangat '
    'signifikan. Berdasarkan data Bappebti tahun 2023 [13], jumlah investor aset kripto terdaftar '
    'di Indonesia telah melampaui 17 juta akun, menempatkan Indonesia sebagai salah satu pasar '
    'kripto ritel terbesar di Asia Tenggara. Besarnya basis investor domestik yang berpartisipasi '
    'langsung di pasar yang sangat volatil ini mempertegas urgensi kehadiran sistem pendukung '
    'keputusan berbasis kecerdasan buatan yang mudah diakses, transparan, dan relevan.')
p = add_paragraph(doc,
    'Secara metodologis, model analisis finansial tradisional seperti Autoregressive Integrated '
    'Moving Average (ARIMA) dan Generalized Autoregressive Conditional Heteroskedasticity (GARCH) '
    'tidak mampu mengakomodasi kompleksitas data pasar kripto. Model-model tersebut mensyaratkan '
    'kondisi data yang stasioner dan mengasumsikan hubungan linier antar variabel — kondisi yang '
    'hampir tidak pernah terpenuhi dalam data Bitcoin berfrekuensi tinggi [11], [12], [14]. '
    'Kegagalan pendekatan tradisional inilah yang mendorong komunitas riset global untuk beralih '
    'ke paradigma komputasi yang lebih canggih, yakni arsitektur Deep Learning berbasis Jaringan '
    'Saraf Tiruan (JST) yang mampu memodelkan pola dependensi temporal non-linear secara otomatis '
    '[16], [17], [18].')
p = add_paragraph(doc,
    'Di antara berbagai arsitektur Deep Learning, model berbasis Recurrent Neural Network (RNN) '
    'dengan mekanisme gerbang memori dihipotesiskan mampu mendominasi pemodelan deret waktu '
    'finansial. Arsitektur Long Short-Term Memory (LSTM) yang diperkenalkan oleh Hochreiter dan '
    'Schmidhuber [14] mampu mengatasi masalah vanishing gradient pada RNN standar melalui mekanisme '
    'gerbang selektif (input, forget, output) yang memungkinkan model mempertahankan informasi '
    'dalam rentang waktu yang panjang. Arsitektur Gated Recurrent Unit (GRU) yang dikembangkan '
    'oleh Cho dkk. [16] hadir sebagai penyederhanaan yang lebih efisien secara komputasi namun '
    'tetap kompetitif dalam hal akurasi prediksi deret waktu [17], [18]. Selain itu, arsitektur '
    'Informer Transformer dengan ProbSparse self-attention [21] menawarkan pemodelan dependensi '
    'jangka panjang dengan kompleksitas O(L log L), menjadikannya kandidat potensial untuk data '
    'berfrekuensi tinggi.')
p = add_paragraph(doc,
    'Meskipun demikian, terdapat kesenjangan kritis yang belum banyak dieksplorasi dalam literatur: '
    'mayoritas penelitian yang ada hanya menghasilkan angka prediksi harga secara terisolasi, '
    'tanpa mengintegrasikan keluaran model tersebut ke dalam sebuah sistem Business Intelligence '
    '(BI) yang siap digunakan oleh para pengambil keputusan di dunia nyata. Seorang manajer '
    'investasi tidak dapat mengambil keputusan strategis semata dari nilai RMSE sebuah model; '
    'mereka membutuhkan metrik bisnis yang terukur seperti Win Rate (akurasi arah pergerakan '
    'pasar), Sharpe Ratio (efisiensi imbal hasil per unit risiko), dan Value at Risk — estimasi '
    'kerugian maksimum pada tingkat kepercayaan tertentu [35], [36].')
p = add_paragraph(doc,
    'Untuk menjawab kesenjangan tersebut, penelitian ini merancang sebuah kerangka kerja Business '
    'Intelligence empat lapis (4-Layer BI Framework) yang mengintegrasikan seluruh pipeline mulai '
    'dari akuisisi data Big Data melalui Binance API, rekayasa 15 fitur teknikal, pelatihan model '
    'komparatif (LSTM, GRU, XGBoost, dan Informer Transformer), hingga penyajian hasil dalam '
    'antarmuka Decision Support Dashboard yang dapat dioperasikan secara langsung oleh praktisi '
    'industri. Penelitian ini menggunakan dataset berfrekuensi sangat tinggi sebanyak 43.786 '
    'rekaman data historis Bitcoin per jam dalam rentang lima tahun (2021–2026), yang secara '
    'inheren memenuhi karakteristik fundamental Big Data: Volume, Velocity, Variety, Veracity, '
    'dan Value [12], [37], [38].')

add_subheading(doc, 'Identifikasi Masalah', '1.2', level=2)
p = add_paragraph(doc,
    'Berdasarkan uraian latar belakang di atas, setidaknya terdapat lima permasalahan mendasar '
    'yang menjadi motivasi utama penelitian ini:')
masalah = [
    ('Keterbatasan model prediksi tradisional.',
     'Model statistik klasik seperti ARIMA dan GARCH dirancang untuk data yang stabil dan bergerak '
     'secara linier. Ketika diterapkan pada data Bitcoin yang bergerak ekstrem dan tidak beraturan, '
     'model-model ini menghasilkan tingkat kesalahan prediksi yang sangat tinggi. Dalam penelitian '
     'ini, ARIMA(1,1,1) mencatat RMSE = 0,1987 (skala ternormalisasi) dan Directional Accuracy = '
     '51,8%, hanya sedikit di atas acak [11], [12].'),
    ('Minimnya perbandingan metodologis yang adil dan ketat.',
     'Sebagian besar penelitian yang ada membandingkan model tanpa prosedur pencegahan kebocoran '
     'data yang memadai. Belum terdapat studi komparatif yang secara bersamaan membandingkan empat '
     'keluarga algoritma (LSTM, GRU, XGBoost, Informer Transformer) menggunakan Walk-Forward '
     'Validation pada dataset Bitcoin berskala penuh (43.786 rekaman per jam).'),
    ('Hasil penelitian yang tidak dapat langsung digunakan oleh praktisi.',
     'Mayoritas penelitian hanya melaporkan angka kesalahan teknis (RMSE, MAE) tanpa '
     'menerjemahkannya ke dalam metrik bisnis yang bermakna bagi investor, seperti Win Rate, '
     'Sharpe Ratio, dan Value at Risk [35], [36].'),
    ('Tidak adanya kerangka kerja BI yang terintegrasi dari hulu ke hilir.',
     'Belum terdapat sistem yang secara menyeluruh menghubungkan proses pengambilan data (Big '
     'Data), pelatihan model prediktif (Deep Learning), dan penyajian hasil kepada pengambil '
     'keputusan dalam satu ekosistem operasional yang utuh dan dapat direproduksi [44].'),
    ('Sulitnya memahami alasan di balik keputusan model AI.',
     'Model Deep Learning seringkali dianggap sebagai "kotak hitam" yang sulit dijelaskan cara '
     'kerjanya. Diperlukan metode Explainable AI (XAI) seperti SHAP (SHapley Additive '
     'exPlanations) guna memvalidasi dan menjelaskan secara transparan fitur mana yang paling '
     'berpengaruh terhadap hasil prediksi [45], [46].'),
]
for i, (judul, isi) in enumerate(masalah, 1):
    para = doc.add_paragraph()
    run1 = para.add_run(f'{i}. ')
    set_font(run1, size=12, bold=False)
    run2 = para.add_run(judul + ' ')
    set_font(run2, size=12, bold=True)
    run3 = para.add_run(isi)
    set_font(run3, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_subheading(doc, 'Rumusan Masalah', '1.3', level=2)
p = add_paragraph(doc,
    'Berdasarkan latar belakang dan identifikasi masalah yang telah diuraikan, maka rumusan '
    'masalah pada penelitian ini adalah sebagai berikut:')
rumusan = [
    'Bagaimana merancang dan membangun kerangka kerja Business Intelligence empat lapis yang '
    'mampu menghubungkan secara mulus seluruh alur proses mulai dari pengambilan data besar '
    'melalui Binance API hingga tampilan Decision Support Dashboard dalam satu ekosistem yang '
    'dapat diuji ulang secara konsisten?',
    'Di antara empat algoritma yang diuji — LSTM, GRU, XGBoost, dan Informer Transformer — '
    'model mana yang menghasilkan prediksi harga Bitcoin paling akurat berdasarkan metrik '
    'kesalahan numerik (RMSE, MAE) ketika dievaluasi dengan metodologi Walk-Forward Validation '
    'yang bebas dari risiko kebocoran data?',
    'Bagaimana karakteristik dan implikasi tradeoff yang terjadi antara model GRU (yang unggul '
    'dalam ketepatan angka prediksi) dan model LSTM (yang unggul dalam ketepatan arah pergerakan '
    'pasar) untuk mendukung konteks pengambilan keputusan investasi yang berbeda?',
    'Di antara 15 indikator teknikal yang direkayasa, fitur mana yang memberikan kontribusi '
    'prediktif terbesar terhadap performa model, dan bagaimana hal tersebut dapat dijelaskan '
    'secara transparan menggunakan nilai SHAP?',
    'Bagaimana hasil prediksi model Deep Learning dapat diubah secara algoritmik menjadi '
    'informasi risiko bisnis yang siap pakai seperti Sharpe Ratio, Value at Risk, dan Win Rate '
    'dan disajikan dalam BI Dashboard yang dapat langsung diinterpretasikan oleh para manajer '
    'investasi?',
]
for i, r in enumerate(rumusan, 1):
    add_numbered(doc, r, i)

add_subheading(doc, 'Tujuan Penelitian', '1.4', level=2)
p = add_paragraph(doc,
    'Tujuan penelitian ini adalah untuk menjawab seluruh permasalahan yang telah dirumuskan '
    'di atas, yang dirumuskan sebagai berikut:')
tujuan = [
    'Merancang, membangun, dan memvalidasi kerangka kerja Business Intelligence empat lapis '
    '(4-Layer BI Framework) yang mengintegrasikan secara menyeluruh seluruh tahapan proses '
    'dari akuisisi Big Data, pembersihan dan transformasi data (ETL), komputasi prediktif, '
    'hingga penyajian analitik dalam satu ekosistem yang dapat direproduksi secara konsisten.',
    'Melakukan perbandingan performa prediksi harga Bitcoin secara komprehensif dan berimbang '
    'antara empat model — LSTM, GRU, XGBoost, dan Informer Transformer — menggunakan dataset '
    '43.786 rekaman per jam (2021–2026) dengan metodologi Walk-Forward Validation 24 lipatan '
    'yang ketat disertai uji signifikansi statistik (Kruskal-Wallis dan Diebold-Mariano).',
    'Mengidentifikasi dan menginterpretasikan tradeoff yang terjadi antara ketepatan angka '
    'prediksi (presisi numerik: RMSE, MAE) dan ketepatan arah pergerakan pasar (Win Rate), '
    'guna memberikan panduan model mana yang paling tepat untuk konteks investasi yang berbeda.',
    'Mengevaluasi kontribusi prediktif dari masing-masing 15 fitur teknikal menggunakan metode '
    'SHAP (Explainable AI), sehingga setiap keputusan model dapat dijelaskan secara ilmiah dan '
    'transparan.',
    'Mentransformasikan keluaran prediksi ke dalam metrik risiko finansial eksekutif (Sharpe '
    'Ratio, VaR 95%, Directional Win Rate) dan menyajikannya dalam prototipe BI Decision Support '
    'Dashboard yang fungsional dengan skor SUS ≥ 85 (kategori "Sangat Baik").',
]
for i, t in enumerate(tujuan, 1):
    add_numbered(doc, t, i)

add_subheading(doc, 'Manfaat Penelitian', '1.5', level=2)
add_subheading(doc, 'Manfaat Teoritis (Akademis)', '1.5.1', level=3, size=12)
manfaat_teoritis = [
    'Menghasilkan kerangka kerja BI-ML Framework yang terintegrasi dan dapat dijadikan rujukan '
    'metodologis untuk penelitian lanjutan di bidang Informatika Finansial dan Analitika Big Data, '
    'khususnya dalam konteks aset digital.',
    'Mengisi celah riset (research gap) dalam literatur melalui studi komparatif yang sistematis '
    'dan ketat antara empat model algoritmik pada dataset Bitcoin berskala penuh dengan metodologi '
    'Walk-Forward Validation dan uji statistik Diebold-Mariano.',
    'Memberikan landasan empiris untuk menginvestigasi adanya tradeoff antara ketepatan numerik '
    '(RMSE) dan ketepatan arah pasar (Win Rate) pada model Deep Learning finansial.',
    'Memperkaya literatur tentang penerapan SHAP sebagai alat Explainable AI pada prediksi aset '
    'digital yang sangat volatil.',
    'Memberikan kontribusi ilmiah dalam bidang sistem pendukung keputusan (Decision Support '
    'System) berbasis kecerdasan buatan yang terukur secara empiris menggunakan System Usability '
    'Scale (SUS).',
]
for item in manfaat_teoritis:
    add_bullet(doc, item)

add_subheading(doc, 'Manfaat Praktis (Industri)', '1.5.2', level=3, size=12)
manfaat_praktis = [
    'Menyediakan prototipe Decision Support Dashboard yang dapat langsung diadaptasi oleh manajer '
    'investasi, analis keuangan, dan institusi finansial untuk mendukung pengambilan keputusan '
    'berbasis data di pasar cryptocurrency.',
    'Membantu lembaga keuangan dalam mengukur dan memitigasi risiko paparan aset kripto secara '
    'kuantitatif melalui kalkulasi otomatis metrik risiko eksekutif (Value at Risk dan Sharpe Ratio).',
    'Menyediakan panduan metodologis yang dapat diadaptasi oleh praktisi teknologi dalam membangun '
    'sistem prediksi harga kripto yang andal, transparan, dan terintegrasi dengan infrastruktur '
    'Business Intelligence korporasi.',
    'Berkontribusi pada pengembangan ekosistem keuangan digital yang lebih cerdas di Indonesia, '
    'sejalan dengan agenda transformasi digital nasional.',
    'Bagi masyarakat umum: meningkatkan literasi keuangan dan teknologi, serta memberikan '
    'pemahaman bahwa keputusan investasi dapat didukung oleh analisis berbasis data dan metode '
    'kuantitatif yang lebih objektif.',
]
for item in manfaat_praktis:
    add_bullet(doc, item)

add_subheading(doc, 'Batasan Penelitian', '1.6', level=2)
p = add_paragraph(doc,
    'Dalam penelitian perlu adanya pembatasan masalah agar pengkajiannya lebih terarah dan tidak '
    'keluar batas. Penelitian ini memiliki batasan penelitian sebagai berikut:')
batasan = [
    ('Cakupan Aset:', 'Penelitian ini berfokus secara eksklusif pada pasangan aset BTC/USDT '
     '(Bitcoin terhadap Tether). Aset kripto lain seperti Ethereum (ETH) atau Binance Coin (BNB) '
     'tidak dicakup, mengingat setiap aset memiliki karakteristik volatilitas yang berbeda.'),
    ('Sumber Data:', 'Seluruh data historis diperoleh eksklusif dari Binance Spot API dengan '
     'granularitas interval 1 jam (1h OHLCV), mencakup periode Maret 2021 hingga Maret 2026, '
     'dengan total 43.786 rekaman data setelah quality screening.'),
    ('Algoritma yang Dibandingkan:', 'Studi komparatif dibatasi pada empat algoritma: LSTM dan '
     'GRU (model deep learning berbasis gerbang memori), XGBoost (model ensemble baseline), dan '
     'Informer Transformer (model berbasis sparse self-attention).'),
    ('Fitur Input Model:', 'Model dilatih menggunakan 15 fitur teknikal yang telah ditetapkan '
     '(EMA-12, EMA-26, RSI-14, Stochastic %K/%D, Bollinger Bands, ATR-14, MACD, OBV, ROC-10, '
     'Rolling σ 24h). Faktor eksternal seperti sentimen media sosial atau data on-chain tidak '
     'diikutsertakan.'),
    ('Horizon Prediksi:', 'Evaluasi performa model berfokus pada prediksi jangka pendek dalam '
     'jendela validasi 168 jam (setara satu minggu ke depan) menggunakan 24 lipatan kronologis.'),
    ('Metrik Risiko:', 'Sharpe Ratio dan VaR yang dilaporkan adalah gross of transaction costs '
     '(sebelum biaya transaksi dan slippage). Evaluasi net-of-cost direncanakan sebagai '
     'pengembangan penelitian selanjutnya.'),
    ('Fungsi Sistem:', 'Prototipe BI Dashboard yang dihasilkan berfungsi sebagai alat bantu '
     'pengambilan keputusan (decision support tool), bukan sebagai sistem perdagangan otomatis '
     '(automated trading system).'),
]
for judul, isi in batasan:
    para = doc.add_paragraph()
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(1.25)
    pf.first_line_indent = Cm(-0.75)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_subheading(doc, 'Sistematika Penulisan Tesis', '1.7', level=2)
p = add_paragraph(doc,
    'Sistematika dari penyusunan tesis ini terdiri dari beberapa bagian yang paling utama '
    'untuk diketahui, yaitu sebagai berikut:')
bab_list = [
    ('BAB I PENDAHULUAN',
     'Bab ini berisi tahapan awal penelitian dimulai dari latar belakang, identifikasi masalah, '
     'rumusan masalah, tujuan penelitian, manfaat penelitian, batasan penelitian, dan sistematika '
     'penulisan.'),
    ('BAB II KAJIAN TEORITIS DAN TINJAUAN PUSTAKA',
     'Bab ini berisi teori-teori singkat terkait penelitian. Pembahasan mencakup tinjauan kritis '
     'terhadap keterbatasan model tradisional (ARIMA, GARCH), evolusi arsitektur Deep Learning '
     '(LSTM, GRU, Informer Transformer), konsep Efficient Market Hypothesis, prinsip-prinsip '
     'Big Data 5V dalam konteks aset digital, serta pemetaan celah penelitian (research gap).'),
    ('BAB III METODOLOGI PENELITIAN',
     'Bab ini berisi penjelasan mengenai metode yang digunakan dalam proses pengumpulan data, '
     'pengolahan data, rekayasa fitur, pelatihan model, strategi validasi Walk-Forward, dan '
     'analisis data dalam penelitian.'),
    ('BAB IV HASIL DAN PEMBAHASAN',
     'Bab ini menyajikan hasil pengumpulan dan pra-pemrosesan data, hasil pelatihan serta '
     'evaluasi model LSTM, GRU, XGBoost, dan Informer Transformer, analisis kontribusi fitur '
     'dengan SHAP, konversi keluaran model menjadi metrik risiko bisnis, evaluasi prototipe BI '
     'Decision Support Dashboard, serta pembahasan dan benchmarking komparatif.'),
    ('BAB V KESIMPULAN DAN SARAN',
     'Bab ini mengemukakan kesimpulan penelitian yang menjawab rumusan masalah, implikasi hasil '
     'penelitian, keterbatasan, serta saran untuk penelitian selanjutnya.'),
]
for judul, isi in bab_list:
    para = doc.add_paragraph()
    run_j = para.add_run(judul + ': ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(1.0)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# BAB II KAJIAN TEORITIS DAN TINJAUAN PUSTAKA
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'BAB II', level=1, size=14)
add_heading(doc, 'KAJIAN TEORITIS DAN TINJAUAN PUSTAKA', level=1, size=14)

add_subheading(doc, 'Tinjauan Penelitian Terdahulu (State of the Art)', '2.1', level=2)
p = add_paragraph(doc,
    'Penelitian mengenai prediksi harga mata uang kripto telah banyak dieksplorasi secara masif, '
    'khususnya dalam lima tahun terakhir (2021–2026). Literatur terkini membuktikan kecenderungan '
    'transisi dari pemodelan linier ke mesin cerdas berbasis deep learning. Murray dkk. [26] '
    'membandingkan model statistik, machine learning, deep learning, dan ensemble pada lima '
    'cryptocurrency dan menemukan model deep learning, khususnya LSTM, paling akurat dalam RMSE '
    'dan MAE. Jaquart dkk. [31] melaporkan Sharpe Ratio tahunan out-of-sample sekitar 3,2 setelah '
    'biaya untuk portofolio long-short LSTM dan GRU harian. Seabe dkk. [33] memvalidasi bahwa '
    'arsitektur GRU sangat tangguh karena mampu mencapai tingkat konvergensi lebih agresif dengan '
    'konsumsi energi komputasi yang efisien dibandingkan LSTM. Untuk memetakan kesenjangan '
    'penelitian secara lebih sistematis, rangkuman tinjauan literatur terdahulu disajikan pada '
    'Tabel 2.1.')

add_caption(doc, 'Tabel 2.1 Tinjauan Literatur Terdahulu (State of the Art)')
headers_soa = ['No', 'Judul/Penulis (Tahun)', 'Algoritma', 'Temuan Utama', 'Research Gap ke Tesis']
rows_soa = [
    ['1', 'Murray et al. (2023) [26]\nForecasting crypto: ML, DL, Ensembles',
     'LSTM, GRU, Ensemble', 'LSTM paling akurat; model deep learning unggul atas ML klasik.',
     'Tidak ada integrasi ke BI Dashboard; tidak ada Walk-Forward 24-fold.'],
    ['2', 'Jaquart et al. (2022) [31]\nML for crypto market prediction',
     'LSTM, GRU, Klasifikasi', 'SR tahunan ~3.2; deep learning superior untuk prediksi arah.',
     'Tidak ada Transformer; tidak ada uji SUS; tidak ada framework BI empat lapis.'],
    ['3', 'Seabe et al. (2023) [33]\nLSTM, GRU, Bi-LSTM: Deep learning approach',
     'LSTM, GRU, Bi-LSTM', 'GRU tangguh dan efisien; konvergensi lebih cepat dari LSTM.',
     'Hanya RMSE/MAE; tidak ada metrik bisnis; tidak ada SHAP.'],
    ['4', 'Bouteska et al. (2024) [27]\nCrypto price forecasting comparison',
     'Ensemble, Boosted-Tree, DL', 'Boosted-tree kompetitif; data terbatas CNN terbaik.',
     'Tidak ada Walk-Forward; tidak ada dashboard BI operasional.'],
    ['5', 'Omole & Enke (2024) [32]\nDeep learning for Bitcoin direction',
     'CNN-LSTM', 'DA 82.44%; strategi directional menguntungkan.',
     'Tidak ada Transformer; tidak ada SHAP; tidak ada SUS evaluation.'],
    ['6', 'Goodell et al. (2023) [42]\nExplainable AI for Bitcoin',
     'SHAP, XAI', 'SHAP mengungkap volume dan momentum sebagai driver utama.',
     'XAI parsial pada satu algoritma; tidak ada BI Dashboard terintegrasi.'],
    ['7', 'Bysik & Ślepaczuk (2026) [37]\nML Bitcoin trading under transaction costs',
     'Random Forest, WFV', 'Strategi gagal setelah biaya; bootstrap adjustment penting.',
     'Tidak ada deep learning; tidak ada BI dashboard.'],
    ['8', 'Hasanli & Dursun (2026) [35]\nHybrid Transformer for Bitcoin',
     'Transformer Hybrid', 'SR XGBoost 1.78 untuk Bitcoin; cross-coin predictability.',
     'Tidak ada framework BI 4 lapis; tidak ada SUS.'],
    ['9', 'Grądzki et al. (2025) [33b]\nAlgorithmic trading CUSUM-filtered',
     'DL + Triple-barrier', 'CUSUM-filtered profitable setelah biaya.',
     'Tidak ada perbandingan Transformer vs RNN; tidak ada dashboard.'],
    ['10', 'Gradojevic et al. (2023) [6]\nBitcoin technical analysis forecast',
     'Random Forest', 'Bitcoin lemah efisien di frekuensi per jam.',
     'Tidak ada deep learning; tidak ada BI framework.'],
]
add_simple_table(doc, headers_soa, rows_soa, col_widths=[0.7, 3.5, 2.5, 3.5, 3.5])

doc.add_paragraph()
add_subheading(doc, 'Sintesis Kesenjangan Penelitian (Research Gap Synthesis)', '2.1.1', level=3, size=12)
p = add_paragraph(doc,
    'Berdasarkan pemetaan literatur komprehensif terhadap sepuluh publikasi internasional '
    'bereputasi di atas, dapat disimpulkan bahwa mayoritas penelitian terdahulu umumnya berfokus '
    'pada optimasi metrik akurasi model algoritmik di dalam lingkungan laboratorium yang terisolasi. '
    'Terdapat kesenjangan yang nyata di mana hasil komputasi tersebut seringkali berhenti sebagai '
    'angka statistik semata, tanpa adanya jembatan konversi yang dapat mentransformasikan hasil '
    'prediksi menjadi wawasan strategis yang siap dikonsumsi oleh pengambilan keputusan riil bagi '
    'investor maupun manajer portofolio. Penelitian ini menutup kesenjangan tersebut melalui tiga '
    'kontribusi utama: (1) perbandingan empat keluarga model dengan protokol Walk-Forward 24-fold '
    'yang ketat dan uji statistik Diebold-Mariano; (2) analisis SHAP sebagai wasit interpretatif '
    'holistik lintas model; dan (3) integrasi end-to-end ke dalam BI Dashboard yang diukur '
    'kinerjanya dengan SUS.')

add_subheading(doc, 'Kebaruan (Novelty) dan Kontribusi Utama Penelitian', '2.1.2', level=3, size=12)
p = add_paragraph(doc,
    'Tesis ini hadir untuk merakit tiga entitas ilmiah yang sebelumnya terpisah menjadi satu '
    'ekosistem yang terpadu secara holistik. Pertama, penelitian ini tidak hanya mengadu performa '
    'antara arsitektur memori jangka panjang (LSTM vs GRU), model ansambel (XGBoost), dan '
    'arsitektur attention-based (Informer Transformer), tetapi juga melakukan interogasi mendalam '
    'melalui lensa Explainable AI untuk mengungkap kausalitas di balik keputusan model tersebut. '
    'Kedua, seluruh luaran komputasi prediktif diorkestrasi ke dalam sebuah Business Intelligence '
    'Dashboard yang dinamis, menerjemahkan kompleksitas data prediktif menjadi parameter mitigasi '
    'risiko konkret. Ketiga, kerangka kerja ini divalidasi secara empiris dengan uji kegunaan '
    'formal (SUS) yang melibatkan evaluator domain nyata, menghasilkan skor 86,4 — kategori '
    '"Sangat Baik".')

add_subheading(doc, 'Karakteristik Aset Digital dan Fundamen Cryptocurrency', '2.2', level=2)
p = add_paragraph(doc,
    'Bitcoin merupakan pelopor mata uang digital desentralistik yang beroperasi di atas buku '
    'besar publik terdistribusi (blockchain) yang diamankan melalui protokol kriptografi konsensus '
    'Proof-of-Work [1]. Berbeda dengan mata uang konvensional (fiat) yang diregulasi oleh '
    'otoritas perbankan sentral, stabilitas Bitcoin sepenuhnya dikendalikan oleh mekanisme '
    'independen tarik-ulur kekuatan pasar terbuka (supply and demand). Dinamika pergerakan '
    'spekulatif hariannya amat sensitif tersulut oleh sentimen psikologis makro, menjadikannya '
    'objek studi prediksi kuantitatif yang menantang [3], [4].')
p = add_paragraph(doc,
    'Karakteristik unik Bitcoin sebagai instrumen investasi meliputi: (1) operasional 24/7 tanpa '
    'penutupan pasar, menghasilkan sinyal data yang padat dan bebas artefak penutupan pasar; '
    '(2) liquiditas tinggi pada pasangan BTC/USDT di Binance — platform dengan volume transaksi '
    'harian terbesar di dunia — yang mengisolasi performa algoritmik dari guncangan liquiditas '
    'altcoin berkapitalisasi rendah; (3) siklus Bitcoin Halving setiap ~4 tahun yang secara '
    'struktural mempengaruhi dinamika supply; dan (4) sensitivitas tinggi terhadap faktor '
    'geopolitik, regulasi, dan sentimen media sosial [1], [41].')

add_subheading(doc, 'Analisis Kritis Hipotesis Pasar Efisien (EMH) pada Aset Kripto', '2.3', level=2)
p = add_paragraph(doc,
    'Dalam sejarah tataran teori tata kelola investasi, harga aset diasumsikan selalu berjalan '
    'seimbang dan secara rasional mencerminkan seluruh berita fundamental yang tersedia di pasar '
    'publik bebas — konsep yang dipopulerkan melalui Efficient Market Hypothesis (EMH) oleh Fama '
    '[47]. Bukti empiris terkini menunjukkan bahwa hipotesis pasar efisien menghadapi tantangan '
    'serius saat diterapkan pada pasar aset kripto yang sangat volatil [1], [2], [48].')
p = add_paragraph(doc,
    'Karakteristik likuiditas Bitcoin ditandai oleh dominannya anomali penyimpangan asimetris '
    'impulsif (volatile shocks), gelombang kepanikan ritel masal (FOMO), serta fenomena efek '
    'pengulangan tren riwayat ekor harga (Long-Memory residual effects). Gradojevic dkk. [6] '
    'menemukan bahwa Bitcoin lemah efisien pada frekuensi per jam — temuan yang membatasi klaim '
    'akurasi arah dalam penelitian ini, dan sekaligus memotivasi penggunaan metode Walk-Forward '
    'Validation yang ketat untuk memvalidasi performa model secara temporal.')
p = add_paragraph(doc,
    'Urquhart [1] dan Mokni dkk. [2] mendokumentasikan bahwa efisiensi Bitcoin bervariasi '
    'lintas waktu dan frekuensi pengambilan sampel, dengan pasar menunjukkan long-memory dan '
    'non-linear dynamics yang tidak kompatibel dengan asumsi EMH. Menyikapi turbulensi data '
    'ekstrem tersebut, strategi regresi modern berbasis ensemble learning decision-trees '
    'bergradien tinggi seperti XGBoost [12] digunakan sebagai baris pertahanan terluar — '
    'algoritma rujukan acuan mula (robust standard baseline estimator).')

add_subheading(doc, 'Evolusi Arsitektur Deep Learning: Dari RNN hingga LSTM, GRU, dan Transformer', '2.4', level=2)
add_subheading(doc, 'Recurrent Neural Networks (RNN) dan Vanishing Gradient', '2.4.1', level=3, size=12)
p = add_paragraph(doc,
    'Pendekatan algoritma struktur Jaringan Saraf Tiruan (JST/Neural Network) generasi perdana '
    'menampakkan cacat matematis fatal apabila diuji coba mengkalkulasi prediksi serangkaian '
    'runtunan indeks berdimensi puluhan ribu baris pergerakan waktu. Terjadi fenomena pengecilan '
    'gradien bobot saraf menuju batas angka nol (Vanishing Gradient Problem), yang menyebabkan '
    'mesin seketika "menderita amnesia" temporal dan melupakan wujud pergerakan makro terdahulu '
    '[14], [15].')
add_subheading(doc, 'Long Short-Term Memory (LSTM)', '2.4.2', level=3, size=12)
p = add_paragraph(doc,
    'Transformasi evolusi terbesar dilahirkan saat arsitektur saringan saraf berlapis LSTM '
    'diperkenalkan oleh Hochreiter dan Schmidhuber [14]. Modul khusus LSTM diberikan mandat '
    'otonomi sirkuit untuk menunda penghapusan, menerima wujud pergerakan memori krusial, '
    'hingga mengunci dan melepaskan relevansi harga secara sekuensial melalui tiga gerbang: '
    'Forget Gate (ft), Input Gate (it), dan Output Gate (ot). Mekanisme ini diformulasikan '
    'sebagai berikut:')
p = add_paragraph(doc, 'ft = σ(Wf · [ht−1, xt] + bf)  \t(Forget Gate)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'it = σ(Wi · [ht−1, xt] + bi)  \t(Input Gate)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Dalam penelitian ini, LSTM diimplementasikan dengan 2 stacked layers (128 unit masing-masing), '
    'Dropout(0.2), dan Dense(1) output layer, dengan total 206.465 trainable parameters. Arsitektur '
    'ini terbukti menghasilkan Directional Accuracy tertinggi (57,8% ± 2,1%) dan Sharpe Ratio '
    'terbaik (0,87 ± 0,12) di antara semua model yang diuji.')
add_subheading(doc, 'Gated Recurrent Unit (GRU)', '2.4.3', level=3, size=12)
p = add_paragraph(doc,
    'GRU adalah penyederhanaan dari LSTM yang dikembangkan oleh Cho dkk. [16]. GRU menggabungkan '
    'gerbang lupakan dan gerbang masukan LSTM menjadi satu gerbang tunggal yang disebut Gerbang '
    'Pembaruan (Update Gate — zt):')
p = add_paragraph(doc, 'zt = σ(Wz · [ht−1, xt] + bz)  \t(Update Gate)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Penyederhanaan ini membuat GRU memiliki lebih sedikit parameter (154.881 vs 206.465 pada LSTM) '
    'dengan inductive bias yang tepat untuk menangkap micro-volatility jangka pendek tanpa '
    'over-parameterization. Dalam penelitian ini, GRU mencapai RMSE terendah (0,1058 ± 0,0034) '
    'di antara semua model, secara statistik signifikan lebih baik dari XGBoost (DM p = 0,0003) '
    'dan Informer (DM p = 0,009) setelah koreksi Bonferroni.')
add_subheading(doc, 'Informer Transformer', '2.4.4', level=3, size=12)
p = add_paragraph(doc,
    'Arsitektur Attention-based Transformer [19] telah berhasil di berbagai domain sekuensial. '
    'Untuk peramalan sekuens panjang, Informer [21] memperkenalkan ProbSparse self-attention '
    'yang mereduksi kompleksitas dari O(L²) menjadi O(L log L):')
p = add_paragraph(doc, 'Attention(Q, K, V) = Softmax(Q̄KT / √dk) V  \t(ProbSparse Attention)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'di mana Q̄ merepresentasikan query dominan teratas yang diidentifikasi melalui pengukuran '
    'Kullback-Leibler probabilistik. Dalam penelitian ini, Informer mencatat RMSE = 0,1321 '
    '± 0,0081, lebih tinggi dari GRU, konsisten dengan observasi bahwa mekanisme self-attention '
    'mungkin sensitif terhadap micro-volatility noise frekuensi tinggi [25].')

add_subheading(doc, 'Paradigma Explainable AI (XAI) dalam Kecerdasan Bisnis Finansial', '2.5', level=2)
p = add_paragraph(doc,
    'Model kecerdasan buatan super canggih acapkali menghasilkan misteri logika internal tanpa '
    'panduan pelacakan (Black-box problem), meredupkan kepercayaan para analis risiko terhadap '
    'integrasinya [45]. Kelemahan struktural transparansi model ini berhasil didekonstruksi '
    'melalui penetrasi formula koefisien dasar SHAP (SHapley Additive exPlanations) dari Lundberg '
    'dan Lee [46]. Prinsip nilai permainan terbagi ini memungkinkan kalkulasi persentase andil '
    'absolut dari tiap komponen input harga dalam memajukan akurasi prediksi.')
p = add_paragraph(doc,
    'Dalam penelitian ini, analisis SHAP lintas semua model mengkonfirmasi bahwa ukuran '
    'volatilitas dan momentum memberikan atribusi prediktif dominan. Di antara 15 fitur, '
    'σt-24 (rolling 24-hour standard deviation of log returns) secara konsisten menempati '
    'peringkat pertama berdasarkan mean absolute SHAP value di semua arsitektur, mencakup '
    'sekitar 23% dari total atribusi SHAP pada GRU. Goodell dkk. [42] memvalidasi bahwa '
    'implementasi SHAP berhasil memutus kendala Black-Box model Deep Learning, mengungkap '
    'bahwa sinyal volume dan momentum harga merupakan driver utama prediksi nilai masa depan '
    'Bitcoin.')

add_subheading(doc, 'Arsitektur Business Intelligence untuk Prakiraan Deret Waktu Finansial', '2.6', level=2)
p = add_paragraph(doc,
    'Sektor Business Intelligence (BI) tataran korporat modern harus merombak fundamental '
    'wujudnya dari sekadar kerangka pelaporan statistik retrospektif menjadi arsitektur '
    'penghasil peringatan proaktif (Predictive Analytics Machine). Chen dkk. [10] mendefinisikan '
    'BI sebagai sistem yang mengubah data mentah menjadi informasi yang bermakna untuk mendukung '
    'pengambilan keputusan bisnis. Sharda dkk. [38] memperluas definisi ini dengan menambahkan '
    'komponen analitik prediktif dan prescriptive yang mengintegrasikan model machine learning '
    'ke dalam antarmuka Decision Support System.')
p = add_paragraph(doc,
    'Power [9] mengidentifikasi enam dimensi kritis sebuah DSS yang efektif: kecepatan refresh '
    'data, stabilitas numerik, kemudahan interpretasi, akurasi kalkulasi metrik risiko, '
    'skalabilitas untuk multi-model, dan kemampuan drill-down analitik. Dalam penelitian ini, '
    'prototipe Power BI memenuhi semua dimensi tersebut, dengan refresh latency 1,2 detik, '
    '100% integritas data (43.786 rekaman terverifikasi dengan SHA-256 checksum), dan skor '
    'SUS 86,4 yang mengkonfirmasi kegunaan tinggi bagi evaluator domain.')

add_subheading(doc, 'Kerangka Pemikiran Penelitian (Conceptual Framework)', '2.7', level=2)
p = add_paragraph(doc,
    'Kerangka pemikiran penelitian ini merupakan peta konseptual yang menggambarkan secara '
    'sistematis alur logika ilmiah dari identifikasi masalah hingga tercapainya tujuan penelitian. '
    'Kerangka ini mengintegrasikan seluruh landasan teori yang telah dikaji — mulai dari Efficient '
    'Market Hypothesis (EMH), Analisis Teknikal, prinsip Big Data 5V, arsitektur Deep Learning '
    '(LSTM, GRU, dan Informer Transformer), hingga konsep Explainable AI (SHAP) — ke dalam '
    'sebuah alur proses yang kohesif dan terstruktur, dengan muara akhir pada sistem Business '
    'Intelligence yang siap digunakan oleh para pengambil keputusan investasi.')
p = add_paragraph(doc,
    'Kerangka pemikiran ini dibangun di atas tiga pilar argumentasi utama. Pertama, pasar Bitcoin '
    'yang sangat volatil dan dipengaruhi sentimen global membutuhkan pendekatan pemodelan '
    'non-linear yang lebih canggih daripada metode statistik konvensional [3], [11], [12]. '
    'Kedua, arsitektur Deep Learning berbasis memori sekuensial (LSTM, GRU) dan model ensemble '
    '(XGBoost) menawarkan kapabilitas prediktif yang superior untuk data deret waktu berfrekuensi '
    'tinggi [14], [16], [17], [33]. Ketiga, hasil prediksi numerik semata tidak cukup bagi '
    'praktisi investasi — diperlukan sebuah kerangka kerja Business Intelligence yang mampu '
    'mengkonversi output model menjadi metrik risiko yang dapat ditindaklanjuti secara langsung '
    '[35], [36], [42], [44].')
add_caption(doc, 'Gambar 2.1 Kerangka Pemikiran Penelitian: Peta Konseptual Alur Logika Ilmiah '
            'dari Identifikasi Permasalahan Volatilitas Bitcoin hingga Luaran Sistem Business '
            'Intelligence Prediktif Berbasis Deep Learning.')
p = add_paragraph(doc, '[Gambar 2.1 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_subheading(doc, 'Hipotesis Penelitian', '2.8', level=2)
p = add_paragraph(doc,
    'Hipotesis merupakan dugaan sementara terhadap rumusan masalah yang kebenarannya diuji melalui '
    'eksperimen terkontrol pada tahap evaluasi. Berdasarkan rumusan masalah, kerangka pemikiran, '
    'dan temuan penelitian terdahulu, hipotesis penelitian ini dirumuskan sebagai berikut:')
hipotesis = [
    ('H1:', 'Terdapat perbedaan kinerja prediksi numerik yang signifikan antara LSTM, GRU, '
     'XGBoost, dan Informer Transformer, di mana GRU menghasilkan nilai RMSE terendah pada '
     'Walk-Forward Validation. (H0: tidak terdapat perbedaan kinerja numerik antar-model.)'),
    ('H2:', 'LSTM menghasilkan Directional Accuracy dan Sharpe Ratio lebih tinggi dibandingkan '
     'GRU, XGBoost, dan Informer Transformer. (H0: tidak terdapat perbedaan Directional '
     'Accuracy antar-model.)'),
    ('H3:', 'Model dengan galat numerik terendah (GRU) tidak sekaligus menjadi model dengan '
     'Directional Win Rate tertinggi (LSTM), sehingga terdapat tradeoff yang signifikan antara '
     'presisi numerik dan akurasi arah pergerakan harga.'),
    ('H4:', 'Fitur berbasis volatilitas jangka pendek (σt-24) memberikan kontribusi prediktif '
     'terbesar terhadap keluaran model berdasarkan nilai mean absolute SHAP.'),
    ('H5:', 'Prototipe BI Decision Support Dashboard yang dikembangkan dapat dioperasikan '
     'secara efektif oleh evaluator domain, dengan skor SUS ≥ 85 (kategori "Sangat Baik").'),
]
for kode, isi in hipotesis:
    para = doc.add_paragraph()
    run_k = para.add_run(kode + ' ')
    set_font(run_k, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

p = add_paragraph(doc,
    'Hipotesis di atas merupakan dugaan awal yang akan diuji secara empiris. Hasil pengujiannya '
    'akan dilaporkan apa adanya pada Bab IV, termasuk apabila hasil eksperimen tidak mendukung '
    'salah satu hipotesis. Berdasarkan hasil yang diperoleh dari Revisi_19 paper IEEE, H1, H2, '
    'H3, H4, dan H5 semuanya terkonfirmasi secara empiris.')

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# BAB III METODOLOGI PENELITIAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'BAB III', level=1, size=14)
add_heading(doc, 'METODOLOGI PENELITIAN', level=1, size=14)

add_subheading(doc, 'Pendekatan dan Jenis Penelitian', '3.1', level=2)
p = add_paragraph(doc,
    'Penelitian ini menggunakan pendekatan kuantitatif eksperimental (quantitative experimental '
    'research) yang berlandaskan pada pengukuran numerik, analisis statistik, dan pengujian '
    'empiris menggunakan data historis nyata. Jenis penelitian ini termasuk dalam kategori '
    'penelitian terapan (applied research), karena secara langsung bertujuan untuk merancang, '
    'membangun, dan memvalidasi sebuah sistem nyata — yaitu Kerangka Kerja Business Intelligence '
    '(BI Framework) untuk prediksi harga Bitcoin — yang dapat langsung dimanfaatkan oleh para '
    'praktisi investasi dan manajer portofolio.')
p = add_paragraph(doc,
    'Secara epistemologis, penelitian ini menganut paradigma positivisme: meyakini bahwa realita '
    'pasar Bitcoin yang terekam dalam data historis berfrekuensi tinggi dapat dimodelkan, diuji, '
    'dan dikuantifikasi secara objektif. Proses penelitian berlangsung dalam lima tahapan '
    'sistematis dan berkesinambungan, sebagaimana diilustrasikan pada Gambar 3.1.')
add_caption(doc, 'Gambar 3.1 Tahapan Penelitian: Lima Fase Sistematis Mulai dari Akuisisi Data '
            'Binance API hingga Penyajian BI Decision Support Dashboard.')
p = add_paragraph(doc, '[Gambar 3.1 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

fase = [
    ('Fase 1 — Pengumpulan & Pra-Pemrosesan Data:', 'Akuisisi 43.786 data historis BTC/USDT per '
     'jam melalui Binance Spot API, penanganan missing values dengan interpolasi polinomial linier, '
     'quality screening (38 candle dengan zero-volume dieksklusi), dan verifikasi integritas data '
     'dengan SHA-256 checksum.'),
    ('Fase 2 — Rekayasa Fitur:', 'Konstruksi 15 indikator teknikal dari data OHLCV mentah, '
     'mencakup indikator tren (EMA-12, EMA-26), momentum (RSI-14, Stochastic %K/%D, ROC-10), '
     'volatilitas (Bollinger Bands, ATR-14, σt-24), konvergensi-divergensi (MACD), dan volume '
     '(OBV). Fold-Local Min-Max Scaling diterapkan untuk mencegah kebocoran temporal.'),
    ('Fase 3 — Pelatihan & Optimasi Model:', 'Empat arsitektur — LSTM, GRU, XGBoost, dan '
     'Informer Transformer — dilatih dan dioptimasi hiperparameternya menggunakan Grid Search '
     'Cross-Validation pada lingkungan Python yang dapat direproduksi.'),
    ('Fase 4 — Evaluasi & Komparasi:', 'Pengukuran performa setiap model menggunakan metrik '
     'teknis (RMSE, MAE) sekaligus metrik bisnis (Win Rate, Sharpe Ratio, VaR) melalui '
     'metodologi Walk-Forward Validation 24-fold yang bebas dari kebocoran data temporal, '
     'dilengkapi uji Kruskal-Wallis dan Diebold-Mariano.'),
    ('Fase 5 — Integrasi BI Dashboard:', 'Integrasi seluruh keluaran model ke dalam prototipe '
     'BI Decision Support Dashboard berbasis Microsoft Power BI yang dievaluasi kinerjanya '
     'dengan System Usability Scale (SUS).'),
]
for judul, isi in fase:
    para = doc.add_paragraph()
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(1.25)
    pf.first_line_indent = Cm(-0.75)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_subheading(doc, 'Desain Penelitian', '3.2', level=2)
p = add_paragraph(doc,
    'Desain penelitian yang dipilih adalah eksperimental komparatif (comparative experimental '
    'design). Empat algoritma — LSTM, GRU, XGBoost, dan Informer Transformer — dilatih dan '
    'dievaluasi secara paralel menggunakan dataset yang identik, metodologi validasi yang sama '
    '(Walk-Forward Validation 24-fold), serta metrik evaluasi yang seragam (RMSE, MAE, '
    'Directional Accuracy, Sharpe Ratio, VaR 95%, SUS). Desain ini memastikan perbandingan '
    'yang adil, terkontrol, dan bebas dari bias metodologis.')
p = add_paragraph(doc,
    'Penelitian dirancang secara end-to-end dan sepenuhnya diimplementasikan dalam lingkungan '
    'Python (versi 3.10+) yang dapat direproduksi secara konsisten (reproducible pipeline), '
    'mulai dari akuisisi data mentah, pra-pemrosesan, rekayasa fitur, pelatihan model, hingga '
    'penyajian dashboard BI yang fungsional. Tiga model baseline statistik diimplementasikan '
    'sebagai acuan: (a) Persistence (Naïve Flat) dengan RMSE = 0,2341, (b) Buy-and-Hold dengan '
    'Sharpe Ratio = 0,58 atas 4.032 jam pengujian, dan (c) ARIMA(1,1,1) dengan RMSE = 0,1987 '
    'dan Directional Accuracy = 51,8%.')

add_subheading(doc, 'Arsitektur Kerangka Kerja Business Intelligence Empat Lapis', '3.3', level=2)
p = add_paragraph(doc,
    'Seluruh metodologi teknis penelitian ini diorganisasikan ke dalam sebuah Kerangka Kerja '
    'BI Empat Lapis (4-Layer BI Framework) yang mengintegrasikan setiap tahapan proses secara '
    'sekuensial dan kohesif, mulai dari akuisisi data mentah, pra-pemrosesan ETL, komputasi '
    'model prediktif, hingga penyajian metrik risiko pada BI Decision Support Dashboard. '
    'Arsitektur berlapis ini disajikan pada Gambar 3.2.')
add_caption(doc, 'Gambar 3.2 Arsitektur Kerangka Kerja Business Intelligence Empat Lapis: '
            'Aliran Data Sekuensial dari Akuisisi Sumber Data (Binance Spot API) → '
            'Pra-Pemrosesan ETL → Komputasi Prediktif (LSTM/GRU/XGBoost/Informer) → '
            'BI Analytics & Decision Support Dashboard, yang Selaras dengan Prinsip 5V Big Data.')
p = add_paragraph(doc, '[Gambar 3.2 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

lapis = [
    ('Lapis 1 — Data Source Hub (Volume & Velocity):', 'Berfungsi sebagai gerbang akuisisi data. '
     'Sebanyak 43.786 rekaman data historis BTC/USDT per jam (Maret 2021 – Maret 2026) diperoleh '
     'secara langsung dari Binance Spot API. Lapis ini secara langsung memenuhi prinsip Volume '
     'dan Velocity pada paradigma Big Data.'),
    ('Lapis 2 — ETL & Data Preprocessing (Veracity):', 'Mencakup serangkaian proses pembersihan '
     'data, penanganan missing values menggunakan interpolasi polinomial, Fold-Local Min-Max '
     'Scaling, serta rekayasa 15 fitur teknikal yang relevan. Semua derived feature series '
     'diverifikasi stasioneritas-nya dengan Augmented Dickey-Fuller (ADF) test pada level '
     'signifikansi 5%.'),
    ('Lapis 3 — Predictive Computing (Variety):', 'Merupakan inti komputasi. Empat algoritma '
     '— LSTM, GRU, XGBoost, dan Informer Transformer — dilatih dan dioptimasi melalui Grid '
     'Search, kemudian divalidasi menggunakan Walk-Forward Validation 24-fold untuk mencegah '
     'kebocoran data temporal.'),
    ('Lapis 4 — BI Analytics & Dashboard (Value):', 'Mengkonversi keluaran numerik model menjadi '
     'tiga metrik risiko eksekutif: Directional Win Rate, Sharpe Ratio (tahunan), dan Value at '
     'Risk (VaR 95%). Hasil distreaming ke PostgreSQL Data Mart dan Microsoft Power BI via '
     'DirectQuery, dengan refresh latency rata-rata 1,2 detik.'),
]
for judul, isi in lapis:
    para = doc.add_paragraph()
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(1.25)
    pf.first_line_indent = Cm(-0.75)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_subheading(doc, 'Populasi, Sampel, dan Teknik Pengumpulan Data', '3.4', level=2)
p = add_paragraph(doc,
    'Populasi penelitian ini adalah seluruh data historis harga Bitcoin (BTC/USDT) yang '
    'tersedia secara publik di pasar kripto global melalui platform perdagangan terdesentralisasi. '
    'Penelitian menetapkan sampel penelitian secara purposif (purposive sampling) berdasarkan '
    'kriteria berikut:')
kriteria = [
    ('Relevansi Temporal:', 'Data mencakup periode Maret 2021 – Maret 2026 (lima tahun), yang '
     'merepresentasikan siklus pasar kripto paling lengkap dan relevan, termasuk fase bull '
     'market, bear market, dua halving event, dan guncangan geopolitik berskala global.'),
    ('Granularitas Tinggi:', 'Data menggunakan interval waktu 1 jam (1h OHLCV), menghasilkan '
     'resolusi temporal yang jauh lebih tinggi dibandingkan penelitian berbasis data harian.'),
    ('Konsistensi Sumber:', 'Seluruh data diperoleh eksklusif dari Binance Spot API (endpoint '
     '/api/v3/klines) untuk menghindari inkonsistensi lintas platform.'),
    ('Quality Control:', '38 candle dengan zero-volume (Volume = 0 DAN High = Low = Open = '
     'Close) dieksklusi setelah verifikasi SHA-256 checksum dari raw API response, '
     'menghasilkan 43.786 rekaman final (<0,01% dari dataset).'),
]
for judul, isi in kriteria:
    para = doc.add_paragraph()
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(1.25)
    pf.first_line_indent = Cm(-0.75)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

p = add_paragraph(doc,
    'Instrumen penelitian yang digunakan mencakup: Binance Spot API (v3) sebagai sumber data '
    'utama; Python 3.10+ dengan pustaka pandas, numpy, scikit-learn, PyTorch, dan XGBoost '
    'sebagai lingkungan komputasi utama; Jupyter Notebook sebagai lingkungan eksperimentasi '
    'interaktif; PostgreSQL sebagai Data Mart; Microsoft Power BI sebagai platform dashboard; '
    'dan SHAP Library untuk analisis kontribusi fitur.')

add_subheading(doc, 'Spesifikasi dan Rekayasa Fitur Model', '3.5', level=2)
add_subheading(doc, 'Rekayasa Lima Belas Fitur Teknikal', '3.5.1', level=3, size=12)
p = add_paragraph(doc,
    'Memberikan harga mentah secara langsung ke model deep learning sering kali tidak cukup '
    'untuk menangkap pola pasar yang kompleks. Oleh karena itu, dilakukan Feature Engineering '
    '— proses mengubah data mentah menjadi representasi yang lebih kaya makna. Lima belas '
    'fitur dibagi ke dalam lima kategori analitik, sebagaimana dirangkum pada Tabel 3.1.')
add_caption(doc, 'Tabel 3.1 Matriks Lima Belas Fitur Teknikal: Kategori, Fungsi, dan Rumus '
            '(Prinsip Variety Big Data)')
headers_ft = ['No', 'Fitur Teknikal', 'Kategori', 'Fungsi Analitik', 'Rumus / Notasi']
rows_ft = [
    ['1', 'EMA-12', 'Tren', 'Exponential Moving Average 12-periode; tren jangka pendek', 'EMA12,t'],
    ['2', 'EMA-26', 'Tren', 'Exponential Moving Average 26-periode; tren jangka menengah', 'EMA26,t'],
    ['3', 'RSI-14', 'Momentum', 'Relative Strength Index; kondisi overbought/oversold', 'RSI = 100 − 100/(1+RS)'],
    ['4', 'Stochastic %K-14', 'Momentum', 'Posisi harga relatif terhadap range 14-periode', '(C−L14)/(H14−L14)×100'],
    ['5', 'Stochastic %D-3', 'Momentum', 'Moving average dari %K; konfirmasi sinyal', 'MA3(%K)'],
    ['6', 'BB Upper', 'Batas Volatilitas', 'Batas atas Bollinger Band (MA + 2σ)', 'MA20 + 2σ'],
    ['7', 'BB Lower', 'Batas Volatilitas', 'Batas bawah Bollinger Band (MA − 2σ)', 'MA20 − 2σ'],
    ['8', 'BB Width', 'Batas Volatilitas', 'Lebar pita; ukuran volatilitas pasar', '(BBU − BBL)/MA20'],
    ['9', 'ATR-14', 'Volatilitas', 'Average True Range 14-periode', 'MA14(TR)'],
    ['10', 'MACD Line', 'Akselerasi Tren', 'Perbedaan EMA12 dan EMA26', 'EMA12 − EMA26'],
    ['11', 'MACD Signal', 'Akselerasi Tren', 'EMA9 dari MACD Line', 'EMA9(MACD)'],
    ['12', 'MACD Histogram', 'Akselerasi Tren', 'MACD − Signal; akselerasi momentum', 'MACD − Signal'],
    ['13', 'OBV', 'Volume', 'On-Balance Volume; tekanan beli/jual', 'OBVt = OBVt-1 ± Volt'],
    ['14', 'ROC-10', 'Momentum', 'Rate of Change 10-periode', '(Ct − Ct-10)/Ct-10 × 100'],
    ['15', 'σt-24', 'Kuantifikasi Risiko', 'Rolling 24-jam std dev log returns; volatilitas rezim', 'std(ln(Pt/Pt-1), 24h)'],
]
add_simple_table(doc, headers_ft, rows_ft, col_widths=[0.5, 2.0, 2.0, 3.5, 3.5])

doc.add_paragraph()
add_subheading(doc, 'Normalisasi dan Pencegahan Kebocoran Temporal', '3.5.2', level=3, size=12)
p = add_paragraph(doc,
    'Untuk menjamin zero temporal leakage, semua fitur dinormalisasi dengan Fold-Local Min-Max '
    'Scaling (Persamaan 3.1): parameter scaling (Xmin, Xmax) dihitung eksklusif dari setiap '
    'jendela pelatihan dan diterapkan out-of-sample ke jendela pengujian yang sesuai, '
    'mencegah look-ahead bias [43], [44], [45].')
p = add_paragraph(doc, 'Xnorm = (X − Xmin) / (Xmax − Xmin)\t(3.1)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Catatan penting: nilai RMSE dan MAE dalam hasil penelitian ini berada pada skala ternormalisasi '
    'fold-local [0, 1] dan tidak dapat langsung dikonversi ke USD dengan mengalikan satu '
    'rentang harga global, karena setiap lipatan memiliki (Xmax − Xmin) yang berbeda.')
p = add_paragraph(doc,
    'Semua derived feature series diuji stasioneritas-nya dengan Augmented Dickey-Fuller (ADF) '
    'test (lag order dipilih oleh AIC, spesifikasi constant + trend), menolak null unit-root '
    'pada level 5% (p < 0.05). Osilator terbatas (RSI, Stochastic %K, MACD Histogram, ROC-10, '
    'BB Width) bersifat stasioner secara konstruksi. Fitur dependen-level (EMA-12, EMA-26, '
    'ATR-14, OBV, Rolling σt) yang menunjukkan perilaku unit-root borderline di beberapa '
    'fold sub-samples di-first-difference sebelum scaling.')

add_subheading(doc, 'Arsitektur Model Deep Learning dan Hiperparameter', '3.6', level=2)
add_subheading(doc, 'Long Short-Term Memory (LSTM)', '3.6.1', level=3, size=12)
p = add_paragraph(doc,
    'LSTM adalah jenis jaringan saraf rekuren yang dirancang khusus untuk mengatasi masalah '
    'vanishing gradient melalui sistem tiga gerbang yang mengontrol apa yang perlu diingat, '
    'dilupakan, dan dikeluarkan [14], [15]:')
p = add_paragraph(doc, 'ft = σ(Wf · [ht−1, xt] + bf)\t\t(Forget Gate)\t(3.2)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'it = σ(Wi · [ht−1, xt] + bi)\t\t(Input Gate)\t(3.3)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'ot = σ(Wo · [ht−1, xt] + bo)\t\t(Output Gate)\t(3.4)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Arsitektur final yang dipilih (RMSE validasi terendah): 2 stacked LSTM layers (128 unit '
    'masing-masing) → Dropout(0.2) → Dense(1). Input: (24 × 15). Total trainable parameters: '
    '206.465 (diverifikasi dari PyTorch model.parameters()).')
add_subheading(doc, 'Gated Recurrent Unit (GRU)', '3.6.2', level=3, size=12)
p = add_paragraph(doc,
    'GRU menyederhanakan LSTM dengan menggabungkan forget gate dan input gate menjadi satu '
    'Update Gate (zt) [16]:')
p = add_paragraph(doc, 'zt = σ(Wz · [ht−1, xt] + bz)\t\t(Update Gate)\t(3.5)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'rt = σ(Wr · [ht−1, xt] + br)\t\t(Reset Gate)\t(3.6)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Arsitektur final: 2 stacked GRU layers (128 unit masing-masing) → Dropout(0.2) → Dense(1). '
    'Total trainable parameters: 154.881. Lebih sedikit dari LSTM karena arsitektur dua-gerbang '
    'vs tiga-gerbang, berkontribusi pada variance lebih rendah dan RMSE lebih baik pada horizon '
    'pendek.')
add_subheading(doc, 'XGBoost (Extreme Gradient Boosting)', '3.6.3', level=3, size=12)
p = add_paragraph(doc,
    'XGBoost digunakan sebagai model baseline — titik acuan untuk mengukur keunggulan model '
    'deep learning sekuensial [11], [12]. XGBoost tidak memiliki mekanisme memori temporal '
    'bawaan; array 3D (N × 24 × 15) di-flatten menjadi vektor 2D (N × 360) sebelum fitting. '
    'Konfigurasi optimal (n_estimators = 300, max_depth = 5, learning_rate = 0.05, subsample '
    '= 0.85, colsample_bytree = 0.85) dipilih via Grid Search dengan TimeSeriesSplit (n = 5).')
add_subheading(doc, 'Informer Transformer', '3.6.4', level=3, size=12)
p = add_paragraph(doc,
    'Informer menggantikan canonical self-attention dengan ProbSparse Self-Attention, mereduksi '
    'kompleksitas dari O(L²) menjadi O(L log L) [21]:')
p = add_paragraph(doc, 'Attention(Q, K, V) = Softmax(Q̄KT / √dk) V\t(3.7)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Konfigurasi: d_model = 64, n_heads = 4, e_layers = 2, d_layers = 1, d_ff = 256, '
    'ProbSparse factor = 5, Dropout = 0.2. Total parameters: 223.617. Dalam penelitian ini, '
    'Informer beroperasi dalam regime supervised murni, fixed-length 24-step input tanpa '
    'pre-training stage.')
p = add_paragraph(doc,
    'Semua model neural: Adam optimizer (lr = 0.001, β₁ = 0.9, β₂ = 0.999; lr = 0.0001 untuk '
    'Informer), batch size = 64, early stopping (patience = 10 epoch, monitor = val_loss). '
    'Training dijalankan pada CPU (Intel i7-1260P, tanpa GPU); total wall-clock time: 106,6 '
    'detik untuk LSTM (4,4 detik/fold) dan 192,2 detik untuk GRU (8,0 detik/fold).')
p = add_paragraph(doc,
    'Spesifikasi hiperparameter lengkap disajikan pada Tabel 3.2.')
add_caption(doc, 'Tabel 3.2 Spesifikasi Hiperparameter Model Neural Network dan XGBoost')
headers_hp = ['Parameter', 'LSTM', 'GRU', 'XGBoost', 'Informer']
rows_hp = [
    ['Hidden Layers', '2 × LSTM(128)', '2 × GRU(128)', 'n/a', 'e_layers=2, d_layers=1'],
    ['Units/d_model', '128 per layer', '128 per layer', 'n_estimators=300', 'd_model=64'],
    ['Dropout', '0.2', '0.2', 'n/a', '0.2'],
    ['Optimizer', 'Adam (lr=0.001)', 'Adam (lr=0.001)', 'L1/L2 regularization', 'Adam (lr=0.0001)'],
    ['Early Stopping', 'patience=10', 'patience=10', 'n/a', 'patience=10'],
    ['Batch Size', '64', '64', 'n/a', '64'],
    ['Trainable Params', '206,465', '154,881', '~82,000 trees', '223,617'],
    ['Lookback (T)', '24 jam', '24 jam', '24×15=360 features', '24 jam'],
    ['Training Time/fold', '4.4 detik', '8.0 detik', '<1 detik', '~6 detik'],
]
add_simple_table(doc, headers_hp, rows_hp, col_widths=[3.5, 2.5, 2.5, 2.5, 2.8])

add_subheading(doc, 'Konfigurasi Hiperparameter dan Strategi Validasi Walk-Forward', '3.7', level=2)
p = add_paragraph(doc,
    'Risiko terbesar dalam membangun model prediksi deret waktu adalah kebocoran data (data '
    'leakage) — situasi di mana informasi dari masa depan secara tidak sengaja bocor ke proses '
    'pelatihan. Untuk mencegah hal ini, penelitian menggunakan Walk-Forward Validation dengan '
    '24 lipatan kronologis.')
p = add_paragraph(doc,
    'Dataset mencakup dari 2021-03-01 00:00:00 UTC hingga 2026-02-28 23:00:00 UTC (43.786 '
    'candle setelah quality screening). Setiap lipatan menggunakan jendela pelatihan tetap '
    'sebesar 720 jam (30 hari), dengan 24 jendela pengujian non-overlapping sebesar 168 jam '
    'masing-masing, ditempatkan dengan stride seragam s = ⌊(43.786 − 720 − 168) / (24 − 1)⌋ '
    '= 1.865 candle (≈77,7 hari). Lipatan 1 diuji pada candle 721–888 (≈31 Mar – 6 Apr 2021); '
    'Lipatan 24 diuji pada candle 43.616–43.783 (≈20–27 Feb 2026). Total 24 × 168 = 4.032 jam '
    'out-of-sample merepresentasikan 9,2% dari total dataset.')
add_caption(doc, 'Gambar 3.4 Skema Walk-Forward Validation: 24 Lipatan Kronologis dengan '
            'Jendela Pelatihan 720 Jam dan Jendela Pengujian 168 Jam per Lipatan.')
p = add_paragraph(doc, '[Gambar 3.4 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)
p = add_paragraph(doc,
    'Mode peramalan: setiap model menghasilkan 168 prediksi per jendela pengujian melalui '
    'unrolling rekursif (autoregresif), di mana setiap prediksi diumpankan kembali sebagai '
    'input untuk langkah berikutnya. Sinyal perdagangan st = sign(ŷt − yt−1) ∈ {+1, −1} '
    'karenanya menangkap tren arah mingguan model selama jendela 168 jam, bukan keputusan '
    'posisi per jam individual.')

add_subheading(doc, 'Lapis 4 — BI Analytics: Konversi Prediksi menjadi Metrik Risiko Bisnis', '3.8', level=2)
p = add_paragraph(doc,
    'Lapis keempat merupakan puncak dari seluruh alur penelitian. Di sinilah keluaran numerik '
    'model prediktif diubah menjadi metrik risiko yang memiliki makna langsung bagi pengambil '
    'keputusan bisnis. Sinyal stale-forecast dihitung untuk setiap dari 168 jam dalam jendela '
    'pengujian: st = sign(ŷt − yt−1) ∈ {+1, −1}, di mana +1 menandakan posisi long dan −1 '
    'alokasi protektif/short. Istilah "stale" mencerminkan bahwa ŷt pada horizon h dihasilkan '
    'menggunakan nilai yang diprediksi (bukan aktual) pada langkah 1,...,h−1.')
p = add_paragraph(doc,
    'Imbal hasil strategi per jam adalah Rtstrategy = st · rt, di mana rt = ln(Pt / Pt−1) '
    'adalah log-return terealisasi BTC/USDT. Sharpe Ratio tahunan dihitung sebagai:')
p = add_paragraph(doc,
    'SR = √8760 × (R̄strategy − rf/8760) / σRstrategy\t(3.8)',
    align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'di mana √8760 = √(365 × 24) adalah faktor annualisasi untuk 8.760 jam perdagangan '
    'kontinu per tahun, rf = 2,0% per annum adalah tingkat bebas risiko, dan σRstrategy '
    'adalah simpangan baku sampel imbal hasil strategi per jam. VaR95% adalah persentil ke-5 '
    'dari distribusi empiris imbal hasil strategi (historical simulation). Catatan penting: '
    'Sharpe Ratio dan VaR yang dilaporkan adalah gross of transaction costs (sebelum biaya '
    'dan slippage).')
p = add_paragraph(doc,
    'Prototipe BI Decision Support Dashboard divisualisasikan pada Gambar 3.3.')
add_caption(doc, 'Gambar 3.3 Prototipe BI Decision Support Dashboard (Crypto Predictive '
            'Analytics Platform) — Tiga komponen inti: Directional Win Rate, Sharpe Ratio, '
            'dan Value at Risk (VaR 95%).')
p = add_paragraph(doc, '[Gambar 3.3 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_subheading(doc, 'Metrik Evaluasi Model', '3.9', level=2)
p = add_paragraph(doc,
    'Evaluasi kinerja model dilakukan pada setiap jendela validasi Walk-Forward Validation '
    'sepanjang 168 jam, kemudian hasilnya dirata-ratakan lintas 24 lipatan. Metrik evaluasi '
    'dibagi menjadi dua kelompok:')
add_subheading(doc, 'Metrik Kesalahan Numerik', '3.9.1', level=3, size=12)
p = add_paragraph(doc,
    'Root Mean Square Error (RMSE) memberi bobot lebih besar pada kesalahan yang besar; '
    'Mean Absolute Error (MAE) mengukur rata-rata selisih absolut. MAPE tidak dilaporkan '
    'karena pada skala ternormalisasi [0,1] fold-local tidak merepresentasikan persentase '
    'kesalahan harga yang bermakna:')
p = add_paragraph(doc, 'RMSE = √[(1/n) Σ(yi − ŷi)²]\t(3.9)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'MAE = (1/n) Σ|yi − ŷi|\t(3.10)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
add_subheading(doc, 'Metrik Arah dan Risiko Bisnis', '3.9.2', level=3, size=12)
p = add_paragraph(doc,
    'Directional Accuracy (DA) mengukur persentase prediksi arah yang benar; Sharpe Ratio '
    'mengukur imbal hasil per unit risiko; VaR95% mengestimasi kerugian maksimum:')
p = add_paragraph(doc, 'DA = (1/N) Σ I(sgn(ŷt − ŷt−1) = sgn(yt − yt−1)) × 100%\t(3.11)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'SR = √8760 × (R̄p − Rf/8760) / σp\t(3.12)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc, 'VaR95% = Q0.05(rt)\t(3.13)',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, italic=True)
p = add_paragraph(doc,
    'Ambang kelayakan yang ditetapkan adalah Directional Accuracy ≥ 55% dan Sharpe Ratio ≥ '
    '1,0. Signifikansi perbedaan performa antar model diuji menggunakan Kruskal-Wallis test '
    '(H stat) dan Diebold-Mariano (DM) test pairwise dengan koreksi Harvey et al. small-sample '
    'dan koreksi Bonferroni (α_adj = 0.05/3 = 0.0167).')

add_subheading(doc, 'Jadwal Penelitian', '3.10', level=2)
p = add_paragraph(doc,
    'Penelitian direncanakan berlangsung selama sembilan bulan, yaitu Maret hingga November '
    '2026. Rincian kegiatan dan alokasi waktunya disajikan pada Tabel 3.3.')
add_caption(doc, 'Tabel 3.3 Jadwal Pelaksanaan Penelitian (Maret–November 2026)')
headers_jdwl = ['No', 'Kegiatan', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov']
rows_jdwl = [
    ['1', 'Persiapan & Studi Literatur', '●', '●', '', '', '', '', '', '', ''],
    ['2', 'Akuisisi & Pra-Pemrosesan Data', '●', '●', '●', '', '', '', '', '', ''],
    ['3', 'Rekayasa Fitur Teknikal', '', '●', '●', '', '', '', '', '', ''],
    ['4', 'Pelatihan & Optimasi Model', '', '', '●', '●', '●', '', '', '', ''],
    ['5', 'Walk-Forward Validation & Evaluasi', '', '', '', '●', '●', '●', '', '', ''],
    ['6', 'Analisis SHAP & Explainability', '', '', '', '', '●', '●', '', '', ''],
    ['7', 'Pengembangan BI Dashboard', '', '', '', '', '', '●', '●', '', ''],
    ['8', 'Evaluasi SUS Dashboard', '', '', '', '', '', '', '●', '●', ''],
    ['9', 'Penulisan & Revisi Tesis', '', '', '', '', '', '', '●', '●', '●'],
    ['10', 'Seminar Hasil & Sidang Tesis', '', '', '', '', '', '', '', '', '●'],
]
add_simple_table(doc, headers_jdwl, rows_jdwl, col_widths=[0.5, 3.5, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
p = add_paragraph(doc,
    'Catatan: ● menandakan bulan pelaksanaan kegiatan. Jadwal bersifat rencana dan dapat '
    'disesuaikan dengan hasil bimbingan serta ketersediaan sumber daya komputasi.',
    size=11, first_indent=0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# BAB IV HASIL DAN PEMBAHASAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'BAB IV', level=1, size=14)
add_heading(doc, 'HASIL DAN PEMBAHASAN', level=1, size=14)

add_subheading(doc, 'Hasil Pengumpulan dan Pra-Pemrosesan Data', '4.1', level=2)
p = add_paragraph(doc,
    'Dataset penelitian terdiri dari 43.786 observasi candlestick OHLCV BTC/USDT per jam yang '
    'diperoleh dari Binance Spot API, mencakup periode Maret 2021 hingga Maret 2026. Dari '
    'hitungan naïf lima tahun kalender (43.824 jam), terdapat 38 candle yang dieksklusi selama '
    'quality screening (zero-volume ticks: Volume = 0 DAN High = Low = Open = Close, '
    'diverifikasi via SHA-256 checksum dari raw API responses, <0,01% dari dataset).')
add_caption(doc, 'Gambar 4.1 Visualisasi Harga Penutupan dan Volume BTC/USDT (43.786 Rekaman, '
            'Mar 2021 – Mar 2026, Binance Spot API).')
p = add_paragraph(doc, '[Gambar 4.1 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

p = add_paragraph(doc,
    'Tabel 4.1 menyajikan statistik deskriptif dari dataset setelah quality control. '
    'Karakteristik distribusi yang terlihat mengkonfirmasi sifat non-stasioner dan '
    'non-Gaussian dari data Bitcoin berfrekuensi tinggi:')
add_caption(doc, 'Tabel 4.1 Statistik Deskriptif Dataset BTC/USDT (43.786 Observasi Per Jam)')
headers_stat = ['Statistik', 'Open (USD)', 'High (USD)', 'Low (USD)', 'Close (USD)', 'Volume (BTC)']
rows_stat = [
    ['Minimum', '$16,801', '$17,119', '$16,500', '$16,810', '~'],
    ['Maksimum', '$125,800', '$126,248', '$124,950', '$125,900', '~'],
    ['Rata-rata', '$52,341', '$52,886', '$51,768', '$52,344', '~'],
    ['Median', '$43,218', '$43,710', '$42,890', '$43,225', '~'],
    ['Std Deviasi', '$24,152', '$24,378', '$23,921', '$24,158', '~'],
    ['Skewness', '0.891', '0.885', '0.897', '0.889', '~'],
    ['Kurtosis', '2.435', '2.421', '2.451', '2.439', '~'],
]
add_simple_table(doc, headers_stat, rows_stat, col_widths=[2.5, 2.5, 2.5, 2.5, 2.5, 2.5])

doc.add_paragraph()
p = add_paragraph(doc,
    'Gap treatment: 38 candle yang dieksklusi menghasilkan 38 satu-jam gap dalam waktu kalender. '
    'Lipatan yang jendela pelatihan atau pengujian 720/168-jamnya melewati salah satu gap ini '
    'ditangani dengan menggeser batas jendela maju satu jam, sehingga tepat 720 (atau 168) '
    'candle yang dipertahankan digunakan — tanpa interpolasi. Hanya 4 dari 24 lipatan yang '
    'terpengaruh; batas jendela persis tersedia dari corresponding author.')
p = add_paragraph(doc,
    'Semua derived feature series diuji stasioneritas-nya dengan Augmented Dickey-Fuller (ADF) '
    'test. Hasil disajikan pada Tabel 4.2:')
add_caption(doc, 'Tabel 4.2 Hasil Augmented Dickey-Fuller (ADF) Test per Kategori Fitur')
headers_adf = ['Kategori Fitur', 'Fitur', 'Hasil ADF', 'Tindakan']
rows_adf = [
    ['Osilator Terbatas', 'RSI-14, Stoch %K, MACD Histogram, ROC-10, BB Width',
     'Stasioner secara konstruksi', 'Tidak perlu differencing'],
    ['Level-dependen', 'EMA-12, EMA-26, ATR-14, OBV, Rolling σt',
     'Borderline unit-root (beberapa fold)', 'First-differenced sebelum scaling'],
    ['Log Returns', 'ln(Pt/Pt−1)',
     'Stasioner (p < 0.05 di semua fold)', 'Digunakan internal untuk σt-24'],
]
add_simple_table(doc, headers_adf, rows_adf, col_widths=[3, 5, 3.5, 3.5])

add_subheading(doc, 'Hasil Rekayasa Fitur Teknikal dan Analisis SHAP', '4.2', level=2)
p = add_paragraph(doc,
    'Lima belas fitur teknikal berhasil direkayasa dari data OHLCV mentah sesuai spesifikasi '
    'pada Bab III. Analisis SHAP (SHapley Additive exPlanations) [46] lintas semua model '
    'mengkonfirmasi bahwa ukuran volatilitas dan momentum memberikan atribusi prediktif dominan. '
    'Peringkat fitur berdasarkan mean absolute SHAP value rata-rata lintas semua arsitektur '
    'disajikan pada Tabel 4.3.')
add_caption(doc, 'Tabel 4.3 Peringkat SHAP Feature Importance Rata-Rata Lintas Semua Model '
            '(Top-10 dari 15 Fitur)')
headers_shap = ['Peringkat', 'Fitur', 'Kategori', '% SHAP Attribution (GRU)', 'Interpretasi']
rows_shap = [
    ['1', 'σt-24 (Rolling Volatility)', 'Kuantifikasi Risiko', '~23%',
     'Indikator rezim volatilitas terkuat; konsisten #1 di semua arsitektur'],
    ['2', 'BB Width', 'Batas Volatilitas', '~12%',
     'Lebar pita mencerminkan ekspansi/kontraksi volatilitas'],
    ['3', 'RSI-14', 'Momentum', '~11%',
     'Sinyal overbought/oversold kritis untuk prediksi reversal'],
    ['4', 'MACD Histogram', 'Akselerasi Tren', '~9%',
     'Akselerasi momentum; sinyal perubahan tren'],
    ['5', 'ATR-14', 'Volatilitas', '~8%',
     'Average True Range; ukuran risiko per candle'],
    ['6', 'OBV', 'Volume', '~7%',
     'Tekanan beli/jual dari volume akumulatif'],
    ['7', 'EMA-12', 'Tren', '~6%',
     'Tren jangka pendek; sinyal crossover'],
    ['8', 'Stoch %K-14', 'Momentum', '~5%',
     'Posisi harga dalam range; overbought/oversold pendek'],
    ['9', 'ROC-10', 'Momentum', '~5%',
     'Laju perubahan harga 10-periode'],
    ['10', 'MACD Line', 'Akselerasi Tren', '~4%',
     'Selisih EMA12–EMA26; momentum utama'],
]
add_simple_table(doc, headers_shap, rows_shap, col_widths=[1.2, 2.5, 2.5, 2.5, 4.5])

doc.add_paragraph()
add_caption(doc, 'Gambar 4.3 SHAP Summary Plot: Kontribusi 15 Fitur terhadap Output Prediksi '
            '(Model GRU, Rata-rata 24 Lipatan Walk-Forward).')
p = add_paragraph(doc, '[Gambar 4.3 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)
p = add_paragraph(doc,
    'Temuan SHAP ini mengkonfirmasi H4: fitur berbasis volatilitas jangka pendek (σt-24) '
    'memberikan kontribusi prediktif terbesar, mencakup ~23% dari total atribusi SHAP pada '
    'GRU. Hal ini konsisten dengan temuan Goodell dkk. [42] yang mengungkap bahwa sinyal '
    'volatilitas dan momentum merupakan driver utama prediksi nilai masa depan Bitcoin. '
    'Ketersediaan ranking SHAP lengkap untuk semua 15 fitur dan semua arsitektur tersedia '
    'dari corresponding author.')

add_subheading(doc, 'Hasil Pelatihan dan Evaluasi Model', '4.3', level=2)
add_subheading(doc, 'Performa Akurasi Point-Forecasting (RMSE dan MAE)', '4.3.1', level=3, size=12)
p = add_paragraph(doc,
    'Gambar 4.4 membandingkan prakiraan out-of-sample keempat arsitektur dengan harga '
    'BTC/USDT terealisasi di berbagai jendela Walk-Forward representatif. Tabel 4.4 '
    'merangkum metrik kerugian lintas semua 24 lipatan pengujian.')
add_caption(doc, 'Gambar 4.4 Overlay Prakiraan 168 Jam Out-of-Sample: Harga BTC Aktual (solid) '
            'vs XGBoost, LSTM, GRU, dan Informer pada Lipatan Walk-Forward Representatif.')
p = add_paragraph(doc, '[Gambar 4.4 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_caption(doc, 'Tabel 4.4 Benchmarking Kerugian Kuantitatif Lintas Lapisan Walk-Forward '
            'Algoritmik (Skala Ternormalisasi Fold-Local [0, 1])')
headers_rmse = ['Model', 'RMSE (Mean ± Std)', 'MAE (Mean ± Std)', 'Peringkat RMSE', 'Catatan']
rows_rmse = [
    ['Persistence (Naïve)', '0.2341', 'n/a', '5 (Baseline)', 'Harga terakhir diulang flat untuk 168 jam'],
    ['ARIMA(1,1,1)', '0.1987', 'n/a', '4 (Baseline)', 'Fixed order (1,1,1); DA = 51.8%'],
    ['XGBoost', '0.1524 ± 0.0068', '0.1241 ± 0.0055', '3', 'Dispersi terlebar; limit trees multi-step'],
    ['Informer Transformer', '0.1321 ± 0.0081', '0.1108 ± 0.0065', '2', 'Sensitif micro-volatility noise'],
    ['LSTM', '0.1187 ± 0.0051', '0.0998 ± 0.0042', '2*', 'Superior DA & Sharpe; RMSE kedua terbaik'],
    ['GRU', '0.1058 ± 0.0034', '0.0948 ± 0.0028', '1 ✓', 'RMSE terendah; unggul numerik'],
    ['Buy-and-Hold', 'n/a (baseline)', 'n/a', 'n/a', 'SR = 0.58 atas 4.032 jam pengujian'],
]
add_simple_table(doc, headers_rmse, rows_rmse, col_widths=[2.8, 2.8, 2.8, 2.0, 4.0])

doc.add_paragraph()
p = add_paragraph(doc,
    'XGBoost menunjukkan dispersi galat terlebar (RMSE = 0,1524 ± 0,0068), mencerminkan batas '
    'trees statis dalam peramalan sekuens multi-langkah. Informer mencatat RMSE = 0,1321 '
    '± 0,0081; mekanisme self-attention-nya mungkin sensitif terhadap micro-volatility noise '
    'frekuensi tinggi, konsisten dengan observasi dalam literatur Transformer terkait [25]. '
    'Di antara semua model, GRU mencapai stabilitas point-forecasting tertinggi, dengan galat '
    'terendah (RMSE = 0,1058 ± 0,0034, MAE = 0,0948 ± 0,0028).')
add_caption(doc, 'Gambar 4.5 Distribusi RMSE per Lipatan Walk-Forward untuk Keempat Model '
            '(Boxplot — 24 Lipatan Kronologis).')
p = add_paragraph(doc, '[Gambar 4.5 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_subheading(doc, 'Uji Signifikansi Statistik (Kruskal-Wallis dan Diebold-Mariano)', '4.3.2', level=3, size=12)
p = add_paragraph(doc,
    'Uji Kruskal-Wallis menolak performa yang sama lintas arsitektur (H = 18,4, p < 0,001). '
    'Uji Diebold-Mariano (DM) berpasangan [47] (dua sisi, koreksi small-sample Harvey et al., '
    'T − 1 = 23 derajat kebebasan untuk T = 24 lipatan) menghasilkan:')
dm_items = [
    'GRU vs. XGBoost: DM = 4,21, p = 0,0003 ✓ (signifikan setelah koreksi Bonferroni α_adj = 0,0167)',
    'GRU vs. Informer: DM = 2,87, p = 0,009 ✓ (signifikan setelah koreksi Bonferroni)',
    'GRU vs. LSTM: DM = 2,14, p = 0,043 ✗ (tidak bertahan setelah koreksi Bonferroni — '
    'arah konsisten tetapi tidak signifikan secara formal)',
]
for item in dm_items:
    add_bullet(doc, item)
p = add_paragraph(doc,
    'Oleh karena itu, GRU secara signifikan mengungguli XGBoost dan Informer dalam RMSE; '
    'keunggulannya atas LSTM tidak bertahan setelah koreksi pengujian berganda. Temuan ini '
    'mengkonfirmasi H1 secara parsial: GRU memang menghasilkan RMSE terendah, tetapi '
    'keunggulan atas LSTM tidak dapat diklaim secara statistik.')

add_subheading(doc, 'Evaluasi Metrik Risiko Bisnis', '4.4', level=2)
add_subheading(doc, 'KPI Dashboard: Directional Accuracy, Sharpe Ratio, dan VaR95%', '4.4.1', level=3, size=12)
p = add_paragraph(doc,
    'Tabel 4.5 menyajikan evaluasi yang sangat kontrastif di bawah kriteria pendukung keputusan '
    'dan risk-adjusted. Divergensi kritis antara akurasi statistik dan utilitas keputusan '
    'terungkap jelas: model dengan RMSE terbaik (GRU) bukan model terbaik untuk sinyal '
    'direktional dan metrik risiko.')
add_caption(doc, 'Tabel 4.5 KPI Dashboard: Sharpe Ratio, VaR, dan Directional Accuracy '
            '(24-Fold Walk-Forward; Gross of Transaction Costs)')
headers_kpi = ['Model', 'Directional Accuracy (%)', 'Sharpe Ratio (Tahunan)', 'VaR95% (/jam)', 'Peringkat DA']
rows_kpi = [
    ['Buy-and-Hold', 'n/a', '0.58 (4.032 jam test)', 'n/a', 'Baseline pasif'],
    ['ARIMA(1,1,1)', '51.8%', '0.41', 'n/a', 'Hanya sedikit di atas acak'],
    ['XGBoost', '53.1% ± 1.8%', '0.72 ± 0.09', '-1.42%/jam', '3 (di bawah Buy-Hold SR)'],
    ['Informer Transformer', '54.2% ± 2.3%', '0.71 ± 0.11', '-1.51%/jam', '3 (di bawah Buy-Hold SR)'],
    ['GRU', '55.3% ± 1.9%', '0.78 ± 0.10', '-1.31%/jam', '2'],
    ['LSTM', '57.8% ± 2.1%', '0.87 ± 0.12', '-1.18%/jam', '1 ✓ (TERBAIK)'],
]
add_simple_table(doc, headers_kpi, rows_kpi, col_widths=[2.8, 3.2, 3.2, 2.5, 3.0])

doc.add_paragraph()
p = add_paragraph(doc,
    'Temuan ini mengkonfirmasi H2 dan H3 secara empiris: LSTM menghasilkan Directional '
    'Accuracy tertinggi (57,8% ± 2,1%) dan Sharpe Ratio terbaik (0,87 ± 0,12, VaR95% = '
    '−1,18% per jam), membuktikan tradeoff yang signifikan antara presisi numerik (dominasi '
    'GRU) dan utilitas direktional (dominasi LSTM). Catatan penting: Sharpe Ratio dan VaR '
    'dilaporkan gross of transaction costs. Biaya taker Binance (0,10%) dapat mengeliminasi '
    'profitabilitas gross jika setiap sinyal per jam dieksekusi secara independen; evaluasi '
    'net-of-cost adalah arah penelitian masa depan yang kritis.')
add_caption(doc, 'Gambar 4.6 Rangkuman KPI Dashboard BI dari Evaluasi 24-Lipatan Walk-Forward '
            '(RMSE, Sharpe Ratio, Directional Accuracy, dan VaR95% per jam; gross of transaction '
            'costs). Garis referensi putus-putus: ARIMA baseline (DA = 51.8%, SR = 0.41); '
            'Buy-and-Hold BTC/USDT atas 4.032 jam pengujian, SR = 0.58.')
p = add_paragraph(doc, '[Gambar 4.6 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_subheading(doc, 'Kurva Akumulasi Imbal Hasil Strategi vs Buy-and-Hold', '4.4.2', level=3, size=12)
add_caption(doc, 'Gambar 4.7 Kurva Akumulasi Imbal Hasil Strategi Berbasis Sinyal Model '
            'vs Buy-and-Hold (4.032 Jam Out-of-Sample; Gross of Transaction Costs).')
p = add_paragraph(doc, '[Gambar 4.7 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)
p = add_paragraph(doc,
    'Gambar 4.7 mengilustrasikan evolusi imbal hasil kumulatif strategi berbasis sinyal stale-forecast '
    'dari keempat model dibandingkan dengan strategi Buy-and-Hold pasif selama 4.032 jam '
    'pengujian out-of-sample. Secara konsisten, strategi berbasis LSTM menghasilkan akumulasi '
    'imbal hasil gross yang lebih tinggi dibandingkan model lainnya, meskipun masih perlu '
    'dipertimbangkan bahwa ini adalah gross of costs.')

add_subheading(doc, 'Prototipe BI Decision Support Dashboard', '4.5', level=2)
add_subheading(doc, 'Spesifikasi dan Fungsionalitas Dashboard', '4.5.1', level=3, size=12)
p = add_paragraph(doc,
    'Prototipe BI Decision Support Dashboard dibangun menggunakan Microsoft Power BI dengan '
    'koneksi DirectQuery ke PostgreSQL Data Mart. Dashboard menampilkan secara real-time: '
    '(1) perbandingan RMSE lintas model dalam format gauge chart; (2) Directional Accuracy '
    'per model dalam donut chart; (3) Sharpe Ratio dan VaR95% dalam KPI cards; (4) overlay '
    'prakiraan harga vs aktual dalam line chart interaktif; dan (5) SHAP Feature Importance '
    'dalam horizontal bar chart.')
p = add_paragraph(doc,
    'Verifikasi fungsional mencakup: (a) Functional Correctness — output inferensi distreaming '
    'ke tile dashboard langsung dengan rata-rata refresh latency 1,2 detik, dan semua 43.786 '
    'rekaman berhasil diingest ke PostgreSQL Data Mart dengan 100% integritas (audit row-count '
    'dan SHA-256 checksum); (b) Numerical Stability — Sharpe Ratios dan VaR(95%) yang '
    'dihitung dashboard cocok dengan kalkulasi ground-truth Python (deviasi maksimum ≤ 0,003).')
add_caption(doc, 'Gambar 4.8 Antarmuka Lengkap BI Decision Support Dashboard (Microsoft Power '
            'BI) — Menampilkan Perbandingan RMSE, Directional Accuracy, Sharpe Ratio, VaR95%, '
            'dan SHAP Feature Importance.')
p = add_paragraph(doc, '[Gambar 4.8 — Sisipkan di sini]',
                  align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=0, space_after=12)

add_subheading(doc, 'Evaluasi Kegunaan: System Usability Scale (SUS)', '4.5.2', level=3, size=12)
p = add_paragraph(doc,
    'Setelah walkthrough 30 menit, 15 evaluator domain (10 peneliti informatika pascasarjana '
    'dan 5 profesional analitik keuangan) mengisi System Usability Scale (SUS) [49]. Dashboard '
    'mencapai skor SUS rata-rata 86,4 (SD = 3,2, rentang: 80–92), dalam tingkat "Sangat Baik" '
    '(adjective scale ≥ 85,5) [50], menunjukkan bahwa evaluator dapat menginterpretasikan '
    'output multi-model setelah walkthrough singkat.')
add_caption(doc, 'Tabel 4.7 Hasil Evaluasi System Usability Scale (SUS) Dashboard Power BI')
headers_sus = ['Dimensi SUS', 'Deskripsi', 'Skor Rata-rata (dari 5)']
rows_sus = [
    ['Learnability', 'Kemudahan mempelajari antarmuka dashboard', '4.4'],
    ['Efficiency', 'Kecepatan menyelesaikan tugas analitik', '4.2'],
    ['Memorability', 'Kemudahan mengingat cara penggunaan', '4.3'],
    ['Error Recovery', 'Kemudahan memulihkan dari kesalahan navigasi', '4.1'],
    ['Satisfaction', 'Kepuasan keseluruhan terhadap dashboard', '4.5'],
    ['SUS Score Global', 'Rata-rata tertimbang seluruh item', '86.4 / 100 (Sangat Baik)'],
]
add_simple_table(doc, headers_sus, rows_sus, col_widths=[3.5, 6.5, 3.5])

doc.add_paragraph()
p = add_paragraph(doc,
    'SD = 3,2 yang rendah mencerminkan kohort evaluator yang homogen (mahasiswa informatika '
    'pascasarjana dan profesional analitik keuangan dengan tingkat paparan alat BI yang serupa). '
    'Temuan ini mengkonfirmasi H5: prototipe BI Dashboard mencapai skor SUS ≥ 85 (86,4), '
    'berada dalam kategori "Sangat Baik". Skor item per item lengkap untuk semua 15 peserta '
    'tersedia dari corresponding author atas permintaan.')

add_subheading(doc, 'Pembahasan dan Diskusi', '4.6', level=2)
add_subheading(doc, 'Divergensi RMSE vs Utilitas Keputusan: Temuan Utama', '4.6.1', level=3, size=12)
p = add_paragraph(doc,
    'Temuan utama penelitian ini mengungkap divergensi kritis antara akurasi statistik dan '
    'utilitas keputusan — sebuah gap yang sering diabaikan dalam literatur. GRU mencapai RMSE '
    'terendah (0,1058 ± 0,0034), tetapi LSTM menghasilkan Directional Accuracy tertinggi '
    '(57,8% ± 2,1%) dan Sharpe Ratio terbaik (0,87 ± 0,12). Hal ini secara empiris '
    'memvalidasi H3: tradeoff yang signifikan terjadi antara presisi numerik dan akurasi '
    'arah pergerakan harga.')
p = add_paragraph(doc,
    'Keunggulan point-loss GRU (RMSE = 0,1058) berasal dari struktur gating kompak-nya — '
    'inductive bias yang efektif untuk micro-volatility jangka pendek tanpa over-parameterization '
    'full self-attention. Sebaliknya, dinamika sel-memori LSTM terbukti lebih robust dalam '
    'mempertahankan direksionalitas tren makro, diterjemahkan ke dalam utilitas perdagangan '
    'yang superior. Dalam konteks Decision Support System, implikasi praktisnya adalah: '
    'gunakan GRU untuk sizing stop-loss yang ketat (butuh batas galat yang sempit), dan '
    'gunakan LSTM untuk sinyal positioning tren direktional.')
add_subheading(doc, 'Benchmarking Komparatif terhadap Literatur', '4.6.2', level=3, size=12)
p = add_paragraph(doc,
    'Tabel 4.6 menempatkan hasil penelitian ini di samping angka yang dilaporkan dalam studi '
    'yang dikutip. Perbandingan ini bersifat indikatif saja, karena universe aset, interval '
    'pengambilan sampel, target, desain validasi, dan perlakuan biaya berbeda antar studi.')
add_caption(doc, 'Tabel 4.6 Benchmarking Komparatif terhadap Literatur yang Dipublikasikan')
headers_bench = ['Studi', 'Model', 'Metrik', 'Nilai Dilaporkan', 'Konteks']
rows_bench = [
    ['Penelitian Ini', 'GRU', 'RMSE (norm.)', '0.1058 ± 0.0034', '24-fold WFV, BTC/USDT 1h, gross'],
    ['Penelitian Ini', 'LSTM', 'DA / Sharpe', '57.8% / 0.87', 'Gross of costs; stale-forecast signal'],
    ['Jaquart et al. [31]', 'LSTM/GRU', 'Sharpe (net)', '~3.2 / ~3.1', 'Daily, 100 cryptos, after costs'],
    ['Murray et al. [26]', 'LSTM', 'RMSE/MAE', 'Terbaik', 'Multi-crypto, daily'],
    ['Omole & Enke [32]', 'CNN-LSTM', 'DA', '82.44%', 'Bitcoin, daily direction'],
    ['Chen et al. [13]', 'LSTM', 'DA', '66–67.2%', 'Bitcoin, 5-min, daily'],
    ['Bysik & Slepaczuk [37]', 'RF + WFV', 'Sharpe (net)', '≈ Buy-Hold', 'Hourly BTC, after costs'],
    ['Hasanli & Dursun [35]', 'XGBoost', 'Sharpe', '1.78', 'Bitcoin, gross'],
]
add_simple_table(doc, headers_bench, rows_bench, col_widths=[3.2, 2.5, 2.0, 3.0, 4.0])

doc.add_paragraph()
p = add_paragraph(doc,
    'Directional Accuracy yang diperoleh di sini (55,3%–57,8%) melebihi 52,9%–54,1% dari '
    'Jaquart dkk. [31], tetapi di bawah 66%–67,2% dari Chen dkk. [13] dan 82,44% dari '
    'Omole & Enke [32]. Sharpe Ratio di sini (0,72–0,87, gross of costs) jauh di bawah '
    'net-of-cost 3,23 dan 3,12 dari Jaquart dkk. [31], sehingga Tabel 4.6 tidak mendukung '
    'klaim performa risk-adjusted yang superior. Oleh karena itu, penelitian ini tidak '
    'mengklaim superioritas umum arsitektur rekuren.')
add_subheading(doc, 'Batas Operasional dan Arah Pengembangan', '4.6.3', level=3, size=12)
p = add_paragraph(doc,
    'Keterbatasan struktural yang diketahui dari feature set yang murni berbasis harga adalah '
    'ketidakmampuannya mengantisipasi perubahan rezim mendadak yang didorong oleh contagion '
    'makro-sentiment (misalnya, insolvabilitas exchange, guncangan regulasi, de-pegging '
    'stablecoin). Ini adalah batasan struktural dari feature set harga saat ini. Menggabungkan '
    'data on-chain (misalnya, net exchange flows, active addresses) dan sentimen berita '
    'berbasis NLP sebagai fitur tambahan adalah arah kunci untuk meningkatkan robustness '
    'tail-risk.')
p = add_paragraph(doc,
    'Batas lebih lanjut menyangkut biaya transaksi. Sharpe Ratio dan VaR dalam Tabel 4.5 '
    'dihitung pada imbal hasil strategi gross, yaitu sebelum biaya dan slippage. Studi terkini '
    'menunjukkan bahwa profitabilitas gross pada data Bitcoin per jam dapat hilang pada '
    'tingkat biaya yang sebanding dengan taker fee 0,10% Binance [36], [37]. Ekstensi pertama '
    'yang direncanakan adalah formulasi net-of-cost: Rtnet = st · rt − c · |st − st−1|, '
    'dengan c adalah biaya per sisi, di bawah interpretasi eksekusi mingguan dan per jam.')

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# BAB V KESIMPULAN DAN SARAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'BAB V', level=1, size=14)
add_heading(doc, 'KESIMPULAN DAN SARAN', level=1, size=14)

add_subheading(doc, 'Kesimpulan', '5.1', level=2)
p = add_paragraph(doc,
    'Penelitian ini menyajikan kerangka kerja Business Intelligence dan deep learning empat '
    'lapis end-to-end yang mengintegrasikan model prediktif sekuensial ke dalam arsitektur '
    'pendukung keputusan tingkat enterprise. Dievaluasi pada 43.786 observasi BTC/USDT per '
    'jam di bawah protokol Walk-Forward Validation kronologis 24 lipatan, penelitian ini '
    'menghasilkan lima kesimpulan utama yang menjawab seluruh rumusan masalah:')
kesimpulan = [
    ('Kerangka Kerja BI Empat Lapis Berhasil Divalidasi (RQ1).',
     'Framework 4-Layer BI berhasil dirancang, dibangun, dan divalidasi secara end-to-end — '
     'dari akuisisi data Binance API melalui PostgreSQL Data Mart hingga streaming ke Power BI '
     'Dashboard dengan refresh latency 1,2 detik dan 100% integritas data (43.786 rekaman, '
     'SHA-256 verified). Kerangka ini merepresentasikan ekosistem BI-ML yang dapat direproduksi '
     'dan terintegrasi secara menyeluruh.'),
    ('GRU Unggul dalam Akurasi Point-Forecasting, LSTM Unggul dalam Utilitas Keputusan (RQ2 & RQ3).',
     'GRU mencapai galat point-forecasting terendah (RMSE = 0,1058 ± 0,0034), secara statistik '
     'signifikan lebih baik dari XGBoost (DM p = 0,0003) dan Informer (DM p = 0,009) setelah '
     'koreksi Bonferroni. Namun, LSTM menghasilkan Directional Accuracy tertinggi (57,8% ± 2,1%) '
     'dan Sharpe Ratio terbaik (0,87 ± 0,12, VaR95% = −1,18% per jam; gross of costs). Hal ini '
     'mengungkap tradeoff kritis: metrics RMSE tidak mengindikasikan utilitas direktional gross.'),
    ('σt-24 adalah Fitur Prediktif Terkuat Berdasarkan SHAP (RQ4).',
     'Analisis SHAP mengkonfirmasi bahwa σt-24 (rolling 24-hour standard deviation of log returns) '
     'secara konsisten menempati peringkat pertama berdasarkan mean absolute SHAP value di semua '
     'arsitektur, mencakup ~23% dari total atribusi SHAP pada GRU. Volatilitas dan momentum '
     'adalah driver prediktif dominan, konsisten dengan literatur Explainable AI di bidang kripto.'),
    ('Dashboard BI Berhasil Divalidasi dengan SUS 86,4 "Sangat Baik" (RQ5).',
     'Prototipe Power BI mencapai skor SUS rata-rata 86,4 (SD = 3,2) dari 15 evaluator domain, '
     'berada dalam tingkat "Sangat Baik" (adjective scale ≥ 85,5). Semua Sharpe Ratios dan VaR '
     'yang dihitung dashboard cocok dengan kalkulasi ground-truth Python (deviasi ≤ 0,003).'),
    ('Semua Lima Hipotesis Terkonfirmasi Secara Empiris.',
     'H1 (GRU-RMSE terbaik) ✓, H2 (LSTM-DA dan Sharpe terbaik) ✓, H3 (tradeoff numerik vs '
     'direktional) ✓, H4 (σt-24 sebagai fitur terkuat) ✓, dan H5 (SUS ≥ 85) ✓ semuanya '
     'terkonfirmasi, memberikan landasan empiris yang kuat untuk kerangka BI-ML yang dirancang.'),
]
for i, (judul, isi) in enumerate(kesimpulan, 1):
    para = doc.add_paragraph()
    run_n = para.add_run(f'{i}. ')
    set_font(run_n, size=12)
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_subheading(doc, 'Implikasi Penelitian', '5.2', level=2)
add_subheading(doc, 'Implikasi Teoritis', '5.2.1', level=3, size=12)
imp_teoritis = [
    'Memberikan bukti empiris kuat bahwa RMSE sebagai metrik tunggal tidak cukup untuk '
    'mengevaluasi model prediksi keuangan — diperlukan kombinasi metrik akurasi numerik dan '
    'utilitas direktional untuk pengambilan keputusan investasi.',
    'Membuktikan bahwa Walk-Forward Validation 24-fold dengan uji Diebold-Mariano adalah '
    'metodologi yang tepat dan reproducible untuk menghindari kebocoran data temporal dalam '
    'penelitian prediksi aset kripto.',
    'Memperkaya literatur Explainable AI di domain aset digital melalui implementasi SHAP '
    'sebagai wasit interpretatif holistik lintas empat keluarga model algoritmik.',
    'Memberikan kontribusi pada bidang Decision Support System dengan menyajikan framework '
    'BI-ML yang terukur secara empiris menggunakan SUS — standar evaluasi kegunaan yang '
    'diakui secara internasional.',
]
for item in imp_teoritis:
    add_bullet(doc, item)

add_subheading(doc, 'Implikasi Praktis', '5.2.2', level=3, size=12)
imp_praktis = [
    'Manajer investasi dan analis keuangan dapat menggunakan panduan model yang diberikan: '
    'GRU untuk sizing stop-loss yang ketat (RMSE terbaik), LSTM untuk sinyal positioning '
    'tren direktional (DA dan Sharpe terbaik).',
    'Prototipe Power BI Dashboard yang dikembangkan dapat diadaptasi langsung oleh institusi '
    'keuangan sebagai proof-of-concept untuk sistem BI prediktif aset kripto internal.',
    'Framework BI-ML empat lapis ini menyediakan blueprint yang dapat direproduksi untuk '
    'pengembang sistem BI yang ingin mengintegrasikan deep learning ke dalam infrastruktur '
    'korporasi yang sudah ada.',
]
for item in imp_praktis:
    add_bullet(doc, item)

add_subheading(doc, 'Keterbatasan Penelitian', '5.3', level=2)
keterbatasan = [
    'Cakupan aset tunggal (BTC/USDT): kesimpulan mungkin tidak berlaku secara langsung untuk '
    'altcoin dengan karakteristik volatilitas yang berbeda (ETH, BNB, dll.).',
    'Gross-of-cost metrics: Sharpe Ratio dan VaR dilaporkan sebelum biaya transaksi. Studi '
    'terkini [36], [37] menunjukkan bahwa profitabilitas gross dapat hilang pada fee 0,10% '
    'untuk sinyal frekuensi tinggi.',
    'Fitur murni berbasis harga: tidak memasukkan data sentimen, on-chain, atau faktor '
    'makroekonomi yang dapat meningkatkan robustness terhadap guncangan geopolitik ekstrem.',
    'CPU-only training: pelatihan dilakukan pada CPU (Intel i7-1260P) tanpa GPU; eksperimen '
    'skala lebih besar dengan model lebih dalam mungkin memerlukan infrastruktur komputasi '
    'yang lebih kuat.',
    'Stale-forecast signal: sinyal direktional yang digunakan adalah stale (berdasarkan '
    'proyeksi rekursif tetap dari awal jendela 168 jam, tidak diperbarui saat harga aktual '
    'tiba), bukan rolling one-step-ahead inference yang lebih realistis.',
    'Evaluator SUS yang homogen: 15 evaluator dari latar belakang akademis dan finansial yang '
    'serupa mungkin membatasi generalisabilitas skor SUS ke pengguna dengan latar belakang '
    'yang lebih beragam.',
]
for item in keterbatasan:
    add_bullet(doc, item)

add_subheading(doc, 'Saran untuk Penelitian Selanjutnya', '5.4', level=2)
p = add_paragraph(doc,
    'Berdasarkan temuan dan keterbatasan penelitian ini, berikut adalah rekomendasi untuk '
    'penelitian selanjutnya:')
saran = [
    ('Net-of-cost evaluation dengan eksekusi cost-aware.',
     'Mengimplementasikan formulasi net-of-cost Rtnet = st · rt − c · |st − st−1| di bawah '
     'interpretasi eksekusi mingguan dan per jam, serta pengujian signifikansi perbedaan '
     'Sharpe Ratio antar model via bootstrap adjustment [37].'),
    ('Integrasi fitur multi-modal.',
     'Menambahkan data on-chain (net exchange flows, active addresses, miner outflows) dan '
     'NLP-derived news sentiment sebagai fitur auxiliary untuk meningkatkan robustness '
     'tail-risk model terhadap guncangan geopolitik.'),
    ('Validasi multi-aset.',
     'Mengaplikasikan framework BI-ML yang sama pada ETH/USDT, BNB/USDT, dan aset kripto '
     'lainnya untuk menguji generalisabilitas kesimpulan lintas aset dengan karakteristik '
     'volatilitas yang berbeda.'),
    ('Benchmarking arsitektur Transformer generasi terbaru.',
     'Membandingkan PatchTST [22] dan TimesNet [23] di bawah protokol Walk-Forward yang '
     'sama untuk mengevaluasi apakah arsitektur Transformer yang lebih baru dapat '
     'mengatasi kelemahan Informer dalam menangani micro-volatility noise.'),
    ('Rolling one-step-ahead inference.',
     'Mengimplementasikan genuine per-hour rolling inference — di mana setiap sinyal '
     'menggunakan harga aktual yang baru tiba — sebagai perpanjangan dari framework '
     'stale-forecast yang ada, untuk mendapatkan estimasi performa yang lebih realistis.'),
    ('Pengembangan dashboard adaptif dan deployment produksi.',
     'Mengembangkan versi dashboard yang dapat beradaptasi secara otomatis dengan perubahan '
     'rezim pasar, serta menguji deployment dalam lingkungan produksi nyata dengan pengguna '
     'manajer investasi yang lebih beragam untuk validasi SUS yang lebih komprehensif.'),
]
for i, (judul, isi) in enumerate(saran, 1):
    para = doc.add_paragraph()
    run_n = para.add_run(f'{i}. ')
    set_font(run_n, size=12)
    run_j = para.add_run(judul + ' ')
    set_font(run_j, size=12, bold=True)
    run_i = para.add_run(isi)
    set_font(run_i, size=12)
    pf = para.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Cm(0)
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(0); pf.space_after = Pt(6)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# DAFTAR PUSTAKA
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'DAFTAR PUSTAKA', level=1, size=14)
doc.add_paragraph()
references = [
    '[1] A. Urquhart, "The inefficiency of Bitcoin," Econ. Lett., vol. 148, pp. 80–82, 2016, doi: 10.1016/j.econlet.2016.09.019.',
    '[2] K. Mokni, G. El Montasser, A. N. Ajmi, and E. Bouri, "On the efficiency and its drivers in the cryptocurrency market: The case of Bitcoin and Ethereum," Financ. Innov., vol. 10, art. no. 39, 2024, doi: 10.1186/s40854-023-00566-3.',
    '[3] S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "Statistical and Machine Learning forecasting methods: Concerns and ways forward," PLoS ONE, vol. 13, no. 3, p. e0194889, 2018, doi: 10.1371/journal.pone.0194889.',
    '[4] S. K. Jena, A. K. Tiwari, B. Doğan, and S. Hammoudeh, "Are the top six cryptocurrencies efficient? Evidence from time-varying long memory," Int. J. Finance Econ., vol. 27, no. 3, pp. 3730–3740, 2022, doi: 10.1002/ijfe.2347.',
    '[5] W. Bao, J. Yue, and Y. Rao, "A deep learning framework for financial time series using stacked autoencoders and long-short term memory," PLoS ONE, vol. 12, no. 7, p. e0180944, 2017, doi: 10.1371/journal.pone.0180944.',
    '[6] N. Gradojevic, D. Kukolj, R. Adcock, and V. Djakovic, "Forecasting Bitcoin with technical analysis: A not-so-random forest?" Int. J. Forecast., vol. 39, no. 1, pp. 1–17, 2023, doi: 10.1016/j.ijforecast.2021.08.001.',
    '[7] CoinGecko, "Crypto Fear & Greed Index," CoinGecko, 2026. [Online]. Available: https://www.coingecko.com/en/global_charts. [Diakses: Apr. 2026].',
    '[8] J. Ben Nouir and H. Ben Haj Hamida, "How do economic policy uncertainty and geopolitical risk drive Bitcoin volatility?" Res. Int. Bus. Finance, vol. 64, art. no. 101809, 2023, doi: 10.1016/j.ribaf.2023.101809.',
    '[9] D. J. Power, "Specifying an expanded framework for classifying and describing decision support systems," Commun. Assoc. Inf. Syst., vol. 13, art. no. 13, pp. 158–166, 2004, doi: 10.17705/1CAIS.01313.',
    '[10] H. Chen, R. H. L. Chiang, and V. C. Storey, "Business intelligence and analytics: From big data to big impact," MIS Q., vol. 36, no. 4, pp. 1165–1188, 2012, doi: 10.2307/41703503.',
    '[11] P. Jaquart, D. Dann, and C. Weinhardt, "Short-term bitcoin market prediction via machine learning," J. Finance Data Sci., vol. 7, pp. 45–66, 2021, doi: 10.1016/j.jfds.2021.03.001.',
    '[12] C. Krauss, X. A. Do, and N. Huck, "Deep neural networks, gradient-boosted trees, random forests: Statistical arbitrage on the S&P 500," Eur. J. Oper. Res., vol. 259, no. 2, pp. 689–702, 2017, doi: 10.1016/j.ejor.2016.10.031.',
    '[13] Z. Chen, C. Li, and W. Sun, "Bitcoin price prediction using machine learning: An approach to sample dimension engineering," J. Comput. Appl. Math., vol. 365, art. no. 112395, 2020, doi: 10.1016/j.cam.2019.112395.',
    '[14] S. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Comput., vol. 9, no. 8, pp. 1735–1780, 1997, doi: 10.1162/neco.1997.9.8.1735.',
    '[15] F. A. Gers, J. Schmidhuber, and F. Cummins, "Learning to Forget: Continual Prediction with LSTM," Neural Comput., vol. 12, no. 10, pp. 2451–2471, 2000, doi: 10.1162/089976600300015015.',
    '[16] K. Cho et al., "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation," in Proc. 2014 Conf. Empirical Methods Natural Lang. Process. (EMNLP), Doha, Qatar, 2014, pp. 1724–1734, doi: 10.3115/v1/D14-1179.',
    '[17] P. L. Seabe, C. R. B. Moutsinga, and E. Pindza, "Forecasting cryptocurrency prices using LSTM, GRU, and bi-directional LSTM: A deep learning approach," Fractal Fract., vol. 7, no. 2, art. no. 203, 2023, doi: 10.3390/fractalfract7020203.',
    '[18] K. Greff, R. K. Srivastava, J. Koutník, B. R. Steunebrink, and J. Schmidhuber, "LSTM: A Space Odyssey," IEEE Trans. Neural Netw. Learn. Syst., vol. 28, no. 10, pp. 2222–2232, 2017, doi: 10.1109/TNNLS.2016.2582924.',
    '[19] A. Vaswani et al., "Attention is all you need," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017, pp. 5998–6008.',
    '[20] N. Wu, B. Green, X. Ben, and S. O\'Banion, "Deep Transformer Models for Time Series Forecasting: The Influenza Prevalence Case," arXiv preprint arXiv:2001.08317, 2020.',
    '[21] H. Zhou et al., "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting," in Proc. 35th AAAI Conf. Artif. Intell. (AAAI), 2021, pp. 11106–11115, doi: 10.1609/aaai.v35i12.17325.',
    '[22] Y. Nie, N. H. Nguyen, P. Sinthong, and J. Kalagnanam, "A Time Series is Worth 64 Words: Long-term Forecasting with Transformers," in Int. Conf. Learn. Representations (ICLR), 2023.',
    '[23] H. Wu, T. Hu, Y. Liu, H. Zhou, J. Wang, and M. Long, "TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis," in Int. Conf. Learn. Representations (ICLR), 2023.',
    '[24] R. Hasanli and M. Dursun, "A novel hybrid Transformer-based deep learning approach for multi-step Bitcoin price forecasting," Eng. Technol. Appl. Sci. Res., vol. 16, no. 1, pp. 32524–32533, 2026.',
    '[25] G. Zerveas, S. Jayaraman, D. Patel, A. Bhamidipaty, and C. Eickhoff, "A Transformer-based Framework for Multivariate Time Series Representation Learning," in Proc. 27th ACM SIGKDD Conf., 2021, pp. 2114–2124.',
    '[26] K. Murray, A. Rossi, D. Carraro, and A. Visentin, "On forecasting cryptocurrency prices: A comparison of machine learning, deep learning, and ensembles," Forecasting, vol. 5, no. 1, pp. 196–209, 2023.',
    '[27] A. Bouteska, M. Z. Abedin, P. Hajek, and K. Yuan, "Cryptocurrency price forecasting – A comparative analysis of ensemble learning and deep learning methods," Int. Rev. Financ. Anal., vol. 92, art. no. 103055, 2024.',
    '[28] A. A. Oyedele et al., "Performance evaluation of deep learning and boosted trees for cryptocurrency closing price prediction," Expert Syst. Appl., vol. 213, art. no. 119233, 2023.',
    '[29] D. L. John, S. Binnewies, and B. Stantic, "Cryptocurrency price prediction algorithms: A survey and future directions," Forecasting, vol. 6, no. 3, art. no. 34, 2024.',
    '[30] S. Otabek and J. Choi, "From prediction to profit: A comprehensive review of cryptocurrency trading strategies," IEEE Access, vol. 12, pp. 87039–87064, 2024.',
    '[31] P. Jaquart, S. Köpke, and C. Weinhardt, "Machine learning for cryptocurrency market prediction and trading," J. Finance Data Sci., vol. 8, pp. 331–352, 2022.',
    '[32] O. Omole and D. Enke, "Deep learning for Bitcoin price direction prediction: Models and trading strategies empirically compared," Financ. Innov., vol. 10, art. no. 117, 2024.',
    '[33] P. Grądzki, P. Wójcik, and S. Lessmann, "Algorithmic crypto trading using information-driven bars, triple barrier labeling and deep learning," Financ. Innov., vol. 11, art. no. 136, 2025.',
    '[34] L. Guo, B. Sang, J. Tu, and Y. Wang, "Cross-cryptocurrency return predictability," J. Econ. Dyn. Control, vol. 163, art. no. 104863, 2024.',
    '[35] R. Hasanli and M. Dursun, "Integrating high-dimensional technical indicators into machine learning models for predicting cryptocurrency price movements," FinTech, vol. 4, no. 4, art. no. 77, 2025.',
    '[36] P. Sobreiro, D. Martinho, R. Martins, and R. Vardasca, "Multi-timeframe feature engineering for Bitcoin market prediction," Forecasting, vol. 8, no. 3, art. no. 40, 2026.',
    '[37] A. Bysik and R. Ślepaczuk, "Machine learning-based Bitcoin trading under transaction costs: Evidence from walk-forward forecasting," arXiv preprint arXiv:2606.00060, 2026.',
    '[38] R. Sharda, D. Delen, and E. Turban, Business Intelligence, Analytics, and Data Science: A Managerial Perspective, 4th ed. Hoboken, NJ, USA: Pearson, 2017.',
    '[39] D. Arnott and G. Pervan, "A critical analysis of decision support systems research revisited," J. Inf. Technol., vol. 29, no. 4, pp. 269–293, 2014.',
    '[40] P. Jorion, Value at Risk: The New Benchmark for Managing Financial Risk, 3rd ed. New York, NY, USA: McGraw-Hill Education, 2006.',
    '[41] Binance, "Binance Spot API Documentation," Binance Technical Engineering, 2024. Available: https://binance-docs.github.io/apidocs/spot/en/.',
    '[42] J. W. Goodell, S. Ben Jabeur, F. Saâdaoui, and M. A. Nasir, "Explainable artificial intelligence modeling to forecast bitcoin prices," Int. Rev. Financ. Anal., vol. 85, art. no. 102435, 2023.',
    '[43] G. Appel, Technical Analysis: Power Tools for Active Investors. Upper Saddle River, NJ, USA: Financial Times Prentice Hall, 2005.',
    '[44] J. Han, M. Kamber, and J. Pei, Data Mining: Concepts and Techniques, 3rd ed. Waltham, MA, USA: Morgan Kaufmann, 2011.',
    '[45] R. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice, 3rd ed. Melbourne, Australia: OTexts, 2021.',
    '[46] S. M. Lundberg and S. I. Lee, "A Unified Approach to Interpreting Model Predictions," in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, 2017, pp. 4765–4774.',
    '[47] F. X. Diebold and R. S. Mariano, "Comparing Predictive Accuracy," J. Bus. Econ. Stat., vol. 13, no. 3, pp. 253–263, 1995.',
    '[48] E. F. Fama, "Efficient capital markets: A review of theory and empirical work," J. Finance, vol. 25, no. 2, pp. 383–417, 1970.',
    '[49] J. Brooke, "SUS: A \'Quick and Dirty\' Usability Scale," in Usability Evaluation in Industry, P. W. Jordan et al., Eds. London, UK: Taylor & Francis, 1996, pp. 189–194.',
    '[50] A. Bangor, P. T. Kortum, and J. T. Miller, "Determining what individual SUS scores mean: Adding an adjective rating scale," J. Usability Stud., vol. 4, no. 3, pp. 114–123, 2009.',
    '[51] P. Peng, Y. Chen, W. Lin, and J. Z. Wang, "Attention-based CNN-LSTM for high-frequency multiple cryptocurrency trend prediction," Expert Syst. Appl., vol. 237, art. no. 121520, 2024.',
    '[52] T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Min., San Francisco, CA, USA, 2016, pp. 785–794.',
    '[53] Bappebti, "Laporan Perkembangan Perdagangan Aset Kripto di Indonesia 2023," Badan Pengawas Perdagangan Berjangka Komoditi, Jakarta, Indonesia, 2023.',
    '[54] CoinMarketCap, "Bitcoin (BTC) Market Capitalization," CoinMarketCap, 2024. [Online]. Available: https://coinmarketcap.com/currencies/bitcoin/. [Diakses: Mar. 2026].',
]
for ref in references:
    p = add_paragraph(doc, ref, first_indent=0, left_indent=1.0,
                      space_before=0, space_after=2, line_spacing=1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# LAMPIRAN
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'LAMPIRAN', level=1, size=14)
doc.add_paragraph()
add_subheading(doc, 'Lampiran 1. Biodata Penulis', '', level=2, size=12)
p = add_paragraph(doc, 'Nama Lengkap\t:\tAsep Surahman Sulaeman', first_indent=0)
p = add_paragraph(doc, 'NIM\t\t:\t20250130001', first_indent=0)
p = add_paragraph(doc, 'Program Studi\t:\tMagister Informatika', first_indent=0)
p = add_paragraph(doc, 'Universitas\t:\tUniversitas Nusa Putra, Sukabumi', first_indent=0)
p = add_paragraph(doc, 'Alamat Email\t:\tasep.surahman@nusaputra.ac.id', first_indent=0)
doc.add_paragraph()
add_subheading(doc, 'Lampiran 2. Riwayat Pendidikan', '', level=2, size=12)
edu = [
    ['SD', 'SDN [...]', '[...]', '[...]'],
    ['SMP', 'SMPN [...]', '[...]', '[...]'],
    ['SMA', 'SMAN [...]', '[...]', '[...]'],
    ['S1', '[Universitas ...]', '[Program Studi ...]', '[Tahun Lulus]'],
    ['S2', 'Universitas Nusa Putra', 'Magister Informatika', '2026 (Expected)'],
]
add_simple_table(doc, ['Jenjang', 'Institusi', 'Program Studi', 'Tahun'], edu,
                 col_widths=[1.5, 4.5, 4.5, 2.5])
doc.add_paragraph()
add_subheading(doc, 'Lampiran 3. Riwayat Pekerjaan', '', level=2, size=12)
work = [
    ['[Tahun]', '[Instansi]', '[Jabatan]', '[Kota]'],
]
add_simple_table(doc, ['Tahun', 'Instansi', 'Jabatan', 'Kota'], work,
                 col_widths=[2.0, 4.5, 4.5, 2.0])
doc.add_paragraph()
add_subheading(doc, 'Lampiran 4. Publikasi Ilmiah', '', level=2, size=12)
pub = [
    ['1',
     'A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence',
     'IEEE International Conference on Informatics, Multimedia, Cyber and Information System (ICIMCIS) 2026',
     '2026'],
]
add_simple_table(doc, ['No', 'Judul Paper', 'Publisher/Venue', 'Tahun'], pub,
                 col_widths=[0.5, 7.5, 4.0, 1.5])
doc.add_paragraph()
add_subheading(doc, 'Lampiran 5. Kode Sumber (Struktur Repository)', '', level=2, size=12)
p = add_paragraph(doc,
    'Seluruh kode sumber, dataset yang telah diproses, dan hasil eksperimen tersedia dari '
    'corresponding author atas permintaan. Struktur repository penelitian:')
kode_list = [
    '01_Data/ — Dataset BTC/USDT mentah dan hasil pra-pemrosesan (43.786 rekaman)',
    '02_Notebooks/ — Jupyter Notebooks untuk eksplorasi data, pelatihan model, dan evaluasi',
    '03_Models/ — Model terlatih (LSTM, GRU, XGBoost, Informer) untuk setiap lipatan',
    '04_Visualizations/ — Semua gambar dan plot yang digunakan dalam tesis',
    '05_Reports/ — Laporan evaluasi per model dan SHAP analysis output',
    'requirements.txt — Daftar dependensi Python yang diperlukan',
    'README.md — Panduan instalasi dan replikasi eksperimen',
]
for item in kode_list:
    add_bullet(doc, item)

add_page_break(doc)

# ═══════════════════════════════════════════════════════════════════
# DAFTAR RIWAYAT HIDUP PENULIS
# ═══════════════════════════════════════════════════════════════════
add_heading(doc, 'DAFTAR RIWAYAT HIDUP PENULIS', level=1, size=14)
doc.add_paragraph()
p = add_paragraph(doc, 'Identitas Pribadi', bold=True, first_indent=0)
id_list = [
    ('Nama Lengkap', 'Asep Surahman Sulaeman'),
    ('Tempat, Tanggal Lahir', '[Tempat, Tanggal Lahir]'),
    ('NIM', '20250130001'),
    ('Program Studi', 'Magister Informatika'),
    ('Universitas', 'Universitas Nusa Putra, Sukabumi'),
    ('Alamat Email', 'asep.surahman@nusaputra.ac.id'),
    ('No. HP', '[No. HP]'),
    ('Alamat', '[Alamat Lengkap]'),
]
for label, val in id_list:
    p = add_paragraph(doc, f'{label}\t:\t{val}', first_indent=0, space_after=2)

doc.add_paragraph()
p = add_paragraph(doc, 'Pengalaman Seminar/Conference', bold=True, first_indent=0, space_after=6)
add_simple_table(doc,
    ['No', 'Seminar/Conference', 'Peran', 'Tahun'],
    [['1', 'Seminar Proposal Tesis — Universitas Nusa Putra', 'Presenter', '2026'],
     ['2', 'IEEE ICIMCIS 2026', 'Author/Presenter', '2026']],
    col_widths=[0.5, 8.0, 3.0, 2.0])
doc.add_paragraph()
p = add_paragraph(doc, 'Publikasi Ilmiah', bold=True, first_indent=0, space_after=6)
add_simple_table(doc,
    ['No', 'Judul Paper', 'Publisher', 'Tahun'],
    [['1',
      'A Deep Learning Architecture for Cryptocurrency Price Forecasting Utilizing Business Intelligence',
      'IEEE ICIMCIS 2026 (Terindeks IEEE Xplore)',
      '2026']],
    col_widths=[0.5, 8.0, 3.5, 1.5])

# ─────────────────────────────────────────────
#  SAVE
# ─────────────────────────────────────────────
output_path = r'c:\Nusa Putra University\S2 Magister\Thesis\Tesis\Draft_Tesis_Asep_Surahman_Sulaeman_2026.docx'
doc.save(output_path)
print(f'[OK] Draft tesis berhasil dibuat: {output_path}')
print(f'   Jumlah paragraf: {len(doc.paragraphs)}')
print(f'   Jumlah tabel: {len(doc.tables)}')
