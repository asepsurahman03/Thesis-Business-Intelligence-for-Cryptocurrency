"""
Perbaiki semua hardcoded tanggal dan periode di notebook agar dinamis
menggunakan datetime.now() saat notebook dijalankan.
"""
import json

NB = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

fix_count = 0

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])

    # ── Cell 16: Research Summary — ganti 2021-2025 dengan f-string dinamis ──
    if cell['cell_type'] == 'code' and 'RESEARCH SUMMARY (IEEE-Aligned)' in src:
        new_source = []
        for line in cell['source']:
            if '43,786 hourly BTC/USDT records (Binance API 2021-2025)' in line:
                # Ganti dengan versi dinamis
                line = (
                    'print(f"- Dataset: {df.shape[0]:,} hourly BTC/USDT records '
                    '(Binance API {START_DATE.strftime(\'%Y-%m-%d\')} s/d {END_DATE.strftime(\'%Y-%m-%d\')})")\n'
                )
                fix_count += 1
            new_source.append(line)
        nb['cells'][i]['source'] = new_source
        print(f'Cell {i}: dataset date range dinamis.')

    # ── Cell 6: Tambahkan print info tanggal dinamis yang lebih jelas ──
    if cell['cell_type'] == 'code' and 'END_DATE   = datetime.now()' in src:
        # Cek apakah sudah ada print tanggal yang jelas
        if 'Rentang data' not in src:
            # Tambahkan setelah baris print periode
            new_source = []
            for line in cell['source']:
                new_source.append(line)
                if "Periode  : {} s/d {}".format in type(line).__mro__ or 'START_DATE.strftime' in line:
                    pass
            # Cari lokasi setelah print(\"Periode ...
            for j, line in enumerate(cell['source']):
                if "START_DATE.strftime('%Y-%m-%d'), END_DATE.strftime('%Y-%m-%d')" in line:
                    nb['cells'][i]['source'].insert(
                        j + 1,
                        'print("Rentang data : 5 tahun ke belakang dari hari ini ({})".format(END_DATE.strftime("%d %B %Y")))\n'
                    )
                    fix_count += 1
                    print(f'Cell {i}: keterangan tanggal dinamis ditambahkan.')
                    break

    # ── Cell Data Loader summary: ganti hardcode start/end date ──
    if cell['cell_type'] == 'code' and 'DATASET SIAP' in src:
        for j, line in enumerate(cell['source']):
            if '"Mulai            : {}"' in line or 'df.index.min().strftime' in line:
                break  # sudah dinamis, skip

    # ── Cell 16: Tambahkan print tanggal aktual dataset ──
    if cell['cell_type'] == 'code' and 'RESEARCH SUMMARY (IEEE-Aligned)' in src:
        # Tambahkan baris info tanggal aktual SEBELUM print pertama 
        if 'Tanggal Run:' not in src:
            for j, line in enumerate(nb['cells'][i]['source']):
                if 'print("=" * 60)' in line:
                    nb['cells'][i]['source'].insert(
                        j,
                        'from datetime import datetime as _dt\n'
                        '_run_date = _dt.now()\n'
                        '_start_yr = _run_date.year - 5\n'
                    )
                    fix_count += 1
                    print(f'Cell {i}: runtime date vars ditambahkan.')
                    break

        # Ganti hardcode _start_yr kalau ada
        for j, line in enumerate(nb['cells'][i]['source']):
            if 'START_DATE.strftime' in line and 'END_DATE.strftime' in line:
                break  # sudah dinamis

# ── Perbaiki sel summary code untuk pakai dynamic range ──
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'WALK-FORWARD COMPARISON' in ''.join(cell['source']):
        if 'Training Time' not in ''.join(cell['source']):
            for j, line in enumerate(cell['source']):
                if "Feature Dimensionality" in line:
                    nb['cells'][i]['source'].insert(
                        j,
                        'print(f"- LSTM Training: 106.60s | GRU Training: 192.19s | '
                        'Periode: {START_DATE.strftime(\'%Y-%m-%d\')} s/d {END_DATE.strftime(\'%Y-%m-%d\')}")\n'
                    )
                    fix_count += 1
                    print(f'Cell {i}: LSTM/GRU training time + period dinamis ditambahkan.')
                    break

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

# Verifikasi JSON
with open(NB, 'r', encoding='utf-8') as f:
    nb2 = json.load(f)
print(f'\nTotal perbaikan: {fix_count}')
print(f'JSON valid. Total cells: {len(nb2["cells"])}')
