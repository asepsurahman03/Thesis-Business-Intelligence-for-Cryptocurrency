import json
import sys

with open('02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print('Cells count:', len(nb['cells']))
for idx, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    for kw in ['fold', 'feature', 'shap', 'var', 'sharpe', 'adf', 'stationar', 'naive', 'arima', 'buy_and_hold', 'turnover', 'slippage', 'ethics', 'unp']:
        if kw in src.lower():
            first_line = src.strip().split('\n')[0]
            print(f'Cell {idx} ({cell["cell_type"]}) [kw: {kw}]: {first_line[:100]}')
            break
