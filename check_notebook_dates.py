import json
from datetime import datetime, timedelta

nb_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f'Total cells: {len(nb["cells"])}')
print()

# Tampilkan semua cell code dengan nomor dan preview
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        preview = src[:300].replace('\n', ' | ')
        print(f'Cell {i}: {preview}')
        print()

# Cek apakah ada referensi Binance API
print('\n=== CEK REFERENSI BINANCE API ===')
binance_cells = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'binance' in src.lower() or 'ccxt' in src.lower() or 'kline' in src.lower():
            print(f'Cell {i}: DITEMUKAN referensi Binance')
            binance_cells.append(i)

if not binance_cells:
    print('TIDAK ADA referensi Binance API langsung di notebook')
    print('Data diambil dari CSV file yang sudah ada.')

# Cek tanggal di data CSV
print('\n=== CEK RENTANG DATA CSV ===')
import pandas as pd
import os

data_dir = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\01_Data'
end_date = datetime.now()
start_5y = end_date - timedelta(days=5*365)
print(f'Sekarang: {end_date.strftime("%Y-%m-%d")}')
print(f'5 tahun lalu: {start_5y.strftime("%Y-%m-%d")}')
print()

for fname in os.listdir(data_dir):
    if fname.endswith('.csv'):
        fpath = os.path.join(data_dir, fname)
        df = pd.read_csv(fpath)
        print(f'File: {fname}')
        print(f'  Shape: {df.shape}')
        
        # Coba temukan kolom tanggal
        date_col = None
        for col in df.columns:
            if any(k in col.lower() for k in ['date', 'time', 'timestamp', 'price']):
                date_col = col
                break
        
        if date_col:
            try:
                dates = pd.to_datetime(df[date_col])
                print(f'  Kolom tanggal: [{date_col}]')
                print(f'  Mulai: {dates.min()}')
                print(f'  Akhir: {dates.max()}')
                
                coverage_ok = str(dates.min())[:10] <= start_5y.strftime('%Y-%m-%d') or \
                             (dates.max() - dates.min()).days >= 365*5 - 10
                print(f'  Cakupan 5 tahun: {"OK" if coverage_ok else "KURANG"}')
            except Exception as e:
                print(f'  Error parsing tanggal: {e}')
        else:
            print(f'  Kolom tersedia: {list(df.columns)}')
        print()
