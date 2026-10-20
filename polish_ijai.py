import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

doc = docx.Document('05_Reports/Manuscript_IJAI_FINAL.docx')

# Define regex for headings
heading_pattern = re.compile(r'^([IVX]+)\.\s+(.*)')
subheading_pattern = re.compile(r'^([A-Z])\.\s+(.*)')

h1_counter = 0
h2_counters = {}

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    
    # Identify title, abstract, etc. based on index or content
    is_title = (i == 0)
    is_authors = (i == 1)
    is_affiliation = (i == 2)
    
    # Process text for headings
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
    
    # Apply styling
    for run in p.runs:
        run.font.name = 'Times New Roman'
        
        if is_title:
            run.font.size = Pt(16)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_authors:
            run.font.size = Pt(10)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_affiliation:
            run.font.size = Pt(8)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_heading:
            run.font.size = Pt(10)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        elif is_subheading:
            run.font.size = Pt(10)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            run.font.size = Pt(10)
            if not p.alignment == WD_ALIGN_PARAGRAPH.CENTER:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

doc.save('05_Reports/Manuscript_IJAI_FINAL.docx')
print("Successfully polished the document to match IJAI format.")
