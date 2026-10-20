import json

nb = json.load(open("02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb", encoding="utf-8"))
cell = nb["cells"][6]
src = cell["source"]

print("Tipe:", type(src))
print("Jumlah item:", len(src))
print()
for j in range(min(8, len(src))):
    print(f"[{j}] {repr(src[j])}")

print()
# Cek apakah ada string dengan \\n literal (escape ganda = salah)
bad = [i for i, s in enumerate(src) if "\\\\n" in repr(s) and "\\n" not in s]
if bad:
    print("MASALAH di baris:", bad)
else:
    print("FORMAT OK - Tidak ada literal backslash-n yang salah")
    
# Coba compile kode untuk cek syntax
full_code = "".join(src)
try:
    compile(full_code, "<notebook_cell>", "exec")
    print("SYNTAX CHECK: OK - kode valid Python")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
