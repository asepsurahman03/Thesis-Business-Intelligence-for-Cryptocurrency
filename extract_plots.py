import nbformat
import base64
import os

notebook_path = r'e:/Nusa Putra/S2/Semester 1/Big Data Analysis/Penelitian/Analisis Bit Coin/02_Notebooks/Bitcoin_BigData_Analysis_MasterClass.ipynb'
output_dir = r'e:/Nusa Putra/S2/Semester 1/Big Data Analysis/Penelitian/Analisis Bit Coin/04_Visualizations'

os.makedirs(output_dir, exist_ok=True)

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

image_count = 0
for cell in nb.cells:
    if cell.cell_type == 'code' and 'outputs' in cell:
        cell_images = []
        for output in cell.outputs:
            if 'data' in output and 'image/png' in output['data']:
                cell_images.append(output['data']['image/png'])
        
        source = "".join(cell.source).lower()
        
        for i, image_data in enumerate(cell_images):
            image_bytes = base64.b64decode(image_data)
            
            filename = None
            
            # Logic based on source content and image index in cell
            if 'visualisasi tren 5 tahun' in source or 'historical performance' in source:
                filename = 'btc_5year_trend.png'
            elif ('actual' in source or 'forecast' in source) and 'residual' in source:
                if i == 0:
                    filename = 'forecast_comparison.png'
                else:
                    filename = 'residual_analysis.png'
            elif 'actual' in source or 'forecast' in source or 'perbandingan' in source:
                filename = 'forecast_comparison.png'
            elif 'residual' in source or 'error distribution' in source:
                filename = 'residual_analysis.png'
            
            if not filename:
                image_count += 1
                filename = f'plot_{image_count}.png'
            
            target_path = os.path.join(output_dir, filename)
            with open(target_path, 'wb') as img_file:
                img_file.write(image_bytes)
            print(f"Saved: {filename} to {target_path}")
