html_file = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"

with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Fix Equation 4 specifically (form feed \f and backspace \b in bar)
target = '$$ \sigma_t = \sqrt{\x0crac{1}{n} \sum (\Delta P_i - \x08ar{P})^2} \eqno{(4)} $$'
replacement = r'$$ \sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2} \eqno{(4)} $$'

html = html.replace(target, replacement)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Equation 4 specifically fixed.")
