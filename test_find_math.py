import os
import win32com.client
import time

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

doc_path = os.path.abspath('05_Reports/test_com_math.docx')
if os.path.exists(doc_path):
    os.remove(doc_path)

doc = word.Documents.Add()
selection = word.Selection
selection.TypeText("Here is an inline equation $x^2 + y^2 = z^2$ and here is a block equation $$\int_{0}^{1} x dx$$ and another one in the table.")

# Add a table
doc.Tables.Add(selection.Range, 2, 2)
table = doc.Tables(1)
table.Cell(1,1).Range.Text = "Testing Table $E=mc^2$"
table.Cell(2,2).Range.Text = "$$A = \pi r^2$$"

doc.SaveAs(doc_path)

def convert_latex_to_omath(doc):
    # Find all $...$ and $$...$$
    # We can use wildcard search in Word: \$*\$ 
    # But wildcard search matches the longest string or shortest?
    # In Word, wildcard \$*\$ is greedy, it might match from the first $ to the last $ in the paragraph.
    # To make it lazy, we can search for \$[!\$]{1,}\$
    
    find = doc.Content.Find
    find.ClearFormatting()
    find.Text = "\$*\$"
    find.MatchWildcards = True
    
    # Let's iterate using execute
    while find.Execute():
        rng = find.Parent
        text = rng.Text
        print("Found:", text)
        
        # Word's Find might be greedy, so we might need a custom approach.
        # Alternatively, using Python to find text in paragraphs and replace them using COM.
        pass

convert_latex_to_omath(doc)

doc.Close()
word.Quit()
