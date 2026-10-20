import os
from bs4 import BeautifulSoup
import re

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Update CSS
style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    # Remove CSS counter for bab
    css = re.sub(r'h1::before\s*{[^}]+}', '', css)
    css = re.sub(r'counter-reset:\s*bab\s*;', '', css)
    # Add page styling
    css += """
        h1.bab-header { font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; margin-top: 0px; margin-bottom: 30px; line-height: 1.5; }
        .page { margin-left: auto; margin-right: auto; }
        @media print {
            @page { size: A4; margin: 0; }
            body { background-color: white; }
            .page { width: 100%; min-height: auto; box-shadow: none; margin: 0; padding: 40mm 30mm 30mm 40mm; page-break-after: always; }
        }
    """
    style_tag.string = css

# Map roman numerals
romans = ["I", "II", "III", "IV", "V", "VI", "VII"]

# Find all H1s in the document.
h1s = soup.find_all('h1')

bab_idx = 0
for h1 in h1s:
    text = h1.get_text(separator=" ").strip().lower()
    # Skip front matter
    if any(x in text for x in ['orisin', 'pengesahan', 'pengantar', 'abstrak', 'abstract', 'daftar isi', 'lampiran']):
        # If it doesn't have the class yet
        h1['class'] = h1.get('class', []) + ['bab-header']
        continue
        
    # We are at a thesis bab
    h1['class'] = h1.get('class', []) + ['bab-header']
    
    if text == "pendahuluan" or text == "tinjauan pustaka" or text == "metodologi penelitian" or text == "hasil dan pembahasan" or text == "kesimpulan dan saran":
        # Make the content BAB X <br> TITLE
        title_text = h1.get_text(separator=" ").strip()
        if "BAB" not in title_text.upper():
            h1.clear()
            h1.append(BeautifulSoup(f"BAB {romans[bab_idx]}<br>{title_text.upper()}", 'html.parser'))
            bab_idx += 1
    elif text == "daftar pustaka":
        if "DAFTAR" not in h1.get_text():
            h1.clear()
            h1.append(BeautifulSoup(f"DAFTAR PUSTAKA", 'html.parser'))


# Now, split the mega page.
# Find the page containing PENDAHULUAN
# It's usually inside <div class="page-content"> which is inside <div class="page">
for page in soup.find_all('div', class_='page'):
    h1_inside = page.find('h1')
    if h1_inside and 'BAB I' in h1_inside.text:
        # This is the main page containing all chapters!
        # We need to split it by BAB.
        # But wait, children might be inside page-content
        content_container = page.find('div', class_='page-content')
        if not content_container:
            content_container = page
            
        elements = list(content_container.contents)
        
        current_page = page
        current_container = content_container
        
        for elem in elements:
            if elem.name == 'h1' and ('BAB ' in elem.text or 'DAFTAR PUSTAKA' in elem.text):
                if elem != h1_inside:
                    # Create a new page
                    new_page = soup.new_tag('div', attrs={'class': 'page'})
                    new_content = soup.new_tag('div', attrs={'class': 'page-content'}) if page.find('div', class_='page-content') else new_page
                    if page.find('div', class_='page-content'):
                        new_page.append(new_content)
                    
                    current_page.insert_after(new_page)
                    current_page = new_page
                    current_container = new_content
            
            # extract elem and append to current container
            elem.extract()
            current_container.append(elem)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
