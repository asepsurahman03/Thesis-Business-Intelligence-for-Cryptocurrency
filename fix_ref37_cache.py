import re
import os

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# I will systematically force replace all formats of reference 37 just in case it stuck in cache.
new_ref_37 = r'<p>[37] J. Bollen, H. Mao, and X. Zeng, "Twitter mood predicts the stock market," <i>J. Comput. Sci.</i>, vol. 2, no. 1, pp. 1-8, 2011.</p>'

html = re.sub(r'<p>\[37\] J\. Bollen.*?<\/p>', new_ref_37, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Safely replaced reference 37 on the new file name.")
