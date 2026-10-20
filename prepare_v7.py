import docx
import re
import shutil
from docx.enum.text import WD_ALIGN_PARAGRAPH

v4_path = '05_Reports/Manuscript_IJAI_FINAL_V4.docx'
v7_path = '05_Reports/Manuscript_IJAI_FINAL_V7.docx'

shutil.copy(v4_path, v7_path)
doc = docx.Document(v7_path)

inline_replacements = [
    (r'\\\(O\(L \\log L\)\\\)', r'$O(L \\log L)$'),
    (r'\[p < 0\.05\]', r'$p < 0.05$'),
    (r'\[p < 0\.001\]', r'$p < 0.001$'),
    (r'\[\\sigma_t\]', r'$\sigma_t$'),
    (r'\[f_t\]', r'$f_t$'),
    (r'\[z_t\]', r'$z_t$'),
    (r'\\\(d_t = L\(e_\{1t\}\) - L\(e_\{2t\}\)\\\)', r'$d_t = L(e_{1t}) - L(e_{2t})$'),
    (r'\[H\]-statistic', r'$H$-statistic'),
    (r'\[H\]', r'$H$'),
    (r'\+3\[\\sigma\]', r'$+3\sigma$'),
    (r'\[\\sigma\]', r'$\sigma$'),
    (r'\\\(\\sigma\\\)', r'$\sigma$'),
    (r'\\\[\\bar\{Q\}\\\]', r'$\bar{Q}$'), 
    (r'\[\\bar\{Q\}\]', r'$\bar{Q}$')
]

block_replacements = [
    (r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}} {(1)}  (1)", 
     r"$$ X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}} $$"),
     
    (r"MACD = EMA_{12}(P) - EMA_{26}(P) {(2)}  (2)", 
     r"$$ MACD = EMA_{12}(P) - EMA_{26}(P) $$"),
     
    (r"\sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2} {(3)}  (3)", 
     r"$$ \sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2} $$"),
     
    (r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) {(4)}  (4)", 
     r"$$ f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) $$"),
     
    (r"z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z) {(5)}  (5)", 
     r"$$ z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z) $$"),
     
    (r"Attention(Q, K, V) = Softmax\left(\frac{\bar{Q} K^T}{\sqrt{d}}\right) V {(6)}  (6)", 
     r"$$ \text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{\bar{Q} K^T}{\sqrt{d}}\right) V $$"),
     
    (r"DM = \frac{\bar{d}}{\sqrt{\hat{V}_{\bar{d}}/T}} {(7)}  (7)", 
     r"$$ DM = \frac{\bar{d}}{\sqrt{\hat{V}_{\bar{d}}/T}} $$")
]

for p in doc.paragraphs:
    text = p.text
    original_text = text
    
    # Block equations
    is_block = False
    for pat, rep in block_replacements:
        if pat in text:
            text = text.replace(pat, rep)
            is_block = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
    # Inline equations
    if not is_block:
        for pat, rep in inline_replacements:
            text = re.sub(pat, lambda m, r=rep: r, text)
            
    if text != original_text:
        p.text = text
        for run in p.runs:
            run.font.name = 'Times New Roman'

doc.save(v7_path)
print("Saved V7 with proper LaTeX formatting.")
