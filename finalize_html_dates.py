"""
Update Manuscript_IEEE_FINAL_2026.html:
Sesuaikan semua referensi tanggal dataset dengan periode aktual notebook:
  START: 23 Maret 2021
  END:   23 Maret 2026
  
Berdasarkan temuan scan raw HTML, strings yang perlu diubah:
1. 'oral coverage spans March 24, 2021, to March 23, 2026'  ← sudah benar (hampir)
2. 'between Mar 2021 and Mar 2026'  ← sudah benar
3. 'Binance API (2021-2026)'  ← sudah benar

Yang masih ada masalah:
- "March 24, 2021" seharusnya "March 23, 2021" (off by 1 day)
- Fig.1 caption bisa lebih presisi
"""

HTML = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'

with open(HTML, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original = content
changed = []

# Perbaiki off-by-one: March 24, 2021 -> March 23, 2021
fixes = [
    ('March 24, 2021',   'March 23, 2021'),
    ('March 24, 2021',   'March 23, 2021'),
    # Pastikan rentang referensi figure konsisten
    ('Jan 2021 and Dec 2026', 'Mar 2021 and Mar 2026'),
    ('Jan 2021 and Dec 2025', 'Mar 2021 and Mar 2026'),
    ('Jan 2021 and Mar 2026', 'Mar 2021 and Mar 2026'),
    # Pastikan abstract konsisten
    ('(2021\u20132025)', '(2021\u20132026)'),
    ('2021\u20132025',   '2021\u20132026'),
    # Timezone note
    ('January 1, 2021',  'March 23, 2021'),
    ('December 31, 2025', 'March 23, 2026'),
    ('December 31, 2026', 'March 23, 2026'),
    # "Studies from 2023-2025"
    ('2023\u20132025 employing PatchTST', '2023\u20132026 employing PatchTST'),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        changed.append(f'[OK] "{old}" -> "{new}"')
    else:
        changed.append(f'[--] Not found: "{old}"')

if content != original:
    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(content)
    print('File HTML berhasil diupdate.\n')
else:
    print('Tidak ada perubahan.\n')

for c in changed:
    print(c)

# Verifikasi hasil
print('\n=== VERIFIKASI AKHIR ===')
import re
txt = re.sub(r'<[^>]+>', ' ', content)
txt = ' '.join(txt.split())

checks = {
    '2021-2026 period': '2021\u20132026' in txt or '2021\u20132026' in content,
    'March 23, 2021': 'March 23, 2021' in content,
    'March 23, 2026': 'March 23, 2026' in content,
    'Mar 2021': 'Mar 2021' in content,
    'Mar 2026': 'Mar 2026' in content,
    '43,786 records': '43,786' in content,
    'NOT 2021-2025': '2021\u20132025' not in content,
    'NOT Dec 2025': 'Dec 2025' not in content,
    'NOT Jan 2021': 'Jan 2021' not in content,
}

for label, ok in checks.items():
    print(f'  {"[OK]" if ok else "[XX]"} {label}')
