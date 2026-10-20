import subprocess
import sys

venv_python = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\.venv\Scripts\python.exe"

test_code = """
import sys
print("Python:", sys.version)
print("Executable:", sys.executable)
import torch
print("PyTorch:", torch.__version__)
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
print("Semua modul torch berhasil diimport!")
"""

result = subprocess.run(
    [venv_python, "-c", test_code],
    capture_output=True,
    text=True
)
print("STDOUT:", result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Exit code:", result.returncode)
