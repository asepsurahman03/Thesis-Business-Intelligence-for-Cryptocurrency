import os
from bs4 import BeautifulSoup
import re

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# We inject Paged.js into head to automatically handle perfect A4 pagination!
head_tag = soup.find('head')
if head_tag:
    # check if pagedjs already there
    if not soup.find('script', src=lambda x: x and 'paged.polyfill.js' in x):
        paged_script = soup.new_tag('script', src="https://unpkg.com/pagedjs/dist/paged.polyfill.js")
        head_tag.append(paged_script)

style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    # Strip out all our previous .page or @page or counter stuff
    css = re.sub(r'h[123]::before\s*{[^}]+}', '', css)
    css = re.sub(r'counter-reset:[^;]+;', '', css)
    css = re.sub(r'\.page\s*{[^}]+}', '', css)
    css = re.sub(r'@media\s*print\s*{[^}]+}', '', css)
    
    # Add new css specifically for paged.js
    css += """
        /* Paged.js specific styling for A4 thesis */
        @page {
            size: A4;
            margin-top: 40mm;
            margin-bottom: 30mm;
            margin-left: 40mm;
            margin-right: 30mm;
        }
        
        body { 
            background-color: #525659; 
            font-family: "Times New Roman", Times, serif; 
            font-size: 12pt; 
            line-height: 1.5; 
            margin: 0; 
            text-align: justify;
        }

        .pagedjs_pages {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
        }

        .pagedjs_page {
            background-color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }

        /* Thesis specific typography */
        h1.bab-header { font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; margin-top: 0px; margin-bottom: 30px; line-height: 1.5; page-break-before: always; }
        
        h1.front-matter-title {
            page-break-before: always;
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
            margin-top: 0px;
            margin-bottom: 30px;
            line-height: 1.5;
        }
        
        h2 { font-size: 12pt; font-weight: bold; text-align: left; margin-top: 20px; margin-bottom: 10px; }
        h3 { font-size: 11pt; font-weight: bold; text-align: left; margin-top: 15px; margin-bottom: 5px; }

        .cover-page { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; height: 100%;}
        .cover-type { font-size: 14pt; font-weight: bold; text-transform: uppercase; margin-top: 2in; margin-bottom: 50px; }
        .cover-title { font-size: 14pt; font-weight: bold; text-transform: uppercase; margin-bottom: 80px; line-height: 1.5; }
        .cover-author { font-size: 12pt; font-weight: normal; margin-bottom: 50px; }
        .cover-author strong { font-weight: bold; text-transform: uppercase; }
        .cover-img { margin-bottom: 80px; }
        .cover-inst { font-size: 14pt; font-weight: bold; text-transform: uppercase; position: absolute; bottom: 0; line-height: 1.5; width: 100%; text-align: center; }
    """
    style_tag.string = css

# Remove all <div class="page"> completely, replacing them with their contents
# since Paged.js handles physical pagination automatically.
for page_div in soup.find_all('div', class_='page'):
    page_div.unwrap() # Removes the <div class="page"> but keeps the content
    
for pcontent_div in soup.find_all('div', class_='page-content'):
    pcontent_div.unwrap() # Discard content wrappers

# Re-number logic.
# First, remove any hardcoded numbers or 'BAB' strings from previous runs so we don't duplicate
bab_counter = 0
subbab_counter = 0
subsubbab_counter = 0

# We process h1, h2, h3 sequentially.
for tag in soup.find_all(['h1', 'h2', 'h3']):
    orig_text = tag.get_text(separator=" ").strip()
    
    # Check if it's a front-matter H1
    if tag.name == 'h1':
        if any(x in orig_text.lower() for x in ['orisin', 'pengesahan', 'pengantar', 'abstrak', 'abstract', 'daftar isi', 'lampiran', 'daftar pustaka', 'referensi']):
            tag['class'] = tag.get('class', []) + ['front-matter-title']
            # Clean up the text if it has BAB I etc (it shouldn't, but just in case)
            clean_text = re.sub(r'^BAB\s+[IVX]+[\s\n]*', '', orig_text, flags=re.IGNORECASE)
            tag.string = clean_text
            continue
            
        # It's a BAB
        bab_counter += 1
        subbab_counter = 0
        subsubbab_counter = 0
        
        # Clean current BAB text
        clean_text = re.sub(r'^BAB\s+[IVX]+\s*', '', orig_text, flags=re.IGNORECASE)
        # We want: BAB X <br> TITLE
        romans = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
        bab_roman = romans[bab_counter] if bab_counter < len(romans) else str(bab_counter)
        
        tag.clear()
        tag.append(BeautifulSoup(f"BAB {bab_roman}<br>{clean_text}", 'html.parser'))
        tag['class'] = tag.get('class', []) + ['bab-header']
        
    elif tag.name == 'h2':
        # Ensure it's inside thesis body (bab_counter > 0)
        # Some h2 might be in Lampiran A... ignore those.
        if bab_counter > 0 and not 'Lampiran' in orig_text:
            subbab_counter += 1
            subsubbab_counter = 0
            # Strip out any old numbering like "1.1 " or "A. "
            clean_text = re.sub(r'^(\d+\.\d+\s+|[A-Z]\.\s+)', '', orig_text)
            tag.string = f"{bab_counter}.{subbab_counter} {clean_text}"
            
    elif tag.name == 'h3':
        if bab_counter > 0 and not 'Lampiran' in orig_text:
            subsubbab_counter += 1
            clean_text = re.sub(r'^(\d+\.\d+\.\d+\s+|[A-Z]\.\s+)', '', orig_text)
            tag.string = f"{bab_counter}.{subbab_counter}.{subsubbab_counter} {clean_text}"


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
