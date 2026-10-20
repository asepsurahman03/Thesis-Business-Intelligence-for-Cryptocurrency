import os
import win32com.client
import shutil

v9_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V5.docx')
v10_path = os.path.abspath('05_Reports/Manuscript_IJAI_FINAL_V10.docx')

shutil.copy(v9_path, v10_path)

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc = word.Documents.Open(v10_path)

# IJAI formatting for tables
try:
    for i in range(1, doc.Tables.Count + 1):
        table = doc.Tables(i)
        
        # 1. Ensure table is centered horizontally on the page
        table.Rows.Alignment = 1 # wdAlignRowCenter
        
        # 2. Make table fit the page width optimally
        table.AutoFitBehavior(2) # wdAutoFitWindow
        
        # 3. Standardize font inside table
        table.Range.Font.Name = "Times New Roman"
        
        # In academic papers, table font is usually slightly smaller than body text, 
        # or exactly 10pt if body is 10pt. Let's use 9pt for tables to ensure fit, or 10pt.
        # IJAI uses 10pt body, so 9pt for tables is a safe, clean standard.
        table.Range.Font.Size = 9
        
        # 4. Center text vertically and horizontally in cells
        for row in table.Rows:
            for cell in row.Cells:
                cell.VerticalAlignment = 1 # wdCellAlignVerticalCenter
                # Don't overwrite horizontal alignment if they already designed it nicely,
                # but making everything left or center is common. 
                # We will leave paragraph alignment as is, just fix borders.
        
        # 5. Fix Borders (Standard academic style: top and bottom borders only)
        # Actually, let's just make sure all borders are visible or match standard if they were messy.
        # It's safer to just set the AutoFormat or leave borders alone.
        table.Borders.Enable = True
        
    print(f"Successfully processed {doc.Tables.Count} tables.")
except Exception as e:
    print(f"Error processing tables: {e}")

doc.Save()
doc.Close()
word.Quit()
