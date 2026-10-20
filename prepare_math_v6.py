import docx
import re
import shutil
from docx.enum.text import WD_ALIGN_PARAGRAPH

v4_path = '05_Reports/Manuscript_IJAI_FINAL_V4.docx'
v6_path = '05_Reports/Manuscript_IJAI_FINAL_V6.docx'

shutil.copy(v4_path, v6_path)
doc = docx.Document(v6_path)

inline_replacements = [
    (r'\\\(O\(L \\log L\)\\\)', r'#MATH#O(L \\log L)#/MATH#'),
    (r'\[p < 0\.05\]', r'#MATH#p < 0.05#/MATH#'),
    (r'\[\\sigma_t\]', r'#MATH#\\sigma_t#/MATH#'),
    (r'\[f_t\]', r'#MATH#f_t#/MATH#'),
    (r'\[z_t\]', r'#MATH#z_t#/MATH#'),
    (r'\\\(d_t = L\(e_\{1t\}\) - L\(e_\{2t\}\)\\\)', r'#MATH#d_t = L(e_{1t}) - L(e_{2t})#/MATH#'),
    (r'\[p < 0\.001\]', r'#MATH#p < 0.001#/MATH#'),
    (r'\[H\]', r'#MATH#H#/MATH#'),
    (r'\+3\[\\sigma\]', r'+3#MATH#\\sigma#/MATH#'),
    (r'\[\\sigma\]', r'#MATH#\\sigma#/MATH#'),
    (r'\\\(\\sigma\\\)', r'#MATH#\\sigma#/MATH#'),
    (r'\\\[\\bar\{Q\}\\\]', r'#MATH#\\bar{Q}#/MATH#'), # \[\bar{Q}\]
    (r'\[\\bar\{Q\}\]', r'#MATH#\\bar{Q}#/MATH#')
]

block_replacements = [
    (r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}", r"#MATH#X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}#/MATH#"),
    (r"MACD = EMA_{12}(P) - EMA_{26}(P)", r"#MATH#MACD = EMA_{12}(P) - EMA_{26}(P)#/MATH#"),
    (r"\sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2}", r"#MATH#\sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2}#/MATH#"),
    (r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)", r"#MATH#f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)#/MATH#"),
    (r"z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)", r"#MATH#z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)#/MATH#"),
    (r"Attention(Q, K, V) = Softmax\left(\frac{\bar{Q} K^T}{\sqrt{d}}\right) V", r"#MATH#Attention(Q, K, V) = Softmax\left(\frac{\bar{Q} K^T}{\sqrt{d}}\right) V#/MATH#"),
    (r"DM = \frac{\bar{d}}{\sqrt{\hat{V}_{\bar{d}}/T}}", r"#MATH#DM = \frac{\bar{d}}{\sqrt{\hat{V}_{\bar{d}}/T}}#/MATH#")
]

for p in doc.paragraphs:
    text = p.text
    original_text = text
    
    # 1. Block Equations
    is_block = False
    for pat, rep in block_replacements:
        if pat in text:
            text = rep
            is_block = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            break
            
    # 2. Inline Equations
    if not is_block:
        for pat, rep in inline_replacements:
            text = re.sub(pat, rep, text)
            
    if text != original_text:
        # Re-write paragraph keeping same formatting roughly
        # Since it's plain text replacement, we will just replace the text
        # and set font to Times New Roman.
        p.text = text
        for run in p.runs:
            run.font.name = 'Times New Roman'

doc.save(v6_path)
print("Saved to V6 with math markers.")
