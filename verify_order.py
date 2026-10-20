import json

NB = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'class InformerTransformer' in src and 'models_to_train' in src:
            idx_class  = src.index('class InformerTransformer')
            idx_dict   = src.index('models_to_train')
            print(f'Cell {i}: InformerTransformer class defined at char {idx_class}')
            print(f'Cell {i}: models_to_train used at char {idx_dict}')
            if idx_class < idx_dict:
                print('  ✅ ORDER OK — class defined BEFORE usage')
            else:
                print('  ❌ ORDER WRONG — class defined AFTER usage')
            break
