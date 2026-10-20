
# -*- coding: utf-8 -*-
"""
IEEE Word Document Generator - Final Version
Menghasilkan dokumen Word format IEEE lengkap dengan:
- Layout 2 kolom
- Persamaan matematika sebagai gambar (matplotlib)
- Tabel format IEEE
- Gambar embedded
- Referensi format IEEE
"""

import re, base64, io, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mathtext
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─────────────────────────────────────────────────────────────────
# RENDER LATEX EQUATION → PNG → bytes
# ─────────────────────────────────────────────────────────────────
def render_equation(latex_str, eq_number='', fontsize=11):
    """Render LaTeX equation to PNG bytes using matplotlib."""
    # Clean up the LaTeX
    latex = latex_str.strip()
    latex = re.sub(r'\\eqno\{?\([^)]+\)\}?', '', latex).strip()
    latex = re.sub(r'\$\$|\$', '', latex).strip()
    # Build display string with equation number
    if eq_number:
        display = f"${latex}$"
        label   = f"({eq_number})"
    else:
        display = f"${latex}$"
        label   = ''

    fig = plt.figure(figsize=(3.2, 0.55))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.patch.set_alpha(0)

    try:
        ax.text(0.05, 0.5, display, transform=ax.transAxes,
                fontsize=fontsize, ha='left', va='center',
                fontfamily='serif',
                math_fontfamily='cm')
        if label:
            ax.text(0.97, 0.5, label, transform=ax.transAxes,
                    fontsize=fontsize-1, ha='right', va='center',
                    fontfamily='serif')
    except Exception:
        ax.text(0.5, 0.5, f"[Equation {eq_number}]", transform=ax.transAxes,
                fontsize=10, ha='center', va='center')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                transparent=True, pad_inches=0.02)
    plt.close(fig)
    buf.seek(0)
    return buf

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def set_font(run, name='Times New Roman', size=10, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    for attr in ('w:ascii','w:hAnsi','w:cs','w:eastAsia'):
        rFonts.set(qn(attr), name)
    existing = rPr.find(qn('w:rFonts'))
    if existing is not None:
        rPr.remove(existing)
    rPr.insert(0, rFonts)

def set_spacing(para, before=0, after=0, line=None):
    pPr = para._p.get_or_add_pPr()
    old = pPr.find(qn('w:spacing'))
    if old is not None:
        pPr.remove(old)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(int(before)))
    sp.set(qn('w:after'),  str(int(after)))
    if line:
        sp.set(qn('w:line'),     str(int(line)))
        sp.set(qn('w:lineRule'), 'auto')
    pPr.append(sp)

def set_indent(para, left=0, right=0, firstLine=None, hanging=None):
    pPr = para._p.get_or_add_pPr()
    old = pPr.find(qn('w:ind'))
    if old is not None:
        pPr.remove(old)
    ind = OxmlElement('w:ind')
    if left:      ind.set(qn('w:left'),      str(int(left)))
    if right:     ind.set(qn('w:right'),     str(int(right)))
    if firstLine: ind.set(qn('w:firstLine'), str(int(firstLine)))
    if hanging:   ind.set(qn('w:hanging'),   str(int(hanging)))
    pPr.append(ind)

def add_border_para(para, sides=None):
    """Add border lines to paragraph."""
    pPr = para._p.get_or_add_pPr()
    old = pPr.find(qn('w:pBdr'))
    if old is not None:
        pPr.remove(old)
    pBdr = OxmlElement('w:pBdr')
    for side, val, sz in (sides or []):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'),   val)
        el.set(qn('w:sz'),    str(sz))
        el.set(qn('w:space'), '4')
        el.set(qn('w:color'), '000000')
        pBdr.append(el)
    pPr.append(pBdr)

def add_page_number_field(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = ' PAGE '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def clean_text(txt):
    txt = txt.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    txt = txt.replace('&nbsp;', ' ').replace('&isin;', ' ∈ ').replace('&larr;', ' ← ')
    txt = txt.replace('\\pm', '±').replace('\\leq', '≤').replace('\\geq', '≥')
    txt = re.sub(r'\\\(([^)]+)\\\)', r'\1', txt)
    txt = re.sub(r'\$\$[^$]+\$\$', '', txt)
    txt = re.sub(r'\$([^$]+)\$', r'\1', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt.strip()

# ─────────────────────────────────────────────────────────────────
# PARSE HTML
# ─────────────────────────────────────────────────────────────────
html_path = 'Manuscript_IEEE_FINAL_2026.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
print("[1] HTML parsed")

# Extract header info
title_text   = (soup.find(class_='title')   or {}).get_text(strip=True) if soup.find(class_='title') else "Manuscript"
authors_text = (soup.find(class_='authors') or {}).get_text(strip=True) if soup.find(class_='authors') else ""
affil_el     = soup.find(class_='affiliation')
affil_lines  = []
if affil_el:
    for part in affil_el.stripped_strings:
        affil_lines.append(part.strip())

abs_el = soup.find(class_='abstract-section')
abstract_text = ''
keywords_text = ''
if abs_el:
    raw = abs_el.get_text(' ', strip=True)
    if 'Keywords' in raw:
        sp = re.split(r'Keywords[—\-]', raw, 1)
        abstract_text = re.sub(r'^Abstract[—\-]', '', sp[0]).strip()
        keywords_text = sp[1].strip() if len(sp) > 1 else ''
    else:
        abstract_text = re.sub(r'^Abstract[—\-]', '', raw).strip()

print(f"[2] Title: {title_text[:70]}...")
print(f"[3] Authors: {authors_text}")

# ─────────────────────────────────────────────────────────────────
# CREATE DOCUMENT
# ─────────────────────────────────────────────────────────────────
doc = Document()

# Page: Letter, narrow margins (IEEE)
sec0 = doc.sections[0]
sec0.page_width    = Inches(8.5)
sec0.page_height   = Inches(11)
sec0.left_margin   = Inches(0.625)
sec0.right_margin  = Inches(0.625)
sec0.top_margin    = Inches(0.75)
sec0.bottom_margin = Inches(1.0)

# Default style
doc.styles['Normal'].font.name = 'Times New Roman'
doc.styles['Normal'].font.size = Pt(10)

# ─────────────────────────────────────────────────────────────────
# TITLE BLOCK (full width)
# ─────────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(title_text)
set_font(r, size=18)
set_spacing(p, before=0, after=100)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(authors_text)
set_font(r, size=11)
set_spacing(p, before=0, after=40)

for line in affil_lines:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line)
    set_font(r, size=10, italic=True)
    set_spacing(p, before=0, after=20)

# Separator line
p = doc.add_paragraph()
add_border_para(p, [('bottom', 'single', 6)])
set_spacing(p, before=60, after=60)

# Abstract
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r1 = p.add_run("Abstract—")
set_font(r1, size=9, bold=True, italic=True)
r2 = p.add_run(abstract_text)
set_font(r2, size=9, italic=True)
set_indent(p, left=432, right=432)
set_spacing(p, before=40, after=40)

# Keywords
if keywords_text:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p.add_run("Keywords—")
    set_font(r1, size=9, bold=True)
    r2 = p.add_run(keywords_text)
    set_font(r2, size=9)
    set_indent(p, left=432, right=432)
    set_spacing(p, before=0, after=80)

# Separator
p = doc.add_paragraph()
add_border_para(p, [('bottom', 'single', 6)])
set_spacing(p, before=60, after=80)

# ─────────────────────────────────────────────────────────────────
# START 2-COLUMN SECTION via sectPr in paragraph
# ─────────────────────────────────────────────────────────────────
p_break = doc.add_paragraph()
set_spacing(p_break, 0, 0)
pPr = p_break._p.get_or_add_pPr()
sPr = OxmlElement('w:sectPr')
cols_el = OxmlElement('w:cols')
cols_el.set(qn('w:num'),        '2')
cols_el.set(qn('w:space'),      '360')
cols_el.set(qn('w:equalWidth'), '1')
sPr.append(cols_el)
tp = OxmlElement('w:type')
tp.set(qn('w:val'), 'continuous')
sPr.append(tp)
pPr.append(sPr)

# ─────────────────────────────────────────────────────────────────
# SECTION / SUBSECTION COUNTERS
# ─────────────────────────────────────────────────────────────────
sec_count  = [0]
roman_nums = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']

def add_heading1(doc, text):
    sec_count[0] += 1
    num = roman_nums[sec_count[0]-1] if sec_count[0] <= len(roman_nums) else str(sec_count[0])
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{num}. {text.upper()}")
    set_font(r, size=10, bold=True)
    set_spacing(p, before=120, after=60)

def add_heading2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_font(r, size=10, italic=True, bold=False)
    set_spacing(p, before=80, after=40)

def add_body(doc, text):
    text = clean_text(text)
    if not text:
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text)
    set_font(r, size=10)
    set_indent(p, firstLine=216)
    set_spacing(p, before=0, after=60, line=240)

# ─────────────────────────────────────────────────────────────────
# ADD EQUATION IMAGE
# ─────────────────────────────────────────────────────────────────
eq_counter = [0]

def add_equation(doc, raw_latex):
    eq_counter[0] += 1
    num = str(eq_counter[0])
    # Extract the actual LaTeX
    latex = raw_latex.strip()
    latex = re.sub(r'\\eqno\{?\([^)]+\)\}?', '', latex)
    latex = re.sub(r'\$\$|\$', '', latex).strip()
    buf = render_equation(latex, num)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run()
    r.add_picture(buf, width=Inches(2.9))
    set_spacing(p, before=60, after=60)

# ─────────────────────────────────────────────────────────────────
# ADD TABLE (IEEE style)
# ─────────────────────────────────────────────────────────────────
def add_ieee_table(doc, data, caption=''):
    if not data:
        return
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(caption.upper())
        set_font(r, size=8, bold=True)
        set_spacing(p, before=80, after=20)

    nrows = len(data)
    ncols = max(len(row) for row in data)
    tbl = doc.add_table(rows=nrows, cols=ncols)
    tbl.style = 'Table Grid'

    col_w = 3.1 / ncols
    for i, row in enumerate(data):
        for j, cell_text in enumerate(row):
            cell = tbl.cell(i, j)
            cell.width = Inches(col_w)
            cp = cell.paragraphs[0]
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cr = cp.add_run(str(cell_text))
            is_hdr = (i == 0)
            set_font(cr, size=8, bold=is_hdr)
            set_spacing(cp, before=20, after=20)
            # Cell borders
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                b = OxmlElement(f'w:{side}')
                if side in ['left','right']:
                    b.set(qn('w:val'), 'none')
                    b.set(qn('w:sz'),  '0')
                elif i == 0 and side == 'top':
                    b.set(qn('w:val'), 'double')
                    b.set(qn('w:sz'),  '6')
                elif i == 0 and side == 'bottom':
                    b.set(qn('w:val'), 'single')
                    b.set(qn('w:sz'),  '4')
                elif i == nrows-1 and side == 'bottom':
                    b.set(qn('w:val'), 'single')
                    b.set(qn('w:sz'),  '6')
                else:
                    b.set(qn('w:val'), 'none')
                    b.set(qn('w:sz'),  '0')
                b.set(qn('w:color'), '000000')
                tcBorders.append(b)
            old = tcPr.find(qn('w:tcBorders'))
            if old is not None:
                tcPr.remove(old)
            tcPr.append(tcBorders)
    set_spacing(doc.paragraphs[-1], before=0, after=80)

# ─────────────────────────────────────────────────────────────────
# ADD FIGURE
# ─────────────────────────────────────────────────────────────────
fig_counter = [0]

def add_figure(doc, b64_str, caption=''):
    fig_counter[0] += 1
    try:
        img_data = base64.b64decode(b64_str)
        buf = io.BytesIO(img_data)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run()
        r.add_picture(buf, width=Inches(3.0))
        set_spacing(p, before=60, after=20)
    except Exception as e:
        print(f"  [WARN] Fig embed failed: {e}")
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"[Figure {fig_counter[0]}]")
        set_font(r, size=8, italic=True)
        set_spacing(p, before=60, after=20)

    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run(caption)
        set_font(cr, size=8)
        set_spacing(cp, before=0, after=80)

# ─────────────────────────────────────────────────────────────────
# ADD ALGORITHM BOX
# ─────────────────────────────────────────────────────────────────
def add_algorithm(doc, title, lines):
    # Title with top double border
    p = doc.add_paragraph()
    r = p.add_run(title)
    set_font(r, size=8.5, bold=True)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_border_para(p, [('top','double',6),('bottom','single',4)])
    set_spacing(p, before=80, after=20)

    for line in lines:
        line = clean_text(line)
        if not line:
            continue
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(line)
        set_font(r, size=8.5)
        set_spacing(p, before=0, after=0)

    # Bottom border
    p = doc.add_paragraph()
    add_border_para(p, [('bottom','double',6)])
    set_spacing(p, before=0, after=80)

# ─────────────────────────────────────────────────────────────────
# ADD REFERENCE LIST
# ─────────────────────────────────────────────────────────────────
def add_reference(doc, text):
    text = clean_text(text)
    if not text:
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_font(r, size=8)
    set_indent(p, left=360, hanging=360)
    set_spacing(p, before=0, after=30)

# ─────────────────────────────────────────────────────────────────
# PARSE & RENDER BODY
# ─────────────────────────────────────────────────────────────────
pages = soup.find_all('div', class_='page')
print(f"[4] Found {len(pages)} pages to process")

total_figs = 0
total_eqs  = 0
total_tbls = 0

for page_idx, page in enumerate(pages):
    content = page.find('div', class_='page-content')
    if not content:
        continue

    for child in content.children:
        if not hasattr(child, 'name') or child.name is None:
            continue

        tag = child.name
        cls = child.get('class', [])
        cls_str = ' '.join(cls)

        # H1 - Section heading
        if tag == 'h1':
            txt = child.get_text(strip=True)
            add_heading1(doc, txt)

        # H2 - Subsection
        elif tag == 'h2':
            txt = child.get_text(strip=True)
            add_heading2(doc, txt)

        # Paragraph
        elif tag == 'p':
            txt = child.get_text(' ', strip=True)
            add_body(doc, txt)

        # Equation
        elif tag == 'div' and 'equation' in cls_str:
            raw = child.get_text(' ', strip=True)
            add_equation(doc, raw)
            total_eqs += 1

        # Figure
        elif tag == 'div' and 'figure' in cls_str:
            img = child.find('img')
            cap = child.find(class_='figure-caption')
            cap_text = cap.get_text(strip=True) if cap else f"Fig. {fig_counter[0]+1}."
            if img and img.get('src','').startswith('data:image'):
                b64 = img['src'].split(',',1)[1]
                add_figure(doc, b64, cap_text)
                total_figs += 1

        # Algorithm / Pseudocode
        elif tag == 'div' and 'pseudo' in cls_str:
            title_el = child.find(class_='pseudo-title')
            content_el = child.find(class_='pseudo-content')
            title_txt = title_el.get_text(strip=True) if title_el else "Algorithm"
            body_txt = content_el.get_text('\n') if content_el else child.get_text('\n')
            lines = [l.strip() for l in body_txt.split('\n') if l.strip()]
            add_algorithm(doc, title_txt, lines)

        # Table container
        elif tag == 'div' and 'table-container' in cls_str:
            cap_el  = child.find(class_='table-title')
            tbl_el  = child.find('table')
            cap_txt = cap_el.get_text(strip=True) if cap_el else ''
            if tbl_el:
                data = []
                for row in tbl_el.find_all('tr'):
                    cells = row.find_all(['th','td'])
                    data.append([c.get_text(strip=True) for c in cells])
                add_ieee_table(doc, data, cap_txt)
                total_tbls += 1

        # References div
        elif tag == 'div' and 'references' in cls_str:
            for rc in child.children:
                if not hasattr(rc, 'name'):
                    continue
                if rc.name == 'h1':
                    add_heading1(doc, rc.get_text(strip=True))
                elif rc.name == 'p':
                    add_reference(doc, rc.get_text(' ', strip=True))

        # UL list
        elif tag == 'ul':
            for li in child.find_all('li'):
                p = doc.add_paragraph(style='List Bullet')
                r = p.add_run(clean_text(li.get_text(' ', strip=True)))
                set_font(r, size=10)
                set_spacing(p, before=0, after=30)

print(f"[5] Content rendered: {total_figs} figs, {total_eqs} eqs, {total_tbls} tables")

# ─────────────────────────────────────────────────────────────────
# PAGE NUMBERS IN FOOTER
# ─────────────────────────────────────────────────────────────────
for sec in doc.sections:
    footer = sec.footer
    if not footer.paragraphs:
        footer.add_paragraph()
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.clear()
    run = fp.add_run()
    set_font(run, size=10)
    add_page_number_field(run)

# ─────────────────────────────────────────────────────────────────
# RUNNING HEADER
# ─────────────────────────────────────────────────────────────────
for sec in doc.sections:
    header = sec.header
    if not header.paragraphs:
        header.add_paragraph()
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hp.clear()
    r = hp.add_run("IEEE JOURNAL — DEEP LEARNING & BI FRAMEWORK FOR CRYPTOCURRENCY PRICE PREDICTION")
    set_font(r, size=8, italic=True)

# ─────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────
out = 'Manuscript_IEEE_FINAL_2026_CLEAN.docx'
doc.save(out)
print(f"[6] SAVED: {out}")
print(f"    Size: {os.path.getsize(out):,} bytes")
