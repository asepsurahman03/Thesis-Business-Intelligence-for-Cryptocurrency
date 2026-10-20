import os
import re
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    
    # We will explicitly add page numbers using standard Paged.js @page blocks
    # We need to ensure @page isn't duplicated incorrectly.
    css = re.sub(r'@page\s*{[^}]*}', '', css)
    
    css += """
        /* Paged.js Page numbering and A4 setup */
        @page {
            size: A4;
            margin-top: 40mm;
            margin-bottom: 30mm;
            margin-left: 40mm;
            margin-right: 30mm;
            @bottom-center {
                content: counter(page);
                font-family: "Times New Roman", Times, serif;
                font-size: 12pt;
                padding-top: 10px;
            }
        }
        
        /* Remove page number from the first page (cover) */
        @page:first {
            @bottom-center {
                content: none;
            }
            margin-top: 30mm;
        }
        
        /* Global typography */
        body { 
            background-color: #e0e0e0; /* light gray background to contrast white A4 pages on screen */
            font-family: "Times New Roman", Times, serif; 
            font-size: 12pt; 
            line-height: 1.5; 
            margin: 0; 
            text-align: justify;
        }

        .pagedjs_pages {
            margin-bottom: 40px;
        }

        .pagedjs_page {
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.2) !important;
            margin: 20px auto !important;
        }

        p { text-indent: 1.25cm; margin: 0 0 10px 0; }
        
        /* Fix Table and Images alignment */
        table { margin: 15px auto; width: 90%; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 6px; text-align: center; }
        .figure { text-align: center; margin: 20px 0; }
        .figure img { max-width: 100%; height: auto; display: block; margin: 0 auto; box-shadow: none; border: 1px solid #ccc; padding: 5px; }
        .figure-caption { text-align: center; font-size: 10pt; margin-top: 5px; font-style: italic; }
        
        .equation { text-align: center; margin: 20px 0; font-style: italic; }
    """
    style_tag.string = css

# Clean up any leftover duplicate Paged.js scripts if they ran previously
scripts = soup.find_all('script')
pjs_count = 0
for s in scripts:
    if s.get('src') and 'paged.polyfill.js' in s.get('src'):
        pjs_count += 1
        if pjs_count > 1:
            s.decompose()

# Tidy up DOM (just checking if any H1 needs centering)
for h1 in soup.find_all('h1'):
    if 'text-align' not in str(h1.get('style', '')):
        h1['style'] = h1.get('style', '') + '; text-align: center;'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
