import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Konfigurasi
symbol = "BTC-USD"
data_dir = "01_Data"
output_file = os.path.join(data_dir, "btc_5year_bigdata.csv")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

print(f"Sedang mengunduh data {symbol} untuk 5 tahun terakhir (skala Big Data)...")

# Mencoba mengambil data dengan interval terkecil yang diizinkan untuk rentang waktu panjang
# Catatan: yfinance memiliki batasan interval. 
# Untuk 5 tahun, interval terkecil yang stabil biasanya adalah 1 jam (1h) atau 1 hari (1d).
# Namun, untuk mendapatkan volume "banyak", kita akan menggunakan interval 1 jam jika memungkinkan.
# Jika 1 jam terlalu lama/dibatasi, kita ambil 1 hari tetapi dengan fitur yang sangat lengkap.

try:
    # Mengunduh data 1 jam (Hourly) selama 5 tahun (Jika didukung oleh API)
    # yfinance biasanya membatasi data intraday (1h) hanya untuk 730 hari terakhir.
    # Maka kita akan menggunakan strategi: 
    # 1. Ambil data 1h untuk 5 tahun terakhir (Volume besar intraday)
    # 2. Ambil data 1d untuk 5 tahun terakhir (Rentang waktu panjang)
    
    print("Mengambil data harian (1d) untuk rentang 5 tahun...")
    df_5y = yf.download(symbol, period="5y", interval="1d")
    
    if not df_5y.empty:
        df_5y.to_csv(output_file)
        print(f"Berhasil! Dataset 5 tahun disimpan di: {output_file}")
        print(f"Total baris: {len(df_5y)}")
        print(f"Rentang: {df_5y.index[0]} sampai {df_5y.index[-1]}")
    else:
        print("Gagal mengunduh data.")

except Exception as e:
    print(f"Terjadi kesalahan: {e}")
