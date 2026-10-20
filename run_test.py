import subprocess, sys, os

result = subprocess.run(
    [sys.executable, 'test_binance_conn.py'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace',
    cwd=r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin'
)
out_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\binance_test_out.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\nSTDERR:\n")
    f.write(result.stderr)
print("Saved to " + out_path)
