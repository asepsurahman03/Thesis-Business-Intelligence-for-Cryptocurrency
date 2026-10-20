import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

doc_path = os.path.abspath('05_Reports/test_eq_number.docx')
if os.path.exists(doc_path):
    os.remove(doc_path)

doc = word.Documents.Add()
selection = word.Selection

latex_str = r"X_{norm} = (X - X_{min})/(X_{max} - X_{min})#(1)"
selection.TypeText(latex_str)

start = selection.Start - len(latex_str)
end = selection.Start
rng = doc.Range(start, end)

doc.OMaths.Add(rng)
omath = doc.OMaths(doc.OMaths.Count)
omath.BuildUp()

doc.SaveAs(doc_path)
doc.Close()
word.Quit()
print("Saved to test_eq_number.docx")
