import json

nb = json.load(open("02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb", encoding="utf-8"))

errors = []
for i, cell in enumerate(nb["cells"]):
    if cell.get("cell_type") != "code":
        continue
    src = cell.get("source", [])
    if not src:
        continue
    full_code = "".join(src)
    try:
        compile(full_code, f"cell_{i+1}", "exec")
    except SyntaxError as e:
        errors.append((i, e, full_code))

if not errors:
    print("Semua cells OK!")
else:
    for idx, err, code in errors:
        print(f"Cell index {idx} (Cell ke-{idx+1}) ERROR:")
        print(f"  Error: {err}")
        print(f"  Baris error: {err.lineno}")
        lines = code.split("\n")
        # Tampilkan sekitar baris error
        start = max(0, err.lineno - 3)
        end = min(len(lines), err.lineno + 2)
        for ln, line in enumerate(lines[start:end], start=start+1):
            marker = " <-- ERROR" if ln == err.lineno else ""
            print(f"    {ln:3d}: {repr(line)}{marker}")
        print()
