import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('nb_cells_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

cells = text.split('============================== CELL ')
for c in cells[1:]:
    lines = c.split('\n')
    header = lines[0]
    print(f"*** CELL {header} ***")
    for line in lines[1:25]:
        print("  ", line)
    print()
