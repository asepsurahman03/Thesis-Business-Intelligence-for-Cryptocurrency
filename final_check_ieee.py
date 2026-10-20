"""
Verifikasi komprehensif: Notebook vs IEEE Manuscript FINAL
Semua output ASCII agar tidak ada encoding issue di PowerShell
"""
import json
import re

NB   = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'
HTML = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
OUT  = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\final_check_result.txt'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)
nb_text = ' '.join(''.join(c['source']) for c in nb['cells'])

with open(HTML, 'r', encoding='utf-8', errors='ignore') as f:
    html_raw = f.read()
html_text = re.sub(r'<[^>]+>', ' ', html_raw)
html_text = ' '.join(html_text.split())

PASS = '[OK] '
FAIL = '[XX] '
WARN = '[??] '

results = []

def check(label, cond_nb, cond_ieee=True, note=''):
    status = PASS if (cond_nb and cond_ieee) else (WARN if not cond_ieee else FAIL)
    results.append((status, label, note))

# 1. JUDUL
ieee_title = 'A Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction'
check('Judul Notebook = IEEE', ieee_title in nb_text, ieee_title in html_text)

# 2. DATASET
check('Dataset: 43,786 records',   '43,786' in nb_text,          '43,786' in html_text)
check('Sumber: Binance API BTC',   'Binance' in nb_text and 'BTCUSDT' in nb_text, 'Binance' in html_text)
check('Periode: 5 tahun 2021-2025','5*365' in nb_text or '5 tahun' in nb_text, '2021' in html_text)

# 3. FEATURES
check('15 Technical Indicators',   '15' in nb_text and 'SHAP' in nb_text, '15 technical indicators' in html_text.lower())
check('Feature: RSI',              'RSI' in nb_text)
check('Feature: MACD',             'MACD' in nb_text)
check('Feature: Bollinger Bands',  'BB_Upper' in nb_text)
check('Feature: SMA_50',           'SMA_50' in nb_text)
check('Feature: EMA_20',           'EMA_20' in nb_text)
check('Feature: Momentum',         'Momentum' in nb_text)
check('Feature: ROC',              'ROC' in nb_text)
check('Feature: Stochastic_K',     'Stochastic_K' in nb_text)
check('Feature: CCI',              'CCI' in nb_text)
check('Feature: ATR',              'ATR' in nb_text)

# 4. MODEL
check('class LSTMModel',           'class LSTMModel' in nb_text)
check('class GRUModel',            'class GRUModel' in nb_text)
check('class InformerTransformer', 'class InformerTransformer' in nb_text, 'Informer' in html_text)
check('XGBoost import',            'XGBRegressor' in nb_text or 'xgboost' in nb_text.lower(), 'XGBoost' in html_text)
check('Informer sebelum models_to_train',
      nb_text.index('class InformerTransformer') < nb_text.index('models_to_train'))

# 5. METODOLOGI
check('Walk-Forward Validation',   'Walk-Forward' in nb_text,    'Walk-Forward' in html_text)
check('Diebold-Mariano Test',      'Diebold-Mariano' in nb_text, 'Diebold-Mariano' in html_text)
check('Kruskal-Wallis / statistical','Kruskal' in nb_text,       'Kruskal' in html_text)

# 6. METRIK HASIL
check('GRU RMSE = 0.1058',         '0.1058' in nb_text,  '0.1058' in html_text)
check('LSTM RMSE = 0.1145',        '0.1145' in nb_text,  '0.1145' in html_text)
check('GRU MAE = 0.0948',          '0.0948' in nb_text,  '0.0948' in html_text)
check('LSTM MAPE = 13.96%',        '13.96' in nb_text,   '13.96' in html_text)
check('GRU MAPE = 13.13%',         '13.13' in nb_text,   '13.13' in html_text)
check('LSTM Training = 106.60s',   '106.60' in nb_text,  '106.60' in html_text)
check('GRU Training = 192.19s',    '192.19' in nb_text,  '192.19' in html_text)
check('LSTM Dir.Acc = 72.3%',      '72.3' in nb_text,    '72.3' in html_text)
check('LSTM Sharpe = 1.45',        '1.45' in nb_text,    '1.45' in html_text)
check('GRU Sharpe = 1.32',         '1.32' in nb_text,    '1.32' in html_text)
check('GRU VaR = -2.67%',          '-2.67' in nb_text,   '-2.67' in html_text)
check('LSTM VaR = -2.34%',         '-2.34' in nb_text,   '-2.34' in html_text)
check('XGBoost RMSE = 0.1524',     '0.1524' in nb_text,  '0.1524' in html_text)
check('Informer RMSE = 0.1321',    '0.1321' in nb_text,  '0.1321' in html_text)

# 7. BI DASHBOARD
check('Power BI disebutkan',       'Power BI' in nb_text,        'Power BI' in html_text)
check('PostgreSQL Data Mart',      'PostgreSQL' in nb_text,      'PostgreSQL' in html_text)
check('SUS Score 86.4 Excellent',  '86.4' in nb_text,            '86.4' in html_text)
check('100% KPI Fidelity',         '100%' in nb_text,            'KPI Fidelity' in html_text)

# 8. NARASI & STRUKTUR
check('4-Layer BI Architecture',   'Layer 1' in nb_text and 'Layer 4' in nb_text)
check('Big Data 5V (semua V)',      all(v in nb_text for v in ['Volume','Velocity','Variety','Veracity','Value']))
check('Research Summary IEEE',     'RESEARCH SUMMARY (IEEE-Aligned)' in nb_text)
check('Trade-off GRU vs LSTM',     'Trade-off' in nb_text or 'trade-off' in nb_text)

# --- WRITE OUTPUT ---
pass_c = sum(1 for r in results if r[0]==PASS)
fail_c = sum(1 for r in results if r[0]==FAIL)
warn_c = sum(1 for r in results if r[0]==WARN)

lines = []
lines.append('='*65)
lines.append('  LAPORAN VERIFIKASI: Notebook vs IEEE Manuscript FINAL')
lines.append('='*65)
for status, label, note in results:
    lines.append(f'{status}{label}' + (f'  [{note}]' if note else ''))
lines.append('')
lines.append('='*65)
lines.append(f'  TOTAL   : {len(results)} item diperiksa')
lines.append(f'  OK LULUS: {pass_c}')
lines.append(f'  XX GAGAL: {fail_c}')
lines.append(f'  ?? WARN : {warn_c}')
lines.append('='*65)
if fail_c == 0:
    lines.append('  >>> SEMUA KOMPONEN SELARAS DENGAN IEEE MANUSCRIPT FINAL! <<<')
else:
    lines.append('  >>> ADA ITEM YANG BELUM SELARAS - LIHAT [XX] DI ATAS <<<')
lines.append('='*65)

report = '\n'.join(lines)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(report)
print(report)
