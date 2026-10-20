import yfinance as yf
import pandas as pd
import time
import os
from datetime import datetime, timedelta
from binance.client import Client # Import Binance client

# Konfigurasi
data_dir = "01_Data"
output_file = os.path.join(data_dir, "btc_5year_hourly_bigdata.csv")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Tanggal sekarang dan 5 tahun lalu
end_date = datetime.now()
target_start_date = end_date - timedelta(days=5*365) # Target 5 tahun data

# Binance API (tidak perlu API key untuk data publik, tapi bisa ditambahkan jika diperlukan)
# BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
# BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
# client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
client = Client("", "") # Initialize client without API keys for public data

# Batas awal data Binance untuk BTCUSDT (sekitar 17 Agustus 2017)
BINANCE_GLOBAL_START_DATE = datetime(2017, 8, 17)

# yfinance mendukung 1h untuk maksimal 729 hari per request
YFINANCE_MAX_DAYS_PER_BATCH = 729

print(f"Mengunduh data Bitcoin hourly 5 tahun:")
print(f"  Target Dari: {target_start_date.strftime('%Y-%m-%d')}")
print(f"  Sampai: {end_date.strftime('%Y-%m-%d')}")
print()

def download_binance_data(symbol, interval, start_date_str, end_date_str):
    """Mengunduh data dari Binance."""
    print(f"Mengunduh data Binance ({symbol}, {interval}): {start_date_str} - {end_date_str}", end="")
    klines = client.get_historical_klines(symbol, interval, start_date_str, end_date_str)
    
    if not klines:
        print(" -> Kosong")
        return pd.DataFrame()

    df = pd.DataFrame(klines, columns=[
        'Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 
        'Close_Time', 'Quote_Asset_Volume', 'Number_of_Trades', 
        'Taker_Buy_Base_Asset_Volume', 'Taker_Buy_Quote_Asset_Volume', 'Ignore'
    ])
    
    df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    df = df[['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.set_index('Open_Time')
    print(f" -> {len(df)} baris")
    return df

def download_yfinance_data(symbol, interval, start_date, end_date):
    """Mengunduh data dari yfinance dengan batching."""
    all_data = []
    current_start = start_date
    batch_num = 0

    while current_start < end_date:
        batch_num += 1
        current_end = min(current_start + timedelta(days=YFINANCE_MAX_DAYS_PER_BATCH), end_date)
        
        print(f"Mengunduh data yfinance ({symbol}, {interval}) Batch {batch_num}: {current_start.strftime('%Y-%m-%d')} - {current_end.strftime('%Y-%m-%d')}", end="")
        
        try:
            df_chunk = yf.download(
                symbol, 
                start=current_start.strftime('%Y-%m-%d'),
                end=current_end.strftime('%Y-%m-%d'), 
                interval=interval, 
                progress=False,
                auto_adjust=True
            )
            
            if not df_chunk.empty:
                if hasattr(df_chunk.columns, 'levels'):
                    df_chunk.columns = [col[0] if isinstance(col, tuple) else col for col in df_chunk.columns]
                
                # Rename columns to match Binance output
                df_chunk = df_chunk.rename(columns={
                    'Datetime': 'Open_Time', # yfinance can sometimes use Datetime for index
                    'Adj Close': 'Close' # Use Adj Close as Close
                })
                df_chunk = df_chunk[['Open', 'High', 'Low', 'Close', 'Volume']]
                all_data.append(df_chunk)
                print(f" -> {len(df_chunk)} baris")
            else:
                print(f" -> Kosong")
                
        except Exception as e:
            print(f" -> Error: {e}")
        
        current_start = current_end
        time.sleep(1) # Be nice to the API

    if all_data:
        df_combined = pd.concat(all_data)
        return df_combined
    return pd.DataFrame()

# --- Strategi Penggabungan Data ---

# 1. Tentukan tanggal split antara Binance dan yfinance
#    Kita akan mencoba mengambil data Binance sejauh mungkin ke belakang,
#    dan yfinance untuk data yang lebih baru.
#    Untuk memastikan 5 tahun data, kita perlu data dari target_start_date.
#    Binance biasanya memiliki data yang lebih lama.

#    Ambil data Binance dari BINANCE_GLOBAL_START_DATE hingga 1 tahun sebelum end_date
#    Ini memberikan overlap yang cukup dan memastikan kita mendapatkan data historis yang dalam.
binance_end_for_download = end_date - timedelta(days=365) # Ambil Binance sampai 1 tahun lalu
binance_start_for_download = max(target_start_date, BINANCE_GLOBAL_START_DATE)

print(f"\n--- Mengunduh data dari Binance ---")
df_binance = download_binance_data(
    'BTCUSDT', 
    '1h', 
    binance_start_for_download.strftime('%d %b %Y %H:%M:%S'), 
    binance_end_for_download.strftime('%d %b %Y %H:%M:%S')
)

# 2. Tentukan tanggal mulai yfinance
#    yfinance akan mengambil data dari tanggal mulai Binance yang kita inginkan
#    hingga tanggal sekarang. Ini akan menciptakan overlap.
yfinance_start_for_download = binance_start_for_download

print(f"\n--- Mengunduh data dari yfinance ---")
df_yfinance = download_yfinance_data(
    'BTC-USD', 
    '1h', 
    yfinance_start_for_download, 
    end_date
)

# 3. Gabungkan dan bersihkan data
if not df_binance.empty and not df_yfinance.empty:
    print("\nMenggabungkan data Binance dan yfinance...")
    df_combined = pd.concat([df_binance, df_yfinance])
elif not df_binance.empty:
    print("\nHanya data Binance yang tersedia.")
    df_combined = df_binance
elif not df_yfinance.empty:
    print("\nHanya data yfinance yang tersedia.")
    df_combined = df_yfinance
else:
    print("\nGagal mengunduh data dari kedua sumber!")
    df_combined = pd.DataFrame()

if not df_combined.empty:
    df_final = df_combined[~df_combined.index.duplicated(keep='first')] # Hapus duplikat (overlap)
    df_final = df_final.sort_index()
    
    # Filter untuk memastikan hanya 5 tahun terakhir
    df_final = df_final[df_final.index >= target_start_date]

    # Reset index untuk menjadikan Datetime sebagai kolom Open_Time
    df_final.index.name = 'Open_Time'
    df_final = df_final.reset_index()
    
    # Pastikan hanya ada kolom yang dibutuhkan
    cols_needed = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    cols_available = [c for c in cols_needed if c in df_final.columns]
    df_final = df_final[cols_available]
    
    # Simpan ke CSV
    df_final.to_csv(output_file, index=False)
    
    print(f"\nSELESAI!")
    print(f"File disimpan: {output_file}")
    print(f"Total baris: {len(df_final)}")
    print(f"Dari: {df_final['Open_Time'].min()}")
    print(f"Sampai: {df_final['Open_Time'].max()}")
else:
    print("\nGagal mengunduh atau menggabungkan data!")
