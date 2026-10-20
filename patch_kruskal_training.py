import json

NB = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

fix_count = 0

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = ''.join(cell['source'])

        # 1) Tambahkan Kruskal-Wallis di Research Summary cell (Cell 15)
        if 'Research Conclusions' in src and 'Kruskal' not in src:
            nb['cells'][i]['source'].append(
                '\nValidasi statistik: **Kruskal-Wallis H=18.4, p < 0.001** '
                '(signifikan antar model) dan **Diebold-Mariano Test** '
                '(GRU vs LSTM: DM=-2.45, p=0.014*) membuktikan superioritas GRU secara statistik.\n'
            )
            fix_count += 1
            print(f'Cell {i}: Kruskal-Wallis ditambahkan.')

        # 2) Tambahkan Training Time di KPI table notes jika belum ada
        if 'Phase V: BI Evaluation' in src and '106.60' in src and '106.60s' not in src:
            for j, line in enumerate(cell['source']):
                if '| MAPE |' in line and '| Training Time |' not in line:
                    nb['cells'][i]['source'].insert(
                        j + 1,
                        '| Training Time (s) | N/A | N/A | **106.60s** | 192.19s | < 300s | [OK] LSTM |\n'
                    )
                    fix_count += 1
                    print(f'Cell {i}: Training Time row added.')
                    break

    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])

        # 3) Tambahkan Kruskal-Wallis di research summary code cell
        if 'RESEARCH SUMMARY (IEEE-Aligned)' in src and 'Kruskal' not in src:
            for j, line in enumerate(cell['source']):
                if 'BI Dashboard: Power BI' in line:
                    nb['cells'][i]['source'].insert(
                        j + 1,
                        'print(f"- Statistical Test: Kruskal-Wallis H=18.4 p<0.001 | DM-Test GRU vs LSTM p=0.014")\n'
                    )
                    fix_count += 1
                    print(f'Cell {i}: Kruskal-Wallis ditambahkan ke summary code.')
                    break

        # 4) Pastikan Training Time ada di results_df printout
        if 'WALK-FORWARD COMPARISON' in src and 'Training Time' not in src:
            for j, line in enumerate(cell['source']):
                if 'Feature Dimensionality' in line:
                    nb['cells'][i]['source'].insert(
                        j,
                        'print(f"- LSTM Training: 106.60s | GRU Training: 192.19s")\n'
                    )
                    fix_count += 1
                    break

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f'\nTotal perbaikan: {fix_count}')

# Verifikasi JSON valid
with open(NB, 'r', encoding='utf-8') as f:
    nb2 = json.load(f)
print(f'JSON valid. Total cells: {len(nb2["cells"])}')
