"""
Post-processor for Manuscript_IEEE_FINAL_2026.docx
Adds: 2-column layout (body), page numbers, running header, column rule.
"""

import copy
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree

DOCX_PATH = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.docx"

# ─── Helper functions ─────────────────────────────────────────────────────────

def get_or_create_sectPr(section):
    return section._sectPr

def set_two_columns(sectPr, num_cols=2, space_twips=720, with_rule=True):
    """Set column count on a sectPr element."""
    # Remove existing cols
    for old in sectPr.findall(qn('w:cols')):
        sectPr.remove(old)
    cols = OxmlElement('w:cols')
    cols.set(qn('w:num'), str(num_cols))
    cols.set(qn('w:space'), str(space_twips))  # 720 twips = 0.5 inch
    if with_rule:
        cols.set(qn('w:sep'), '1')
    sectPr.append(cols)

def add_page_numbers(section, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    """Add centred page numbers to the footer of a section."""
    footer = section.footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.clear()
    para.alignment = alignment

    run = para.add_run()
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)

    instrText = OxmlElement('w:instrText')
    instrText.text = ' PAGE '
    run._r.append(instrText)

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar2)

def add_running_header(section, header_text, left_text='', right_text=''):
    """Add a running header with a bottom border."""
    header = section.header
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.clear()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = para.add_run(header_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9)
    run.italic = True

    # Bottom border
    pPr = para._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)

def remove_two_col_note(doc):
    """Remove the '— Begin Two-Column Layout —' placeholder note."""
    to_remove = []
    for i, para in enumerate(doc.paragraphs):
        if 'Begin Two-Column Layout' in para.text:
            to_remove.append(para._element)
    for el in to_remove:
        el.getparent().remove(el)

def find_separator_paragraph(doc):
    """Find the horizontal rule paragraph that separates header from body."""
    for i, para in enumerate(doc.paragraphs):
        pPr = para._p.find(qn('w:pPr'))
        if pPr is not None:
            pBdr = pPr.find(qn('w:pBdr'))
            if pBdr is not None:
                bot = pBdr.find(qn('w:bottom'))
                if bot is not None:
                    return i, para
    return None, None

def insert_section_break_after(para_el, new_sectPr):
    """
    Insert a continuous section break after the given paragraph element
    so the body following it uses new_sectPr settings (2 columns).
    """
    # The sectPr goes inside the pPr of the paragraph BEFORE the new section starts
    pPr = para_el.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        para_el.insert(0, pPr)

    # Remove any existing sectPr
    for old_s in pPr.findall(qn('w:sectPr')):
        pPr.remove(old_s)

    # Clone new_sectPr and mark as continuous
    new_s = copy.deepcopy(new_sectPr)
    # Set type = continuous
    type_el = new_s.find(qn('w:type'))
    if type_el is None:
        type_el = OxmlElement('w:type')
        new_s.insert(0, type_el)
    type_el.set(qn('w:val'), 'continuous')

    pPr.append(new_s)

# ─── Main ─────────────────────────────────────────────────────────────────────

def polish():
    print("Loading document ...")
    doc = Document(DOCX_PATH)

    # 1. Remove the placeholder note
    remove_two_col_note(doc)

    # 2. Find separator paragraph index (the horizontal rule after abstract)
    sep_idx, sep_para = find_separator_paragraph(doc)
    print(f"  Separator paragraph at index: {sep_idx}")

    # 3. Set up running header and page numbers on the main (only) section
    main_section = doc.sections[0]

    # Running header
    add_running_header(
        main_section,
        "A Deep Learning and BI Framework for Cryptocurrency Price Prediction"
    )

    # Page numbers in footer
    add_page_numbers(main_section)

    # 4. Apply 2-column layout to entire document body via the document sectPr
    #    We'll use the "continuous" section break approach:
    #    - Section 1 (before separator): 1 column  → header block
    #    - Section 2 (body):             2 columns → article body
    #
    # The main sectPr (end of document) will be 2-column.
    # A continuous break after the separator paragraph starts the 2-col section.

    body = doc.element.body
    main_sectPr = body.find(qn('w:sectPr'))

    # Make the main sectPr 2-column
    set_two_columns(main_sectPr, num_cols=2, space_twips=720, with_rule=True)

    # Insert a 1-column continuous break right after the separator paragraph
    # so the header block stays single-column
    if sep_para is not None:
        # Create a 1-column sectPr clone for the header area
        one_col_sectPr = copy.deepcopy(main_sectPr)
        # Make it 1-column
        for old_cols in one_col_sectPr.findall(qn('w:cols')):
            one_col_sectPr.remove(old_cols)
        cols_one = OxmlElement('w:cols')
        cols_one.set(qn('w:num'), '1')
        one_col_sectPr.append(cols_one)

        insert_section_break_after(sep_para._element, one_col_sectPr)
        print("  Inserted 1-col / 2-col section break after abstract separator.")

    # 5. Ensure page margins (already set in generator but confirm)
    main_section.top_margin    = Inches(0.75)
    main_section.bottom_margin = Inches(1.0)
    main_section.left_margin   = Inches(0.75)
    main_section.right_margin  = Inches(0.75)

    # 6. Save
    doc.save(DOCX_PATH)
    print(f"[OK] Polished and saved: {DOCX_PATH}")


if __name__ == '__main__':
    polish()
