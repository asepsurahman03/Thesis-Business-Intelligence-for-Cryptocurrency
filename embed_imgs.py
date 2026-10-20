import base64
import re
import os

html_file = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"
base_dir = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

def repl(match):
    src = match.group(1)
    if src.startswith('data:') or src.startswith('http'): 
        return match.group(0)
        
    img_name = src.split('/')[-1]
    img_path = os.path.join(base_dir, img_name)
    
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        ext = img_name.split('.')[-1].lower()
        mime = 'image/png' if ext == 'png' else 'image/jpeg'
        return f'src="data:{mime};base64,{b64}"'
    else:
        print(f"Warning: {img_path} not found.")
    return match.group(0)

new_html = re.sub(r'src="([^"]+)"', repl, html)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Images successfully embedded into HTML as Base64!")
