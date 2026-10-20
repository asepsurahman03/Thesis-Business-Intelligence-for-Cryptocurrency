import os, glob, re

folder = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
updated = 0

replacements = {
    # LSTM metrics
    '0.0725': '0.1145', '0,0725': '0,1145',
    '0.0689': '0.1145', '0,0689': '0,1145',
    '8.75%': '13.96%', '8,75%': '13,96%',
    '7.84%': '13.96%', '7,84%': '13,96%',
    '139.10': '106.60', '139,10': '106,60', '139s': '106s',
    '166.1s': '106.6s',
    '0.0629': '0.1008', '0,0629': '0,1008',
    '0.1008': '0.1008', '0,0508': '0,1008',

    # GRU metrics
    '0.0678': '0.1058', '0,0678': '0,1058',
    '0.0818': '0.1058', '0,0818': '0,1058',
    '8.31%': '13.13%', '8,31%': '13,13%',
    '9.38%': '13.13%', '9,38%': '13,13%',
    '241.12': '192.19', '241,12': '192,19', '241s': '192s',
    '168.2s': '192.2s',
    '0.0751': '0.0948', '0,0751': '0,0948',
    '0.0948': '0.0948', '0,0378': '0,0948',
    
    # Text changes
    '42% faster': '44% faster',
    'unggulan GRU (RMSE: 0,0678': 'unggulan GRU (RMSE: 0,1058',
    'sedikit lebih cepat': 'sekitar 85 detik lebih cepat',
    '25% lebih efisien': '44% lebih lama melatih',
    'LSTM unggul dalam 4 dari 5 metri': 'GRU unggul di akurasi namun LSTM lebih cepat',
    '4 dari 5 m': 'akurasi (sebaliknya GRU unggul)',
    'Error rata-rata LSTM lebih rendah 19.3%': 'Error RMSE GRU lebih rendah 7.6% dibanding LSTM'
}

for filepath in glob.glob(os.path.join(folder, '*')):
    if not (filepath.endswith('.md') or filepath.endswith('.html')):
        continue
        
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
        
    content = original
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")
        updated += 1

print(f"Total updated files: {updated}")
