"""
Tambahkan data sisa (2026-02-28 17:00 hingga 2026-03-01 sekarang)
dan update notebook Cell 6 dengan versi final Binance API.
"""
import os, time, requests, pandas as pd, urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_DIR   = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\01_Data'
OUTPUT_CSV = os.path.join(DATA_DIR, 'btc_5year_hourly_bigdata.csv')
BASE_URL   = 'https://data-api.binance.vision'
HEADERS    = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}

# Baca CSV yang ada
df_existing = pd.read_csv(OUTPUT_CSV)
df_existing['Open_Time'] = pd.to_datetime(df_existing['Open_Time'])
last_time = df_existing['Open_Time'].max()
print("Data existing: {:,} baris, terakhir: {}".format(len(df_existing), last_time))

# Tentukan range yang kurang
start_missing = last_time + timedelta(hours=1)
end_now = datetime.now().replace(minute=0, second=0, microsecond=0)
print("Ambil sisa data: {} --> {}".format(start_missing, end_now))

if start_missing >= end_now:
    print("Tidak ada data yang perlu ditambahkan. Data sudah lengkap!")
else:
    start_ms = int(start_missing.timestamp() * 1000)
    end_ms   = int(end_now.timestamp() * 1000)

    params = {
        'symbol'   : 'BTCUSDT',
        'interval' : '1h',
        'startTime': start_ms,
        'endTime'  : end_ms,
        'limit'    : 1000
    }
    try:
        r = requests.get(BASE_URL + '/api/v3/klines', params=params,
                         headers=HEADERS, timeout=30, verify=False)
        r.raise_for_status()
        data = r.json()
        print("Data baru didapat: {} baris".format(len(data)))

        if data:
            rows = []
            for row in data:
                rows.append({
                    'Open_Time': pd.to_datetime(row[0], unit='ms'),
                    'Open'     : float(row[1]),
                    'High'     : float(row[2]),
                    'Low'      : float(row[3]),
                    'Close'    : float(row[4]),
                    'Volume'   : float(row[5]),
                })
            df_new  = pd.DataFrame(rows)
            df_full = pd.concat([df_existing, df_new], ignore_index=True)
            df_full = df_full.drop_duplicates('Open_Time').sort_values('Open_Time').reset_index(drop=True)
            df_full.to_csv(OUTPUT_CSV, index=False)

            days = (df_full['Open_Time'].max() - df_full['Open_Time'].min()).days
            print("Total setelah update: {:,} baris, {} hari ({:.2f} tahun)".format(
                len(df_full), days, days/365.25))
            print("Start: {}".format(df_full['Open_Time'].min()))
            print("End  : {}".format(df_full['Open_Time'].max()))
    except Exception as e:
        print("Error: {}".format(e))

print()
print("Data CSV siap!")
