"""
Complete manuscript revision builder for:
Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(BASE_DIR, "04_Visualizations")
TARGET_DOC = os.path.join(BASE_DIR, "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx")

FIG1_PATH = os.path.join(FIG_DIR, "Fig1_BTC_Price_Volume_300dpi.png")
FIG2_PATH = os.path.join(FIG_DIR, "Fig2_Model_Comparison_300dpi.png")
FIG3_PATH = os.path.join(FIG_DIR, "Fig3_Residual_Distribution_300dpi.png")
FIG4_PATH = os.path.join(FIG_DIR, "Fig4_BI_Dashboard_KPI_300dpi.png")

# Verify figures exist
for p in [FIG1_PATH, FIG2_PATH, FIG3_PATH, FIG4_PATH]:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Missing figure: {p}")
print("All 4 300 DPI figures verified.")

def create_element(name):
    return OxmlElement(name)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right, insideH, insideV
    values: dict(sz=12, val='single', color='000000', space='0')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, attr in [("val", "w:val"), ("color", "w:color"), ("sz", "w:sz"), ("space", "w:space")]:
                if key in edge_data:
                    element.set(qn(attr), str(edge_data[key]))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

print("Helper functions defined.")
