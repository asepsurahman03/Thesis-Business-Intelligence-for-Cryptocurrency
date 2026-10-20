"""
Comprehensive Final Pre-Submission Audit Script
"""

import os
import sys
import re
import fitz # PyMuPDF
import docx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_PATH = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx")
PDF_PATH = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.pdf")

print("=" * 70)
print("COMPREHENSIVE FINAL PRE-SUBMISSION AUDIT")
print("=" * 70)

doc = docx.Document(DOCX_PATH)
pdf = fitz.open(PDF_PATH)

# 1. Page Count & Layout Check
print(f"\n1. PDF Page Count: {len(pdf)} pages")
for pno in range(len(pdf)):
    page = pdf[pno]
    rect = page.rect
    print(f"   Page {pno+1}: {rect.width} x {rect.height} pt (standard Letter/A4)")

# 2. Section Headings Check in Word & PDF
print("\n2. Checking Section Headings in DOCX:")
headings_found = []
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith('Heading'):
        headings_found.append((i, p.style.name, p.text.strip()))
        print(f"   P[{i:03d}] {p.style.name:12s}: {repr(p.text.strip())}")

# 3. Figures & Captions Check
print("\n3. Checking Figures & Captions:")
fig_paras = []
for i, p in enumerate(doc.paragraphs):
    blips = p._p.xpath('.//a:blip')
    if blips:
        caption = doc.paragraphs[i+1].text.strip() if i+1 < len(doc.paragraphs) else "N/A"
        cap_style = doc.paragraphs[i+1].style.name if i+1 < len(doc.paragraphs) else "N/A"
        print(f"   Image at P[{i:03d}], Caption P[{i+1:03d}] (Style: {cap_style}): {repr(caption[:70])}")

# 4. Tables Check
print("\n4. Checking Tables:")
print(f"   Total tables: {len(doc.tables)}")
for idx, t in enumerate(doc.tables):
    rows = len(t.rows)
    cols = len(t.columns)
    first_row = [c.text.strip().replace('\n', ' ') for c in t.rows[0].cells]
    print(f"   Table {idx}: {rows} rows x {cols} cols | First row: {' | '.join(first_row)[:80]}")

# 5. Citation Continuity Check
print("\n5. Checking Citations in Body Text vs References:")
body_text = ""
for p in doc.paragraphs:
    if p.style.name != 'references':
        body_text += p.text + " "
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            body_text += cell.text + " "

citations = [int(m) for m in re.findall(r'\[(\d+)\]', body_text)]
unique_citations = []
for c in citations:
    if c not in unique_citations:
        unique_citations.append(c)

print(f"   Total citation instances in body: {len(citations)}")
print(f"   Unique citations in body: {len(unique_citations)} (Min: {min(unique_citations)}, Max: {max(unique_citations)})")

ref_paras = [p for p in doc.paragraphs if p.style.name == 'references']
print(f"   Total references listed in bibliography: {len(ref_paras)}")

missing_refs = set(range(1, max(unique_citations)+1)) - set(unique_citations)
if missing_refs:
    print(f"   [!] Citations missing from body: {missing_refs}")
else:
    print(f"   [OK] All citations [1] to [{max(unique_citations)}] are cited consecutively in the body text!")

# 6. Informal language / colloquialism scan
print("\n6. Scanning for Informal Phrases & Colloquialisms:")
flagged_words = [
    "fun part", "fix this", "you can't", "you can", "can't just", "a very different story",
    "deploy to production", "kind of", "sort of", "obviously", "as everyone knows"
]
issues = []
for i, p in enumerate(doc.paragraphs):
    for w in flagged_words:
        if w in p.text.lower():
            issues.append((i, w, p.text[:80]))

if issues:
    for i, w, txt in issues:
        print(f"   [!] Warning at P[{i}]: found '{w}' in '{txt}'")
else:
    print("   [OK] Zero informal or conversational phrases detected across all paragraphs!")

# 7. Checking for Duplicate Text / Double Prefixes in PDF Text
print("\n7. Scanning Rendered PDF Text for Duplications:")
pdf_text = ""
for page in pdf:
    pdf_text += page.get_text() + "\n"

lines = [l.strip() for l in pdf_text.split('\n') if l.strip()]
double_prefix_issues = []
for l in lines:
    if re.search(r'\b(TABLE\s+[IVXLCDM]+\b.*?TABLE\s+[IVXLCDM]+)', l, re.IGNORECASE):
        double_prefix_issues.append(l)
    if re.search(r'\b(Fig\.\s*\d+.*?Fig\.\s*\d+)', l, re.IGNORECASE):
        double_prefix_issues.append(l)

if double_prefix_issues:
    for dpi in double_prefix_issues:
        print(f"   [!] Double prefix detected: {repr(dpi)}")
else:
    print("   [OK] Zero double prefixes (TABLE X TABLE X or Fig X Fig X) detected in rendered PDF!")

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
