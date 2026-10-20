import os
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

body = soup.find('body')

# Find the H1 for BAB I
bab1_node = None
for h1 in body.find_all('h1'):
    text = h1.get_text().upper()
    if 'BAB I' in text and 'PENDAHULUAN' in text:
        bab1_node = h1
        break

# Delete everything in body before BAB I
if bab1_node:
    # Iterate over body contents
    # We copy them to a list because modifying while iterating is tricky
    elements = list(body.contents)
    for elem in elements:
        if elem == bab1_node:
            break
        # If it's a tag or NavigableString, extract it
        elem.extract()
        
# Find the H1 for LAMPIRAN
lampiran_node = None
for h1 in body.find_all('h1'):
    text = h1.get_text().upper()
    if 'LAMPIRAN' in text:
        lampiran_node = h1
        break

# Delete LAMPIRAN and everything after it
if lampiran_node:
    elements = list(body.contents)
    delete_now = False
    for elem in elements:
        if elem == lampiran_node:
            delete_now = True
        if delete_now:
            elem.extract()

# Check for cover elements that might have survived if they weren't before BAB I (they should be)
for div in body.find_all('div', class_='cover-img'):
    div.decompose()
for div in body.find_all('div', class_='cover-title'):
    div.decompose()
for div in body.find_all('div', class_='cover-author'):
    div.decompose()
    
# Remove front-matter specific CSS rule for first page cover
style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    import re
    # Remove @page:first { ... }
    css = re.sub(r'@page\s*:\s*first\s*{[^}]*}', '', css)
    # Re-insert regular numbering for the first page since it's now BAB I
    style_tag.string = css

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
