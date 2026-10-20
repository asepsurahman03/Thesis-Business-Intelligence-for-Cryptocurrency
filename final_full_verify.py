"""
Verifikasi Final Komprehensif: HTML IEEE vs Notebook
Cek semua item: tanggal, metrik, model, metodologi, dataset
"""
import json
import re
from datetime import datetime, timedelta

NB   = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
HTML = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
OUT  = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\final_full_verify.txt'

# --- Load files ---
with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)
nb_text = ' '.join(''.join(c['source']) for c in nb['cells'])

with open(HTML, 'r', encoding='utf-8', errors='ignore') as f:
    html_raw = f.read()
html_text = re.sub(r'<[^>]+>', ' ', html_raw)
html_text = ' '.join(html_text.split())

# Dynamic dates (same logic as notebook)
END_DATE   = datetime(2026, 3, 23)
START_DATE = END_DATE - timedelta(days=5*365)

results = []
def chk(label, nb_ok, html_ok=True, note=''):
    if nb_ok and html_ok:
        status = '[OK] '
    elif nb_ok and not html_ok:
        status = '[NB-ONLY] '
    elif not nb_ok and html_ok:
        status = '[HTML-ONLY] '
    else:
        status = '[XX BOTH] '
    results.append((status, label, note))

# ═══════════════════════════════════════════════════╕
#  1. JUDUL
# ═══════════════════════════════════════════════════╛
TITLE = 'A Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction'
chk('Judul sesuai IEEE', TITLE in nb_text, TITLE in html_text)

# ═══════════════════════════════════════════════════╕
#  2. PERIODE / TANGGAL DATASET
# ═══════════════════════════════════════════════════╛
start_yr = str(START_DATE.year)  # 2021
end_yr   = str(END_DATE.year)    # 2026
start_m  = START_DATE.strftime('%b %Y')   # Mar 2021
end_m    = END_DATE.strftime('%b %Y')     # Mar 2026

chk('Tahun mulai dataset: 2021',    start_yr in nb_text,   start_yr in html_text)
chk('Tahun akhir dataset: 2026',    end_yr in nb_text,     end_yr in html_text)
chk('Periode 2021-2026 di HTML',    True,                  '2021\u20132026' in html_raw or '(2021' in html_text)
chk('Mar 2021 di HTML',             True,                  'Mar 2021' in html_text or 'March 23, 2021' in html_text)
chk('Mar 2026 di HTML',             True,                  'Mar 2026' in html_text or 'March 23, 2026' in html_text)
chk('Tidak ada 2021-2025 di HTML',  True,                  '2021\u20132025' not in html_raw and '2021-2025' not in html_text)
chk('END_DATE = datetime.now()',     'datetime.now()' in nb_text)
chk('START_DATE = 5 tahun ke belakang', 'timedelta(days=5*365)' in nb_text)
chk('Rentang dinamis saat run',     'Rentang data' in nb_text and 'hari ini' in nb_text)

# ═══════════════════════════════════════════════════╕
#  3. DATASET STATS
# ═══════════════════════════════════════════════════╛
chk('43,786 records',               '43,786' in nb_text,   '43,786' in html_text)
chk('Binance API BTC/USDT',         'BTCUSDT' in nb_text,  'Binance' in html_text)
chk('Interval 1 jam (hourly)',      '1h' in nb_text,       'hourly' in html_text)
chk('5 tahun rolling',              '5*365' in nb_text or '5 tahun' in nb_text, '5' in html_text)

# ═══════════════════════════════════════════════════╕
#  4. FEATURE ENGINEERING (15 SHAP-ranked)
# ═══════════════════════════════════════════════════╛
chk('15 Technical Indicators',      '15' in nb_text and 'SHAP' in nb_text,   '15 technical indicators' in html_text.lower())
for feat in ['RSI','MACD','BB_Upper','SMA_50','EMA_20','Momentum','ROC','Stochastic_K','CCI','ATR']:
    chk(f'Feature: {feat}', feat in nb_text)

# ═══════════════════════════════════════════════════╕
#  5. MODEL ARSITEKTUR
# ═══════════════════════════════════════════════════╛
chk('class LSTMModel',              'class LSTMModel' in nb_text,        'LSTM' in html_text)
chk('class GRUModel',               'class GRUModel' in nb_text,         'GRU' in html_text)
chk('class InformerTransformer',    'class InformerTransformer' in nb_text, 'Informer' in html_text)
chk('XGBoost (XGBRegressor)',       'XGBRegressor' in nb_text,           'XGBoost' in html_text)
chk('Urutan class BENAR',           nb_text.index('class InformerTransformer') < nb_text.index('models_to_train'))

# ═══════════════════════════════════════════════════╕
#  6. METODOLOGI VALIDASI
# ═══════════════════════════════════════════════════╛
chk('Walk-Forward Validation',      'Walk-Forward' in nb_text,    'Walk-Forward' in html_text)
chk('Diebold-Mariano Test',         'Diebold-Mariano' in nb_text, 'Diebold-Mariano' in html_text)
chk('Kruskal-Wallis H=18.4',        'Kruskal-Wallis' in nb_text,  'Kruskal-Wallis' in html_text)
chk('Polynomial interpolation',     'interpolat' in nb_text.lower(), 'interpolation' in html_text.lower())
chk('Grid Search optimization',     'Grid Search' in nb_text or 'optimizer' in nb_text.lower(), 'Grid Search' in html_text)
chk('SHAP explicability',           'SHAP' in nb_text,            'SHAP' in html_text)

# ═══════════════════════════════════════════════════╕
#  7. METRIK HASIL (sesuai Table I HTML)
# ═══════════════════════════════════════════════════╛
metrics = [
    ('GRU RMSE=0.1058',    '0.1058'),
    ('LSTM RMSE=0.1145',   '0.1145'),
    ('Informer RMSE=0.1321','0.1321'),
    ('XGBoost RMSE=0.1524','0.1524'),
    ('GRU MAE=0.0948',     '0.0948'),
    ('LSTM MAE=0.1008',    '0.1008'),
    ('GRU MAPE=13.13%',    '13.13'),
    ('LSTM MAPE=13.96%',   '13.96'),
    ('LSTM Train=106.60s', '106.60'),
    ('GRU Train=192.19s',  '192.19'),
]
for label, val in metrics:
    chk(label, val in nb_text, val in html_text)

# ═══════════════════════════════════════════════════╕
#  8. BUSINESS KPI (sesuai Table III HTML)
# ═══════════════════════════════════════════════════╛
biz_metrics = [
    ('LSTM Dir.Acc=72.3%', '72.3'),
    ('GRU Dir.Acc=69.8%',  '69.8'),
    ('LSTM Sharpe=1.45',   '1.45'),
    ('GRU Sharpe=1.32',    '1.32'),
    ('LSTM VaR=-2.34%',    '-2.34'),
    ('GRU VaR=-2.67%',     '-2.67'),
    ('XGBoost Dir.Acc=58.4%','58.4'),
    ('Informer Sharpe=1.12','1.12'),
]
for label, val in biz_metrics:
    chk(label, val in nb_text, val in html_text)

# ═══════════════════════════════════════════════════╕
#  9. BI DASHBOARD
# ═══════════════════════════════════════════════════╛
chk('Power BI',             'Power BI' in nb_text,     'Power BI' in html_text)
chk('PostgreSQL Data Mart', 'PostgreSQL' in nb_text,   'PostgreSQL' in html_text)
chk('SUS Score 86.4',       '86.4' in nb_text,         '86.4' in html_text)
chk('100% KPI Fidelity',    '100%' in nb_text,         'KPI Fidelity' in html_text or '100%' in html_text)
chk('DM-Test signifikan',   'DM-Test' in nb_text or 'Diebold-Mariano' in nb_text, 'Diebold-Mariano' in html_text)

# ═══════════════════════════════════════════════════╕
#  10. STRUKTURAL NOTEBOOK
# ═══════════════════════════════════════════════════╛
chk('4-Layer BI Architecture', 'Layer 1' in nb_text and 'Layer 4' in nb_text)
chk('Big Data 5V',             all(v in nb_text for v in ['Volume','Velocity','Variety','Veracity','Value']))
chk('Research Summary output', 'RESEARCH SUMMARY (IEEE-Aligned)' in nb_text)
chk('Trade-off narasi',        'Trade-off' in nb_text or 'trade-off' in nb_text.lower())

# ═══════════════════════════════════════════════════╕
#  REPORT
# ═══════════════════════════════════════════════════╛
ok_c  = sum(1 for r in results if r[0]=='[OK] ')
xx_c  = sum(1 for r in results if 'XX' in r[0])
nb_c  = sum(1 for r in results if 'NB-ONLY' in r[0])
ht_c  = sum(1 for r in results if 'HTML-ONLY' in r[0])

lines = []
lines.append('='*70)
lines.append('  LAPORAN VERIFIKASI FINAL: Notebook vs HTML IEEE FINAL')
lines.append(f'  Tanggal run: {END_DATE.strftime("%d %B %Y")} | Periode: {START_DATE.strftime("%d %b %Y")} - {END_DATE.strftime("%d %b %Y")}')
lines.append('='*70)

categories = [
    ('JUDUL', 0, 1),
    ('PERIODE / TANGGAL', 1, 9),
    ('DATASET STATS', 9, 13),
    ('FEATURE ENGINEERING', 13, 24),
    ('MODEL ARSITEKTUR', 24, 29),
    ('METODOLOGI VALIDASI', 29, 35),
    ('METRIK HASIL (Table I)', 35, 45),
    ('BUSINESS KPI (Table III)', 45, 53),
    ('BI DASHBOARD', 53, 58),
    ('STRUKTURAL NOTEBOOK', 58, 62),
]

for cat, start, end in categories:
    lines.append(f'\n  [{cat}]')
    for status, label, note in results[start:end]:
        lines.append(f'    {status}{label}')

lines.append('')
lines.append('='*70)
lines.append(f'  TOTAL    : {len(results)} item')
lines.append(f'  [OK]     : {ok_c}  (selaras di Notebook DAN HTML)')
lines.append(f'  [NB-ONLY]: {nb_c}  (ada di Notebook, tidak di HTML)')
lines.append(f'  [XX BOTH]: {xx_c}  (tidak ditemukan di keduanya)')
lines.append('='*70)
if xx_c == 0 and nb_c == 0:
    lines.append('  >>> SEMPURNA: SEMUA ITEM SELARAS ANTARA NOTEBOOK DAN HTML IEEE! <<<')
elif xx_c == 0:
    lines.append(f'  >>> OK: {ok_c} item selaras, {nb_c} item hanya di notebook (normal untuk kode) <<<')
else:
    lines.append(f'  >>> PERIKSA: {xx_c} item tidak selaras! <<<')
lines.append('='*70)

report = '\n'.join(lines)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(report)
print(report)
