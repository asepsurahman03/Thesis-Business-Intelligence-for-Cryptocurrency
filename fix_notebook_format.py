"""
Tulis ulang cell data loading di notebook dengan format yang benar.
Format .ipynb: source adalah list of strings, setiap string = satu baris + newline
"""
import json

notebook_path = "02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# ============================================================
# Kode baru yang benar untuk cell Data Loading
# Setiap baris adalah item TERPISAH dalam list
# Diakhiri \n (kecuali baris terakhir)
# ============================================================
new_source = [
    "# ============================================================\n",
    "# Data Loading — Big Data Volume Characteristic\n",
    "# ============================================================\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "print(\"Loading Bitcoin 5-Year Hourly Data...\")\n",
    "df = pd.read_csv('../01_Data/btc_5year_hourly_bigdata.csv')\n",
    "\n",
    "# Data preprocessing\n",
    "df['Timestamp'] = pd.to_datetime(df['Open_Time'])\n",
    "df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)  # Hapus timezone jika ada\n",
    "df.set_index('Timestamp', inplace=True)\n",
    "df.drop('Open_Time', axis=1, inplace=True)\n",
    "\n",
    "# Validasi rentang 5 tahun dari sekarang ke belakang\n",
    "end_date = datetime.now()\n",
    "start_date_5y = end_date - timedelta(days=5*365)\n",
    "\n",
    "# Filter data hanya 5 tahun terakhir dari sekarang\n",
    "df = df[df.index >= pd.Timestamp(start_date_5y)]\n",
    "df = df[df.index <= pd.Timestamp(end_date)]\n",
    "\n",
    "print(f\"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns\")\n",
    "print(f\"Periode 5 Tahun: {start_date_5y.strftime('%Y-%m-%d')} s/d {end_date.strftime('%Y-%m-%d')}\")\n",
    "print(f\"Date range aktual: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}\")\n",
    "print(f\"Columns: {list(df.columns)}\")\n",
    "print()\n",
    "\n",
    "def apply_technical_indicators(df):\n",
    "    # Moving Averages\n",
    "    df['MA7'] = df['Close'].rolling(window=7).mean()\n",
    "    df['MA25'] = df['Close'].rolling(window=25).mean()\n",
    "    \n",
    "    # Kalkulasi RSI\n",
    "    delta = df['Close'].diff()\n",
    "    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()\n",
    "    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()\n",
    "    df['RSI'] = 100 - (100 / (1 + gain/loss))\n",
    "    \n",
    "    # Kalkulasi MACD\n",
    "    exp1 = df['Close'].ewm(span=12, adjust=False).mean()\n",
    "    exp2 = df['Close'].ewm(span=26, adjust=False).mean()\n",
    "    df['MACD'] = exp1 - exp2\n",
    "    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()\n",
    "    \n",
    "    # Volatilitas & Return\n",
    "    df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))\n",
    "    df['Volatility'] = df['Close'].rolling(window=24).std()\n",
    "    \n",
    "    # Bollinger Bands\n",
    "    df['BB_Mid'] = df['Close'].rolling(window=20).mean()\n",
    "    df['BB_Upper'] = df['BB_Mid'] + 2 * df['Close'].rolling(window=20).std()\n",
    "    df['BB_Lower'] = df['BB_Mid'] - 2 * df['Close'].rolling(window=20).std()\n",
    "    \n",
    "    return df.dropna()\n",
    "\n",
    "df = apply_technical_indicators(df)\n",
    "print(f\"Feature Engineering Completed. Final Dimensions: {df.shape}\")"
]

# Cari cell yang berisi data loading (cell index 6)
target_cell_idx = None
for i, cell in enumerate(nb['cells']):
    src_text = ''.join(cell.get('source', []))
    if "btc_5year_hourly_bigdata.csv" in src_text and "apply_technical_indicators" in src_text:
        target_cell_idx = i
        print(f"Ditemukan cell target: index {i} (cell ke-{i+1})")
        break

if target_cell_idx is None:
    print("ERROR: Cell target tidak ditemukan!")
else:
    # Verifikasi format new_source
    print(f"Jumlah baris baru: {len(new_source)}")
    print("Contoh baris pertama:", repr(new_source[0]))
    print("Contoh baris ke-4:", repr(new_source[3]))
    
    # Terapkan
    nb['cells'][target_cell_idx]['source'] = new_source
    nb['cells'][target_cell_idx]['outputs'] = []
    nb['cells'][target_cell_idx]['execution_count'] = None
    
    # Simpan
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"\nNotebook disimpan: {notebook_path}")
    
    # Verifikasi akhir
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb2 = json.load(f)
    
    cell_src = nb2['cells'][target_cell_idx]['source']
    print(f"\nVerifikasi format cell yang sudah diperbaiki:")
    print(f"  Type: {type(cell_src)}")
    print(f"  Jumlah items: {len(cell_src)}")
    print(f"  Item[0]: {repr(cell_src[0])}")
    print(f"  Item[3]: {repr(cell_src[3])}")
    print(f"  Item[4]: {repr(cell_src[4])}")
    print(f"  Item[5]: {repr(cell_src[5])}")
    
    # Cek apakah ada \\n literal yang salah
    has_bad_format = any('\\\\n' in item for item in cell_src)
    print(f"\nFormat salah (ada literal \\\\n): {has_bad_format}")
    print("\nSELESAI!")
