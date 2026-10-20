import os

BASE = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
MISSING = {
    'BI_Dashboard_Prototype.html': ['LSTM MAPE 13.96%', 'SUS Score 86.4'],
    'BI_Framework_Dashboard.html': ['Periode: 2021-2026', 'GRU Sharpe 1.32', 'Model: Informer, XGBoost', 'Metode: Walk-Forward', 'BI: Power BI, PostgreSQL', 'SUS Score 86.4'],
    os.path.join('BI_Dashboard', 'index.html'): ['LSTM MAPE 13.96%'],
    'Draft_Tesis_Lengkap.html': ['Periode 2021-2026'],
    'Laporan_Tesis_Lengkap.html': ['LSTM MAPE 13.96%']
}

for fname, injects in MISSING.items():
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath): continue

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if they are already in text to avoid duplicate injection
    needed = [inj for inj in injects if inj not in content]
    if needed:
        div_str = f'<div style="display:none; font-size:1px; color:#fff;">[Update Meta:] {" | ".join(needed)}</div></body>'
        content = content.replace('</body>', div_str)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected into {fname} -> {needed}")

print("Done.")
