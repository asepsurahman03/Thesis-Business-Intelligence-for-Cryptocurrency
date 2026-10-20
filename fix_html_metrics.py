import os
import re

BASE = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
FILES = [
    os.path.join(BASE, 'BI_Dashboard_Prototype.html'),
    os.path.join(BASE, 'BI_Framework_Dashboard.html'),
    os.path.join(BASE, 'BI_Dashboard', 'index.html'),
    os.path.join(BASE, 'Draft_Tesis_Lengkap.html'),
    os.path.join(BASE, 'Laporan_Tesis_Lengkap.html'),
    os.path.join(BASE, 'Manuscript_IEEE_FINAL_2026_ID.html')
]

replacements = [
    # 1. Dates / Periods
    (r'1 Januari 2021 hingga 31 Desember 2025', '23 Maret 2021 hingga 23 Maret 2026'),
    (r'Januari 2021 dan Desember 2025', 'Maret 2021 dan Maret 2026'),
    (r'Jan 2021 [–\-] Des 2025', 'Mar 2021 – Mar 2026'),
    (r'2021\s*[–\-]\s*2025', '2021–2026'),
    (r'January 1, 2021, to December 31, 2025', 'March 23, 2021, to March 23, 2026'),
    (r'Jan 2021 and Dec 2025', 'Mar 2021 and Mar 2026'),
    (r'2023\s*[–\-]\s*2025 employing PatchTST', '2023–2026 employing PatchTST'),
    
    # 2. Add missing model names to Dashboards if they aren't there
    # (If a file doesn't have it, we might not easily insert it without breaking HTML. 
    # Let's focus on metric updates first).
    
    # 3. Fix exact RMSE / MAPE numbers
    (r'0\.1134\b', '0.1145'), # LSTM RMSE old
    (r'0,1134\b', '0,1145'),
    (r'14\.2%?', '13.96%'),  # LSTM MAPE old
    (r'13\.5%?', '13.13%'),  # GRU MAPE old
    (r'1\.72\b', '1.32'),    # GRU Sharpe old
    (r'1,72\b', '1,32'),
    (r'2\.85\b', '1.45'),    # LSTM Sharpe old
    (r'2,85\b', '1,45'),
    (r'68\.9%', '69.8%'),    # GRU Dir Acc old
    (r'64\.1%', '64.1%'),    # Informer Dir Acc
    (r'55\.7%', '64.1%'),    # Informer Dir Acc old
    (r'0\.1287\b', '0.1524'), # XGBoost RMSE old
    (r'0,1287\b', '0,1524'),
    
    # Time updates
    (r'106\.6s', '106.60s'),
    (r'192\.2s', '192.19s'),
]

for fpath in FILES:
    if not os.path.exists(fpath): continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig_content = content
    for old, new in replacements:
        content = re.sub(old, new, content)
        
    if content != orig_content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(fpath)}")
        
print("Replacement pass completed.")
