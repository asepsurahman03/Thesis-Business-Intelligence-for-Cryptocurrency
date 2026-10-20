import json

nb = json.load(open("02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb", encoding="utf-8"))

cell = nb["cells"][2]
src = cell["source"]
full_code = "".join(src)
lines = full_code.split("\n")

with open("cell3_dump.txt", "w", encoding="utf-8") as f:
    for i, line in enumerate(lines, start=1):
        f.write(f"{i:3d}: {repr(line)}\n")

print(f"Ditulis ke cell3_dump.txt - {len(lines)} baris")
