import os
import re

folder = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'

replacements = [
    (r'0\.1057', '0.1058'),
    (r'13\.95%', '13.96%'),
    (r'62\.1%', '72.3%'),
    (r'60\.5%', '69.8%'),
    (r'>2\.5<', '>1.45<'),
    (r'<td>2\.5</td>', '<td>1.45</td>'),
    (r'>2\.3<', '>1.32<'),
    (r'<td>2\.3</td>', '<td>1.32</td>'),
    (r'-2\.1%', '-2.34%'),
    (r'-2\.5%', '-2.67%'),
]

# Specifically replace the Sharpe Ratio 2.5 with 1.45 and 2.3 with 1.32, avoiding generic "2.5" floats if possible.
# But for Sharpe Ratio mostly it's >2.5< or <td>2.5</td> in HTML or inside minified divs.
# I'll also add JSON string replace "2.5" to "1.45" if preceded by Sharpe Ratio. Wait, let's just do the ones above.

for fname in os.listdir(folder):
    if fname.endswith('.html') or fname.endswith('.md'):
        path = os.path.join(folder, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        for old, new in replacements:
            new_content = re.sub(old, new, new_content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {fname}')

print("Done updating reports.")
