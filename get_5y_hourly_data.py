import requests
import pandas as pd
import time
import os
from datetime import datetime, timedelta

# Konfigurasi
symbol = "BTCUSDT"
interval = "1h"
data_dir = "01_Data"
output_file = os.path.join(data_dir, "btc_5year_hourly_bigdata.csv")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Waktu sekarang dan 5 tahun yang lalu
end_time = int(datetime.now().timestamp() * 1000)
start_time = int((datetime.now() - timedelta(days=5*365)).timestamp() * 1000)

print(f"Rentang waktu pengambilan data:")
print(f"  Dari: {datetime.fromtimestamp(start_time/1000).strftime('%Y-%m-%d %H:%M')}")
print(f"  Sampai: {datetime.fromtimestamp(end_time/1000).strftime('%Y-%m-%d %H:%M')}")
print(f"Sedang mengunduh High Frequency Data (1 Jam) selama 5 tahun...")
print()

all_data = []
current_start = start_time
batch_num = 0
max_retries = 3

def fetch_batch(url, retries=3):
    """Fetch data with retry logic"""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                else:
                    print(f"API Error response: {data}")
                    return None
            else:
                print(f"HTTP Error {response.status_code}, attempt {attempt+1}/{retries}")
                time.sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error (attempt {attempt+1}/{retries}): {str(e)[:50]}")
            if attempt < retries - 1:
                print(f"  Menunggu {2 ** (attempt+1)} detik sebelum retry...")
                time.sleep(2 ** (attempt+1))
        except Exception as e:
            print(f"Error (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2)
    return None

while current_start < end_time:
    batch_num += 1
    
    # API Binance: Limit 1000 records per request
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={current_start}&limit=1000"
    
    data = fetch_batch(url, retries=max_retries)
    
    if data is None or len(data) == 0:
        print(f"\nTidak ada data atau error pada batch {batch_num}")
        break
    
    all_data.extend(data)
    
    # Update current_start untuk batch berikutnya
    last_close_time = data[-1][6]
    current_start = last_close_time + 1
    
    # Hentikan jika sudah melewati end_time
    if current_start >= end_time:
        break
    
    # Progress info
    progress_date = datetime.fromtimestamp(current_start / 1000).strftime('%Y-%m-%d %H:%M')
    print(f"Batch {batch_num:4d}: Hingga {progress_date} | Total: {len(all_data):6d} baris", end='\r')
    
    # Jeda singkat
    time.sleep(0.15)

print()

if len(all_data) == 0:
    print("GAGAL: Tidak ada data yang berhasil diunduh!")
    print("Coba lagi nanti atau periksa koneksi internet.")
else:
    print(f"\nMenggabungkan {len(all_data)} baris data...")
    
    # Kolom API Binance
    columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 
               'Quote_Asset_Volume', 'Number_of_Trades', 'Taker_Buy_Base_Value', 
               'Taker_Buy_Quote_Value', 'Ignore']
    
    df = pd.DataFrame(all_data, columns=columns)
    
    # Pembersihan Data
    df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
    
    # Pastikan tipe data numerik
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    
    # Simpan hanya kolom utama
    df_save = df[['Open_Time'] + numeric_cols].copy()
    df_save = df_save.drop_duplicates(subset=['Open_Time']).sort_values('Open_Time')
    df_save.to_csv(output_file, index=False)
    
    print(f"\nSELESAI!")
    print(f"Dataset berhasil disimpan: {output_file}")
    print(f"Total baris data: {len(df_save)}")
    print(f"Rentang waktu: {df_save['Open_Time'].min()} sampai {df_save['Open_Time'].max()}")
