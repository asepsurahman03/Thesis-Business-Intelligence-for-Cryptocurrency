import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V10.docx')
doc = word.Documents.Open(doc_path)

# Fix captions by iterating paragraphs
for i in range(1, doc.Paragraphs.Count + 1):
    p = doc.Paragraphs(i)
    text = p.Range.Text.strip()
    
    if text.startswith("Table I."):
        p.Range.Text = p.Range.Text.replace("Table I.", "Table 1.")
        # Re-apply bolding to "Table 1." if needed or just replace string
    elif text.startswith("Table III."):
        p.Range.Text = p.Range.Text.replace("Table III.", "Table 2.")

# Add caption to Table 3
try:
    if doc.Tables.Count == 3:
        table3 = doc.Tables(3)
        rng = table3.Range
        rng.Collapse(Direction=1) # wdCollapseStart
        # Insert a paragraph before table 3
        rng.InsertParagraphBefore()
        rng = table3.Range
        rng.Collapse(Direction=1)
        rng.MoveStart(Unit=4, Count=-1) # Move to the new empty paragraph
        rng.Text = "Table 3. Comparative Benchmarking Against Published Literature\n"
        rng.ParagraphFormat.Alignment = 1 # Center align caption, standard for IJAI
        # Also let's make sure Table 1 and 2 captions are centered or follow template.
except Exception as e:
    print("Error fixing table 3 caption:", e)

# Final sweep to make sure all table captions are styled nicely (Times New Roman, 10pt)
for i in range(1, doc.Paragraphs.Count + 1):
    p = doc.Paragraphs(i)
    text = p.Range.Text.strip()
    if text.startswith("Table 1.") or text.startswith("Table 2.") or text.startswith("Table 3."):
        p.Range.Font.Name = "Times New Roman"
        p.Range.Font.Size = 10
        p.Format.Alignment = 1 # wdAlignParagraphCenter

doc.Save()
doc.Close()
word.Quit()
print("Table captions fixed!")
