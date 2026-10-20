import docx
import os
import shutil
import win32com.client
from docx.enum.text import WD_ALIGN_PARAGRAPH

v4_path = '05_Reports/Manuscript_IJAI_FINAL_V4.docx'
v5_path = '05_Reports/Manuscript_IJAI_FINAL_V5.docx'

shutil.copy(v4_path, v5_path)

# First pass with python-docx
doc = docx.Document(v5_path)

eq_markers = [
    "X_{\\text{norm}}", 
    "MACD = EMA_{12}(P)", 
    "\\sigma_t = \\sqrt{\\frac{1}{n}", 
    "f_t = \\sigma(W_f", 
    "z_t = \\sigma(W_z", 
    "\\text{Attention}(Q, K, V)", 
    "DM = \\frac{\\bar{d}}"
]

replacements = [
    r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}",
    r"MACD = EMA_{12}(P) - EMA_{26}(P)",
    r"\sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2}",
    r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)",
    r"z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)",
    r"Attention(Q, K, V) = Softmax\left(\frac{\bar{Q} K^T}{\sqrt{d}}\right) V",
    r"DM = \frac{\bar{d}}{\sqrt{\hat{V}_{\bar{d}}/T}}"
]

# Clean up equation paragraphs to hold exactly the pure latex string
for p in doc.paragraphs:
    for i, marker in enumerate(eq_markers):
        if marker in p.text:
            p.text = replacements[i]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break

doc.save(v5_path)

# Second pass with COM to build equations
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_abs = os.path.abspath(v5_path)
wdoc = word.Documents.Open(doc_abs)

# Iterate through paragraphs
for i in range(1, wdoc.Paragraphs.Count + 1):
    p = wdoc.Paragraphs(i)
    text = p.Range.Text.strip()
    
    # We identify equation paragraphs if they match our replacements
    # Since Text from COM might have trailing special chars, we check substring
    for rep in replacements:
        if rep in text:
            rng = p.Range
            # Exclude the paragraph mark from selection
            rng.End = rng.End - 1
            
            wdoc.OMaths.Add(rng)
            break

# Build all equations
for i in range(1, wdoc.OMaths.Count + 1):
    omath = wdoc.OMaths(i)
    omath.BuildUp()

wdoc.Save()
wdoc.Close()
word.Quit()

print("Equations rendered to MS Word OMath objects successfully.")
