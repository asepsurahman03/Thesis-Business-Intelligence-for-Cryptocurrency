import json, ast

NB_PATH = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
OUT     = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\syntax_check_result.txt'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

lines_out = ["=== CEK SYNTAX SEMUA CODE CELLS ===\n"]
all_ok = True

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    if not src.strip():
        continue
    try:
        ast.parse(src)
        lines_out.append(f"Cell {i:2d}: OK\n")
    except SyntaxError as e:
        all_ok = False
        lines_out.append(f"Cell {i:2d}: ERROR baris {e.lineno} - {e.msg}\n")
        lines_txt = src.splitlines()
        for idx in range(max(0, e.lineno-3), min(len(lines_txt), e.lineno+2)):
            marker = " <-- ERROR" if idx == e.lineno-1 else ""
            lines_out.append(f"         {idx+1:3d}: {repr(lines_txt[idx])}{marker}\n")
        lines_out.append("\n")

lines_out.append("\n")
if all_ok:
    lines_out.append("SEMUA CELL SYNTAX OK!\n")
else:
    lines_out.append("ADA ERROR - perlu diperbaiki!\n")

with open(OUT, 'w', encoding='utf-8') as f:
    f.writelines(lines_out)

print(''.join(lines_out))
