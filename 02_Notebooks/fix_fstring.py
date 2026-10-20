"""
Script untuk memperbaiki f-string yang bermasalah di notebook.
Jalankan: python fix_fstring.py
"""

import json
import os

NOTEBOOK_PATH = "Bitcoin_BigData_Analysis_MasterClass.ipynb"

def load_notebook(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notebook(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"✅ Notebook disimpan: {path}")

def fix_fstring_in_cells(nb):
    """Perbaiki f-string yang bermasalah di semua cells."""
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            new_source = []
            changed = False
            for line in source:
                # Fix: print(f'\n{'='*50}') → print('\n' + '='*50)
                if "print(f'\\\\n{'='*50}')" in line:
                    new_line = line.replace("print(f'\\\\n{'='*50}')", "print('\\\\n' + '='*50)")
                    new_source.append(new_line)
                    changed = True
                # Fix: print(f'{'='*50}') → print('='*50)
                elif "print(f'{'='*50}')" in line:
                    new_line = line.replace("print(f'{'='*50}')", "print('='*50)")
                    new_source.append(new_line)
                    changed = True
                else:
                    new_source.append(line)
            if changed:
                nb['cells'][i]['source'] = new_source
                print(f"✅ F-string diperbaiki di cell {i}")
    return nb

def fix_notebook():
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"❌ File tidak ditemukan: {NOTEBOOK_PATH}")
        return

    print(f"📂 Membaca notebook: {NOTEBOOK_PATH}")
    nb = load_notebook(NOTEBOOK_PATH)

    nb = fix_fstring_in_cells(nb)

    save_notebook(nb, NOTEBOOK_PATH)
    print("\n🎉 F-string berhasil diperbaiki!")

if __name__ == "__main__":
    fix_notebook()
