import docx
from lxml import etree
import latex2mathml.converter
import copy

doc_path = '05_Reports/Manuscript_IJAI_FINAL_V5.docx'
doc = docx.Document(doc_path)

nsmap = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
         'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

xslt_path = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
xslt = etree.parse(xslt_path)
transform = etree.XSLT(xslt)

def latex_to_omml(latex_str):
    latex_str = latex_str.replace(r'\text{Attention}', r'\mathrm{Attention}')
    latex_str = latex_str.replace(r'\text{Softmax}', r'\mathrm{Softmax}')
    latex_str = latex_str.strip()
    try:
        mathml_str = latex2mathml.converter.convert(latex_str)
        dom = etree.fromstring(mathml_str)
        new_dom = transform(dom)
        return new_dom.getroot()
    except Exception as e:
        print(f"Error converting: {latex_str} -> {e}")
        return None

latex_formulas = [
    r"O(L \log L)", # 0
    r"p < 0.05", # 1
    r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}", # 2
    r"MACD = EMA_{12} - EMA_{26}", # 3
    r"\sigma_t", # 4
    r"\sigma_t = \sqrt{\frac{1}{n} \sum_{i=0}^{n-1} (P_{t-i} - \bar{P})^2}", # 5
    r"f_t", # 6
    r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)", # 7
    r"z_t", # 8
    r"z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)", # 9
    r"O(L \log L)", # 10
    r"\mathrm{Attention}(Q, K, V) = \mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V", # 11
    r"\bar{Q}", # 12
    r"\pm", # 13
    r"\pm", # 14
    r"H", # 15
    r"p < 0.001", # 16
    r"d_t = L(e_{1t}) - L(e_{2t})", # 17
    r"DM = \frac{\bar{d}}{\sqrt{V_d / T}}", # 18
    r"\pm", # 19
    r"\pm", # 20
    r"\pm", # 21
    r"\pm", # 22
    r"\pm", # 23
    r"\pm", # 24
    r"\pm", # 25
    r"\pm", # 26
    r"\pm", # 27
    r"\pm", # 28
    r"\sigma", # 29
    r"\sigma", # 30
    r"\pm", # 31
    r"\pm", # 32
    r"\pm", # 33
    r"\pm", # 34
    r"\pm", # 35
    r"\pm", # 36
    r"\pm", # 37
    r"\pm", # 38
    r"\pm", # 39
    r"\pm", # 40
    r"\pm", # 41
    r"\pm", # 42
    r"\pm", # 43
    r"\pm", # 44
    r"\pm", # 45
    r"\pm", # 46
    r"p < 0.001", # 47
    r"p = 0.014", # 48
    r"3\sigma", # 49
]

maths = doc.element.xpath('//m:oMath')
print(f"Found {len(maths)} math elements.")

if len(maths) == len(latex_formulas):
    for i, m in enumerate(maths):
        new_omml = latex_to_omml(latex_formulas[i])
        if new_omml is not None:
            # The new_omml is a new m:oMath element.
            # We want to replace m with new_omml.
            parent = m.getparent()
            parent.replace(m, new_omml)
    
    doc.save(doc_path)
    print("Successfully replaced all math elements with perfectly formatted OMML.")
else:
    print(f"Mismatch: found {len(maths)} math elements but have {len(latex_formulas)} formulas.")
