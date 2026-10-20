import fitz # PyMuPDF
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pdf_path = "Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.pdf"
doc = fitz.open(pdf_path)

print("=" * 60)
print(f"VERIFYING RENDERED PDF TEXT (Total Pages: {len(doc)})")
print("=" * 60)

full_pdf_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    full_pdf_text += f"\n--- PAGE {page_num + 1} ---\n" + text

# Check Table headings in PDF text
print("\n[TABLE HEADINGS IN PDF]:")
for line in full_pdf_text.split('\n'):
    if 'TABLE' in line or 'TABLE I' in line or 'TABLE II' in line or 'TABLE III' in line:
        print("  ", repr(line.strip()))

# Check Figure captions in PDF text
print("\n[FIGURE CAPTIONS IN PDF]:")
for line in full_pdf_text.split('\n'):
    if 'Fig.' in line or 'Figure' in line:
        print("  ", repr(line.strip()))

# Check Section Headings in PDF text
print("\n[SECTION HEADINGS IN PDF]:")
for line in full_pdf_text.split('\n'):
    if any(line.strip().startswith(h) for h in ['I. ', 'II. ', 'III. ', 'IV. ', 'A. ', 'B. ', 'C. ', 'D. ', 'E. ', 'F. ']):
        print("  ", repr(line.strip()))

print("\nPDF verification finished.")
