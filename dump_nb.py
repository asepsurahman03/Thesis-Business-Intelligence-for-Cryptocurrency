import json

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    cell_type = cell.get('cell_type', 'unknown')
    src = ''.join(cell.get('source', []))
    print("=" * 60)
    print("CELL %d (%s)" % (i+1, cell_type))
    print("=" * 60)
    print(src[:2000])
    
    if cell_type == 'code' and cell.get('outputs'):
        print("--- OUTPUT ---")
        for out in cell['outputs']:
            otype = out.get('output_type', '')
            if otype == 'stream':
                txt = ''.join(out.get('text', []))
                print(txt[:1500])
            elif otype in ('execute_result', 'display_data'):
                data = out.get('data', {})
                if 'text/plain' in data:
                    txt = ''.join(data['text/plain'])
                    print(txt[:1500])
    print()
