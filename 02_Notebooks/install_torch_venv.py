"""
Install PyTorch langsung ke venv yang digunakan notebook.
"""
import subprocess
import sys
import os

venv_python = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\.venv\Scripts\python.exe"
venv_pip = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\.venv\Scripts\pip.exe"

print("=" * 60)
print("INSTALL PYTORCH KE VENV NOTEBOOK")
print("=" * 60)

# Step 1: Cek lokasi site-packages
check_code = """
import site
print("Site packages:", site.getsitepackages())
"""
result = subprocess.run([venv_python, "-c", check_code], capture_output=True, text=True)
print("Site packages:", result.stdout.strip())

# Step 2: Install menggunakan python -m pip (lebih reliable)
print("\nInstalling PyTorch...")
result = subprocess.run(
    [venv_python, "-m", "pip", "install", "torch",
     "--index-url", "https://download.pytorch.org/whl/cpu",
     "--force-reinstall", "-v"],
    capture_output=True,
    text=True
)

# Tampilkan progress
lines = result.stdout.split('\n')
for line in lines:
    if any(kw in line.lower() for kw in ['installing', 'successfully', 'error', 'warning', 'collected']):
        print(line)

if result.returncode == 0:
    print("\n✅ PyTorch berhasil diinstall!")
else:
    print("\n❌ Gagal:", result.stderr[-500:])

# Step 3: Verifikasi
print("\nVerifikasi...")
verify_code = """
import torch
print("PyTorch versi:", torch.__version__)
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
print("Semua import berhasil!")
"""
result = subprocess.run([venv_python, "-c", verify_code], capture_output=True, text=True)
if result.returncode == 0:
    print(result.stdout)
    print("✅ Notebook siap dijalankan!")
else:
    print("❌ Error:", result.stderr[-300:])
