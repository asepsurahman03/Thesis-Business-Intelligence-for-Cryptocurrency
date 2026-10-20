import zipfile
import xml.etree.ElementTree as ET

z = zipfile.ZipFile(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\Template\Lampiran 3 - Template Thesis (S-2, Ind) (1).dotx')
xml_content = z.read('word/document.xml')
root = ET.fromstring(xml_content)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

lines = []
for p in root.findall('.//w:p', ns):
    text = ''.join(node.text for node in p.findall('.//w:t', ns))
    if text.strip():
        lines.append(text.strip())

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\Template\template_outline.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
