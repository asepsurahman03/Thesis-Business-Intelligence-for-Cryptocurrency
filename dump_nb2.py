import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Focus on code cells with model training / accuracy related outputs
keywords = ['accuracy', 'mse', 'mae', 'rmse', 'loss', 'train', 'test', 'epoch', 'predict', 'fit', 'score', 'mape', 'r2', 'r_squared']

output_lines = []
for i, cell in enumerate(nb['cells']):
    cell_type = cell.get('cell_type', 'unknown')
    src = ''.join(cell.get('source', []))
    src_lower = src.lower()
    
    is_relevant = any(kw in src_lower for kw in keywords)
    
    if is_relevant or (cell_type == 'code' and cell.get('outputs')):
        output_lines.append("=" * 60)
        output_lines.append("CELL %d (%s)" % (i+1, cell_type))
        output_lines.append("=" * 60)
        output_lines.append(src[:3000])
        
        if cell_type == 'code' and cell.get('outputs'):
            output_lines.append("--- OUTPUT ---")
            for out in cell['outputs']:
                otype = out.get('output_type', '')
                if otype == 'stream':
                    txt = ''.join(out.get('text', []))
                    output_lines.append(txt[:2000])
                elif otype in ('execute_result', 'display_data'):
                    data = out.get('data', {})
                    if 'text/plain' in data:
                        txt = ''.join(data['text/plain'])
                        output_lines.append(txt[:2000])
        output_lines.append("")

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\nb_analysis.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Done. Total cells:", len(nb['cells']))
