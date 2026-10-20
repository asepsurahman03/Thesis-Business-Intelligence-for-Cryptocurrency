import json

nb_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Tampilkan semua cell secara detail
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        print(f'======= Cell {i} (code) =======')
        print(src)
        print()
    else:
        src = ''.join(cell['source'])
        print(f'======= Cell {i} (markdown) =======')
        print(src[:100])
        print()
