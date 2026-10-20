import os
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
import re

file_in = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
file_out = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026_ID.html'

with open(file_in, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

translator = GoogleTranslator(source='en', target='id')

# We only want to translate specific tags that contain text
tags_to_translate = ['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'th']
div_classes = ['title', 'authors', 'affiliation', 'abstract-section', 'figure-caption']

count = 0
for tag in soup.find_all(True):
    # Only target specific tags
    if tag.name in tags_to_translate or (tag.name == 'div' and tag.get('class') and any(c in tag['class'] for c in div_classes)):
        
        # Avoid translating base64 images that might somehow be inside
        if tag.find('img'):
            continue
        
        # Avoid references maybe? No, references [25] are ok to vaguely translate, but maybe better to keep original? Let's translate everything to Indonesian.
        # Actually translating references can break formatting. Let's skip references.
        if tag.text.startswith('[1]') or tag.text.startswith('[2]') or tag.text.startswith('[3]'):
            if re.match(r'^\[\d+\]\s+[A-Z\.]+', tag.text.strip()):
                continue # Skip references list
                
        # Skip purely numeric/symbols inside td
        if tag.name == 'td' or tag.name == 'th':
            # if cell is just numbers, %, -, +
            clean_str = re.sub(r'[\d\.\%\-\±\s]', '', tag.text.strip())
            if len(clean_str) == 0:
                continue
                
        # Don't translate empty elements
        html_str = tag.decode_contents().strip()
        if not html_str:
            continue
            
        try:
            # We must break it into smaller chunks if > 5000 chars, but p tags are rarely > 5000
            if len(html_str) < 4900:
                trans = translator.translate(html_str)
                # Parse translated HTML back into soup and replace contents
                new_tag_content = BeautifulSoup(trans, 'html.parser')
                tag.clear()
                for c in new_tag_content.contents:
                    tag.append(c)
                count += 1
                time.sleep(0.3)
        except Exception as e:
            print(f"Failed to translate: {html_str[:30]} Error: {e}")

print(f"Translated {count} elements.")

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Translation complete and saved to:", file_out)
