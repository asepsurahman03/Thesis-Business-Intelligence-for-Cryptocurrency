import os
import win32com.client

input_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V5.docx')

bracket_formulas = {
    r"[±]": r"\pm",
}

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
        rng.Text = clean_text
        doc_com.OMaths.Add(rng)
        for i in range(1, rng.OMaths.Count + 1):
            rng.OMaths(i).BuildUp()
            
        find = doc_com.Content.Find
        find.ClearFormatting()
        find.Text = search_text
        find.Forward = True
        find.Wrap = 1

doc_com.Save()
doc_com.Close()
word.Quit()
print("Finished converting [±] formulas natively using Word COM.")
