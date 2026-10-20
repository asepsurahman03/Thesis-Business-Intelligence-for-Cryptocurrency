"""
Embed 300 DPI figures into the FINAL revised manuscript
and run a last verification audit.
"""

import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.ns import qn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "04_Visualizations")
DOC_SRC = os.path.join(BASE_DIR, "A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting_REVISED_v2.docx")
DOC_OUT = os.path.join(BASE_DIR, "05_Reports", "Deep_Learning_Cryptocurrency_BI_FINAL_SUBMIT.docx")

FIGURES = {
    1: os.path.join(FIG_DIR, 'Fig1_BTC_Price_Volume_300dpi.png'),
    2: os.path.join(FIG_DIR, 'Fig2_Model_Comparison_300dpi.png'),
    3: os.path.join(FIG_DIR, 'Fig3_Residual_Distribution_300dpi.png'),
    4: os.path.join(FIG_DIR, 'Fig4_BI_Dashboard_KPI_300dpi.png'),
}

doc = Document(DOC_SRC)

def para_text(p):
    return "".join(r.text for r in p.runs)

def set_text(p, new_text):
    if p.runs:
        for r in p.runs: r.text = ""
        p.runs[0].text = new_text
    else:
        p.add_run(new_text)

print("=" * 70)
print("FINAL AUDIT + FIGURE EMBED")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT: Quick citation order check
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT] Citation order verification...")

# Find references section
ref_start = None
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    if re.match(r'^\[1\]\t', txt) or re.match(r'^\[1\] ', txt):
        ref_start = i
        break

# Collect body text citations
body_text = ""
for i, p in enumerate(doc.paragraphs):
    if ref_start and i >= ref_start:
        break
    body_text += para_text(p) + " "
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            body_text += cell.text + " "

citations_found = []
seen = set()
for m in re.finditer(r'\[(\d+)\]', body_text):
    n = int(m.group(1))
    if n not in seen:
        seen.add(n)
        citations_found.append(n)

# Check for out-of-order
issues = []
for i, n in enumerate(citations_found):
    if n != i + 1:
        issues.append(f"Position {i+1}: found [{n}], expected [{i+1}]")

if issues:
    print(f"  [!] {len(issues)} citation order issue(s):")
    for iss in issues:
        print(f"    {iss}")
else:
    print(f"  [OK] All {len(citations_found)} citations in correct order [1]-[{max(citations_found)}]")

# Specific check for [15]-[17]
for t in [15, 16, 17, 37, 38, 39, 40]:
    if t in citations_found:
        pos = citations_found.index(t) + 1
        status = "[OK]" if pos == t else f"[!] at position {pos}"
        print(f"  [{t}] {status}")

# arXiv count
print("\n[AUDIT] arXiv preprint count...")
arxiv_count = 0
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p)
    if ref_start and i < ref_start:
        continue
    if "arXiv preprint" in txt or ("arXiv" in txt and "arxiv.org" in txt and "Workshop" not in txt):
        arxiv_count += 1
        print(f"  Para [{i}]: {txt[:100]}")
print(f"  True arXiv preprints: {arxiv_count} (limit: 2) {'[OK]' if arxiv_count <= 2 else '[!] EXCEEDS LIMIT'}")

# ─────────────────────────────────────────────────────────────────────────────
# EMBED FIGURES: Find each figure in doc tables (they're stored as images in tables)
# and replace with new high-quality versions
# ─────────────────────────────────────────────────────────────────────────────
print("\n[EMBED] Searching for figure locations in document...")

from docx.oxml import OxmlElement
from lxml import etree

# Find paragraphs just before/after each figure caption
fig_caption_paras = {}
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    for n in [1, 2, 3, 4]:
        pattern = f"Figure {n}."
        if txt.startswith(pattern) or txt.startswith(f"Fig. {n}."):
            fig_caption_paras[n] = i
            print(f"  Fig. {n} caption at para [{i}]")

# Check for inline images using relationships
print("\n[EMBED] Checking for existing inline images...")
inline_shapes = doc.inline_shapes
print(f"  Document has {len(inline_shapes)} inline shape(s)")
for j, shape in enumerate(inline_shapes):
    try:
        print(f"    Shape {j}: width={shape.width}, height={shape.height}, type={shape.type}")
    except:
        print(f"    Shape {j}: (error reading)")

# Check for images in run elements
print("\n[EMBED] Scanning for drawing/image XML elements...")
img_paras = []
for i, p in enumerate(doc.paragraphs):
    if p._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip') is not None:
        img_paras.append(i)
        print(f"  Image found at paragraph [{i}]")

if not img_paras and len(inline_shapes) == 0:
    print("  No inline images found in paragraphs.")
    print("  Images may be in text boxes or floating — will insert after captions instead.")

# ─────────────────────────────────────────────────────────────────────────────
# INSERT IMAGES: Add images immediately before each figure caption
# This is the safest approach — insert as new paragraph with image
# ─────────────────────────────────────────────────────────────────────────────
print("\n[EMBED] Inserting high-resolution figures...")

from docx.oxml.ns import nsmap
from copy import deepcopy

def insert_image_before_para(doc, para_idx, img_path, width_inches=5.5):
    """Insert an image paragraph before the paragraph at para_idx."""
    if not os.path.exists(img_path):
        print(f"  [!] Image not found: {img_path}")
        return False
    
    # Create a temporary doc to get the image paragraph XML
    from docx import Document as TempDoc
    tmp = TempDoc()
    tmp_para = tmp.add_paragraph()
    run = tmp_para.add_run()
    run.add_picture(img_path, width=Inches(width_inches))
    tmp_para.alignment = 1  # center
    
    # Get the XML element
    img_xml = deepcopy(tmp_para._element)
    
    # Insert before the target paragraph
    target_para = doc.paragraphs[para_idx]
    target_para._element.addprevious(img_xml)
    return True

# Insert figures before their captions
# Note: we process in reverse order to avoid index shifting
inserted = 0
for fig_num in sorted(fig_caption_paras.keys(), reverse=True):
    cap_idx = fig_caption_paras[fig_num]
    img_path = FIGURES.get(fig_num)
    
    if img_path and os.path.exists(img_path):
        # Check if there's already an image just before the caption
        has_image_before = False
        if cap_idx > 0:
            prev_para = doc.paragraphs[cap_idx - 1]
            if prev_para._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip') is not None:
                has_image_before = True
        
        if not has_image_before:
            success = insert_image_before_para(doc, cap_idx, img_path, width_inches=5.5)
            if success:
                print(f"  Inserted Fig. {fig_num} at para [{cap_idx}]")
                inserted += 1
        else:
            print(f"  Fig. {fig_num} already has image before caption — skipping")
    else:
        print(f"  [!] Fig. {fig_num} image not found: {img_path}")

print(f"  Total figures inserted: {inserted}")

# ─────────────────────────────────────────────────────────────────────────────
# FINAL VERIFICATION: paragraph sentence counts
# ─────────────────────────────────────────────────────────────────────────────
print("\n[FINAL CHECK] Short paragraph count...")
short_count = 0
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    style = p.style.name if p.style else ""
    if not txt or "Heading" in style or len(txt) < 50:
        continue
    if txt.startswith('[') and ']' in txt[:5]:
        continue
    if txt.startswith('Fig') or txt.startswith('Table') or txt.startswith('Algorithm'):
        continue
    # Skip pseudocode lines
    if any(x in txt for x in ['←', ':=', 'end for', 'do\n', '//\n']):
        continue
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if s.strip() and len(s.strip()) > 10]
    if len(sentences) < 2 and len(txt) > 60:
        short_count += 1

print(f"  Remaining single-sentence body paragraphs: {short_count}")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE FINAL SUBMISSION FILE
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
doc.save(DOC_OUT)
print(f"[OK] FINAL SUBMISSION FILE SAVED:")
print(f"     {DOC_OUT}")
print("=" * 70)
