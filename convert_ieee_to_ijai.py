import shutil
import docx
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re

source = '05_Reports/Manuscript_IEEE_FINAL_2026_WORD.docx'
target = '05_Reports/Manuscript_IJAI_FINAL_V2.docx'

# Copy the original file to preserve images/tables/equations
shutil.copy(source, target)

doc = docx.Document(target)

# Change page layout
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    
    # Remove multiple columns
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        for col in cols:
            col.set(qn('w:num'), '1')

# Patterns for headings
heading_pattern = re.compile(r'^([IVX]+)\.\s+(.*)')
subheading_pattern = re.compile(r'^([A-Z])\.\s+(.*)')

h1_counter = 0
h2_counters = {}

# Process paragraphs
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    
    is_title = (i == 0)
    is_authors = (i == 1)
    is_affiliation = (i == 2)
    
    m_head = heading_pattern.match(text)
    m_sub = subheading_pattern.match(text)
    
    is_heading = False
    is_subheading = False
    
    if m_head:
        h1_counter += 1
        h2_counters[h1_counter] = 0
        p.text = f"{h1_counter}. {m_head.group(2).upper()}"
        is_heading = True
    elif m_sub and h1_counter > 0:
        h2_counters[h1_counter] += 1
        p.text = f"{h1_counter}.{h2_counters[h1_counter]}. {m_sub.group(2)}"
        is_subheading = True
    elif text.upper() == 'ABSTRACT':
        p.text = 'ABSTRACT'
        is_heading = True
    elif text.upper().startswith('KEYWORDS'):
        pass
    
    # Apply styling
    # We want Times New Roman 10pt for everything except Title and Affiliation
    # Note: iterating through runs and changing font
    for run in p.runs:
        run.font.name = 'Times New Roman'
        
        if is_title:
            run.font.size = Pt(16)
            run.bold = True
        elif is_authors:
            run.font.size = Pt(10)
        elif is_affiliation:
            run.font.size = Pt(8)
        elif is_heading:
            run.font.size = Pt(10)
            run.bold = True
        elif is_subheading:
            run.font.size = Pt(10)
            run.bold = True
        else:
            run.font.size = Pt(10)
            
    # Paragraph alignment
    if is_title or is_authors or is_affiliation:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif is_heading or is_subheading:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        # Avoid forcing alignment on equations or specific elements, but generally justify
        # We can just set it to JUSTIFY unless it's centered already
        if p.alignment != WD_ALIGN_PARAGRAPH.CENTER:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

doc.save(target)
print(f"Successfully converted IEEE doc to IJAI layout and saved as {target}")
