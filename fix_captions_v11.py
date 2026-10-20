import os
import win32com.client
import shutil

v10_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V10.docx')
v11_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V11.docx')
shutil.copy(v10_path, v11_path)

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc = word.Documents.Open(v11_path)

captions = [
    "Table 1. Quantitative Loss Benchmarking Across Algorithmic Walk-Forward Layers",
    "Table 2. KPI Dashboard (Sharpe, VaR, Dir. Acc.)",
    "Table 3. Comparative Benchmarking Against Published Literature"
]

try:
    for i in range(1, 4):
        table = doc.Tables(i)
        
        # 1. Clean the first cell
        cell = table.Cell(1, 1)
        raw_text = cell.Range.Text.replace('\x07', '')
        parts = raw_text.split('\r')
        
        # The last non-empty part is the actual header text
        # Sometimes there's a trailing empty string due to split('\r') ending with '\r'
        real_parts = [p.strip() for p in parts if p.strip()]
        header_text = real_parts[-1] if real_parts else ""
        
        # Replace cell content with ONLY the header
        cell.Range.Text = header_text
        
        # 2. Insert caption OUTSIDE the table
        # We get the range of the table, collapse to start
        rng = table.Range
        rng.Collapse(Direction=1) # wdCollapseStart
        
        # Move up to escape the table. 
        # Actually, wdCollapseStart on a table might still be inside the first cell.
        # To go before the table, we move the range start backward by 1 character
        rng.MoveStart(Unit=1, Count=-1) # wdCharacter
        rng.Collapse(Direction=1)
        
        # Insert text and paragraph mark
        rng.InsertAfter(captions[i-1] + "\n")
        
        # Get the paragraph we just inserted and format it
        # Since we inserted it, rng now covers the text? No, InsertAfter expands it.
        # Let's re-collapse and adjust
        p_rng = doc.Range(rng.Start, rng.Start + len(captions[i-1]))
        p_rng.Font.Name = "Times New Roman"
        p_rng.Font.Size = 10
        p_rng.ParagraphFormat.Alignment = 1 # Center
        p_rng.ParagraphFormat.SpaceAfter = 6 # Small gap before table
        
except Exception as e:
    print(f"Error: {e}")

doc.Save()
doc.Close()
word.Quit()
print("Captions extracted and tables cleaned!")
