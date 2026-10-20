import docx
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

doc = docx.Document('Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx')

print("--- CHECKING ALL NUMBERED STYLES IN THE DOCUMENT ---")
for i, p in enumerate(doc.paragraphs):
    s_name = p.style.name
    if s_name in ['Heading 1', 'Heading 2', 'Heading 3', 'table head', 'figure caption']:
        print(f"[{i:03d}] Style: {s_name:15s} | Text: {repr(p.text)}")
