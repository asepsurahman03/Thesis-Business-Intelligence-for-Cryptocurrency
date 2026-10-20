import sys

html_path = r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_Format_Comprehensive.html"

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find the start of the [22] reference string
idx = html.find('[22] F. Diebold')
if idx == -1:
    print("Could not find [22] tag! The file might be corrupted.")
    sys.exit(1)

# Find the preceding <p> opening tag to safely cut the file right before [22] begins
start_p = html.rfind('<p>', 0, idx)
if start_p != -1 and (idx - start_p) < 50:
    content = html[:start_p]
else:
    # Fallback to cutting just before the [22] text
    content = html[:idx - 1]

# Define the absolute perfect ending without any truncation
valid_ending = """                <p>[22] F. Diebold and R. Mariano, "Comparing Predictive Accuracy," <i>J. Bus. Econ. Stat.</i>, vol. 13, pp. 253-263, 1995.</p>
            </div>

        </div>
        <div class="page-number">- 5 -</div>
    </div>

</body>
</html>
"""

# Save the completely repaired file
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content + valid_ending)

print("HTML structure and Reference [22] repaired successfully.")
