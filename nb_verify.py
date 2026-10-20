import json

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
nb = json.load(open(file_path, encoding='utf-8'))

out = open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\nb_verify.txt', 'w', encoding='utf-8')
for i, cell in enumerate(nb['cells']):
    out.write('=== CELL ' + str(i) + ' (' + cell['cell_type'] + ') ===\n')
    out.write(''.join(cell['source'])[:800])
    out.write('\n\n')
out.close()
print('Done. Total cells: ' + str(len(nb['cells'])))
