import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Show ALL code cells fully
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', []))
        print("=" * 70)
        print("CELL %d (code)" % (i+1))
        print("=" * 70)
        print(src)
        print()
