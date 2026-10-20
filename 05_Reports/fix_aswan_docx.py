# -*- coding: utf-8 -*-
"""
fix_aswan_docx.py
Apply 3 IJ-AI compliance fixes directly on the original Aswan (1).docx:
  Fix 1 – Title: shorten to 9 words, no acronyms
  Fix 2 – Abstract (in Table[0]): expand acronyms, remove citations, <= 200 words
  Fix 3 – Structure IMRADC:
           - Delete "LITERATURE REVIEW AND RELATED WORK" heading; merge content into Introduction
           - Rename subsections 2.x -> 1.x (inside Introduction)
           - Rename "SYSTEM ARCHITECTURE AND FRAMEWORK DESIGN" -> "METHOD", 3.x -> 2.x
           - Rename "EMPIRICAL RESULTS AND CRITICAL ANALYSIS" -> "RESULTS AND DISCUSSION", 4.x -> 3.x
           - Rename "CONCLUSION" numbering stays (no number needed - already unnumbered)
"""

import copy
import re
from docx import Document
from docx.oxml.ns import qn

SRC = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1).docx")

DST = (r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports"
       r"\A Deep Learning and Business Intelligence Framework for CryptocurrencyPrice Prediction"
       r" Comparative Analysis of Sequence Networks against State-of-the-Art Transformers - Aswan (1) - REVISED.docx")

doc = Document(SRC)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: replace text in a paragraph preserving all run formatting
# ─────────────────────────────────────────────────────────────────────────────
def replace_para_text(para, new_text):
    """Replace full paragraph text, keeping formatting of the first run."""
    # Collect format from first run (if any)
    if not para.runs:
        para.add_run(new_text)
        return
    fmt_run = para.runs[0]
    # Clear all runs from XML
    for run in para.runs:
        run._element.getparent().remove(run._element)
    # Add single new run with original formatting
    new_run = para.add_run(new_text)
    new_run.bold      = fmt_run.bold
    new_run.italic    = fmt_run.italic
    new_run.underline = fmt_run.underline
    if fmt_run.font.size:
        new_run.font.size = fmt_run.font.size
    if fmt_run.font.name:
        new_run.font.name = fmt_run.font.name


def get_full_text(para):
    return "".join(r.text for r in para.runs)


# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 – TITLE  (paragraph index 0, style='Title')
# ─────────────────────────────────────────────────────────────────────────────
NEW_TITLE = ("Deep Learning Framework for Cryptocurrency Price Prediction "
             "Using Business Intelligence")

title_para = doc.paragraphs[0]
replace_para_text(title_para, NEW_TITLE)
print("[Fix 1] Title updated.")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2 – ABSTRACT in Table[0], cell row-index 1, col-index 1
# The abstract cell is the large text cell in the second row, second column.
# ─────────────────────────────────────────────────────────────────────────────
NEW_ABSTRACT = (
    "Cryptocurrency markets exhibit inherent volatility that complicates predictive "
    "modeling, demanding methods that bridge deep learning with enterprise decision "
    "support systems. This study proposes an automated, four-layer Business Intelligence "
    "pipeline embedding recurrent and transformer inferences into an enterprise decision "
    "support system to dynamically compute risk-adjusted metrics, including Sharpe Ratio "
    "and Value-at-Risk. Analyzing 43,786 hourly Bitcoin/USDT records spanning 2021\u20132026, "
    "we evaluated XGBoost, Long Short-Term Memory, Gated Recurrent Unit, and the Informer "
    "Transformer. Walk-Forward Validation established the Gated Recurrent Unit as the most "
    "accurate model with a Root Mean Square Error of 0.1058 (p\u202f<\u202f0.001). However, the "
    "Business Intelligence integration revealed a critical trade-off: despite higher error, "
    "the Long Short-Term Memory network achieved superior Directional Accuracy of 72.3% "
    "and a Sharpe Ratio of 1.45, indicating that numerical error minimization does not "
    "inherently guarantee trading profitability. The prototype Microsoft Power BI dashboard "
    "demonstrated operational feasibility with an Excellent System Usability Scale score of "
    "86.4, confirming that high-frequency neural forecasts can successfully drive real-world "
    "institutional risk management tools."
)

abs_table = doc.tables[0]
# Find the cell that contains the old abstract text
for row in abs_table.rows:
    for cell in row.cells:
        if "Decision Support Systems (DSS)" in cell.text and "Analyzing 43,786" in cell.text:
            # Clear all paragraphs in this cell and replace
            for p in cell.paragraphs:
                for run in p.runs:
                    run._element.getparent().remove(run._element)
            # Write new abstract into the first paragraph
            first_p = cell.paragraphs[0]
            new_run = first_p.add_run(NEW_ABSTRACT)
            # Copy font from paragraph style if possible
            print("[Fix 2] Abstract cell updated.")
            break

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3 – SECTION HEADINGS & SUBSECTION NUMBERING
# ─────────────────────────────────────────────────────────────────────────────
# Strategy:
#   a) Remove the "LITERATURE REVIEW AND RELATED WORK" heading paragraph
#      Its content paragraphs stay but become part of Introduction.
#      Subsections 2.1, 2.2, 2.3 → become un-numbered continuation of Introduction
#      (We simplify: relabel them as 1.1, 1.2, 1.3)
#   b) "SYSTEM ARCHITECTURE AND FRAMEWORK DESIGN" → "METHOD"
#      Subsections 3.x → 2.x
#   c) "EMPIRICAL RESULTS AND CRITICAL ANALYSIS" → "RESULTS AND DISCUSSION"
#      Subsections 4.x → 3.x
#   d) "DISCUSSION" standalone section removal (it's already 4.4 subsection in this doc)

HEADING_RENAMES = {
    "LITERATURE REVIEW AND RELATED WORK": None,          # DELETE this heading
    "SYSTEM ARCHITECTURE AND FRAMEWORK DESIGN": "METHOD",
    "EMPIRICAL RESULTS AND CRITICAL ANALYSIS": "RESULTS AND DISCUSSION",
}

# Subsection renumber map: old_prefix -> new_prefix (string replace on text)
SUBSEC_RENAMES = [
    ("2.1.", "1.1."),
    ("2.2.", "1.2."),
    ("2.3.", "1.3."),
    ("3.1.", "2.1."),
    ("3.2.", "2.2."),
    ("3.3.", "2.3."),
    ("3.4.", "2.4."),
    ("3.5.", "2.5."),
    ("3.5.1", "2.5.1"),
    ("3.5.2", "2.5.2"),
    ("4.1.", "3.1."),
    ("4.2.", "3.2."),
    ("4.3.", "3.3."),
    ("4.4.", "3.4."),
    ("4.4.1.", "3.4.1."),
    ("4.4.2.", "3.4.2."),
]

paragraphs_to_delete = []

for i, para in enumerate(doc.paragraphs):
    txt = get_full_text(para).strip()

    # ── Section heading renames / deletions ──
    for old_heading, new_heading in HEADING_RENAMES.items():
        if txt == old_heading:
            if new_heading is None:
                paragraphs_to_delete.append(para)
                print(f"[Fix 3] Marked for deletion: '{old_heading}'")
            else:
                replace_para_text(para, new_heading)
                print(f"[Fix 3] Renamed: '{old_heading}' -> '{new_heading}'")
            break

    # ── Subsection number renaming ──
    for old_prefix, new_prefix in SUBSEC_RENAMES:
        if txt.startswith(old_prefix):
            new_txt = txt.replace(old_prefix, new_prefix, 1)
            replace_para_text(para, new_txt)
            print(f"[Fix 3] Subsection: '{txt[:60]}' -> '{new_txt[:60]}'")
            break

# Delete paragraphs marked for removal (Literature Review heading only)
for para in paragraphs_to_delete:
    p_elem = para._element
    p_elem.getparent().remove(p_elem)
print(f"[Fix 3] Deleted {len(paragraphs_to_delete)} heading paragraph(s).")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
doc.save(DST)
print(f"\nDone. Saved to:\n{DST}")
