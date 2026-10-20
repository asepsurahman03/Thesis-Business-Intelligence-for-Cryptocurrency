import os
file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken LaTeX escape sequences
content = content.replace(chr(9) + 'ext', '\\text')
content = content.replace(chr(12) + 'rac', '\\frac')
content = content.replace(chr(8) + 'ar', '\\bar')
content = content.replace('\night', '\\right')
content = content.replace(chr(13) + 'ight', '\\right')

# Also fix the pseudo class so it strictly stays within one column and wraps if too long
if 'word-wrap: break-word;' not in content:
    content = content.replace('.pseudo {\n', '.pseudo {\n            width: 100%;\n            box-sizing: border-box;\n            overflow-x: hidden;\n            word-wrap: break-word;\n            white-space: normal;\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML Math and CSS fixed successfully.")
