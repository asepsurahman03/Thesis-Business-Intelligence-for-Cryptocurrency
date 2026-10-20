import json

nb = json.load(open("02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb", encoding="utf-8"))

# Cari dan tampilkan semua code cells dengan detail
print("Detail semua code cells:")
print("="*60)

for i, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") != "code":
        continue
    src = cell.get("source", [])
    if not src:
        continue
    
    full_code = "".join(src)
    
    try:
        compile(full_code, f"cell_{i+1}", "exec")
        status = "OK"
    except SyntaxError as e:
        status = f"ERROR: {e}"
    
    print(f"\nCell {i+1}: {status}")
    print(f"  Baris kode pertama: {repr(full_code[:80])}")
