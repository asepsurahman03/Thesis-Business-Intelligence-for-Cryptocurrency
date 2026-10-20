import os, re

base = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin'
files_to_check = []
for f in os.listdir(base):
    if f.endswith('.py'):
        files_to_check.append(os.path.join(base, f))

print('=== CEK TANGGAL DI FILE PYTHON ROOT ===')

for fpath in files_to_check:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    found_dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
    found_period = re.findall(r'period=["\'][^\'"]+["\']', content)
    found_yf_period = re.findall(r'period\s*=\s*["\'][^\'"]+["\']', content)

    if found_dates or found_period or found_yf_period:
        print()
        print('File: ' + fname)
        if found_dates:
            print('  Tanggal hardcoded: ' + str(set(found_dates)))
        if found_period or found_yf_period:
            print('  Period params: ' + str(set(found_period + found_yf_period)))
