import re

MANUSCRIPT = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html"

with open(MANUSCRIPT, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the current contents:
print("--- Current Titles ---")
for m in re.finditer(r'<div class="table-title">(.*?)</div>', text):
    print(m.group(0))

print("\n--- Current Captions ---")
for m in re.finditer(r'<caption.*?>(.*?)</caption>', text, re.DOTALL):
    print(m.group(0).strip()[:100] + '...')

# We need to replace:
# "Table II. KPI Extraction" to "Table III. KPI Dashboard (Sharpe, VaR, Dir. Acc.)"
# "TABLE III" to "TABLE IV"

text = text.replace('Table II. KPI Extraction: Enterprise Dashboard Parameters', 'Table III. KPI Dashboard (Sharpe, VaR, Dir. Acc.)')
text = text.replace('Table II. KPI Extraction', 'Table III. KPI Dashboard (Sharpe, VaR, Dir. Acc.)')
text = text.replace('TABLE III', 'TABLE IV')
text = text.replace('Table III (KPI Dashboard', 'Table III (KPI Dashboard') # This was added in prev patch, no need to touch

print("\n--- New Titles ---")
for m in re.finditer(r'<div class="table-title">(.*?)</div>', text):
    print(m.group(0))

print("\n--- New Captions ---")
for m in re.finditer(r'<caption.*?>(.*?)</caption>', text, re.DOTALL):
    print(m.group(0).strip()[:100] + '...')

with open(MANUSCRIPT, 'w', encoding='utf-8') as f:
    f.write(text)
