import yfinance as yf
import pandas as pd
import os

# Konfigurasi
symbol = "BTC-USD"
data_dir = "01_Data"
output_file = os.path.join(data_dir, "btc_detailed_bigdata_2y_hourly.csv")

print(f"Mengambil data {symbol} interval 1 JAM untuk 5 tahun terakhir (Maksimum API)...")

# Data 1 jam (Hourly) adalah data paling detail yang bisa ditarik untuk rentang panjang (730 hari)
# Ini akan memberikan sekitar 43,800+ baris data.
df_hourly = yf.download(symbol, period="2y", interval="1h")

if not df_hourly.empty:
    df_hourly.to_csv(output_file)
    print(f"Berhasil! Dataset Hourly disimpan di: {output_file}")
    print(f"Total baris: {len(df_hourly)}")
else:
    print("Gagal mengambil data hourly.")
