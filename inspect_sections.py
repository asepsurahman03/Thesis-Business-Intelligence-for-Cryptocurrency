import docx

doc = docx.Document('Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx')
print('Sections count:', len(doc.sections))
for i, s in enumerate(doc.sections):
    cols = s._sectPr.xpath('.//w:cols/@w:num')
    print(f'Section {i}: top={s.top_margin.pt}pt, bot={s.bottom_margin.pt}pt, left={s.left_margin.pt}pt, right={s.right_margin.pt}pt, cols={cols}')

for p_idx, p in enumerate(doc.paragraphs[:15]):
    print(f"P[{p_idx}] (style: {p.style.name}): {p.text[:60]}")
