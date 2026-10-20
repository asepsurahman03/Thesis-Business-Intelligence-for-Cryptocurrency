import win32com.client
import os

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V10.docx')
doc = word.Documents.Open(doc_path)

for i in range(1, doc.Tables.Count + 1):
    table = doc.Tables(i)
    print(f"\n--- Table {i} ---")
    row_text = []
    try:
        for cell in table.Rows(1).Cells:
            text = cell.Range.Text.replace('\r', '').replace('\x07', '').strip()
            row_text.append(text)
        print("Row 1:", " | ".join(row_text))
        
        row_text2 = []
        for cell in table.Rows(2).Cells:
            text = cell.Range.Text.replace('\r', '').replace('\x07', '').strip()
            row_text2.append(text)
        print("Row 2:", " | ".join(row_text2))
    except Exception as e:
        print("Error reading table content:", e)

doc.Close()
word.Quit()
