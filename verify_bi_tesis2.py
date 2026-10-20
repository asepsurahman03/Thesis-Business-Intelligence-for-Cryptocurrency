"""
Verifikasi yang toleran terhadap format Indonesia (koma untuk desimal, titik untuk ribuan)
"""
import re
import os

BASE = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'

FILES = {
    'BI Dashboard Prototype':    os.path.join(BASE, 'BI_Dashboard_Prototype.html'),
    'BI Framework Dashboard':    os.path.join(BASE, 'BI_Framework_Dashboard.html'),
    'BI Dashboard index':        os.path.join(BASE, 'BI_Dashboard', 'index.html'),
    'Draft Tesis Lengkap':       os.path.join(BASE, 'Draft_Tesis_Lengkap.html'),
    'Laporan Tesis Lengkap':     os.path.join(BASE, 'Laporan_Tesis_Lengkap.html'),
    'IEEE FINAL (ID)':           os.path.join(BASE, 'Manuscript_IEEE_FINAL_2026_ID.html'),
}

# Values account for both EN (0.1058) and ID (0,1058) formats
CHECKS = {
    'Periode 2021-2026':     ['2021\u20132026', '2021-2026', '2021 \u2013 2026'],
    'Tidak ada 2021-2025':   ['2021\u20132025', '2021-2025'],   # MUST ABSENT
    '43,786 records':        ['43,786', '43.786'],
    'GRU RMSE 0.1058':       ['0.1058', '0,1058'],
    'LSTM RMSE 0.1145':      ['0.1145', '0,1145'],
    'GRU MAPE 13.13':        ['13.13', '13,13'],
    'LSTM MAPE 13.96':       ['13.96', '13,96'],
    'LSTM Training 106.60s': ['106.60', '106.6', '106,6', '106.60s', '106,60'],
    'GRU Training 192.19s':  ['192.19', '192.1', '192,19', '192,2'],
    'LSTM Sharpe 1.45':      ['1.45', '1,45'],
    'GRU Sharpe 1.32':       ['1.32', '1,32'],
    'LSTM Dir.Acc 72.3':     ['72.3', '72,3'],
    'Informer disebutkan':   ['Informer', 'informer'],
    'XGBoost disebutkan':    ['XGBoost', 'xgboost'],
    'Walk-Forward':          ['Walk-Forward', 'Walk Forward'],
    'Power BI':              ['Power BI'],
    'PostgreSQL':            ['PostgreSQL'],
    'SUS Score 86.4':        ['86.4', '86,4'],
}

MUST_ABSENT = {'Tidak ada 2021-2025'}

OUT = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\bi_tesis_verify2.txt'
lines = []

all_issues = {}

for fname, fpath in FILES.items():
    if not os.path.exists(fpath): continue

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    txt = re.sub(r'<[^>]+>', ' ', content)
    txt = ' '.join(txt.split())

    file_issues = []
    for check_name, values in CHECKS.items():
        found = any(v in content or v in txt for v in values)
        if check_name in MUST_ABSENT:
            if found: file_issues.append(check_name)
        else:
            if not found: file_issues.append(check_name)

    if file_issues:
        all_issues[fname] = file_issues

lines.append('RINGKASAN MASALAH (Toleran Format ID)\n' + '='*50)
for fname, issues in all_issues.items():
    lines.append(f'[{fname}]')
    for issue in issues:
        lines.append(f'  - {issue}')
    lines.append('')

if not all_issues:
    lines.append("SEMUA FILE SELARAS DENGAN IEEE FINAL!")

report = '\n'.join(lines)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(report)
print(report)
