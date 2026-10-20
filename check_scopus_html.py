import os, re
folder = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports'
files = ['Scopus_Manuscript_Dashboard.html', 'Scopus_Manuscript_Dashboard_ID.html']
out = []
for f in files:
    path = os.path.join(folder, f)
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    out.append(f'=== {f} ===')
    
    abstract = re.search(r'(?s)Abstract.*?</p>', content, re.I)
    if abstract: out.append('Abstract:\n' + abstract.group(0))
    
    abstrak = re.search(r'(?s)Abstrak.*?</p>', content, re.I)
    if abstrak: out.append('Abstrak:\n' + abstrak.group(0))
    
    concl = re.search(r'(?s)Conclusion.*?</p>', content, re.I)
    if concl: out.append('Conclusion:\n' + concl.group(0))

    kesimpulan = re.search(r'(?s)Kesimpulan.*?</p>', content, re.I)
    if kesimpulan: out.append('Kesimpulan:\n' + kesimpulan.group(0))
    
    table_rows = re.findall(r'<tr.*?>.*?LSTM.*?</tr>|<tr.*?>.*?GRU.*?</tr>', content, re.I | re.DOTALL)
    out.append('Table Rows:\n' + '\n'.join(table_rows[:4]))
    out.append('\n')

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\check_html_content.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(out))
print('Done!')
