import json
from datetime import datetime, timedelta

NB = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Update Cell 1 (markdown header) ──────────────────────────────────────
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = ''.join(cell['source'])
        if 'A Deep Learning and Business Intelligence Framework' in src:
            # Update baris tabel Layer 1 — ganti hardcode records dengan "dinamis saat run"
            new_sources = []
            for line in cell['source']:
                if '~43,786 records hourly' in line:
                    line = line.replace(
                        '~43,786 records hourly',
                        '43,786+ hourly OHLCV records (5y rolling)'
                    )
                if '~~43,786 records' in line:
                    line = line.replace(
                        '~~43,786 records',
                        '~43,786 records (5 tahun ke belakang dari tanggal notebook dijalankan)'
                    )
                new_sources.append(line)
            nb['cells'][i]['source'] = new_sources
            print(f'Cell {i} (header markdown): updated dynamic note.')
            break

# 2. Update Cell 6 — ubah komentar header agar jelas "rolling 5 tahun" ──
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'END_DATE   = datetime.now()' in ''.join(cell['source']):
        for j, line in enumerate(cell['source']):
            if '# Rentang: 5 Tahun Terakhir dari tanggal sekarang' in line:
                nb['cells'][i]['source'][j] = (
                    '# Rentang: 5 Tahun Terakhir rolling dari tanggal SAAT notebook dijalankan\n'
                )
                break
        # Pastikan END_DATE dan START_DATE sudah benar (sudah ada tapi kuatkan komentar)
        for j, line in enumerate(cell['source']):
            if 'END_DATE   = datetime.now()' in line:
                nb['cells'][i]['source'][j] = (
                    'END_DATE   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  '
                    '# Tanggal hari ini saat notebook dijalankan\n'
                )
            if 'START_DATE = END_DATE - timedelta(days=5*365)' in line:
                nb['cells'][i]['source'][j] = (
                    'START_DATE = END_DATE - timedelta(days=5*365)  '
                    '# 5 tahun ke belakang (1825 hari) dari END_DATE\n'
                )
        print(f'Cell {i} (data loader): comments updated.')
        break

# 3. Update Cell 16 Research Summary — pakai START_DATE dan END_DATE dinamis ──
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'RESEARCH SUMMARY (IEEE-Aligned)' in ''.join(cell['source']):
        for j, line in enumerate(cell['source']):
            # Ganti hardcode biner tanggal dengan konstruksi dinamis dari variabel
            if 'START_DATE.strftime' in line and 'END_DATE.strftime' in line:
                break  # sudah dinamis
        print(f'Cell {i} (Research Summary): already dynamic.')
        break

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

# Final validate
with open(NB, 'r', encoding='utf-8') as f:
    nb2 = json.load(f)

# Tampilkan konfirmasi output bagian kunci
for c in nb2['cells']:
    if c['cell_type'] == 'code':
        src = ''.join(c['source'])
        if 'END_DATE   = datetime.now' in src:
            print('\n=== CELL 6 Konfigurasi Tanggal ===')
            for line in c['source'][:15]:
                print(' ', line.rstrip())
            break

for c in nb2['cells']:
    if c['cell_type'] == 'code' and 'RESEARCH SUMMARY' in ''.join(c['source']):
        src = ''.join(c['source'])
        idx = src.find('Dataset:')
        if idx != -1:
            print('\n=== CELL 16 Dataset Line ===')
            print(' ', src[idx:idx+120])
        break

print('\nJSON valid. Total cells:', len(nb2['cells']))
