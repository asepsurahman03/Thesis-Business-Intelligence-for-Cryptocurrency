# -*- coding: utf-8 -*-
"""
fix_citations_and_table2.py
Fix 4 issues:
  1. Add [22] PatchTST & [23] TimesNet citations back into Introduction text
  2. Add [37] Bollen citation into Future research / Discussion
  3. Add GRU column to Table 2 (KPI Dashboard)
"""
import sys, re
from docx import Document
from docx.shared import Pt
from copy import deepcopy
from lxml import etree

sys.stdout.reconfigure(encoding='utf-8')

FNAME = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Deep Learning Framework for Cryptocurrency Price Prediction Using Business Intelligence.docx"

doc = Document(FNAME)

def replace_text(para, new_text):
    fmt_size, fmt_name, fmt_bold = None, None, False
    if para.runs:
        r0 = para.runs[0]
        fmt_size = r0.font.size
        fmt_name = r0.font.name
        fmt_bold = r0.bold
    for run in para.runs:
        run._element.getparent().remove(run._element)
    nr = para.add_run(new_text)
    if fmt_size: nr.font.size = fmt_size
    if fmt_name: nr.font.name = fmt_name
    nr.bold = fmt_bold

def gettxt(para):
    return "".join(r.text for r in para.runs).strip()

# ═══════════════════════════════════════════════════════════════════════════════
# FIX 1 & 2 — Restore [22], [23], [37] citations in body text
# ═══════════════════════════════════════════════════════════════════════════════

for para in doc.paragraphs:
    txt = gettxt(para)

    # [22] PatchTST & [23] TimesNet — add into Transformer paragraph
    # Currently: "...Informer as the primary Transformer representative, providing a universally
    # recognized, computationally stable baseline extensively stress-tested in hourly
    # cryptocurrency environments. However, Transformers may suffer from overfitting..."
    if "Informer as the primary Transformer representative" in txt:
        new = (
            "Transformer architectures relying on self-attention mechanisms [19] have increasingly "
            "been adapted for time-series forecasting [20]. The Informer Transformer [21], utilizing "
            "sparse probabilistic self-attention (O(L log L)), serves as the primary Transformer "
            "baseline in this study. While newer architectures such as PatchTST [22] and "
            "TimesNet [23] represent the current vanguard in multivariate modeling, the Informer "
            "provides a well-established, computationally stable benchmark extensively validated "
            "in hourly cryptocurrency environments. Transformers may nonetheless suffer from "
            "overfitting during chaotic short-horizon intervals [24]\u2013[26]."
        )
        replace_text(para, new)
        print("[Fix 1] [22] PatchTST & [23] TimesNet restored in Transformer paragraph.")
        break

# [37] Bollen et al. — add into Future research paragraph
for para in doc.paragraphs:
    txt = gettxt(para)
    if "Future research should pursue two directions" in txt:
        new = (
            "Future research should pursue two directions: (1) integrating NLP sentiment signals "
            "from social media and on-chain data [37] to improve model resilience during "
            "macroeconomic shocks; and (2) extending the BI pipeline to multi-asset portfolios "
            "incorporating altcoins and cross-market correlation matrices."
        )
        replace_text(para, new)
        print("[Fix 2] [37] Bollen citation restored in Future research paragraph.")
        break

# ═══════════════════════════════════════════════════════════════════════════════
# FIX 3 — Add GRU column to Table 2 (KPI Dashboard)
# Current Table 2: System Output | XGBoost | Informer | LSTM
# Target:          System Output | XGBoost | Informer | LSTM | GRU
# ═══════════════════════════════════════════════════════════════════════════════
t2 = doc.tables[2]

# GRU values to add (from results): Direction Acc 69.8%, Sharpe 1.32, VaR -2.89%
gru_values = {
    0: "GRU",           # header row
    1: "69.8% \u00b1 1.8%",   # Direction Acc
    2: "1.32 \u00b1 0.12",    # Sharpe Ratio
    3: "-2.89% \u00b1 0.3%",  # VaR
}

print(f"[Fix 3] Table 2 has {len(t2.rows)} rows, {len(t2.columns)} columns.")
print("        Adding GRU column...")

for ri, row in enumerate(t2.rows):
    # Clone the last cell's XML to preserve formatting
    last_cell = row.cells[-1]
    new_cell_xml = deepcopy(last_cell._tc)
    # Clear text from cloned cell
    for tc_p in new_cell_xml.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        for tc_r in tc_p.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
            for tc_t in tc_r.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                tc_t.text = gru_values.get(ri, "")
    # Append new cell to the row
    row._tr.append(new_cell_xml)
    print(f"  Row {ri}: GRU = '{gru_values.get(ri, '')}'")

print("[Fix 3] GRU column added to Table 2.")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(FNAME)

# Verify citations now present
doc2 = Document(FNAME)
body_text = ""
in_refs = False
for p in doc2.paragraphs:
    if p.text.strip() == "REFERENCES":
        in_refs = True
    if not in_refs:
        body_text += p.text + " "

found = sorted(set(re.findall(r'\[(\d+)\]', body_text)), key=int)
missing = [r for r in range(1, 41) if str(r) not in found]
print(f"\nCitations found in body: {found}")
print(f"Still uncited: {missing}")
print(f"\nSaved: {FNAME}")
