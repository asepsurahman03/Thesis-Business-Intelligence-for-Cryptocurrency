import json

nb_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 2 is at index 2
# Let's fix the specific print statement across lines 54 and 55 (0-indexed)
source = nb['cells'][2]['source']

# Find the line that starts with "print('" and doesn't close it properly
for i, line in enumerate(source):
    if line == "print('\n":
        print(f"Found broken print at index {i}")
        # Fix it by adding the next line and removing the newline split
        if i + 1 < len(source):
            next_line = source[i+1]
            fixed_line = "print('\\n" + next_line.replace("\n", "") + "\\n')\n"
            source[i] = fixed_line
            source.pop(i+1)
            print(f"Fixed line: {fixed_line}")
            break
            
# Let's do a more robust string replace just in case it's different
# Let's rebuild the source string and parse it back to array if needed, but array is fine if we just want to replace exactly.
source_str = "".join(nb['cells'][2]['source'])
if "print('\nSemua library berhasil di-import!')" in source_str:
    source_str = source_str.replace(
        "print('\nSemua library berhasil di-import!')", 
        "print('\\nSemua library berhasil di-import!')"
    )
    # Split back into lines with \n attached
    # Doing this might mess up line endings slightly, but let's do it carefully
    lines = [line + '\n' for line in source_str.split('\n')]
    if lines[-1] == '\n':
        lines.pop() # Remove extra empty line at the end if there was no trailing newline
    
    # Actually, the simplest fix is just patching the source list:
    new_source = []
    for line in nb['cells'][2]['source']:
        if line == "print('\n":
            new_source.append("print('\\n")
        elif line == "Semua library berhasil di-import!')":
            # merge with previous or just fix the quote
            pass # wait, it's easier to just do text replacement on the whole cell

source_text = "".join(nb['cells'][2]['source'])
fixed_source_text = source_text.replace("print('\nSemua", "print('\\nSemua")

# Convert back to list of lines preserving newlines
def string_to_lines(text):
    result = []
    start = 0
    while start < len(text):
        pos = text.find('\n', start)
        if pos == -1:
            result.append(text[start:])
            break
        else:
            result.append(text[start:pos+1])
            start = pos + 1
    return result

nb['cells'][2]['source'] = string_to_lines(fixed_source_text)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook cell 2 patched.")
