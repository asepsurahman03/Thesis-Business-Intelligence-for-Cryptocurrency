import os, re, time
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

file_in = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_ID.html'

with open(file_in, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

translator = GoogleTranslator(source='en', target='id')

def translate_html(html_str):
    if len(html_str) < 2: return html_str
    try:
        res = translator.translate(html_str)
        return res
    except:
        return html_str

tags_to_trans = ['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'th']
div_classes = ['title', 'abstract-section', 'figure-caption']

translate_mode = True
count = 0

for tag in soup.find_all(True):
    if tag.name == 'h1' and 'References' in tag.text:
       translate_mode = False
       tag.string = 'Referensi'
       continue
       
    if not translate_mode: continue

    is_translatable = False
    if tag.name in tags_to_trans:
        is_translatable = True
        
    if tag.name == 'div' and tag.get('class') and any(c in tag['class'] for c in div_classes):
        is_translatable = True
        
    if is_translatable:
        if tag.find('img'): continue
        if tag.name == 'td' or tag.name == 'th':
            clean = re.sub(r'[\d\.\%\-\±\s]', '', tag.text.strip())
            if len(clean) == 0: continue
            
        html_raw = tag.decode_contents().strip()
        if not html_raw: continue
        
        trans_res = translate_html(html_raw)
        
        try:
            nc = BeautifulSoup(trans_res, 'html.parser')
            tag.clear()
            for c in nc.contents: tag.append(c)
        except: pass
        count += 1
        time.sleep(0.3)

print('Translated', count)
with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))
