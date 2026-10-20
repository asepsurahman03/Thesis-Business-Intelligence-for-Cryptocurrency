import json
import re

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

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
    # For markdown cells without HTML tags:
    (r'\b2\.5\b', '1.45'),
    (r'\b2\.3\b', '1.32')
]

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

changed = False
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        for i, line in enumerate(source):
            new_line = line
            # only replace 2.5 and 2.3 if they are around "Sharpe" to avoid changing section headings
            for old, new in replacements[:10]:
                new_line = re.sub(old, new, new_line)
            
            if 'Sharpe' in new_line or '1.45' in new_line or '1.32' in new_line or 'Ratio' in new_line or '2.5' in new_line or '2.3' in new_line:
                if 'Sharpe' in new_line or '|' in new_line:
                    new_line = re.sub(r'\b2\.5\b', '1.45', new_line)
                    new_line = re.sub(r'\b2\.3\b', '1.32', new_line)

            if new_line != line:
                source[i] = new_line
                changed = True

if changed:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated perfectly.")
else:
    print("No changes made.")
