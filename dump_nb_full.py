import json

with open('02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('nb_cells_dump.txt', 'w', encoding='utf-8') as out:
    for i, cell in enumerate(nb['cells']):
        out.write(f"\n{'='*30} CELL {i} ({cell['cell_type']}) {'='*30}\n")
        out.write(''.join(cell.get('source', [])))
        out.write("\n")

print("Dumped all cells to nb_cells_dump.txt")
