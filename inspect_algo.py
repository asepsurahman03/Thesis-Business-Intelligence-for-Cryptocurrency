from bs4 import BeautifulSoup

with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
pseudo = soup.find(class_='pseudo')
if pseudo:
    raw = str(pseudo)
    # Print in chunks of 300
    for i in range(0, min(len(raw), 3000), 300):
        print(f"--- chars {i}-{i+300} ---")
        print(raw[i:i+300])
        print()
