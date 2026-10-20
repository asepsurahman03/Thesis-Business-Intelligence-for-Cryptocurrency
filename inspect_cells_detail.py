import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('nb_cells_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

cells = text.split('============================== CELL ')
for cell_num in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
    for c in cells[1:]:
        lines = c.split('\n')
        if lines[0].startswith(f"{cell_num} "):
            print(f"*** CELL {lines[0]} ***")
            print('\n'.join(lines[1:50]))
            print('='*50)
            break
