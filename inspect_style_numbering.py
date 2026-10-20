import docx
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

doc = docx.Document('Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx')

for s in doc.styles:
    if s.name in ['table head', 'figure caption', 'Heading 1', 'Heading 2', 'Caption']:
        xml = s._element.xml
        has_num = 'w:numPr' in xml
        print(f"Style '{s.name}': has_numPr={has_num}")
        print("  XML snippet:", xml[:250])
