"""
Download 5 tahun data BTC dari Binance API.
Menggunakan data-api.binance.vision (CDN endpoint, lebih stabil).
Dengan retry otomatis dan resume dari progress.

Range: 5 tahun dari datetime.now()
"""
import os, time, requests, pandas as pd, urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_DIR     = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\01_Data'
OUTPUT_CSV   = os.path.join(DATA_DIR, 'btc_5year_hourly_bigdata.csv')
PROGRESS_CSV = os.path.join(DATA_DIR, 'btc_download_progress.csv')

# Endpoints diurutkan dari yang paling stabil
ENDPOINTS = [
    'https://data-api.binance.vision',   # CDN - paling stabil
    'https://api.binance.com',
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com',
    'https://api4.binance.com',
]

END_DATE   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = END_DATE - timedelta(days=5*365)

print("=" * 55)
print("  Binance Download: BTCUSDT 1h | 5 Tahun")
print("=" * 55)
print("Range : {} --> {}".format(
    START_DATE.strftime('%Y-%m-%d'), END_DATE.strftime('%Y-%m-%d')))
print()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept'    : 'application/json',
}

def get_working_endpoint():
    for ep in ENDPOINTS:
        try:
            r = requests.get(ep + '/api/v3/ping', headers=HEADERS,
                             timeout=10, verify=False)
            if r.status_code == 200:
                return ep
        except Exception:
            pass
    return None

def fetch_batch(base_url, current_ms, end_ms, retries=6):
    params = {
        'symbol'   : 'BTCUSDT',
        'interval' : '1h',
        'startTime': current_ms,
        'endTime'  : end_ms,
        'limit'    : 1000
    }
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(
                base_url + '/api/v3/klines',
                params=params, headers=HEADERS,
                timeout=30, verify=False
            )
            r.raise_for_status()
            return base_url, r.json()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as e:
            ecode = str(e)
            if '10054' in ecode: reason = 'Connection Reset'
            elif '10061' in ecode: reason = 'Connection Refused'
            else: reason = ecode[:50]
            print("    [Attempt {}/{}] {} -- coba endpoint lain...".format(
                attempt, retries, reason))
            # Rotasi endpoint
            new_ep = get_working_endpoint()
            if new_ep:
                base_url = new_ep
                print("    Ganti ke: " + base_url)
            wait = min(attempt * 4, 30)
            time.sleep(wait)
        except Exception as e:
            print("    [Attempt {}/{}] Error: {}".format(attempt, retries, str(e)[:60]))
            time.sleep(5)
    return base_url, None

# ============================================================
# Cek progress sebelumnya
# ============================================================
all_rows = []
start_ms = int(START_DATE.timestamp() * 1000)
end_ms   = int(END_DATE.timestamp() * 1000)

if os.path.exists(PROGRESS_CSV):
    df_prog = pd.read_csv(PROGRESS_CSV)
    df_prog['Open_Time'] = pd.to_datetime(df_prog['Open_Time'])
    last_t  = df_prog['Open_Time'].max()
    resume  = int(last_t.timestamp() * 1000) + 3_600_000
    all_rows = df_prog.to_dict('records')
    start_ms = resume
    print("Resume dari progress: {:,} baris, lanjut dari {}".format(
        len(all_rows), last_t.strftime('%Y-%m-%d %H:%M')))
else:
    print("Mulai download dari awal...")

print()

# ============================================================
# Main download loop
# ============================================================
print("Mencari endpoint aktif...")
base_url = get_working_endpoint()
if not base_url:
    print("ERROR: Tidak ada endpoint Binance yang bisa diakses!")
    raise SystemExit(1)

print("Menggunakan: " + base_url)
print()

batch   = 0
current = start_ms
abs_start = int(START_DATE.timestamp() * 1000)

while current < end_ms:
    batch += 1
    base_url, data = fetch_batch(base_url, current, end_ms)

    if data is None:
        print("Semua retry habis. Simpan progress dan berhenti.")
        break

    if not data:
        print("Tidak ada data lagi (selesai).")
        break

    for row in data:
        all_rows.append({
            'Open_Time': pd.to_datetime(row[0], unit='ms'),
            'Open'     : float(row[1]),
            'High'     : float(row[2]),
            'Low'      : float(row[3]),
            'Close'    : float(row[4]),
            'Volume'   : float(row[5]),
        })

    current = data[-1][0] + 3_600_000
    pct = min(((current - abs_start) / (end_ms - abs_start)) * 100, 100)
    print("Batch {:3d}: +{:4d} | Total {:,} rows | {:.1f}%".format(
        batch, len(data), len(all_rows), pct))

    # Simpan progress tiap 30 batch
    if batch % 30 == 0:
        df_tmp = pd.DataFrame(all_rows).drop_duplicates('Open_Time').sort_values('Open_Time')
        df_tmp.to_csv(PROGRESS_CSV, index=False)
        print("  [Progress disimpan: {:,} baris]".format(len(df_tmp)))

    time.sleep(0.3)

# ============================================================
# Simpan final
# ============================================================
df_final = pd.DataFrame(all_rows)
df_final = df_final.drop_duplicates('Open_Time').sort_values('Open_Time').reset_index(drop=True)

os.makedirs(DATA_DIR, exist_ok=True)
df_final.to_csv(OUTPUT_CSV, index=False)

days = (df_final['Open_Time'].max() - df_final['Open_Time'].min()).days
done = days >= 365*5 - 30

if done and os.path.exists(PROGRESS_CSV):
    os.remove(PROGRESS_CSV)

print()
print("=" * 55)
print("  HASIL")
print("=" * 55)
print("Source : Binance API (data-api.binance.vision)")
print("Rows   : {:,}".format(len(df_final)))
print("Start  : {}".format(df_final['Open_Time'].min()))
print("End    : {}".format(df_final['Open_Time'].max()))
print("Cover  : {} hari ({:.1f} tahun)".format(days, days/365.25))
if done:
    print("Status : SUKSES - Data 5 Tahun dari Binance API!")
else:
    print("Status : PARTIAL ({:.1f} dari 5 tahun) - Jalankan lagi untuk lanjut".format(days/365.25))
print("File   : " + OUTPUT_CSV)
