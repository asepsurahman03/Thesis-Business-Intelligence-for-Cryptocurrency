import json

NB_PATH = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'BINANCE_ENDPOINTS' in src:
            if 'data-api.binance.vision' not in src:
                new_src = src.replace(
                    "BINANCE_ENDPOINTS = [",
                    "BINANCE_ENDPOINTS = [\n    'https://data-api.binance.vision',"
                )
                nb['cells'][i]['source'] = new_src.splitlines(True)
                print(f"Updated cell {i} with data-api.binance.vision endpoint.")
            else:
                print(f"Cell {i} already has data-api.binance.vision endpoint.")

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
