import base64

html_file = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html'
img_file = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\04_Visualizations\btc_5year_trend.png'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

with open(img_file, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

# Find the figure 1 caption
caption_idx = text.find('<div class="figure-caption">Fig. 1. Hourly closing')
if caption_idx != -1:
    # Find the preceding <img tag
    img_start_idx = text.rfind('<img src=', 0, caption_idx)
    
    # from img_start_idx, find the first '>'
    img_end_idx = text.find('>', img_start_idx)
    
    if img_start_idx != -1 and img_end_idx != -1 and img_end_idx < caption_idx:
        new_img_tag = f'<img src="data:image/png;base64,{b64}"'
        
        # Replace the entire tag efficiently
        new_text = text[:img_start_idx] + new_img_tag + text[img_end_idx:]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Successfully replaced Figure 1 image!")
    else:
        print("Could not find preceding img tag limits.")
else:
    print("Could not find Figure 1 caption.")
