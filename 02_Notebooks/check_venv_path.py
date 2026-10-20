import subprocess
import sys

venv_python = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\.venv\Scripts\python.exe"

# Cek sys.path dari venv python
check_code = """
import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("\\nsite-packages paths:")
for p in sys.path:
    if 'site-packages' in p or 'torch' in p.lower():
        print(" -", p)

print("\\nChecking torch location...")
try:
    import importlib.util
    spec = importlib.util.find_spec('torch')
    if spec:
        print("torch found at:", spec.origin)
    else:
        print("torch NOT found in sys.path")
except Exception as e:
    print("Error:", e)
"""

result = subprocess.run(
    [venv_python, "-c", check_code],
    capture_output=True,
    text=True
)
print("STDOUT:", result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
