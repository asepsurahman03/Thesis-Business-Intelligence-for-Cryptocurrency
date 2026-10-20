import docx
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

doc = docx.Document('Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx')

print("--- INSPECTING PARAGRAPH XML FOR HEADINGS & CAPTIONS ---")
for i in [37, 65, 71, 76, 83, 87, 95]:
    p = doc.paragraphs[i]
    print(f"\nParagraph {i} (Style: {p.style.name}):")
    print("  Text:", repr(p.text))
    print("  Runs:", [repr(r.text) for r in p.runs])
    print("  XML:", p._p.xml[:400])
