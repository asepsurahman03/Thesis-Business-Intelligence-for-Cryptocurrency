"""
Script untuk mengambil data Bitcoin 5 tahun dari Binance API.
Jika Binance tidak bisa diakses (region block), fallback ke yfinance.

Sekarang: 2026-03-01
5 tahun  : 2021-03-01 s/d 2026-03-01
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# KONFIGURASI
# ============================================================
DATA_DIR = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\01_Data'
OUTPUT_FILE = os.path.join(DATA_DIR, 'btc_5year_hourly_bigdata.csv')

BINANCE_ENDPOINTS = [
    'https://api.binance.com',
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com',
    'https://api4.binance.com',
]

SYMBOL = 'BTCUSDT'
INTERVAL = '1h'

END_DATE   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=5*365)

print("=" * 60)
print("  Bitcoin 5-Year Data Downloader (Binance API)")
print("=" * 60)
print("Simbol     : " + SYMBOL)
print("Interval   : " + INTERVAL)
print("Start Date : " + START_DATE.strftime('%Y-%m-%d'))
print("End Date   : " + END_DATE.strftime('%Y-%m-%d'))
print("Output     : " + OUTPUT_FILE)
print()


def test_binance_endpoint(base_url):
    """Test apakah endpoint Binance bisa diakses."""
    try:
        resp = requests.get(base_url + "/api/v3/ping", timeout=10)
        return resp.status_code == 200
    except Exception:
        return False


def fetch_binance_klines(base_url, symbol, interval, start_dt, end_dt):
    """Ambil data klines dari Binance API dengan looping (max 1000 per request)."""
    all_data = []
    start_ms = int(start_dt.timestamp() * 1000)
    end_ms = int(end_dt.timestamp() * 1000)
    current_ms = start_ms
    batch_num = 0

    total_hours = int((end_ms - start_ms) / (3600 * 1000))
    print("Estimasi total data: " + str(total_hours) + " baris")

    while current_ms < end_ms:
        batch_num += 1
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': current_ms,
            'endTime': end_ms,
            'limit': 1000
        }
        try:
            resp = requests.get(base_url + "/api/v3/klines", params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            if not data:
                break

            all_data.extend(data)
            last_time = data[-1][0]
            current_ms = last_time + 3600000  # +1 jam

            pct = min(((current_ms - start_ms) / (end_ms - start_ms)) * 100, 100)
            print("  Batch {:3d}: +{:4d} baris | Total: {:,} | {:.1f}%".format(
                batch_num, len(data), len(all_data), pct))

            time.sleep(0.25)  # rate limiting

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                print("  Rate limit! Tunggu 60 detik...")
                time.sleep(60)
                continue
            print("  HTTP Error: " + str(e))
            break
        except Exception as e:
            print("  Error batch {}: {}".format(batch_num, e))
            break

    return all_data


def convert_binance_to_df(raw_data):
    """Convert raw Binance response ke DataFrame yang kompatibel."""
    cols = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close_Time', 'Quote_Vol', 'Trades', 'Taker_Buy_Base', 'Taker_Buy_Quote', 'Ignore']
    df = pd.DataFrame(raw_data, columns=cols)
    df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
    for c in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[c] = df[c].astype(float)
    df = df[['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df = df.drop_duplicates('Open_Time').sort_values('Open_Time').reset_index(drop=True)
    return df


def fetch_via_yfinance(start_dt, end_dt):
    """Fallback: ambil dari yfinance jika Binance tidak bisa diakses."""
    print("Menggunakan yfinance sebagai sumber data (Binance tidak tersedia)...")
    import yfinance as yf

    print("  Ambil data harian 5 tahun (BTC-USD dari Yahoo Finance)...")
    df_daily = yf.download('BTC-USD',
                           start=start_dt.strftime('%Y-%m-%d'),
                           end=end_dt.strftime('%Y-%m-%d'),
                           interval='1d', progress=False)

    if df_daily.empty:
        raise ValueError("yfinance juga tidak mengembalikan data.")

    # Flatten MultiIndex columns jika ada
    if isinstance(df_daily.columns, pd.MultiIndex):
        df_daily.columns = [col[0] for col in df_daily.columns]

    df_daily.index = pd.to_datetime(df_daily.index)
    df_daily.index.name = 'Open_Time'
    df_daily = df_daily.reset_index()
    df_daily['Open_Time'] = pd.to_datetime(df_daily['Open_Time']).dt.tz_localize(None)

    print("  Interpolasi data harian ke data per jam...")
    df_daily = df_daily.set_index('Open_Time')
    df_daily = df_daily[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

    # Upsample ke 1 jam dengan interpolasi
    df_hourly = df_daily.resample('1h').interpolate(method='time')
    df_hourly = df_hourly.reset_index()
    df_hourly.columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Filter rentang waktu
    df_hourly = df_hourly[
        (df_hourly['Open_Time'] >= pd.Timestamp(start_dt)) &
        (df_hourly['Open_Time'] <= pd.Timestamp(end_dt))
    ].reset_index(drop=True)

    return df_hourly, 'yfinance (interpolated hourly dari data harian)'


# ============================================================
# MAIN: Coba Binance API, fallback ke yfinance
# ============================================================
df_result = None
source_used = None

print("--- Step 1: Cek Binance API endpoints ---")
working_endpoint = None
for ep in BINANCE_ENDPOINTS:
    print("  Testing " + ep + "...", end=' ')
    if test_binance_endpoint(ep):
        print("OK!")
        working_endpoint = ep
        break
    else:
        print("Gagal")

if working_endpoint:
    print("\n--- Step 2: Ambil data dari Binance API ({}) ---".format(working_endpoint))
    raw = fetch_binance_klines(working_endpoint, SYMBOL, INTERVAL, START_DATE, END_DATE)
    if raw:
        df_result = convert_binance_to_df(raw)
        source_used = 'Binance API (' + working_endpoint + ')'
    else:
        print("Binance API tidak mengembalikan data. Fallback ke yfinance...")

if df_result is None:
    print("\n--- Step 2 (Fallback): Ambil data dari yfinance ---")
    df_result, source_used = fetch_via_yfinance(START_DATE, END_DATE)

# ============================================================
# SIMPAN HASIL
# ============================================================
os.makedirs(DATA_DIR, exist_ok=True)
df_result.to_csv(OUTPUT_FILE, index=False)

print()
print("=" * 60)
print("  HASIL DOWNLOAD")
print("=" * 60)
print("Sumber data  : " + source_used)
print("Total baris  : {:,}".format(len(df_result)))
print("Mulai        : " + str(df_result['Open_Time'].min()))
print("Akhir        : " + str(df_result['Open_Time'].max()))
print("Kolom        : " + str(list(df_result.columns)))
print("File disimpan: " + OUTPUT_FILE)

actual_days = (df_result['Open_Time'].max() - df_result['Open_Time'].min()).days
print("Cakupan      : {} hari ({:.1f} tahun)".format(actual_days, actual_days/365.25))
if actual_days >= 365*5 - 30:
    print("Status       : DATA SUDAH MENCAKUP 5 TAHUN (OK)")
else:
    print("Status       : PERINGATAN - Data hanya {} hari, kurang dari 5 tahun".format(actual_days))
print()
