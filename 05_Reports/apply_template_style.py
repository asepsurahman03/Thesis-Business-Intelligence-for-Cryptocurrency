import os
from bs4 import BeautifulSoup
import re

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Change BAB headers from "BAB X <br> TITLE" to "BAB X TITLE" to match the template exactly
for h1 in soup.find_all('h1', class_='bab-header'):
    # check for br
    for br in h1.find_all('br'):
        br.replace_with(' ')

# Check global line spacing and justification just in case
style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    if 'text-align: justify;' not in css:
        css = css.replace('body {', 'body { text-align: justify;')
    style_tag.string = css

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
