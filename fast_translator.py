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

tags_to_translate = ['p', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'th']
div_classes = ['title', 'authors', 'affiliation', 'abstract-section', 'figure-caption']

targets = []

for tag in soup.find_all(True):
    if tag.name in tags_to_translate or (tag.name == 'div' and tag.get('class') and any(c in tag['class'] for c in div_classes)):
        if tag.find('img'):
            continue
        if tag.text.startswith('[1]') or tag.text.startswith('[2]') or tag.text.startswith('[3]'):
            if re.match(r'^\[\d+\]\s+[A-Z\.]+', tag.text.strip()):
                continue 
        if tag.name == 'td' or tag.name == 'th':
            clean_str = re.sub(r'[\d\.\%\-\±\s]', '', tag.text.strip())
            if len(clean_str) == 0:
                continue
        html_str = tag.decode_contents().strip()
        if not html_str:
            continue
        targets.append(tag)

print(f"Total elements to translate: {len(targets)}")

# Batch process by 3000 chars
batch_str = []
batch_tags = []

for tag in targets:
    html_raw = tag.decode_contents().strip()
    # remove newlines to allow our delimiter " ¦ " to work cleanly
    html_raw = html_raw.replace(' \xA6 ', ' ').replace('\n', ' ')
    
    batch_str.append(html_raw)
    batch_tags.append(tag)
    
    # if total len reaches ~3000, trigger translation
    current_join = " \xA6 ".join(batch_str)
    if len(current_join) > 3000:
        try:
            res = translator.translate(current_join)
            res_split = res.split(' \xA6 ')
            # Fallback if split count doesn't match
            if len(res_split) == len(batch_tags):
                for i, r in enumerate(res_split):
                    try:
                        new_content = BeautifulSoup(r, 'html.parser')
                        batch_tags[i].clear()
                        for c in new_content.contents:
                            batch_tags[i].append(c)
                    except: pass
            else:
                print("Split length mismatch. Falling back to individual for this batch.")
                for t, h in zip(batch_tags, batch_str):
                    try:
                        tr = translator.translate(h)
                        nt = BeautifulSoup(tr, 'html.parser')
                        t.clear()
                        for c in nt.contents:
                            t.append(c)
                    except: pass
            print(f"Translated batch of {len(batch_tags)}")
            batch_str = []
            batch_tags = []
        except Exception as e:
            print("Batch error:", e)

# Final batch
if batch_str:
    current_join = " \xA6 ".join(batch_str)
    try:
        res = translator.translate(current_join)
        res_split = res.split(' \xA6 ')
        if len(res_split) == len(batch_tags):
            for i, r in enumerate(res_split):
                try:
                    new_content = BeautifulSoup(r, 'html.parser')
                    batch_tags[i].clear()
                    for c in new_content.contents:
                        batch_tags[i].append(c)
                except: pass
        else:
            for t, h in zip(batch_tags, batch_str):
                try:
                    tr = translator.translate(h)
                    nt = BeautifulSoup(tr, 'html.parser')
                    t.clear()
                    for c in nt.contents:
                        t.append(c)
                except: pass
        print(f"Translated final batch of {len(batch_tags)}")
    except Exception as e:
        print("Final batch error:", e)

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Done!")
