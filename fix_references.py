import re

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(MANUSCRIPT, 'r', encoding='utf-8') as f:
    text = f.read()

# Masalah 1: "As shown in Table II, the LSTM achieved superior directional" -> "Table III"
text = re.sub(r'Table II, the LSTM achieved superior directional', 'Table III, the LSTM achieved superior directional', text, flags=re.IGNORECASE)

# Or something more robust if formatting varies:
text = re.sub(r'As shown in Table II(.*?)LSTM achieved superior directional', r'As shown in Table III\1LSTM achieved superior directional', text, flags=re.IGNORECASE|re.DOTALL)

# Masalah 2: "Table III provides a direct comparison" -> "Table IV"
text = re.sub(r'Table III(.*?)provides a direct comparison', r'Table IV\1provides a direct comparison', text, flags=re.IGNORECASE|re.DOTALL)

with open(MANUSCRIPT, 'w', encoding='utf-8') as f:
    f.write(text)

print("Berhasil diperbaiki.")
