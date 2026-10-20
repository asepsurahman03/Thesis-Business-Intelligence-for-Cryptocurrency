"""
Script untuk mengupdate notebook .ipynb agar:
1. Data loading cell menggunakan validasi 5 tahun dari sekarang ke belakang
2. Menampilkan rentang tanggal yang benar
"""
import json
import os
from datetime import datetime, timedelta

notebook_path = "02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb"

# Tanggal sekarang dan 5 tahun lalu
now = datetime.now()
five_years_ago = now - timedelta(days=5*365)

print(f"Memperbarui notebook: {notebook_path}")
print(f"Tanggal sekarang: {now.strftime('%Y-%m-%d')}")
print(f"5 tahun lalu: {five_years_ago.strftime('%Y-%m-%d')}")

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")

# ============================================================
# UPDATE CELL: Data Loading
# ============================================================
# Source baru untuk cell loading data dengan validasi 5 tahun
new_data_loading_source = [
    "# ============================================================\\n",
    "# Data Loading — Big Data Volume Characteristic\\n",
    "# ============================================================\\n",
    "from datetime import datetime, timedelta\\n",
    "\\n",
    "print(\\\"Loading Bitcoin 5-Year Hourly Data...\\\")\\n",
    "df = pd.read_csv('../01_Data/btc_5year_hourly_bigdata.csv')\\n",
    "\\n",
    "# Data preprocessing\\n",
    "df['Timestamp'] = pd.to_datetime(df['Open_Time'])\\n",
    "df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)  # Hapus timezone jika ada\\n",
    "df.set_index('Timestamp', inplace=True)\\n",
    "df.drop('Open_Time', axis=1, inplace=True)\\n",
    "\\n",
    "# Validasi rentang 5 tahun dari sekarang ke belakang\\n",
    "end_date = datetime.now()\\n",
    "start_date_5y = end_date - timedelta(days=5*365)\\n",
    "\\n",
    "# Filter data hanya 5 tahun terakhir dari sekarang\\n",
    "df = df[df.index >= pd.Timestamp(start_date_5y)]\\n",
    "df = df[df.index <= pd.Timestamp(end_date)]\\n",
    "\\n",
    "print(f\\\"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\\\")\\n",
    "print(f\\\"Periode 5 Tahun: {start_date_5y.strftime('%Y-%m-%d')} s/d {end_date.strftime('%Y-%m-%d')}\\\")\\n",
    "print(f\\\"Date range aktual: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}\\\")\\n",
    "print(f\\\"Columns: {list(df.columns)}\\\")\\n",
    "print()\\n",
    "\\n",
    "def apply_technical_indicators(df):\\n",
    "    # Moving Averages\\n",
    "    df['MA7'] = df['Close'].rolling(window=7).mean()\\n",
    "    df['MA25'] = df['Close'].rolling(window=25).mean()\\n",
    "    \\n",
    "    # Kalkulasi RSI\\n",
    "    delta = df['Close'].diff()\\n",
    "    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()\\n",
    "    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()\\n",
    "    df['RSI'] = 100 - (100 / (1 + gain/loss))\\n",
    "    \\n",
    "    # Kalkulasi MACD\\n",
    "    exp1 = df['Close'].ewm(span=12, adjust=False).mean()\\n",
    "    exp2 = df['Close'].ewm(span=26, adjust=False).mean()\\n",
    "    df['MACD'] = exp1 - exp2\\n",
    "    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()\\n",
    "    \\n",
    "    # Volatilitas & Return\\n",
    "    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))\\n",
    "    df['Volatility'] = df['Close'].rolling(window=24).std()\\n",
    "    \\n",
    "    # Bollinger Bands\\n",
    "    df['BB_Mid'] = df['Close'].rolling(window=20).mean()\\n",
    "    df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(window=20).std()\\n",
    "    df['BB_Lower'] = df['BB_Mid'] - 2 * df['Close'].rolling(window=20).std()\\n",
    "    \\n",
    "    return df.dropna()\\n",
    "\\n",
    "df = apply_technical_indicators(df)\\n",
    "print(f\\\"Feature Engineering Completed. Final Dimensions: {df.shape}\\\")"
]

# ============================================================
# Cari dan update cells yang relevan
# ============================================================
updated_cells = 0

for i, cell in enumerate(nb['cells']):
    source = cell.get('source', [])
    source_text = ''.join(source)
    
    # Update cell data loading
    if "df = pd.read_csv('../01_Data/btc_5year_hourly_bigdata.csv')" in source_text and "apply_technical_indicators" in source_text:
        print(f"\nMemperbarui cell {i+1}: Data Loading & Feature Engineering")
        nb['cells'][i]['source'] = new_data_loading_source
        # Clear outputs
        if 'outputs' in nb['cells'][i]:
            nb['cells'][i]['outputs'] = []
        nb['cells'][i]['execution_count'] = None
        updated_cells += 1
    
    # Update cell markdown: Layer 1 dengan info tanggal
    if "Binance API" in source_text and "43,786 records hourly" in source_text:
        print(f"\nMemperbarui cell {i+1}: Markdown - Layer 1 info")
        actual_records = 43786  # jumlah baris aktual
        start_str = five_years_ago.strftime('%d-%b-%Y')
        end_str = now.strftime('%d-%b-%Y')
        
        new_source = []
        for line in source:
            if "43,786 records hourly" in line:
                line = line.replace("43,786 records hourly", f"~{actual_records:,} records hourly")
            new_source.append(line)
        nb['cells'][i]['source'] = new_source
        updated_cells += 1
    
    # Update markdown yang menyebut "Dataset 5 tahun Bitcoin hourly (~43,786 records)"  
    if "43,786 records" in source_text:
        print(f"\nMemperbarui cell {i+1}: Referensi jumlah records")
        actual_records = 43786
        new_source = []
        for line in source:
            if "43,786 records" in line:
                line = line.replace("43,786 records", f"~{actual_records:,} records")
            new_source.append(line)
        nb['cells'][i]['source'] = new_source
        updated_cells += 1
    
    # Update Title cell jika menyebut tanggal spesifik
    if "Bitcoin (BTC) 5-Year Historical Performance" in source_text:
        print(f"\nDitemukan cell {i+1}: Visualisasi title (tidak perlu diubah - sudah dinamis)")

print(f"\nTotal cells diperbarui: {updated_cells}")

# ============================================================
# Simpan notebook
# ============================================================
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook berhasil disimpan: {notebook_path}")
print("SELESAI!")
