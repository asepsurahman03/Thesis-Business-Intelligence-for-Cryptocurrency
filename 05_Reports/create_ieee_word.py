
# -*- coding: utf-8 -*-
"""
Script to generate a complete IEEE-format Word document from Manuscript_IEEE_FINAL_2026.html
"""

import re
import base64
import io
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENTATION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── helper: set paragraph spacing ──────────────────────────────────────────
def set_para_spacing(para, before=0, after=0, line=None):
    pPr = para._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(before))
    spacing.set(qn('w:after'), str(after))
    if line:
        spacing.set(qn('w:line'), str(line))
        spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)

# ── helper: set font for a run ─────────────────────────────────────────────
def set_run_font(run, name='Times New Roman', size=10, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    # force Times New Roman for complex script
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rPr.append(rFonts)

# ── helper: add horizontal rule ────────────────────────────────────────────
def add_horizontal_rule(doc):
    para = doc.add_paragraph()
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)
    set_para_spacing(para, before=60, after=60)
    return para

# ── helper: make a table with IEEE borders ──────────────────────────────────
def add_ieee_table(doc, data, col_widths=None, header=True):
    if not data:
        return
    rows = len(data)
    cols = len(data[0])
    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Table Grid'
    # set column widths
    if col_widths:
        for i, width in enumerate(col_widths):
            for cell in table.columns[i].cells:
                cell.width = Inches(width)
    # fill data
    for r, row in enumerate(data):
        for c, text in enumerate(row):
            cell = table.cell(r, c)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(text))
            is_header = header and r == 0
            set_run_font(run, size=8, bold=is_header)
            set_para_spacing(p, before=20, after=20)
    # IEEE borders: thick top and bottom for header
    for r in range(rows):
        tr = table.rows[r]._tr
        trPr = tr.get_or_add_trPr()
        for c in range(cols):
            tc = table.cell(r, c)._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for side in ['top', 'bottom', 'left', 'right']:
                border = OxmlElement(f'w:{side}')
                if r == 0 and side == 'top':
                    border.set(qn('w:val'), 'double')
                    border.set(qn('w:sz'), '6')
                elif r == rows - 1 and side == 'bottom':
                    border.set(qn('w:val'), 'single')
                    border.set(qn('w:sz'), '6')
                elif r == 0 and side == 'bottom':
                    border.set(qn('w:val'), 'single')
                    border.set(qn('w:sz'), '6')
                elif side in ['left', 'right']:
                    border.set(qn('w:val'), 'none')
                    border.set(qn('w:sz'), '0')
                else:
                    border.set(qn('w:val'), 'none')
                    border.set(qn('w:sz'), '0')
                border.set(qn('w:color'), '000000')
                tcBorders.append(border)
            tcPr.append(tcBorders)
    return table

# ── helper: embed base64 image ──────────────────────────────────────────────
def add_base64_image(doc, b64_str, width_inches=3.0, caption=''):
    try:
        img_data = base64.b64decode(b64_str)
        img_stream = io.BytesIO(img_data)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_stream, width=Inches(width_inches))
        set_para_spacing(p, before=60, after=30)
        if caption:
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cap_p.add_run(caption)
            set_run_font(run, size=8, italic=False)
            set_para_spacing(cap_p, before=0, after=60)
        return True
    except Exception as e:
        print(f"  [WARN] Image embed failed: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# READ HTML
# ─────────────────────────────────────────────────────────────────────────────
html_path = 'Manuscript_IEEE_FINAL_2026.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
print("HTML parsed OK")

# ─────────────────────────────────────────────────────────────────────────────
# EXTRACT CONTENT
# ─────────────────────────────────────────────────────────────────────────────
title_tag  = soup.find(class_='title')
authors_tag = soup.find(class_='authors')
affil_tag   = soup.find(class_='affiliation')
abstract_tag = soup.find(class_='abstract-section')

title_text   = title_tag.get_text(strip=True) if title_tag else "Manuscript"
authors_text = authors_tag.get_text(strip=True) if authors_tag else ""
affil_text   = affil_tag.get_text(" ", strip=True) if affil_tag else ""

# Extract abstract and keywords
abstract_text = ""
keywords_text = ""
if abstract_tag:
    raw = abstract_tag.get_text(" ", strip=True)
    if "Keywords" in raw or "Keywords—" in raw:
        parts = re.split(r'Keywords[—\-]', raw, maxsplit=1)
        abstract_text = parts[0].replace("Abstract—", "").strip()
        keywords_text = parts[1].strip() if len(parts) > 1 else ""
    else:
        abstract_text = raw.replace("Abstract—", "").strip()

print(f"Title: {title_text[:60]}...")
print(f"Authors: {authors_text}")

# ─────────────────────────────────────────────────────────────────────────────
# CREATE DOCUMENT
# ─────────────────────────────────────────────────────────────────────────────
doc = Document()

# Page setup: letter size with narrow margins (IEEE style)
section = doc.sections[0]
section.page_width  = Inches(8.5)
section.page_height = Inches(11)
section.left_margin   = Inches(0.75)
section.right_margin  = Inches(0.75)
section.top_margin    = Inches(0.75)
section.bottom_margin = Inches(1.0)

# ── default paragraph style ─────────────────────────────────────────────────
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(10)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER BLOCK  (full-width: title, authors, affiliation, abstract, keywords)
# ─────────────────────────────────────────────────────────────────────────────

# ── TITLE ────────────────────────────────────────────────────────────────────
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p_title.add_run(title_text)
set_run_font(run, size=18, bold=False)
set_para_spacing(p_title, before=0, after=120)

# ── AUTHORS ──────────────────────────────────────────────────────────────────
p_auth = doc.add_paragraph()
p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p_auth.add_run(authors_text)
set_run_font(run, size=11)
set_para_spacing(p_auth, before=0, after=40)

# ── AFFILIATION ───────────────────────────────────────────────────────────────
affil_lines = [l.strip() for l in affil_text.split('  ') if l.strip()]
for line in affil_lines:
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_aff.add_run(line)
    set_run_font(run, size=10, italic=True)
    set_para_spacing(p_aff, before=0, after=20)

# separator
add_horizontal_rule(doc)

# ── ABSTRACT ──────────────────────────────────────────────────────────────────
p_abs = doc.add_paragraph()
p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
run1 = p_abs.add_run("Abstract—")
set_run_font(run1, size=9, bold=True, italic=True)
run2 = p_abs.add_run(abstract_text)
set_run_font(run2, size=9, italic=True)
pPr = p_abs._p.get_or_add_pPr()
ind = OxmlElement('w:ind')
ind.set(qn('w:left'), '360')
ind.set(qn('w:right'), '360')
pPr.append(ind)
set_para_spacing(p_abs, before=40, after=40)

# ── KEYWORDS ─────────────────────────────────────────────────────────────────
if keywords_text:
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run1 = p_kw.add_run("Keywords—")
    set_run_font(run1, size=9, bold=True, italic=True)
    run2 = p_kw.add_run(keywords_text)
    set_run_font(run2, size=9)
    pPr = p_kw._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:left'), '360')
    ind.set(qn('w:right'), '360')
    pPr.append(ind)
    set_para_spacing(p_kw, before=0, after=80)

add_horizontal_rule(doc)

# ─────────────────────────────────────────────────────────────────────────────
# NOTE: Two-column body via section break
# ─────────────────────────────────────────────────────────────────────────────
# Add continuous section break and enable 2 columns
from docx.oxml.ns import nsmap
new_section_para = doc.add_paragraph()
set_para_spacing(new_section_para, before=0, after=0)
pPr2 = new_section_para._p.get_or_add_pPr()
sectPr = OxmlElement('w:sectPr')
cols = OxmlElement('w:cols')
cols.set(qn('w:num'), '2')
cols.set(qn('w:space'), '360')
cols.set(qn('w:equalWidth'), '1')
sectPr.append(cols)
type_el = OxmlElement('w:type')
type_el.set(qn('w:val'), 'continuous')
sectPr.append(type_el)
pPr2.append(sectPr)

# ─────────────────────────────────────────────────────────────────────────────
# BODY CONTENT — parse pages
# ─────────────────────────────────────────────────────────────────────────────
section_counter = [0]

def get_section_number():
    section_counter[0] += 1
    roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
    idx = section_counter[0] - 1
    return roman[idx] if idx < len(roman) else str(section_counter[0])

def add_section_heading(doc, text):
    num = get_section_number()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"{num}. {text.upper()}")
    set_run_font(run, size=10, bold=True)
    set_para_spacing(p, before=120, after=60)
    return p

def add_subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_run_font(run, size=10, italic=True, bold=True)
    set_para_spacing(p, before=80, after=40)
    return p

def add_body_para(doc, text):
    text = text.strip()
    if not text:
        return None
    # Clean LaTeX-like markup
    text = re.sub(r'\\\(([^)]+)\\\)', r'[\1]', text)
    text = re.sub(r'\$\$[^$]+\$\$', '[Equation]', text)
    text = re.sub(r'\$[^$]+\$', lambda m: m.group(0).replace('$',''), text)
    text = text.replace('\\pm', '±').replace('\\leq','≤').replace('\\geq','≥')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = text.replace('&isin;', '∈').replace('&larr;', '←').replace('&nbsp;', ' ')
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    set_run_font(run, size=10)
    pPr = p._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:firstLine'), '216')
    pPr.append(ind)
    set_para_spacing(p, before=0, after=60)
    return p

# ─── Tables data (extracted from HTML) ────────────────────────────────────
tables_html = soup.find_all('table')
print(f"Found {len(tables_html)} tables in HTML")

def extract_table_data(table_el):
    data = []
    for row in table_el.find_all('tr'):
        cells = row.find_all(['th','td'])
        data.append([c.get_text(strip=True) for c in cells])
    return data

# ─── Figures (base64 images) ───────────────────────────────────────────────
figures_html = soup.find_all('div', class_='figure')
figure_captions = []
figure_b64 = []
for fig in figures_html:
    img = fig.find('img')
    cap = fig.find(class_='figure-caption')
    if img and img.get('src','').startswith('data:image'):
        src = img['src']
        b64 = src.split(',',1)[1] if ',' in src else ''
        figure_b64.append(b64)
        figure_captions.append(cap.get_text(strip=True) if cap else '')
    else:
        figure_b64.append(None)
        figure_captions.append(cap.get_text(strip=True) if cap else '')

print(f"Found {len(figure_b64)} figures")

# ─── Equations (text form) ─────────────────────────────────────────────────
equations_html = soup.find_all('div', class_='equation')
print(f"Found {len(equations_html)} equations")

def add_equation_para(doc, eq_text, eq_num=''):
    eq_text = re.sub(r'\$\$|\$', '', eq_text).strip()
    eq_text = eq_text.replace('\\eqno','').strip()
    eq_text = re.sub(r'\((\d+)\)\s*$', '', eq_text).strip()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    display = eq_text if len(eq_text) < 120 else eq_text[:117]+'...'
    run = p.add_run(f"  {display}  {eq_num}")
    set_run_font(run, size=9, italic=True)
    set_para_spacing(p, before=60, after=60)
    return p

def add_algorithm_box(doc, title, content_lines):
    p_title = doc.add_paragraph()
    run = p_title.add_run(title)
    set_run_font(run, size=9, bold=True)
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pPr = p_title._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'double'); top.set(qn('w:sz'), '6'); top.set(qn('w:color'), '000000')
    pBdr.append(top)
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single'); bot.set(qn('w:sz'), '4'); bot.set(qn('w:color'), '000000')
    pBdr.append(bot)
    pPr.append(pBdr)
    set_para_spacing(p_title, before=60, after=30)
    for line in content_lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'\\[()$]', '', line)
        line = line.replace('&larr;','←').replace('&isin;','∈').replace('&nbsp;',' ')
        line = line.replace('&lt;','<').replace('&gt;','>').replace('&amp;','&')
        p = doc.add_paragraph()
        run = p.add_run(line)
        set_run_font(run, size=8.5, italic=False)
        set_para_spacing(p, before=0, after=0)
    # closing border
    p_end = doc.add_paragraph()
    pPr2 = p_end._p.get_or_add_pPr()
    pBdr2 = OxmlElement('w:pBdr')
    bot2 = OxmlElement('w:bottom')
    bot2.set(qn('w:val'), 'double'); bot2.set(qn('w:sz'), '6'); bot2.set(qn('w:color'), '000000')
    pBdr2.append(bot2)
    pPr2.append(pBdr2)
    set_para_spacing(p_end, before=0, after=60)

# ─────────────────────────────────────────────────────────────────────────────
# ITERATE BODY PAGES
# ─────────────────────────────────────────────────────────────────────────────
pages = soup.find_all('div', class_='page')
fig_idx = 0
eq_idx = 0
tbl_idx = 0
ref_para_idx = 0

for page in pages:
    content_div = page.find('div', class_='page-content')
    if not content_div:
        continue
    for child in content_div.children:
        if not hasattr(child, 'name') or child.name is None:
            continue
        tag = child.name
        cls = child.get('class', [])

        # ── SECTION HEADING (h1) ─────────────────────────────────────────
        if tag == 'h1':
            text = child.get_text(strip=True)
            if text.lower() == 'references':
                # Special handling for references
                add_section_heading(doc, text)
                continue
            add_section_heading(doc, text)

        # ── SUBSECTION HEADING (h2) ──────────────────────────────────────
        elif tag == 'h2':
            add_subsection_heading(doc, child.get_text(strip=True))

        # ── PARAGRAPH ────────────────────────────────────────────────────
        elif tag == 'p':
            txt = child.get_text(" ", strip=True)
            if txt:
                add_body_para(doc, txt)

        # ── EQUATION ─────────────────────────────────────────────────────
        elif tag == 'div' and 'equation' in cls:
            eq_idx += 1
            eq_text = child.get_text(" ", strip=True)
            add_equation_para(doc, eq_text, f"({eq_idx})")

        # ── FIGURE ───────────────────────────────────────────────────────
        elif tag == 'div' and 'figure' in cls:
            img = child.find('img')
            cap = child.find(class_='figure-caption')
            cap_text = cap.get_text(strip=True) if cap else f"Fig. {fig_idx+1}."
            if img and img.get('src','').startswith('data:image'):
                src = img['src']
                b64 = src.split(',',1)[1] if ',' in src else ''
                success = add_base64_image(doc, b64, width_inches=2.8, caption=cap_text)
                if not success:
                    p = doc.add_paragraph()
                    run = p.add_run(f"[Figure {fig_idx+1}: {cap_text}]")
                    set_run_font(run, size=8, italic=True)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p = doc.add_paragraph()
                run = p.add_run(f"[{cap_text}]")
                set_run_font(run, size=8, italic=True)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            fig_idx += 1

        # ── ALGORITHM / PSEUDOCODE ───────────────────────────────────────
        elif tag == 'div' and 'pseudo' in cls:
            title_div = child.find(class_='pseudo-title')
            content_div2 = child.find(class_='pseudo-content')
            title_txt = title_div.get_text(strip=True) if title_div else "Algorithm"
            content_txt = content_div2.get_text("\n", strip=True) if content_div2 else child.get_text("\n", strip=True)
            lines = content_txt.split('\n')
            add_algorithm_box(doc, title_txt, lines)

        # ── TABLE ────────────────────────────────────────────────────────
        elif tag == 'div' and 'table-container' in cls:
            title_el = child.find(class_='table-title')
            tbl_el = child.find('table')
            if title_el:
                p = doc.add_paragraph()
                run = p.add_run(title_el.get_text(strip=True))
                set_run_font(run, size=8, bold=True)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_para_spacing(p, before=80, after=20)
            if tbl_el:
                data = extract_table_data(tbl_el)
                if data:
                    cols_count = max(len(r) for r in data)
                    col_w = 3.0 / cols_count
                    add_ieee_table(doc, data, col_widths=[col_w]*cols_count)
                    set_para_spacing(doc.paragraphs[-1], before=0, after=80)

        # ── REFERENCES section (div.references > p) ───────────────────────
        elif tag == 'div' and 'references' in cls:
            for ref_child in child.children:
                if not hasattr(ref_child, 'name'):
                    continue
                if ref_child.name == 'h1':
                    add_section_heading(doc, ref_child.get_text(strip=True))
                elif ref_child.name == 'p':
                    txt = ref_child.get_text(" ", strip=True)
                    if txt:
                        p = doc.add_paragraph()
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        run = p.add_run(txt)
                        set_run_font(run, size=8)
                        pPr = p._p.get_or_add_pPr()
                        ind = OxmlElement('w:ind')
                        ind.set(qn('w:left'), '360')
                        ind.set(qn('w:hanging'), '360')
                        pPr.append(ind)
                        set_para_spacing(p, before=0, after=30)

        elif tag == 'ul':
            for li in child.find_all('li'):
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(li.get_text(strip=True))
                set_run_font(run, size=10)
                set_para_spacing(p, before=0, after=30)

print(f"\nProcessed {len(pages)} pages")
print(f"  Figures rendered: {fig_idx}")
print(f"  Equations: {eq_idx}")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER with page numbers
# ─────────────────────────────────────────────────────────────────────────────
for sec in doc.sections:
    footer = sec.footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
out_path = 'Manuscript_IEEE_FINAL_2026_WORD.docx'
doc.save(out_path)
print(f"\n✅ Word document saved: {out_path}")
