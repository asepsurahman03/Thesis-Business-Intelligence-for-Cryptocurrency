import os, re
folder = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
out = []
for f in os.listdir(folder):
    if f.endswith('.md') or f.endswith('.html'):
        path = os.path.join(folder, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            t = file.read()
            # print all instances of RMSE, MAE, MAPE, LSTM, GRU + nearby context with numbers
            matches = re.finditer(r'(.{0,30}(?:RMSE|MAE|MAPE|17500|43800|43,800|43,800|5 tahun|5 tahun|5 years|5 years|LSTM|GRU).{0,30})', t, re.IGNORECASE)
            lines = []
            for m in matches:
                c = m.group(0).replace('\n', ' ')
                if any(char.isdigit() for char in c):  # only lines with numbers (potentially old values)
                    lines.append(c)
            # Remove duplicates
            lines = list(set(lines))
            if lines:
                out.append(f'--- {f} ---')
                out.extend(lines[:20]) # Limit to 20 unique lines per file
                out.append('')

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\report_check.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print("Done writing to report_check.txt")
