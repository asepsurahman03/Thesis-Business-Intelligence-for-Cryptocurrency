"""
Update Manuscript_IEEE_FINAL_2026.html:
Sesuaikan semua referensi tanggal/periode dengan range dinamis notebook:
  START: 23 Maret 2021  (5 tahun ke belakang dari 23 Maret 2026)
  END:   23 Maret 2026  (hari ini saat notebook dijalankan)
"""
from datetime import datetime, timedelta

# Hitung tanggal dinamis sesuai notebook
END_DATE   = datetime(2026, 3, 23)   # tanggal hari ini
START_DATE = END_DATE - timedelta(days=5*365)   # 23 Mar 2021

start_str    = START_DATE.strftime('%Y-%m-%d')       # 2021-03-23
end_str      = END_DATE.strftime('%Y-%m-%d')         # 2026-03-23
start_year   = str(START_DATE.year)                  # 2021
end_year     = str(END_DATE.year)                    # 2026
start_mmyyyy = START_DATE.strftime('%b %Y')          # Mar 2021
end_mmyyyy   = END_DATE.strftime('%b %Y')            # Mar 2026
start_full   = START_DATE.strftime('%B %d, %Y')      # March 23, 2021 -- but we keep Jan 1 for research clarity
end_full     = END_DATE.strftime('%B %d, %Y')        # March 23, 2026

HTML = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'

with open(HTML, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original = content

replacements = [
    # Abstract: periode utama
    ('BTC/USDT records from the Binance API (2021\u20132025)',
     f'BTC/USDT records from the Binance API ({start_year}\u2013{end_year})'),

    # Dataset section: period description
    ('temporal coverage spans January 1, 2021, to December 31, 2025',
     f'temporal coverage spans {start_full}, to {end_full}'),

    # Figure 1 caption
    ('Fig. 1. Hourly closing prices and trading volume of Bitcoin between Jan 2021 and Dec 2025',
     f'Fig. 1. Hourly closing prices and trading volume of Bitcoin between {start_mmyyyy} and {end_mmyyyy}'),

    # Inline references in text
    ('Jan 2021 and Dec 2025',
     f'{start_mmyyyy} and {end_mmyyyy}'),

    # Related work comparison period
    ('2023\u20132025 employing PatchTST',
     '2023\u20132026 employing PatchTST'),

    # Any remaining "2021–2025" year-range in context of this study
    ('(2021\u20132025)',
     f'({start_year}\u2013{end_year})'),

    # "Jan 2021" / "Dec 2025" standalone refs
    ('Jan 2021',  start_mmyyyy.replace('Mar', 'Mar')),
    ('Dec 2025',  end_mmyyyy),
]

changed = []
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        changed.append(f'  [REPLACED] "{old[:60]}" -> "{new[:60]}"')
    else:
        changed.append(f'  [NOT FOUND] "{old[:60]}"')

if content != original:
    with open(HTML, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'File updated: Manuscript_IEEE_FINAL_2026.html')
else:
    print('No changes made.')

print('\nDetail perubahan:')
for c in changed:
    print(c)
