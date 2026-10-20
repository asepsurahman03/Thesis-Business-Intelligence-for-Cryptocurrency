import docx

doc = docx.Document('Revisi 4 A_Deep_Learning_Architecture_for_Cryptocurrency_Price_Forecasting.docx')
with open('all_paragraphs_map.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs):
        blips = p._p.xpath('.//a:blip')
        blip_info = f" [IMAGE: {len(blips)}]" if blips else ""
        f.write(f"[{i:03d}] {p.style.name:16s}{blip_info} | {p.text}\n")

print("Mapped all paragraphs to all_paragraphs_map.txt")
