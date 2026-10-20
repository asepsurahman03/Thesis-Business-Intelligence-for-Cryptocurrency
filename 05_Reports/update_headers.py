import os
import re
from bs4 import BeautifulSoup

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Draft_Tesis_Lengkap.html'

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Update CSS for H3 numbering just in case
style_tag = soup.find('style')
if style_tag and 'subsubbab' not in style_tag.text:
    css = style_tag.string
    css += """
        h2 { counter-reset: subsubbab; }
        h3 { font-size: 11pt; font-weight: bold; text-align: left; margin-top: 15px; margin-bottom: 5px; }
        h3::before { counter-increment: subsubbab; content: counter(bab) "." counter(subbab) "." counter(subsubbab) " "; }
    """
    style_tag.string = css

all_h1 = soup.find_all('h1')

# Because we added front matter (PERNYATAAN ORISINALITAS, HALAMAN PENGESAHAN, KATA PENGANTAR, ABSTRAK, ABSTRACT, DAFTAR ISI, LAMPIRAN)
# We need to skip them when updating thesis chapters.
# The thesis chapters start around the 8th H1 if we count sequentially.
# The IEEE sections we extracted earlier:
# 0 Perkenalan -> PENDAHULUAN
# 1 Tinjauan Pustaka dan Pekerjaan Terkait -> TINJAUAN PUSTAKA
# 2 Arsitektur Sistem dan Desain Kerangka -> METODOLOGI PENELITIAN 
# 3 Rekayasa Fitur dan Analisis SHAP -> change to h2
# 4 Formulasi Algoritma -> change to h2
# 5 Hasil Empiris dan Analisis Kritis -> HASIL DAN PEMBAHASAN
# 6 Diskusi -> change to h2
# 7 Kesimpulan -> KESIMPULAN DAN SARAN
# 8 Pengakuan -> delete section
# 9 Referensi -> DAFTAR PUSTAKA

def downgrade_h2_to_h3_under(h1_node):
    # Find all h2 nodes between this h1 and the next h1 (or end)
    curr = h1_node.find_next_sibling()
    while curr and curr.name != 'h1':
        if curr.name == 'h2':
            curr.name = 'h3'
        curr = curr.find_next_sibling()

# Let's map target H1 texts
for h1 in all_h1:
    text = h1.text.strip().lower()
    text = text.replace('\n', ' ')
    
    if 'perkenalan' in text or 'introduction' in text:
        h1.string = "PENDAHULUAN"
    elif 'tinjauan pustaka' in text or 'pekerjaan terkait' in text:
        h1.string = "TINJAUAN PUSTAKA"
    elif 'arsitektur sistem' in text or 'desain kerangka' in text:
        h1.string = "METODOLOGI PENELITIAN"
    elif 'rekayasa fitur' in text or 'shap' in text:
        # Change to H2
        downgrade_h2_to_h3_under(h1)
        h1.name = 'h2'
        h1.string = "Rekayasa Fitur dan Analisis SHAP"
    elif 'formulasi algoritma' in text:
        # Change to H2
        downgrade_h2_to_h3_under(h1)
        h1.name = 'h2'
        h1.string = "Formulasi Algoritma"
    elif 'hasil empiris' in text or 'analisis kritis' in text:
        h1.string = "HASIL DAN PEMBAHASAN"
    elif 'diskusi' in text:
        downgrade_h2_to_h3_under(h1)
        h1.name = 'h2'
        h1.string = "Diskusi Analisis"
    elif 'kesimpulan' in text:
        h1.string = "KESIMPULAN DAN SARAN"
    elif 'pengakuan' in text:
        # Delete Pengakuan and its P tags until next H1
        curr = h1.find_next_sibling()
        while curr and curr.name != 'h1':
            nxt = curr.find_next_sibling()
            curr.decompose()
            curr = nxt
        h1.decompose()
    elif 'referensi' in text:
        h1.string = "DAFTAR PUSTAKA"

# Save
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))
