import os
import win32com.client
import latex2mathml.converter
from lxml import etree

xslt_path = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
xslt = etree.parse(xslt_path)
transform = etree.XSLT(xslt)

def latex_to_omml_xml(latex_str):
    try:
        mathml_str = latex2mathml.converter.convert(latex_str)
        dom = etree.fromstring(mathml_str)
        new_dom = transform(dom)
        
        # We need to wrap it in proper WordprocessingML for InsertXML
        # InsertXML expects a valid WordprocessingML document.
        # But maybe we can just insert the m:oMath element if we wrap it properly.
        # Let's see what InsertXML expects.
        word_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <w:wordDocument xmlns:w="http://schemas.microsoft.com/office/word/2003/wordml" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
          <w:body>
            <w:p>
              {etree.tostring(new_dom, encoding='unicode')}
            </w:p>
          </w:body>
        </w:wordDocument>
        """
        return word_xml
    except Exception as e:
        print(f"Error: {e}")
        return None

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

doc_path = os.path.abspath('05_Reports/test_insert_xml.docx')
if os.path.exists(doc_path):
    os.remove(doc_path)

doc = word.Documents.Add()
selection = word.Selection
selection.TypeText("Here is an equation: ")

xml = latex_to_omml_xml(r"d_t = L(e_{1t}) - L(e_{2t})")
if xml:
    selection.InsertXML(xml)

selection.TypeText(" and it continues.")

doc.SaveAs(doc_path)
doc.Close()
word.Quit()
print("Done testing InsertXML.")
