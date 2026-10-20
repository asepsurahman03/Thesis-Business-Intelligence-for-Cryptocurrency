import docx
import os
import win32com.client

input_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V5.docx')

# 1. Define the bracketed formulas to replace
bracket_formulas = {
    r"[\sigma_t]": r"\sigma_t",
    r"[f_t]": r"f_t",
    r"[z_t]": r"z_t",
    r"[\bar{Q}]": r"\bar{Q}",
    r"[\sigma]": r"\sigma",
    r"[3\sigma]": r"3\sigma",
    r"[p < 0.001]": r"p < 0.001",
    r"[p = 0.014]": r"p = 0.014",
    r"[H]": r"H",
    r"[p < 0.05]": r"p < 0.05",
}

# 2. Use win32com to find and convert them
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

doc_com = word.Documents.Open(input_path)

for search_text, clean_text in bracket_formulas.items():
    find = doc_com.Content.Find
    find.ClearFormatting()
    
    find.Text = search_text
    find.Forward = True
    find.Wrap = 1 # wdFindContinue
    find.Format = False
    find.MatchCase = True
    find.MatchWholeWord = False
    find.MatchWildcards = False

    while find.Execute():
        rng = find.Parent
        
        # Replace the bracket text with the clean LaTeX string
        rng.Text = clean_text
        
        # Now rng points to the cleaned text, add OMML
        doc_com.OMaths.Add(rng)
        
        for i in range(1, rng.OMaths.Count + 1):
            rng.OMaths(i).BuildUp()
            
        # Reset the Find range to the whole document after the current position
        find = doc_com.Content.Find
        find.ClearFormatting()
        find.Text = search_text
        find.Forward = True
        find.Wrap = 1

doc_com.Save()
doc_com.Close()
word.Quit()
print("Finished converting bracketed formulas natively using Word COM.")
