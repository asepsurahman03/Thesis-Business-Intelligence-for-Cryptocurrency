"""
Script untuk memperbaiki Cell 6 di notebook agar:
1. Coba ambil data langsung dari Binance API (5 tahun terakhir)
2. Fallback ke yfinance jika Binance tidak bisa diakses
3. Simpan ke CSV dan load ke DataFrame
"""
import json
import re

NB_PATH = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

# Kode baru untuk Cell 6 (Data Loading dengan Binance API + fallback)
NEW_CELL6_CODE = r'''# ============================================================
# Data Loading - Big Data Volume Characteristic
# Sumber Data: Binance API (BTCUSDT, 1h) dengan fallback ke yfinance
# Rentang: 5 Tahun Terakhir dari tanggal sekarang
# ============================================================
import os
import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Konfigurasi ---
DATA_DIR = '../01_Data'
CSV_FILE = os.path.join(DATA_DIR, 'btc_5year_hourly_bigdata.csv')
SYMBOL_BINANCE = 'BTCUSDT'
SYMBOL_YAHOO   = 'BTC-USD'
INTERVAL       = '1h'

END_DATE   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=5*365)

print("=" * 60)
print("  Bitcoin 5-Year Data Loader")
print("=" * 60)
print("Periode  : {} s/d {}".format(
    START_DATE.strftime('%Y-%m-%d'), END_DATE.strftime('%Y-%m-%d')))
print()

# ============================================================
# Fungsi Binance API
# ============================================================
BINANCE_ENDPOINTS = [
    'https://api.binance.com',
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com',
]

def test_binance(base_url):
    try:
        r = requests.get(base_url + '/api/v3/ping', timeout=8)
        return r.status_code == 200
    except Exception:
        return False

def fetch_binance_klines(base_url, symbol, interval, start_dt, end_dt):
    """Ambil semua klines dari Binance (loop per 1000 baris)."""
    all_data = []
    start_ms  = int(start_dt.timestamp() * 1000)
    end_ms    = int(end_dt.timestamp() * 1000)
    current   = start_ms
    batch     = 0
    total_est = int((end_ms - start_ms) / 3_600_000)
    print("  Estimasi: {:,} baris (1h candle)".format(total_est))

    while current < end_ms:
        batch += 1
        try:
            params = {'symbol': symbol, 'interval': interval,
                      'startTime': current, 'endTime': end_ms, 'limit': 1000}
            r = requests.get(base_url + '/api/v3/klines', params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            if not data:
                break
            all_data.extend(data)
            current = data[-1][0] + 3_600_000
            pct = min(((current - start_ms) / (end_ms - start_ms)) * 100, 100)
            print("  Batch {:3d}: +{:4d} | Total: {:,} | {:.1f}%".format(
                batch, len(data), len(all_data), pct))
            time.sleep(0.25)
        except Exception as e:
            print("  Error batch {}: {}".format(batch, e))
            break
    return all_data

def binance_to_df(raw):
    cols = ['Open_Time','Open','High','Low','Close','Volume',
            'Close_Time','QVol','Trades','TBBase','TBQuote','Ignore']
    df = pd.DataFrame(raw, columns=cols)
    df['Open_Time'] = pd.to_datetime(df['Open_Time'], unit='ms')
    for c in ['Open','High','Low','Close','Volume']:
        df[c] = df[c].astype(float)
    df = df[['Open_Time','Open','High','Low','Close','Volume']]
    df = df.drop_duplicates('Open_Time').sort_values('Open_Time').reset_index(drop=True)
    return df

# ============================================================
# Fungsi yfinance (fallback)
# ============================================================
def fetch_yfinance(symbol, start_dt, end_dt):
    import yfinance as yf
    print("  Mengunduh data harian dari Yahoo Finance...")
    df_d = yf.download(symbol, start=start_dt.strftime('%Y-%m-%d'),
                       end=end_dt.strftime('%Y-%m-%d'), interval='1d', progress=False)
    if df_d.empty:
        raise ValueError("yfinance tidak mengembalikan data.")
    if isinstance(df_d.columns, pd.MultiIndex):
        df_d.columns = [c[0] for c in df_d.columns]
    df_d.index = pd.to_datetime(df_d.index).tz_localize(None)
    df_d = df_d[['Open','High','Low','Close','Volume']].astype(float)
    print("  Interpolasi harian -> per jam...")
    df_h = df_d.resample('1h').interpolate(method='time').reset_index()
    df_h.columns = ['Open_Time','Open','High','Low','Close','Volume']
    df_h = df_h[
        (df_h['Open_Time'] >= pd.Timestamp(start_dt)) &
        (df_h['Open_Time'] <= pd.Timestamp(end_dt))
    ].reset_index(drop=True)
    return df_h

# ============================================================
# Cek apakah CSV sudah ada dan rentangnya cukup
# ============================================================
def csv_is_valid(path, start_dt, end_dt):
    """Return True jika CSV sudah ada dan rentangnya mencakup 5 tahun."""
    if not os.path.exists(path):
        return False
    try:
        _df = pd.read_csv(path, nrows=5)
        # Cek kolom Open_Time
        if 'Open_Time' not in _df.columns:
            return False
        # Load penuh
        _df = pd.read_csv(path)
        _df['Open_Time'] = pd.to_datetime(_df['Open_Time'])
        days = (_df['Open_Time'].max() - _df['Open_Time'].min()).days
        return days >= 365*5 - 30  # toleransi 30 hari
    except Exception:
        return False

# ============================================================
# MAIN: Load atau Download data
# ============================================================
source_used = None

if csv_is_valid(CSV_FILE, START_DATE, END_DATE):
    print("[INFO] CSV lokal sudah ada dan mencakup 5 tahun. Memuat dari file...")
    df_raw = pd.read_csv(CSV_FILE)
    source_used = 'CSV lokal (btc_5year_hourly_bigdata.csv)'
else:
    print("[INFO] CSV belum ada atau cakupannya kurang. Mengunduh data baru...")
    df_raw   = None
    raw_data = None

    # -- Coba Binance API --
    print("\n[Binance API] Mencari endpoint yang aktif...")
    active_ep = None
    for ep in BINANCE_ENDPOINTS:
        print("  Testing {}...".format(ep), end=' ')
        if test_binance(ep):
            print("OK!")
            active_ep = ep
            break
        else:
            print("Gagal")

    if active_ep:
        print("\n[Binance API] Mengunduh data dari {}...".format(active_ep))
        raw_data = fetch_binance_klines(active_ep, SYMBOL_BINANCE, INTERVAL, START_DATE, END_DATE)
        if raw_data:
            df_raw      = binance_to_df(raw_data)
            source_used = 'Binance API ({})'.format(active_ep)

    # -- Fallback ke yfinance --
    if df_raw is None or len(df_raw) == 0:
        print("\n[yfinance] Binance tidak tersedia, menggunakan Yahoo Finance...")
        df_raw      = fetch_yfinance(SYMBOL_YAHOO, START_DATE, END_DATE)
        source_used = 'Yahoo Finance / yfinance (interpolated hourly)'

    # Simpan ke CSV
    os.makedirs(DATA_DIR, exist_ok=True)
    df_raw.to_csv(CSV_FILE, index=False)
    print("\n[INFO] Data disimpan ke: {}".format(CSV_FILE))

# ============================================================
# Preprocessing: Set index Timestamp
# ============================================================
df = df_raw.copy()
df['Timestamp'] = pd.to_datetime(df['Open_Time'])
df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)
df.set_index('Timestamp', inplace=True)
df.drop('Open_Time', axis=1, errors='ignore', inplace=True)

# Filter sesuai rentang 5 tahun dari sekarang (re-validate)
df = df[(df.index >= pd.Timestamp(START_DATE)) & (df.index <= pd.Timestamp(END_DATE))]

print()
print("=" * 60)
print("  DATASET SIAP")
print("=" * 60)
print("Sumber           : {}".format(source_used))
print("Jumlah baris     : {:,}".format(df.shape[0]))
print("Jumlah kolom     : {}".format(df.shape[1]))
print("Kolom            : {}".format(list(df.columns)))
print("Mulai            : {}".format(df.index.min().strftime('%Y-%m-%d')))
print("Akhir            : {}".format(df.index.max().strftime('%Y-%m-%d')))
actual_days = (df.index.max() - df.index.min()).days
print("Cakupan          : {} hari ({:.1f} tahun)".format(actual_days, actual_days/365.25))
print()

def apply_technical_indicators(df):
    # Moving Averages
    df['MA7']  = df['Close'].rolling(window=7).mean()
    df['MA25'] = df['Close'].rolling(window=25).mean()

    # Kalkulasi RSI
    delta = df['Close'].diff()
    gain  = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + gain/loss))

    # Kalkulasi MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Volatilitas & Return
    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility']  = df['Close'].rolling(window=24).std()

    # Bollinger Bands
    df['BB_Mid']   = df['Close'].rolling(window=20).mean()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(window=20).std()
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['Close'].rolling(window=20).std()

    # Hapus NaN dari kalkulasi indikator
    df.dropna(inplace=True)
    return df

df = apply_technical_indicators(df)

print("Setelah feature engineering:")
print("Jumlah baris     : {:,}".format(df.shape[0]))
print("Kolom teknikal   : {}".format(list(df.columns)))
print()
print("Sample data terbaru (5 baris terakhir):")
print(df[['Close', 'RSI', 'MACD', 'Volatility']].tail())
'''

# Baca notebook
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")

# Temukan cell 6 (index 6, cell yang berisi 'Data Loading')
# Cek dulu cell mana yang mengandung 'Data Loading'
target_cell_idx = None
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'Data Loading' in src or 'btc_5year_hourly_bigdata' in src:
            print(f"  Cell {i}: Berisi 'Data Loading' / 'btc_5year_hourly_bigdata'")
            target_cell_idx = i

if target_cell_idx is not None:
    print(f"\nMemperbaiki Cell {target_cell_idx}...")
    # Update source cell dengan kode baru
    nb['cells'][target_cell_idx]['source'] = NEW_CELL6_CODE.lstrip('\n')
    nb['cells'][target_cell_idx]['outputs'] = []
    nb['cells'][target_cell_idx]['execution_count'] = None
    print(f"Cell {target_cell_idx} berhasil diperbarui!")
else:
    print("ERROR: Cell Data Loading tidak ditemukan!")

# Simpan notebook
with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\nNotebook disimpan: {NB_PATH}")
print("Selesai!")
