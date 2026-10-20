import json

NB_PATH = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell2 = nb['cells'][2]
src = ''.join(cell2['source'])

out_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\cell2_lines.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    for i, line in enumerate(src.splitlines(), 1):
        f.write(f"{i:3d}: {repr(line)}\n")

print("Saved to cell2_lines.txt")
print(f"Total lines: {len(src.splitlines())}")
