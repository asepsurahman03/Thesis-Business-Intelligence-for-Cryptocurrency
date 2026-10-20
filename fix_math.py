import re

html_file = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Equation 1 (tab \t and form feed \f issues)
html = re.sub(r'\$\$ X_\{.*?ext\{norm\}\} = .*?rac\{X - X_\{\\min\}\}\{X_\{\\max\} - X_\{\\min\}\} \\eqno\{\(1\)\} \$\$',
              r'$$ X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}} \eqno{(1)} $$', html)

# Fix Equation 3 (\t issue)
html = re.sub(r'\$\$ RSI = 100 - \\left\(.*?rac\{100\}\{1 \+ .*?rac\{EMA\(.*?ext\{Gain\}\)\}\{EMA\(.*?ext\{Loss\}\)\}\}\\right\) \\eqno\{\(3\)\} \$\$',
              r'$$ RSI = 100 - \left(\frac{100}{1 + \frac{EMA(\text{Gain})}{EMA(\text{Loss})}}\right) \eqno{(3)} $$', html)

# Fix Equation 4 (\f issue in \frac)
html = re.sub(r'\$\$ \\sigma_t = \\sqrt\{.*?rac\{1\}\{n\} \\sum \(\\Delta P_i - \\bar\{P\}\)\^2\} \\eqno\{\(4\)\} \$\$',
              r'$$ \sigma_t = \sqrt{\frac{1}{n} \sum (\Delta P_i - \bar{P})^2} \eqno{(4)} $$', html)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("MathJax equations completely repaired.")
