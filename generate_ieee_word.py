"""
Patch: replace add_pseudocode() in generate_ieee_word.py with an IEEE-formatted version.
Then regenerate the DOCX.
Run this script directly.
"""
import re, os, base64, copy
from io import BytesIO
from bs4 import BeautifulSoup, NavigableString
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HTML_PATH   = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"
OUTPUT_PATH = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_V3.docx"

# ══════════════════════════════════════════════════════════════════════════════
# TEXT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def clean_latex_text(text):
    text = re.sub(r'\\\(\s*\\pm\s*\\\)', '±', text)
    text = re.sub(r'\\\(\s*([^)]+?)\s*\\\)', lambda m: m.group(1).strip(), text)
    text = text.replace(r'\pm', '±')
    text = text.replace('&plusmn;', '±')
    text = text.replace('\x96', '–').replace('\x97', '—')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_algo_text(text):
    """Clean algorithm line text: LaTeX math, HTML entities, arrows."""
    # LaTeX math: \(expr\) → expr, clean underscores
    text = re.sub(r'\\\(([^)]*?)\\\)',
                  lambda m: m.group(1).replace(r'\_', '_').replace('\\', ''),
                  text)
    # HTML entities
    text = (text
            .replace('&larr;', '←')
            .replace('&rarr;', '→')
            .replace('&isin;',  '∈')
            .replace('&amp;',   '&')
            .replace('&nbsp;',  ' ')
            .replace('&lt;',    '<')
            .replace('&gt;',    '>')
            .replace('&sigma;', 'σ')
            )
    # Clean underscores in variable names that look like LaTeX
    text = re.sub(r'\\?_', '_', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ══════════════════════════════════════════════════════════════════════════════
# DOCX HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def set_paragraph_spacing(para, before=0, after=0, line_rule=None, line_val=None):
    pPr = para._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(before * 20)))
    spacing.set(qn('w:after'),  str(int(after  * 20)))
    if line_rule and line_val:
        spacing.set(qn('w:line'),     str(int(line_val * 240)))
        spacing.set(qn('w:lineRule'), line_rule)
    pPr.append(spacing)

def add_run_with_format(para, text, bold=False, italic=False, size_pt=10,
                        font_name='Times New Roman', color=None, mono=False):
    run = para.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.size = Pt(size_pt)
    run.font.name = 'Courier New' if mono else font_name
    if color:
        run.font.color.rgb = RGBColor(*color)
    return run

def para_border(doc, edge, sz=12, before=4, after=4):
    """Add a paragraph with a horizontal border on the given edge."""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=before, after=after)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    e = OxmlElement(f'w:{edge}')
    e.set(qn('w:val'), 'single')
    e.set(qn('w:sz'),    str(sz))
    e.set(qn('w:space'), '1')
    e.set(qn('w:color'), '000000')
    pBdr.append(e); pPr.append(pBdr)
    return p

# ══════════════════════════════════════════════════════════════════════════════
# ALGORITHM RENDERER
# ══════════════════════════════════════════════════════════════════════════════

KEYWORDS = {'for', 'do', 'end for', 'if', 'then', 'else', 'end if',
            'while', 'return', 'begin', 'procedure', 'function'}

def parse_algo_segment(html_fragment):
    """
    Parse mixed bold/italic/plain text from an HTML fragment.
    Returns list of (text, bold, italic) tuples.
    """
    soup = BeautifulSoup(html_fragment, 'html.parser')
    segments = []

    def walk(node, b, i):
        if isinstance(node, NavigableString):
            txt = clean_algo_text(str(node))
            if txt:
                segments.append((txt, b, i))
        elif node.name in ('b', 'strong'):
            for ch in node.children:
                walk(ch, True, i)
        elif node.name in ('i', 'em'):
            for ch in node.children:
                walk(ch, b, True)
        else:
            for ch in node.children:
                walk(ch, b, i)

    for child in soup.children:
        walk(child, False, False)

    return segments

def render_algo_line(doc, line_num_str, segments, indent_level=0, size_pt=8.5):
    """
    Render one algorithm line as a paragraph.
    line_num_str: e.g. "1:" or "Input:" or ""
    segments: list of (text, bold, italic)
    indent_level: number of 4-space indents
    """
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(para, before=0, after=0,
                          line_rule='auto', line_val=1.15)
    pPr = para._p.get_or_add_pPr()
    # Left indent for code block
    ind = OxmlElement('w:ind')
    base_indent  = 360   # 0.25 in inside the box
    code_indent  = base_indent + indent_level * 360  # 0.25 in per level
    num_width    = 400   # width reserved for line number
    ind.set(qn('w:left'), str(code_indent + num_width))
    ind.set(qn('w:hanging'), str(num_width))
    pPr.append(ind)

    # Line number (right-aligned via hanging indent trick)
    if line_num_str:
        nr = para.add_run(line_num_str.ljust(4))
        nr.bold   = False
        nr.italic = False
        nr.font.size = Pt(size_pt)
        nr.font.name = 'Courier New'
        nr.font.color.rgb = RGBColor(80, 80, 80)

    # Code content
    for text, bold, italic in segments:
        # Detect keywords and force bold
        lo = text.strip().lower()
        if lo in KEYWORDS:
            bold = True
        run = para.add_run(text)
        run.bold   = bold
        run.italic = italic
        run.font.size = Pt(size_pt)
        run.font.name = 'Courier New'

    return para

def add_ieee_pseudocode(doc, pseudo_el):
    """
    Render an IEEE-style algorithm box from the <div class="pseudo"> element.
    Layout:
      ══ thick top border ══════════════
      Algorithm 1  Title
      ── thin separator ─────────────────
      Input:   ...
      Output:  ...
      ── thin separator ─────────────────
      1:  // Layer 1: ...
      2:  raw_data ← ...
      ...
      ══ thick bottom border ════════════
    """
    SIZE = 8.5   # font size for all algorithm text

    title_el   = pseudo_el.find(class_='pseudo-title')
    content_el = pseudo_el.find(class_='pseudo-content')

    # ── Top thick border ──────────────────────────────────────────────────────
    para_border(doc, 'top', sz=24, before=10, after=2)

    # ── Algorithm title ───────────────────────────────────────────────────────
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(title_para, before=2, after=2)
    pPr = title_para._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:left'), '200')
    pPr.append(ind)

    if title_el:
        # Bold "Algorithm 1" + normal title text
        for child in title_el.children:
            if isinstance(child, NavigableString):
                txt = clean_algo_text(str(child))
                if txt:
                    add_run_with_format(title_para, txt, bold=False, size_pt=SIZE,
                                        font_name='Times New Roman')
            elif child.name in ('b', 'strong'):
                txt = clean_algo_text(child.get_text())
                add_run_with_format(title_para, txt + '  ', bold=True, size_pt=SIZE,
                                    font_name='Times New Roman')
            elif child.name in ('i', 'em'):
                txt = clean_algo_text(child.get_text())
                add_run_with_format(title_para, txt, italic=True, size_pt=SIZE,
                                    font_name='Times New Roman')

    # ── Thin separator under title ────────────────────────────────────────────
    sep1 = doc.add_paragraph()
    set_paragraph_spacing(sep1, before=2, after=2)
    s1Pr = sep1._p.get_or_add_pPr()
    s1Bdr = OxmlElement('w:pBdr')
    s1B = OxmlElement('w:bottom')
    s1B.set(qn('w:val'), 'single'); s1B.set(qn('w:sz'), '6')
    s1B.set(qn('w:space'), '1');    s1B.set(qn('w:color'), '000000')
    s1Bdr.append(s1B); s1Pr.append(s1Bdr)

    if not content_el:
        para_border(doc, 'bottom', sz=24, before=2, after=10)
        return

    # ── Parse content lines ───────────────────────────────────────────────────
    raw_html = content_el.decode_contents()

    # Split on <br/> or <br> to get individual lines
    lines_html = re.split(r'<br\s*/?>', raw_html)

    input_lines  = []
    code_lines   = []
    in_preamble  = True   # True until we hit the first numbered line

    for line_html in lines_html:
        stripped = BeautifulSoup(line_html, 'html.parser').get_text().strip()
        if not stripped:
            if in_preamble:
                continue
            # blank line in code = separator
            code_lines.append(None)
            continue

        # Determine if this is a numbered code line
        # Pattern: starts with digit(s) followed by ":"
        m = re.match(r'^(\d+)\s*:', stripped)
        if m:
            in_preamble = False

        if in_preamble:
            input_lines.append(line_html)
        else:
            code_lines.append(line_html)

    # ── Render Input/Output preamble ──────────────────────────────────────────
    for line_html in input_lines:
        segments = parse_algo_segment(line_html)
        if not segments:
            continue
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_paragraph_spacing(para, before=1, after=1,
                              line_rule='auto', line_val=1.15)
        pPr = para._p.get_or_add_pPr()
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'),    '360')
        ind.set(qn('w:hanging'), '540')
        pPr.append(ind)

        for text, bold, italic in segments:
            run = para.add_run(text)
            run.bold   = bold
            run.italic = italic
            run.font.size = Pt(SIZE)
            run.font.name = 'Courier New'

    # ── Thin separator after preamble ─────────────────────────────────────────
    sep2 = doc.add_paragraph()
    set_paragraph_spacing(sep2, before=2, after=2)
    s2Pr = sep2._p.get_or_add_pPr()
    s2Bdr = OxmlElement('w:pBdr')
    s2B = OxmlElement('w:bottom')
    s2B.set(qn('w:val'), 'single'); s2B.set(qn('w:sz'), '4')
    s2B.set(qn('w:space'), '1');    s2B.set(qn('w:color'), '000000')
    s2Bdr.append(s2B); s2Pr.append(s2Bdr)

    # ── Render numbered code lines ─────────────────────────────────────────────
    for line_html in code_lines:
        if line_html is None:
            # blank line
            bp = doc.add_paragraph()
            set_paragraph_spacing(bp, before=0, after=0)
            add_run_with_format(bp, ' ', size_pt=4)
            continue

        stripped = BeautifulSoup(line_html, 'html.parser').get_text().strip()
        if not stripped:
            continue

        # Extract line number
        m = re.match(r'^(\d+)\s*:', stripped)
        line_num = m.group(1) + ':' if m else ''

        # Determine indentation from &nbsp; prefix
        nbsp_count = len(re.match(r'^(\s*)', line_html.replace('&nbsp;', ' ')).group(1))
        # More reliable: count leading &nbsp; groups
        nbsp_groups = len(re.findall(r'&nbsp;', line_html.split(':',1)[1][:20]
                                     if ':' in line_html else line_html[:20])) // 4
        # Use visible indent from content after line number
        after_num = re.sub(r'^\d+\s*:\s*', '', stripped)
        indent_level = 0
        if after_num.startswith('    ') or after_num.startswith('\xa0\xa0\xa0\xa0'):
            indent_level = 1

        # Also detect by &nbsp; in the raw html
        if line_num:
            raw_after_num = line_html[line_html.find(':')+1:]
        else:
            raw_after_num = line_html
        nbsp_indent = raw_after_num.count('&nbsp;') // 4
        if nbsp_indent >= 1:
            indent_level = nbsp_indent

        # Parse segments from html (after removing leading line number text)
        # We need to keep the full HTML for formatting
        segments = parse_algo_segment(line_html)

        # Determine if this is a comment line (all italic) or keyword-starting line
        # from plain text
        plain = BeautifulSoup(line_html, 'html.parser').get_text()
        is_comment_only = '//' in plain and not re.match(r'^\s*\d+\s*:', plain.strip())

        render_algo_line(doc, line_num, segments,
                         indent_level=indent_level, size_pt=SIZE)

    # ── Thick bottom border ────────────────────────────────────────────────────
    para_border(doc, 'bottom', sz=24, before=2, after=10)

# ══════════════════════════════════════════════════════════════════════════════
# ALL OTHER HELPERS (copied from generate_ieee_word.py)
# ══════════════════════════════════════════════════════════════════════════════

def html_to_inline(para, element, default_size=10):
    if element is None:
        return
    if isinstance(element, NavigableString):
        t = clean_text(str(element))
        if t:
            add_run_with_format(para, t, size_pt=default_size)
        return
    tag = element.name if element.name else ''
    children = list(element.children)
    if tag in ('b', 'strong'):
        for ch in children:
            if isinstance(ch, NavigableString):
                t = clean_text(str(ch))
                if t: add_run_with_format(para, t, bold=True, size_pt=default_size)
            else: html_to_inline(para, ch, default_size)
    elif tag in ('i', 'em'):
        for ch in children:
            if isinstance(ch, NavigableString):
                t = clean_text(str(ch))
                if t: add_run_with_format(para, t, italic=True, size_pt=default_size)
            else: html_to_inline(para, ch, default_size)
    elif tag == 'sup':
        run = para.add_run(element.get_text())
        run.font.size = Pt(7); run.font.superscript = True
    elif tag == 'br':
        para.add_run('\n')
    else:
        for ch in children: html_to_inline(para, ch, default_size)

def add_body_paragraph(doc, element, default_size=10):
    text = clean_text(element.get_text(separator=' ', strip=True))
    if not text: return
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(para, before=0, after=4, line_rule='auto', line_val=1.0)
    pPr = para._p.get_or_add_pPr()
    ind = OxmlElement('w:ind'); ind.set(qn('w:firstLine'), '216')
    pPr.append(ind)
    html_to_inline(para, element, default_size)

def add_section_heading(doc, text, level=1, section_num=None):
    para = doc.add_paragraph()
    set_paragraph_spacing(para, before=12, after=6)
    if level == 1:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        h = f"{section_num}. {text.upper()}" if section_num else text.upper()
        add_run_with_format(para, h, bold=True, size_pt=10)
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_run_with_format(para, text, italic=True, size_pt=10)

def latex_to_png(latex_str, eq_num=None, dpi=200, fontsize=12):
    tex = re.sub(r'^\$\$\s*', '', latex_str.strip())
    tex = re.sub(r'\s*\$\$$', '', tex)
    eq_num_match = re.search(r'\\eqno\{([^}]+)\}', tex)
    num_str = eq_num_match.group(1) if eq_num_match else (f'({eq_num})' if eq_num else '')
    tex = re.sub(r'\\eqno\{[^}]+\}', '', tex).strip()
    fig = plt.figure(figsize=(5.5, 0.6), facecolor='white')
    try:
        fig.text(0.42, 0.5, f'${tex}$', ha='center', va='center',
                 fontsize=fontsize, fontfamily='serif', math_fontfamily='cm')
    except Exception:
        plain = tex.replace('\\','').replace('{','').replace('}','')
        fig.text(0.42, 0.5, plain, ha='center', va='center',
                 fontsize=fontsize-1, fontfamily='serif')
    if num_str:
        fig.text(0.97, 0.5, num_str, ha='right', va='center',
                 fontsize=fontsize-1, fontfamily='serif')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                pad_inches=0.05, facecolor='white', edgecolor='none')
    plt.close(fig); buf.seek(0)
    return buf

def embed_equation(doc, latex_str, eq_counter):
    try:
        png_buf = latex_to_png(latex_str, eq_num=eq_counter)
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(para, before=6, after=6)
        para.add_run().add_picture(png_buf, width=Inches(3.2))
        print(f"  [EQ {eq_counter}] rendered")
    except Exception as e:
        tex = re.sub(r'\\eqno\{[^}]+\}', f'  ({eq_counter})', latex_str).strip().strip('$')
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(para, before=6, after=6)
        add_run_with_format(para, tex.strip(), italic=True, size_pt=9.5)
        print(f"  [EQ {eq_counter}] fallback: {e}")

def embed_image_from_base64(doc, b64_str):
    try:
        img_stream = BytesIO(base64.b64decode(b64_str))
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(para, before=8, after=4)
        para.add_run().add_picture(img_stream, width=Inches(3.0))
        return True
    except Exception as e:
        print(f"  [WARN] Figure: {e}"); return False

def add_figure_caption(doc, caption_text):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_spacing(para, before=2, after=10)
    add_run_with_format(para, caption_text.strip(), size_pt=8)

def add_reference_paragraph(doc, ref_text):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(para, before=1, after=2)
    pPr = para._p.get_or_add_pPr()
    ind = OxmlElement('w:ind')
    ind.set(qn('w:left'),'360'); ind.set(qn('w:hanging'),'360')
    pPr.append(ind)
    add_run_with_format(para, clean_text(ref_text), size_pt=8)

def add_page_numbers(section):
    footer = section.footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.clear(); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.font.name = 'Times New Roman'; run.font.size = Pt(10)
    for fld_type, instr in [('begin',None),(None,' PAGE '),('end',None)]:
        if fld_type:
            fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), fld_type)
            run._r.append(fc)
        else:
            it = OxmlElement('w:instrText'); it.text = instr; run._r.append(it)

def add_running_header(section, header_text):
    header = section.header
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.clear(); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(header_text)
    run.font.name='Times New Roman'; run.font.size=Pt(9); run.italic=True
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'),'single'); bot.set(qn('w:sz'),'4')
    bot.set(qn('w:space'),'1');   bot.set(qn('w:color'),'000000')
    pBdr.append(bot); pPr.append(pBdr)

def insert_section_break_after(para_el, new_sectPr):
    pPr = para_el.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); para_el.insert(0, pPr)
    for old in pPr.findall(qn('w:sectPr')): pPr.remove(old)
    new_s = copy.deepcopy(new_sectPr)
    type_el = new_s.find(qn('w:type'))
    if type_el is None:
        type_el = OxmlElement('w:type'); new_s.insert(0, type_el)
    type_el.set(qn('w:val'), 'continuous')
    pPr.append(new_s)

def set_two_columns(sectPr, num_cols=2, space_twips=720):
    for old in sectPr.findall(qn('w:cols')): sectPr.remove(old)
    cols = OxmlElement('w:cols')
    cols.set(qn('w:num'), str(num_cols))
    cols.set(qn('w:space'), str(space_twips))
    cols.set(qn('w:sep'), '1')
    sectPr.append(cols)

# ══════════════════════════════════════════════════════════════════════════════
# TABLE HELPERS (same as before)
# ══════════════════════════════════════════════════════════════════════════════

def _set_cell_border_edge(tcBorders, edge, val, sz, color='000000'):
    el = OxmlElement(f'w:{edge}')
    el.set(qn('w:val'), val); el.set(qn('w:sz'), str(sz))
    el.set(qn('w:space'), '0'); el.set(qn('w:color'), color)
    tcBorders.append(el)

def apply_ieee_cell_borders(cell, row_idx, total_rows, is_header_row):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    for old in tcPr.findall(qn('w:tcBorders')): tcPr.remove(old)
    tcBorders = OxmlElement('w:tcBorders')
    _set_cell_border_edge(tcBorders, 'top',    'single' if row_idx==0 else 'none', 24 if row_idx==0 else 0)
    _set_cell_border_edge(tcBorders, 'bottom', 'single' if is_header_row else ('single' if row_idx==total_rows-1 else 'none'), 8 if is_header_row else (24 if row_idx==total_rows-1 else 0))
    for edge in ('left','right','insideH','insideV'):
        _set_cell_border_edge(tcBorders, edge, 'none', 0)
    tcPr.append(tcBorders)

def build_ieee_table(doc, tbl_el, caption_text=None, col_widths_pct=None):
    if caption_text:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(cp, before=10, after=3)
        add_run_with_format(cp, clean_latex_text(caption_text).upper(), bold=True, size_pt=8)
    all_rows = tbl_el.find_all('tr')
    if not all_rows: return
    max_cols = max(len(r.find_all(['th','td'])) for r in all_rows)
    if max_cols == 0: return
    header_row_indices = {0} if all_rows[0].find('th') else set()
    thead = tbl_el.find('thead')
    if thead:
        header_row_indices = {all_rows.index(r) for r in thead.find_all('tr')}
    total_rows = len(all_rows)
    tbl = doc.add_table(rows=total_rows, cols=max_cols)
    tbl.style = 'Normal Table'; tbl.autofit = False
    page_w = Inches(7.0)
    if col_widths_pct and len(col_widths_pct)==max_cols:
        for i, col in enumerate(tbl.columns):
            for cell in col.cells: cell.width = int(page_w * col_widths_pct[i])
    else:
        col_w = int(page_w / max_cols)
        for col in tbl.columns:
            for cell in col.cells: cell.width = col_w
    for r_idx, row_el in enumerate(all_rows):
        cells_el = row_el.find_all(['th','td'])
        is_header = r_idx in header_row_indices
        for c_idx, cell_el in enumerate(cells_el):
            if c_idx >= max_cols: break
            cell = tbl.cell(r_idx, c_idx); cell.text = ''
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT if (c_idx==0 and not is_header) else WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_spacing(para, before=2, after=2)
            txt = clean_latex_text(cell_el.get_text(separator=' ', strip=True))
            add_run_with_format(para, txt, bold=is_header, size_pt=8)
            apply_ieee_cell_borders(cell, r_idx, total_rows, is_header)
    doc.add_paragraph()

TABLE_COL_WIDTHS = {
    'TABLE I':   [0.34, 0.22, 0.22, 0.22],
    'TABLE II':  [0.34, 0.22, 0.22, 0.22],
    'TABLE III': [0.20, 0.20, 0.20, 0.20, 0.20],
    'TABLE IV':  [0.25, 0.12, 0.18, 0.15, 0.15, 0.15],
}
def get_col_widths(caption_text):
    if not caption_text: return None
    u = caption_text.upper()
    for key, w in TABLE_COL_WIDTHS.items():
        if key in u: return w
    return None

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build_document():
    print("Reading HTML ...")
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    doc  = Document()

    section = doc.sections[0]
    section.page_width=Inches(8.5); section.page_height=Inches(11)
    section.top_margin=Inches(0.75); section.bottom_margin=Inches(1.0)
    section.left_margin=Inches(0.75); section.right_margin=Inches(0.75)
    doc.styles['Normal'].font.name = 'Times New Roman'
    doc.styles['Normal'].font.size = Pt(10)

    header_block = soup.find(class_='header-block')
    title_el   = header_block.find(class_='title')       if header_block else None
    authors_el = header_block.find(class_='authors')     if header_block else None
    aff_el     = header_block.find(class_='affiliation') if header_block else None
    abs_el     = header_block.find(class_='abstract-section') if header_block else None

    title_text = clean_text(title_el.get_text()) if title_el else 'Untitled'
    print(f"Title: {title_text[:70]}...")

    tp = doc.add_paragraph()
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(tp, before=0, after=10)
    add_run_with_format(tp, title_text, size_pt=18)

    if authors_el:
        ap = doc.add_paragraph()
        ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_spacing(ap, before=0, after=4)
        add_run_with_format(ap, clean_text(authors_el.get_text()), size_pt=11)

    if aff_el:
        for line in re.split(r'<br\s*/?>', str(aff_el)):
            txt = clean_text(BeautifulSoup(line,'html.parser').get_text())
            if txt:
                lp = doc.add_paragraph()
                lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                set_paragraph_spacing(lp, before=0, after=2)
                add_run_with_format(lp, txt, italic=True, size_pt=10)

    if abs_el:
        doc.add_paragraph()
        abs_p = doc.add_paragraph()
        abs_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_paragraph_spacing(abs_p, before=0, after=6)
        pPr = abs_p._p.get_or_add_pPr()
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'),'360'); ind.set(qn('w:right'),'360')
        pPr.append(ind)
        html_to_inline(abs_p, abs_el, default_size=9.5)

    sep_para = doc.add_paragraph()
    set_paragraph_spacing(sep_para, before=4, after=4)
    sePr = sep_para._p.get_or_add_pPr()
    seBdr = OxmlElement('w:pBdr')
    seBot = OxmlElement('w:bottom')
    seBot.set(qn('w:val'),'single'); seBot.set(qn('w:sz'),'6')
    seBot.set(qn('w:space'),'1'); seBot.set(qn('w:color'),'000000')
    seBdr.append(seBot); sePr.append(seBdr)

    pages = soup.find_all(class_='page')
    section_counter = equation_counter = 0
    references_section = False
    roman_numerals = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
    rendered_tables = set()

    print("Processing pages ...")
    for page in pages:
        pc = page.find(class_='page-content')
        if not pc: continue
        for child in list(pc.children):
            if not hasattr(child,'name') or child.name is None: continue
            tag = child.name

            if tag == 'h1':
                txt = clean_text(child.get_text())
                if not txt: continue
                if txt.lower() == 'references':
                    references_section = True
                    add_section_heading(doc, 'REFERENCES')
                    continue
                references_section = False
                section_counter += 1
                roman = roman_numerals[section_counter-1] if section_counter<=10 else str(section_counter)
                add_section_heading(doc, txt, level=1, section_num=roman)

            elif tag == 'h2':
                txt = clean_text(child.get_text())
                if txt:
                    sp = doc.add_paragraph()
                    sp.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    set_paragraph_spacing(sp, before=10, after=4)
                    add_run_with_format(sp, txt, italic=True, size_pt=10)

            elif tag == 'p':
                if references_section:
                    ref_txt = clean_text(child.get_text())
                    if ref_txt: add_reference_paragraph(doc, ref_txt)
                else:
                    add_body_paragraph(doc, child)

            elif tag == 'table':
                tbl_id = id(child)
                if tbl_id in rendered_tables: continue
                rendered_tables.add(tbl_id)
                caption = None
                for sib in child.previous_siblings:
                    if sib.name is None: continue
                    if sib.name in ('p','div'):
                        sc = sib.get('class',[])
                        if 'table-caption' in sc or 'table-title' in sc:
                            caption = clean_latex_text(sib.get_text(strip=True)); break
                    if sib.name in ('h1','h2','div','table'): break
                if caption is None:
                    hdr_row = child.find('tr')
                    if hdr_row:
                        fc = (hdr_row.find(['th','td']) or hdr_row).get_text(strip=True).lower()
                        if 'model pair' in fc or 'dm stat' in fc:
                            caption = "TABLE II. Pairwise Diebold-Mariano Test Results (Baseline: GRU)"
                print(f"  Standalone table: {caption}")
                build_ieee_table(doc, child, caption, col_widths_pct=get_col_widths(caption))

            elif tag == 'div' and 'figure' in child.get('class',[]):
                img_el = child.find('img')
                cap_el = child.find(class_='figure-caption')
                if img_el:
                    src = img_el.get('src','')
                    if src.startswith('data:image'):
                        b64 = src.split(',',1)[1] if ',' in src else ''
                        if b64: embed_image_from_base64(doc, b64)
                if cap_el: add_figure_caption(doc, clean_text(cap_el.get_text()))

            elif tag == 'div' and 'table-container' in child.get('class',[]):
                caption_el = child.find(class_='table-title')
                if caption_el:
                    caption = clean_latex_text(caption_el.get_text(strip=True))
                else:
                    cap_el2 = child.find(class_='table-caption')
                    caption = clean_latex_text(cap_el2.get_text(separator=' ',strip=True)) if cap_el2 else None
                if caption and 'TABLE IV' in caption.upper():
                    caption = "TABLE IV. Comparative Performance vs. Published Literature"
                tbl_el = child.find('table')
                if tbl_el:
                    tbl_id = id(tbl_el)
                    if tbl_id not in rendered_tables:
                        rendered_tables.add(tbl_id)
                        print(f"  Table: {caption[:70] if caption else 'none'}")
                        build_ieee_table(doc, tbl_el, caption, col_widths_pct=get_col_widths(caption))

            elif tag == 'div' and 'equation' in child.get('class',[]):
                equation_counter += 1
                embed_equation(doc, child.get_text(separator=' ',strip=True), equation_counter)

            elif tag == 'div' and 'pseudo' in child.get('class',[]):
                print("  Rendering Algorithm 1 (IEEE style) ...")
                add_ieee_pseudocode(doc, child)

            elif tag in ('ul','ol'):
                for li in child.find_all('li', recursive=False):
                    lp = doc.add_paragraph(style='List Bullet')
                    set_paragraph_spacing(lp, before=1, after=2)
                    add_run_with_format(lp, clean_text(li.get_text()), size_pt=10)

            elif tag == 'div':
                for pp in child.find_all('p', recursive=False):
                    add_body_paragraph(doc, pp)

    print(f"  Equations rendered: {equation_counter}")

    fp = doc.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(fp, before=12, after=0)
    add_run_with_format(fp, '--- End of Manuscript ---', italic=True, size_pt=8, color=(150,150,150))

    add_running_header(doc.sections[0],
        "A Deep Learning and BI Framework for Cryptocurrency Price Prediction")
    add_page_numbers(doc.sections[0])

    body = doc.element.body
    main_sectPr = body.find(qn('w:sectPr'))
    set_two_columns(main_sectPr, num_cols=2, space_twips=720)

    one_col_sectPr = copy.deepcopy(main_sectPr)
    for old in one_col_sectPr.findall(qn('w:cols')): one_col_sectPr.remove(old)
    c1 = OxmlElement('w:cols'); c1.set(qn('w:num'),'1')
    one_col_sectPr.append(c1)
    insert_section_break_after(sep_para._element, one_col_sectPr)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"\n[OK] Saved: {OUTPUT_PATH}")

if __name__ == '__main__':
    build_document()
