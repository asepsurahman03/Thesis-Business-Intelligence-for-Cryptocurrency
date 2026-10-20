import os
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time

file_in = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_ID.html'

with open(file_in, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

translator = GoogleTranslator(source='en', target='id')

# Safe single tag translation
def translate_html(html_str):
    if len(html_str) < 10: return html_str
    try:
        # Since large chunks might break, we translate raw
        res = translator.translate(html_str)
        return res
    except:
        return html_str

tags_to_translate = ['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'th']
div_classes_to_translate = ['title', 'abstract-section', 'figure-caption']

translate_mode = True

for tag in soup.find_all(True):
    # Stop translating entirely once we reach References
    if tag.name == 'h1' and 'References' in tag.text:
        translate_mode = False
        continue
        
    if not translate_mode:
        continue

    # Skip specific elements
    if tag.name == 'div' and tag.get('class'):
        classes = tag['class']
        if 'authors' in classes or 'affiliation' in classes or 'page-number' in classes:
            continue

    # Identify if tag is translatable
    is_translatable = False
    if tag.name in tags_to_translate:
        is_translatable = True
    elif tag.name == 'div' and tag.get('class') and any(c in tag['class'] for c in div_classes_to_translate):
        is_translatable = True

    if is_translatable:
        if tag.find('img'):
            continue
        html_raw = tag.decode_contents().strip()
        if not html_raw:
            continue
            
        trans_res = translate_html(html_raw)
        
        # apply translation carefully
        try:
            new_content = BeautifulSoup(trans_res, 'html.parser')
            tag.clear()
            for c in new_content.contents:
                tag.append(c)
        except: pass
        
        time.sleep(0.3)

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Fixed translation applied.")
