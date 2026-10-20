import os, glob

folder = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
updated_count = 0

for filepath in glob.glob(os.path.join(folder, '*')):
    if not (filepath.endswith('.md') or filepath.endswith('.html')):
        continue
        
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
        
    content = original
    
    # Update LSTM values
    content = content.replace('0.1145', '0.1145')
    content = content.replace('0.1008', '0.1008')
    content = content.replace('13.96%', '13.96%')
    content = content.replace('106.60', '106.60')
    
    # Update GRU values
    content = content.replace('0.1058', '0.1058')
    content = content.replace('0.0948', '0.0948')
    content = content.replace('13.13%', '13.13%')
    content = content.replace('192.19', '192.19')

    # Fix narrative based on new stats
    # Old narrative: GRU was more accurate, though LSTM was 85.59 seconds faster in training
    # New narrative: LSTM was 85.59 seconds faster in training
    content = content.replace('was more accurate, though LSTM was 85.59 seconds faster in training', 'was more accurate, though LSTM was 85.59 seconds faster in training')
    content = content.replace('while LSTM offered faster training times by approximately 44%', 'while LSTM offered faster training times by approximately 44%')
    
    # Update percentage improvement in RMSE: (0.1145 - 0.1058) / 0.1145 * 100 = 7.6%
    content = content.replace('7.6% improvement in RMSE', '7.6% improvement in RMSE')
    
    # Update 5 years to 5 years (and indonesian equivalents)
    # Be careful not to replace something unintentionally.
    content = content.replace('5 years', '5 years')
    content = content.replace('5-year', '5-year')
    content = content.replace('5 tahun', '5 tahun')
    content = content.replace('43,800', '43,800')
    content = content.replace('43.800', '43.800')
    content = content.replace('43k+', '43k+')
    
    # There was also some mention of data size:
    content = content.replace('43,801', '43,801')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {os.path.basename(filepath)}')
        updated_count += 1

print(f'\nTotal files updated: {updated_count}')
