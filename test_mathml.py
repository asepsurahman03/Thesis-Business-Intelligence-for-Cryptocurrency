import os
import latex2mathml.converter
from lxml import etree
import docx

# 1. Convert LaTeX to MathML
latex_str = r"X_{norm} = \frac{X - X_{min}}{X_{max} - X_{min}}"
mathml_str = latex2mathml.converter.convert(latex_str)
print("MathML:", mathml_str)

# 2. Convert MathML to OMML using MS Word's XSLT
xslt_path = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
if not os.path.exists(xslt_path):
    print("XSLT not found!")
else:
    dom = etree.fromstring(mathml_str)
    xslt = etree.parse(xslt_path)
    transform = etree.XSLT(xslt)
    new_dom = transform(dom)
    omml_str = str(new_dom)
    print("OMML generated.")
    
    # 3. Create a docx and inject OMML
    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(new_dom.getroot())
    
    doc.save('05_Reports/test_omml.docx')
    print("Saved to test_omml.docx")
