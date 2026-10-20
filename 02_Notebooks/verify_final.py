import subprocess
import os

# Set UTF-8 encoding
env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'

venv_python = r"E:\Nusa Putra\S2\Tesis\Analisis Bit Coin\.venv\Scripts\python.exe"

test_code = r"""
import sys
print("===== VERIFIKASI NOTEBOOK =====")
print("Python  :", sys.version.split()[0])
print("Exe     :", sys.executable[-50:])
print()

import pandas as pd
print("pandas  :", pd.__version__)

import numpy as np
print("numpy   :", np.__version__)

import sklearn
print("sklearn :", sklearn.__version__)

import torch
print("torch   :", torch.__version__)

import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("device  :", device)

print()
print("Semua library berhasil diimport!")
print()

# Mini test model
class LSTMModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = torch.nn.LSTM(input_size, hidden_size, num_layers=num_layers, dropout=dropout, batch_first=True)
        self.fc   = torch.nn.Linear(hidden_size, 1)
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        return self.fc(out[:, -1, :])

class GRUModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size=50, num_layers=2, dropout=0.2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers  = num_layers
        self.gru = torch.nn.GRU(input_size, hidden_size, num_layers=num_layers, dropout=dropout, batch_first=True)
        self.fc  = torch.nn.Linear(hidden_size, 1)
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.gru(x, h0)
        return self.fc(out[:, -1, :])

np.random.seed(42)
X = torch.FloatTensor(np.random.rand(10, 24, 7).astype(np.float32))

lstm = LSTMModel(input_size=7)
out_lstm = lstm(X)

gru = GRUModel(input_size=7)
out_gru  = gru(X)

print("LSTM output shape:", tuple(out_lstm.shape), "OK")
print("GRU  output shape:", tuple(out_gru.shape),  "OK")
print()
print("===== NOTEBOOK SIAP DIJALANKAN =====")
"""

result = subprocess.run(
    [venv_python, "-c", test_code],
    capture_output=True,
    text=True,
    encoding='utf-8',
    env=env
)

print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr[-500:])
