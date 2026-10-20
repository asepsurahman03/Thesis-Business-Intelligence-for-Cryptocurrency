import docx
import re
import os
import win32com.client

input_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V5.docx')

# 1. Extract all formulas using python-docx
doc = docx.Document(input_path)
full_text = []
for p in doc.paragraphs:
    full_text.append(p.text)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                full_text.append(p.text)

combined_text = '\n'.join(full_text)
# Find \(...\) and \[...\] and \begin{equation}...\end{equation}
pattern = re.compile(r'(\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{equation\}.*?\\end\{equation\})', re.DOTALL)
formulas = list(set(pattern.findall(combined_text)))

print(f"Found {len(formulas)} unique formulas.")
for f in formulas:
    print(" -", f.replace('\n', ' ')[:50])

# 2. Use win32com to find and convert them
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

doc_com = word.Documents.Open(input_path)

for formula in formulas:
    find = doc_com.Content.Find
    find.ClearFormatting()
    
    search_text = formula
    if len(search_text) > 255:
        # We can't use Find for >255 chars. We'll skip for now or we could use wildcard.
        print(f"Formula too long for Word Find (max 255 chars): {search_text[:30]}...")
        continue
        
    find.Text = search_text.replace('\n', '^p')
    find.Forward = True
    find.Wrap = 1 # wdFindContinue
    find.Format = False
    find.MatchCase = True
    find.MatchWholeWord = False
    find.MatchWildcards = False

    while find.Execute():
        rng = find.Parent
        
        # Clean the delimiters for OMML BuildUp
        is_block = False
        clean_text = formula
        if formula.startswith('\\('):
            clean_text = formula[2:-2].strip()
        elif formula.startswith('\\['):
            clean_text = formula[2:-2].strip()
            is_block = True
        elif formula.startswith('\\begin{equation}'):
            clean_text = formula[16:-14].strip()
            is_block = True
            
        rng.Text = clean_text
        
        # Now rng points to the cleaned text
        doc_com.OMaths.Add(rng)
        
        for i in range(1, rng.OMaths.Count + 1):
            rng.OMaths(i).BuildUp()
            
        # Also let's set alignment if it was a block equation
        if is_block:
            pass # Usually handled by paragraph alignment
            
        # Reset the Find range to the whole document after the current position
        find = doc_com.Content.Find
        find.ClearFormatting()
        find.Text = search_text.replace('\n', '^p')
        find.Forward = True
        find.Wrap = 1

doc_com.Save()
doc_com.Close()
word.Quit()
print("Finished converting formulas natively using Word COM.")
