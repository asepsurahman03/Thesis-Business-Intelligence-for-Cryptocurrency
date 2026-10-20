import json

nb = json.load(open("02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb", encoding="utf-8"))

print("Cek semua code cells untuk syntax errors:")
print("="*60)

errors = []
for i, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") != "code":
        continue
    src = cell.get("source", [])
    if not src:
        continue
    
    # Gabungkan source
    full_code = "".join(src)
    
    # Cek syntax
    try:
        compile(full_code, f"cell_{i+1}", "exec")
        print(f"Cell {i+1:2d}: OK ({len(src)} baris)")
    except SyntaxError as e:
        print(f"Cell {i+1:2d}: ERROR - {e}")
        errors.append((i+1, e, full_code[:200]))

print()
if errors:
    print(f"DITEMUKAN {len(errors)} ERROR:")
    for cell_num, err, preview in errors:
        print(f"\n  Cell {cell_num}: {err}")
        print(f"  Kode awal: {repr(preview[:100])}")
else:
    print("SEMUA CELLS OK - Tidak ada syntax error!")
