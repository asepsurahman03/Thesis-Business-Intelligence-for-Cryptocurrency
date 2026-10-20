"""
Script untuk menggabungkan semua data Bitcoin yang ada dan melengkapi dengan yfinance.
Tujuan: Menghasilkan dataset 5 tahun penuh (hourly) dari sekarang ke belakang.
"""
import pandas as pd
import yfinance as yf
import time
import os
from datetime import datetime, timedelta

data_dir = "01_Data"
output_file = os.path.join(data_dir, "btc_5year_hourly_bigdata.csv")

# ====================================================
# LANGKAH 1: Load data yang sudah ada (Binance, 2021-2024)
# ====================================================
print("=" * 60)
print("LANGKAH 1: Memuat data existing dari Binance (2021-2024)")
print("=" * 60)

df_binance = pd.read_csv(os.path.join(data_dir, "btc_5year_hourly_bigdata.csv"))
df_binance['Open_Time'] = pd.to_datetime(df_binance['Open_Time'])
# Hapus timezone info jika ada
df_binance['Open_Time'] = df_binance['Open_Time'].dt.tz_localize(None)
df_binance = df_binance[['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
df_binance = df_binance.sort_values('Open_Time').drop_duplicates('Open_Time')

print(f"Data Binance: {len(df_binance)} baris")
print(f"  Dari: {df_binance['Open_Time'].min()}")
print(f"  Sampai: {df_binance['Open_Time'].max()}")

# ====================================================
# LANGKAH 2: Download data yang hilang (gap) menggunakan yfinance
# ====================================================
print("\n" + "=" * 60)
print("LANGKAH 2: Download data yang belum ada dengan yfinance")
print("=" * 60)

# Target: 5 tahun dari sekarang
end_target = datetime.now().replace(minute=0, second=0, microsecond=0)
start_target = end_target - timedelta(days=5*365)

# Identifikasi gap
existing_end = df_binance['Open_Time'].max()
existing_start = df_binance['Open_Time'].min()

print(f"Target: {start_target.strftime('%Y-%m-%d')} - {end_target.strftime('%Y-%m-%d')}")
print(f"Data ada: {existing_start.strftime('%Y-%m-%d')} - {existing_end.strftime('%Y-%m-%d')}")

gap_parts = []

# Gap di awal (sebelum data Binance ada)
if start_target < existing_start:
    gap_parts.append(("awal", start_target, existing_start))
    print(f"Gap di awal: {start_target.strftime('%Y-%m-%d')} - {existing_start.strftime('%Y-%m-%d')}")

# Gap di akhir (setelah data Binance berakhir)
if existing_end < end_target:
    gap_parts.append(("akhir", existing_end, end_target))
    print(f"Gap di akhir: {existing_end.strftime('%Y-%m-%d')} - {end_target.strftime('%Y-%m-%d')}")

extra_data = []

for gap_name, gap_start, gap_end in gap_parts:
    print(f"\nMengunduh gap '{gap_name}'...")
    
    # yfinance max 729 hari untuk interval 1h
    cur = gap_start
    while cur < gap_end:
        batch_end = min(cur + timedelta(days=729), gap_end)
        
        print(f"  {cur.strftime('%Y-%m-%d')} - {batch_end.strftime('%Y-%m-%d')}", end="")
        
        try:
            df_chunk = yf.download(
                'BTC-USD',
                start=cur.strftime('%Y-%m-%d'),
                end=(batch_end + timedelta(days=1)).strftime('%Y-%m-%d'),
                interval='1h',
                progress=False,
                auto_adjust=True
            )
            
            if not df_chunk.empty:
                # Flatten kolom multi-level jika ada
                if hasattr(df_chunk.columns, 'levels'):
                    df_chunk.columns = [col[0] if isinstance(col, tuple) else col for col in df_chunk.columns]
                
                # Reset index
                df_chunk.index.name = 'Open_Time'
                df_chunk = df_chunk.reset_index()
                
                # Hapus timezone
                df_chunk['Open_Time'] = pd.to_datetime(df_chunk['Open_Time']).dt.tz_localize(None)
                
                # Ambil kolom yang diperlukan
                cols = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                cols_available = [c for c in cols if c in df_chunk.columns]
                df_chunk = df_chunk[cols_available]
                
                extra_data.append(df_chunk)
                print(f" -> {len(df_chunk)} baris")
            else:
                print(f" -> Kosong")
                
        except Exception as e:
            print(f" -> Error: {e}")
        
        cur = batch_end
        time.sleep(1)

# ====================================================
# LANGKAH 3: Gabungkan semua data
# ====================================================
print("\n" + "=" * 60)
print("LANGKAH 3: Menggabungkan semua data")
print("=" * 60)

all_dfs = [df_binance]
if extra_data:
    all_dfs.extend(extra_data)

df_combined = pd.concat(all_dfs, ignore_index=True)
df_combined['Open_Time'] = pd.to_datetime(df_combined['Open_Time']).dt.tz_localize(None)
df_combined = df_combined.drop_duplicates(subset=['Open_Time']).sort_values('Open_Time').reset_index(drop=True)

# Filter ke range target (5 tahun)
df_combined = df_combined[
    (df_combined['Open_Time'] >= start_target) & 
    (df_combined['Open_Time'] <= end_target)
]

print(f"Total baris setelah digabung: {len(df_combined)}")
print(f"Dari: {df_combined['Open_Time'].min()}")
print(f"Sampai: {df_combined['Open_Time'].max()}")

# ====================================================
# LANGKAH 4: Simpan
# ====================================================
print("\n" + "=" * 60)
print("LANGKAH 4: Menyimpan dataset")
print("=" * 60)

# Pastikan numerik
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    if col in df_combined.columns:
        df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')

df_combined.to_csv(output_file, index=False)

print(f"Dataset disimpan: {output_file}")
print(f"Total baris: {len(df_combined)}")
print(f"Periode: {df_combined['Open_Time'].min().strftime('%Y-%m-%d')} s/d {df_combined['Open_Time'].max().strftime('%Y-%m-%d')}")

# Cek coverage
expected_hours = int((end_target - start_target).total_seconds() / 3600)
coverage = len(df_combined) / expected_hours * 100
print(f"Coverage: {len(df_combined)}/{expected_hours} jam ({coverage:.1f}%)")
