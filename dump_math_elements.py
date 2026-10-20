import docx
from lxml import etree
import latex2mathml.converter

doc_path = '05_Reports/Manuscript_IJAI_FINAL_V5.docx'
doc = docx.Document(doc_path)

nsmap = {'m': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
         'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

maths = doc.element.xpath('//m:oMath')
print(f"Found {len(maths)} math elements.")

with open('05_Reports/math_elements_dump.txt', 'w', encoding='utf-8') as f:
    for i, m in enumerate(maths):
        text = "".join(m.xpath('.//m:t/text()', namespaces=nsmap))
        f.write(f"Math {i}: {text}\n")
