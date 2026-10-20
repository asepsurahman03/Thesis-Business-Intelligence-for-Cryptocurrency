# -*- coding: utf-8 -*-
"""
fix_table2_gru.py  — bersihkan duplikasi teks di kolom GRU (kolom ke-4, index 4)
"""
import sys
from docx import Document
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

FNAME = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
         r"\Deep Learning Framework for Cryptocurrency Price Prediction "
         r"Using Business Intelligence.docx")

doc = Document(FNAME)
t2 = doc.tables[2]

print(f"Table 2: {len(t2.rows)} rows x {len(t2.columns)} columns")

# GRU values per row index
GRU_VALUES = {
    0: "GRU",
    1: "69.8% \u00b1 1.8%",
    2: "1.32 \u00b1 0.12",
    3: "-2.89% \u00b1 0.3%",
}

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

for ri, row in enumerate(t2.rows):
    # GRU is the last column (index 4 after our addition)
    cell = row.cells[-1]
    tc = cell._tc

    # Remove ALL existing paragraph content
    for p_elem in tc.findall(f'{{{W}}}p'):
        # Remove all runs inside this paragraph
        for r_elem in p_elem.findall(f'{{{W}}}r'):
            p_elem.remove(r_elem)
        # Add a fresh run with correct text
        r_new = doc._element.makeelement(f'{{{W}}}r', {})
        t_new = doc._element.makeelement(f'{{{W}}}t', {})
        t_new.text = GRU_VALUES.get(ri, "")
        if " " in t_new.text:
            t_new.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        r_new.append(t_new)
        p_elem.append(r_new)
        break  # only process first paragraph in cell

    print(f"  Row {ri}: set GRU = '{GRU_VALUES.get(ri, '')}'")

doc.save(FNAME)
print(f"\nSaved: {FNAME}")

# Verify
doc2 = Document(FNAME)
t2v = doc2.tables[2]
print("\n=== TABLE 2 VERIFICATION ===")
for ri, row in enumerate(t2v.rows):
    cells = [c.text.strip() for c in row.cells]
    print(f"Row {ri}: {' | '.join(cells)}")
