import win32com.client
import os

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V10.docx')
doc = word.Documents.Open(doc_path)

try:
    for i in range(1, doc.Tables.Count + 1):
        table = doc.Tables(i)
        print(f"\n--- Table {i} ---")
        row_text = []
        try:
            for cell in table.Rows(1).Cells:
                # Remove the weird end-of-cell markers
                text = cell.Range.Text.replace('\r', '').replace('\x07', '').strip()
                row_text.append(text)
            print("Row 1:", " | ".join(row_text))
            
            # Print paragraph immediately before the table
            rng = table.Range
            rng.Collapse(Direction=1) # wdCollapseStart
            rng.MoveStart(Unit=4, Count=-1) # Move to previous paragraph
            print("Text before:", rng.Text.strip())
        except Exception as e:
            print("Error reading table content:", e)
except Exception as e:
    print("Error:", e)
finally:
    doc.Close()
    word.Quit()
