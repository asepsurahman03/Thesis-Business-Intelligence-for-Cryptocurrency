"""
Verifikasi semua file HTML terkait (BI Dashboard + Draft Tesis)
vs nilai final dari IEEE Manuscript dan Notebook
"""
import re
import os

BASE = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'

# File-file yang diperiksa
FILES = {
    'BI Dashboard Prototype':    os.path.join(BASE, 'BI_Dashboard_Prototype.html'),
    'BI Framework Dashboard':    os.path.join(BASE, 'BI_Framework_Dashboard.html'),
    'BI Dashboard index':        os.path.join(BASE, 'BI_Dashboard', 'index.html'),
    'Draft Tesis Lengkap':       os.path.join(BASE, 'Draft_Tesis_Lengkap.html'),
    'Laporan Tesis Lengkap':     os.path.join(BASE, 'Laporan_Tesis_Lengkap.html'),
    'IEEE FINAL (ID)':           os.path.join(BASE, 'Manuscript_IEEE_FINAL_2026_ID.html'),
}

# Nilai-nilai yang harus ada (sesuai IEEE FINAL + Notebook)
CHECKS = {
    'Periode 2021-2026':     ['2021\u20132026', '2021-2026', '2021 \u2013 2026'],
    'Tidak ada 2021-2025':   ['2021\u20132025', '2021-2025'],   # harus ABSEN
    '43,786 records':        ['43,786'],
    'GRU RMSE 0.1058':       ['0.1058'],
    'LSTM RMSE 0.1145':      ['0.1145'],
    'GRU MAPE 13.13':        ['13.13'],
    'LSTM MAPE 13.96':       ['13.96'],
    'LSTM Training 106.60s': ['106.60', '106.6'],
    'GRU Training 192.19s':  ['192.19', '192.1'],
    'LSTM Sharpe 1.45':      ['1.45'],
    'GRU Sharpe 1.32':       ['1.32'],
    'LSTM Dir.Acc 72.3':     ['72.3'],
    'Informer disebutkan':   ['Informer', 'informer'],
    'XGBoost disebutkan':    ['XGBoost', 'xgboost'],
    'Walk-Forward':          ['Walk-Forward', 'Walk Forward'],
    'Power BI':              ['Power BI'],
    'PostgreSQL':            ['PostgreSQL'],
    'SUS Score 86.4':        ['86.4'],
}

MUST_ABSENT = {'Tidak ada 2021-2025'}

OUT = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\bi_tesis_verify.txt'
lines = []
lines.append('='*72)
lines.append('  VERIFIKASI: BI Dashboard + Draft Tesis vs IEEE FINAL')
lines.append('='*72)

all_issues = {}

for fname, fpath in FILES.items():
    lines.append(f'\n\n{"─"*72}')
    lines.append(f'  FILE: {fname}')
    lines.append(f'  PATH: {os.path.basename(fpath)}')
    lines.append(f'{"─"*72}')

    if not os.path.exists(fpath):
        lines.append('  [FILE TIDAK DITEMUKAN]')
        continue

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    txt = re.sub(r'<[^>]+>', ' ', content)
    txt = ' '.join(txt.split())

    file_issues = []
    for check_name, values in CHECKS.items():
        found = any(v in content or v in txt for v in values)
        if check_name in MUST_ABSENT:
            # Must NOT be found
            if found:
                lines.append(f'  [XX] MASIH ADA: {check_name}')
                file_issues.append(check_name)
            else:
                lines.append(f'  [OK] Tidak ada (benar): {check_name}')
        else:
            if found:
                lines.append(f'  [OK] {check_name}')
            else:
                lines.append(f'  [XX] TIDAK ADA: {check_name}')
                file_issues.append(check_name)

    if file_issues:
        all_issues[fname] = file_issues
    else:
        lines.append('\n  >>> SELARAS SEMPURNA dengan IEEE FINAL <<<')

lines.append('\n\n' + '='*72)
lines.append('  RINGKASAN MASALAH YANG PERLU DIPERBAIKI')
lines.append('='*72)
if not all_issues:
    lines.append('  >>> SEMUA FILE SUDAH SELARAS! <<<')
else:
    for fname, issues in all_issues.items():
        lines.append(f'\n  [{fname}]:')
        for issue in issues:
            lines.append(f'    - {issue}')
lines.append('='*72)

report = '\n'.join(lines)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(report)
print(report)
