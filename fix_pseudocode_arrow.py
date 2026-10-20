import re

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace $leftarrow$ with actual HTML arrow &larr;
html = html.replace('$\leftarrow$', '&larr;')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Pseudocode repaired: $\leftarrow$ changed to HTML entity &larr;")
