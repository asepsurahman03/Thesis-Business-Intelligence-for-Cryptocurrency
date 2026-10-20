import re

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(MANUSCRIPT, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'As shown in Table II,\s*the LSTM achieved', 'As shown in Table III, the LSTM achieved', text, flags=re.IGNORECASE)
text = re.sub(r'Table III provides\s*a direct comparison', 'Table IV provides a direct comparison', text, flags=re.IGNORECASE)

with open(MANUSCRIPT, 'w', encoding='utf-8') as f:
    f.write(text)

print("Selesai")
