import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('nb_cells_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

cells = text.split('============================== CELL ')
for c in cells[1:]:
    lines = c.split('\n')
    if lines[0].startswith("12 "):
        print(f"*** CELL {lines[0]} ***")
        for i, line in enumerate(lines[1:]):
            if any(k in line.lower() for k in ['class ', 'def ', 'train', 'epochs', 'lr', 'batch_size', 'hidden', 'layers', 'xgboost', 'informer', 'results']):
                print(f"L{i}: {line[:100]}")
