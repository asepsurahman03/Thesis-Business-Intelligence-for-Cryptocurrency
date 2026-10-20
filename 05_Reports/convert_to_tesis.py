import os
import re
from bs4 import BeautifulSoup

file_in = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_ID.html'
file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_in, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find style tag and replace its contents with Thesis styles
style_tag = soup.find('style')
if style_tag:
    style_tag.string = """
        body { background-color: #525659; font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.5; margin: 0; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; counter-reset: bab; }
        .page { background-color: white; width: 210mm; min-height: 297mm; padding: 40mm 30mm 30mm 40mm; box-shadow: 0 5px 15px rgba(0,0,0,0.5); margin-bottom: 40px; position: relative; box-sizing: border-box; text-align: justify; }
        .page-content { column-count: 1; text-align: justify; }
        .page-number { position: absolute; bottom: 15mm; left: 0; right: 0; text-align: center; font-family: "Times New Roman", Times, serif; font-size: 12pt; }
        .cover-page { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }
        .cover-type { font-size: 14pt; font-weight: bold; text-transform: uppercase; margin-top: 1in; margin-bottom: 50px; }
        .cover-title { font-size: 14pt; font-weight: bold; text-transform: uppercase; margin-bottom: 80px; line-height: 1.5; }
        .cover-author { font-size: 12pt; font-weight: normal; margin-bottom: 50px; }
        .cover-author strong { font-weight: bold; text-transform: uppercase; }
        .cover-img { margin-bottom: 80px; }
        .cover-inst { font-size: 14pt; font-weight: bold; text-transform: uppercase; position: absolute; bottom: 30mm; line-height: 1.5; width: calc(100% - 70mm); }
        h1 { font-size: 12pt; font-weight: bold; text-align: center; text-transform: uppercase; margin-top: 30px; margin-bottom: 20px; white-space: pre-wrap; counter-reset: subbab; }
        h1::before { counter-increment: bab; content: "BAB " counter(bab, upper-roman) "\\A "; }
        h2 { font-size: 12pt; font-weight: bold; font-style: normal; text-align: left; margin-top: 20px; margin-bottom: 10px; }
        h2::before { counter-increment: subbab; content: counter(bab) "." counter(subbab) " "; }
        p { text-indent: 1.25cm; margin: 0 0 10px 0; hyphens: auto; }
        ul, ol { margin: 0 0 10px 0.15in; padding-left: 1.25cm; }
        ul li, ol li { margin-bottom: 5px; }
        .figure { text-align: center; margin: 20px 0; break-inside: avoid; }
        .figure img { width: 100%; max-width: 15cm; border: 1px solid #e5e5e5; display: block; margin: 0 auto; }
        .figure-caption { font-size: 10pt; text-align: center; margin-top: 10px; }
        .table-container { margin: 20px 0; text-align: center; break-inside: avoid; }
        .table-title { font-size: 10pt; text-transform: uppercase; margin-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; font-size: 10pt; margin-bottom: 10px; }
        th, td { border-top: 1px solid black; border-bottom: 1px solid black; padding: 8px; text-align: center; }
        .pseudo { width: 100%; box-sizing: border-box; overflow-x: hidden; word-wrap: break-word; white-space: normal; background-color: transparent; border-top: 2px solid black; border-bottom: 2px solid black; padding: 10px 0; font-family: inherit; font-size: 10pt; line-height: 1.5; margin: 20px 0; break-inside: avoid; text-align: left; }
        .pseudo-title { font-variant: small-caps; text-align: left; border-bottom: 1px solid black; padding-bottom: 5px; margin-bottom: 5px; font-weight: bold; }
        .pseudo-content { padding: 0 10px; }
        .equation { margin: 20px 0; font-size: 12pt; text-align: center; break-inside: avoid; }
        .references h1::before { content: none; }
        .references p { text-indent: -1cm; margin-left: 1cm; margin-bottom: 10px; text-align: left; font-size: 10pt; }
        .abstract-section { font-weight: bold; text-align: justify; font-size: 12pt; }
"""

# Extract the header block to convert it into a cover page
header_block = soup.find('div', class_='header-block')
if header_block:
    title_div = header_block.find('div', class_='title')
    title_text = title_div.text if title_div else "KERANGKA PEMBELAJARAN MENDALAM DAN INTELIJEN BISNIS..."
    
    # We create a cover page BEFORE page-1
    cover_page_html = f"""
    <div class="page cover-page">
        <div class="cover-type">TESIS</div>
        <div class="cover-title">{title_text.upper()}</div>
        <div class="cover-img">
            <img src="https://nusaputra.ac.id/wp-content/uploads/2021/08/logo-nusa-putra-200.png" alt="Logo Universitas Nusa Putra" style="width: 150px; height: 150px; object-fit: contain;">
        </div>
        <div class="cover-author">
            Oleh:<br>
            <strong>Asep Surahman Sulaeman</strong>
        </div>
        <div class="cover-inst">
            PROGRAM STUDI MAGISTER INFORMATIKA<br>
            UNIVERSITAS NUSA PUTRA<br>
            SUKABUMI<br>
            2026
        </div>
    </div>
    """
    cover_soup = BeautifulSoup(cover_page_html, 'html.parser')
    
    # Remove the title/authors/affiliation from the header-block
    if title_div: title_div.extract()
    for div in header_block.find_all('div', class_='authors'):
        div.extract()
    for div in header_block.find_all('div', class_='affiliation'):
        div.extract()
        
    soup.body.insert(0, cover_soup)

# Clean up h2 texts (remove "A. ", "B. ", etc)
for h2 in soup.find_all('h2'):
    text = h2.text.strip()
    new_text = re.sub(r'^[A-Z]\.\s+', '', text)
    h2.string = new_text

# Change 'References' h1 so it doesn't get 'BAB'
for h1 in soup.find_all('h1'):
    text = h1.text.lower()
    if 'referensi' in text or 'pustaka' in text or 'daftar' in text:
        # Wrap it in a div or add class
        h1['style'] = "counter-increment: none;"
        # we can't easily disable counter with inline style unless we override 'content'. 
        pass

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))
