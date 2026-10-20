"""
IJ-AI Final Audit Script:
1. Audit citation order [37] and [38]
2. Count arXiv preprints
3. Check Table II content (DM test p-values)
4. Generate comprehensive revision report
"""

import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from docx import Document

DOC_PATH = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Deep_Learning_Cryptocurrency_BI_REVISED_V3.docx"
doc = Document(DOC_PATH)

def para_text(p):
    return "".join(r.text for r in p.runs)

print("=" * 70)
print("IJ-AI FINAL AUDIT REPORT")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 1: Citation order — find order of first appearance in text
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 1] Citation Order Analysis")
print("-" * 50)

# Collect all paragraphs that are NOT references (i.e., body text)
# References section starts where paragraphs start with "[1]", "[2]" etc.
ref_start_idx = None
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    if txt in ("REFERENCES", "10. REFERENCES", "9. REFERENCES", "REFERENCE"):
        ref_start_idx = i
        break
    if re.match(r'^\[1\]', txt):
        ref_start_idx = i
        break

print(f"  References section starts at paragraph: {ref_start_idx}")

# Extract all [N] citations from body text
body_text = ""
for i, p in enumerate(doc.paragraphs):
    if ref_start_idx and i >= ref_start_idx:
        break
    body_text += para_text(p) + " "

# Also check table cells
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            body_text += cell.text + " "

# Find all citation numbers in order of appearance
citation_pattern = re.compile(r'\[(\d+)\]')
citations_in_order = []
seen = set()
for m in citation_pattern.finditer(body_text):
    num = int(m.group(1))
    if num not in seen:
        seen.add(num)
        citations_in_order.append(num)

print(f"\n  First-appearance order of citations:")
for i, num in enumerate(citations_in_order):
    expected = i + 1
    status = "OK" if num == expected else f"[!] EXPECTED [{expected}]"
    print(f"    Position {i+1:3d}: [{num:2d}]  {status}")

# Check specifically [37] and [38]
print("\n  Key citation positions:")
for target in [35, 36, 37, 38, 39, 40]:
    if target in citations_in_order:
        pos = citations_in_order.index(target) + 1
        print(f"    [{target}] first appears at position {pos} in text")
    else:
        print(f"    [{target}] NOT FOUND in body text")

# Check for any gaps
expected_set = set(range(1, max(citations_in_order) + 1)) if citations_in_order else set()
missing = expected_set - seen
if missing:
    print(f"\n  [!] Citations NOT cited in body text: {sorted(missing)}")
else:
    print(f"\n  All citations [1]–[{max(citations_in_order)}] appear in body text.")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 2: Count arXiv preprints in reference list
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 2] arXiv Preprint Count")
print("-" * 50)

arxiv_refs = []
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p)
    if "arXiv" in txt or "arxiv" in txt.lower() or "2001.08" in txt:
        arxiv_refs.append((i, txt[:120]))

print(f"  ArXiv references found: {len(arxiv_refs)}")
for idx, txt in arxiv_refs:
    print(f"    Para [{idx}]: {txt}")

if len(arxiv_refs) <= 2:
    print(f"\n  [OK] {len(arxiv_refs)} arXiv preprint(s) -- within the limit of 2")
else:
    print(f"\n  [!] {len(arxiv_refs)} arXiv preprints found -- EXCEEDS limit of 2")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 3: Table II Content (Diebold-Mariano pairwise tests)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 3] Table II — Diebold-Mariano Test Results")
print("-" * 50)

dm_table_found = False
for t_idx, table in enumerate(doc.tables):
    # Check all cells for DM-related content
    all_cell_text = " ".join(cell.text for row in table.rows for cell in row.cells)
    if ("Diebold" in all_cell_text or "DM" in all_cell_text or
        "p-value" in all_cell_text.lower() or "p value" in all_cell_text.lower() or
        "0.014" in all_cell_text or "statistic" in all_cell_text.lower()):
        print(f"\n  Table {t_idx} (likely Table II - DM test):")
        dm_table_found = True
        for r_idx, row in enumerate(table.rows):
            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                print(f"    Row {r_idx}: {row_text}")
        print()

if not dm_table_found:
    print("  [!] DM test table not found - searching by position...")
    # Table II should be 2nd table in document
    if len(doc.tables) >= 2:
        table = doc.tables[1]
        print(f"  Table index 1 content (likely Table II):")
        for r_idx, row in enumerate(table.rows):
            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                print(f"    Row {r_idx}: {row_text}")
    else:
        print(f"  Only {len(doc.tables)} tables found in document")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 4: ALL TABLES — list all tables and row counts
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 4] All Tables in Document")
print("-" * 50)
for t_idx, table in enumerate(doc.tables):
    first_row = " | ".join(c.text.strip() for c in table.rows[0].cells if c.text.strip()) if table.rows else ""
    print(f"  Table {t_idx}: {len(table.rows)} rows x {len(table.columns)} cols | First row: {first_row[:80]}")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 5: Verify keywords are fixed (in table 0)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 5] Keywords Verification")
print("-" * 50)
kw_table = doc.tables[0] if doc.tables else None
if kw_table:
    all_kw_text = " ".join(c.text for row in kw_table.rows for c in row.cells)
    has_full_lstm = "Long Short-Term Memory" in all_kw_text
    has_full_gru = "Gated Recurrent Unit" in all_kw_text
    has_short_lstm = re.search(r'\bLSTM\b', all_kw_text) and not has_full_lstm
    has_short_gru = re.search(r'\bGRU\b', all_kw_text) and not has_full_gru
    
    print(f"  'Long Short-Term Memory' in keywords: {'[OK]' if has_full_lstm else '[!] MISSING'}")
    print(f"  'Gated Recurrent Unit' in keywords:  {'[OK]' if has_full_gru else '[!] MISSING'}")
    if has_short_lstm:
        print(f"  [!] 'LSTM' still appears as abbreviation-only in keywords table")
    if has_short_gru:
        print(f"  [!] 'GRU' still appears as abbreviation-only in keywords table")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 6: Verify intro subsections removed
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 6] Introduction Subsection Check")
print("-" * 50)
intro_subsec_pattern = re.compile(r'^\s*1\.[1-9][\.\s]')
found_subsecs = []
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    if intro_subsec_pattern.match(txt) and txt:
        found_subsecs.append((i, txt[:80]))

if found_subsecs:
    print(f"  [!] Introduction subsections STILL PRESENT:")
    for idx, txt in found_subsecs:
        print(f"    Para [{idx}]: {txt}")
else:
    print(f"  [OK] No 1.x subsection headings found in document")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 7: Figure pre-citations check
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 7] Figure Pre-Citation Check")
print("-" * 50)

# Find caption positions
caption_positions = {}
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    for fig_num in [1, 2, 3, 4]:
        if txt.startswith(f"Fig. {fig_num}.") or txt.startswith(f"Figure {fig_num}."):
            if fig_num not in caption_positions:
                caption_positions[fig_num] = i

print(f"  Caption paragraph positions: {caption_positions}")

for fig_num, cap_idx in caption_positions.items():
    # Search for "Figure N" or "Fig. N" in text BEFORE the caption
    precited = False
    for i in range(0, cap_idx):
        txt = para_text(doc.paragraphs[i])
        if f"Figure {fig_num}" in txt or f"Fig. {fig_num}" in txt or f"Fig.{fig_num}" in txt:
            if not (txt.strip().startswith("Fig.") or txt.strip().startswith("Figure")):
                precited = True
                break
    status = "[OK]" if precited else "[!] NOT PRE-CITED"
    print(f"  Fig. {fig_num} (caption at para {cap_idx}): {status}")

# ─────────────────────────────────────────────────────────────────────────────
# AUDIT 8: Paragraph length check (3-sentence rule)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[AUDIT 8] Short Paragraph Check (< 2 sentences)")
print("-" * 50)
short_paras = []
for i, p in enumerate(doc.paragraphs):
    txt = para_text(p).strip()
    style = p.style.name if p.style else ""
    # Skip headings, captions, empty lines, reference entries
    if not txt:
        continue
    if "Heading" in style or "Caption" in style:
        continue
    if txt.startswith("[") and "]" in txt[:5]:  # reference line
        continue
    if txt.startswith("Fig.") or txt.startswith("Figure") or txt.startswith("Table"):
        continue
    if len(txt) < 40:  # very short — likely heading or label
        continue
    
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if s.strip() and len(s.strip()) > 10]
    if len(sentences) < 2 and len(txt) > 60:
        short_paras.append((i, len(sentences), txt[:100]))

if short_paras:
    print(f"  Found {len(short_paras)} paragraph(s) with < 2 sentences:")
    for idx, cnt, txt in short_paras[:15]:  # show first 15
        print(f"    [{idx}] ({cnt} sent.): {txt}")
else:
    print(f"  [OK] All paragraphs have >= 2 sentences")

print("\n" + "=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
