import docx

doc = docx.Document('05_Reports/ijai.docx')
section = doc.sections[0]

print("Page Width:", section.page_width.cm)
print("Page Height:", section.page_height.cm)
print("Left Margin:", section.left_margin.cm)
print("Right Margin:", section.right_margin.cm)
print("Top Margin:", section.top_margin.cm)
print("Bottom Margin:", section.bottom_margin.cm)
