import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

v6_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V6.docx')
doc = word.Documents.Open(v6_path)

# Ensure track changes is off so ranges don't mess up
doc.TrackRevisions = False

# We will iterate finding all occurrences
word.Selection.HomeKey(Unit=6) # wdStory = 6
find = word.Selection.Find
find.ClearFormatting()
find.Text = "#MATH#*#/MATH#"
find.MatchWildcards = True
find.Wrap = 0 # wdFindStop

while find.Execute():
    rng = word.Selection.Range
    text = rng.Text
    # Remove markers
    math_text = text[6:-7]
    rng.Text = math_text
    
    # Selection should now wrap the replaced text
    # Convert to OMath
    doc.OMaths.Add(rng)
    
    # We must collapse the selection to the end so the next search starts after this math
    word.Selection.Collapse(Direction=0)

# Finally build up all equations
for i in range(1, doc.OMaths.Count + 1):
    doc.OMaths(i).BuildUp()

doc.Save()
doc.Close()
word.Quit()
print("All math formulas converted to OMML.")
