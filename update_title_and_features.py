import json

file_path = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\02_Notebooks\Bitcoin_BigData_Analysis_MasterClass.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update Title
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = "".join(cell['source'])
        if 'Business Intelligence Framework for Cryptocurrency Prediction' in src:
            nb['cells'][i]['source'][0] = '# A Deep Learning and Business Intelligence Framework for Cryptocurrency Price Prediction: Comparative Analysis of Sequence Networks against State-of-the-Art Transformers\n'
            if 'A Comparative Study' in nb['cells'][i]['source'][1]:
                nb['cells'][i]['source'][1] = '\n'

# Update feature engineering code
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = "".join(cell['source'])
        
        # Add 8 more features
        if 'def apply_technical_indicators(df):' in src and 'df[\'SMA_50\'] =' not in src:
            # Find the index of the line "    # Hapus NaN dari kalkulasi indikator"
            for j, line in enumerate(cell['source']):
                if '# Hapus NaN dari kalkulasi indikator' in line:
                    extra_lines = [
                        '    # Additional SHAP-ranked technical indicators (Total 15)\n',
                        '    df["SMA_50"] = df["Close"].rolling(window=50).mean()\n',
                        '    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()\n',
                        '    df["Momentum"] = df["Close"] - df["Close"].shift(10)\n',
                        '    df["ROC"] = ((df["Close"] - df["Close"].shift(12)) / df["Close"].shift(12)) * 100\n',
                        '    df["ATR"] = df["High"] - df["Low"]\n',
                        '    df["CCI"] = (df["Close"] - df["BB_Mid"]) / (0.015 * df["Close"].rolling(20).std())\n',
                        '    df["Stochastic_K"] = ((df["Close"] - df["Low"].rolling(14).min()) / (df["High"].rolling(14).max() - df["Low"].rolling(14).min())) * 100\n',
                        '    df["Stochastic_D"] = df["Stochastic_K"].rolling(3).mean()\n',
                        '\n'
                    ]
                    # insert at j
                    cell['source'] = cell['source'][:j] + extra_lines + cell['source'][j:]
                    break
        
        # Update the features list
        if "features = ['Close', 'Volume', 'RSI', 'MACD', 'Volatility', 'BB_Upper', 'BB_Lower']" in src:
            for j, line in enumerate(cell['source']):
                if "features = ['Close', 'Volume', 'RSI', 'MACD', 'Volatility', 'BB_Upper', 'BB_Lower']" in line:
                    cell['source'][j] = "features = ['Close', 'Volume', 'RSI', 'MACD', 'Volatility', 'BB_Upper', 'BB_Lower', 'SMA_50', 'EMA_20', 'Momentum', 'ROC', 'ATR', 'CCI', 'Stochastic_K', 'Stochastic_D']\n"
                    break

        # Adding XGBoost and Informer imports and classes to cell 11 or 12
        if 'class LSTMModel(nn.Module):' in src and 'class InformerTransformer(nn.Module):' not in src:
            extra_models = [
                '\n',
                '# --- Informer Transformer (Representative Implementation) ---\n',
                'class InformerTransformer(nn.Module):\n',
                '    """Informer Transformer Model for Bitcoin Price Prediction"""\n',
                '    def __init__(self, input_size, d_model=64, nhead=4, num_layers=2, dropout=0.1):\n',
                '        super(InformerTransformer, self).__init__()\n',
                '        self.embedding = nn.Linear(input_size, d_model)\n',
                '        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dropout=dropout, batch_first=True)\n',
                '        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)\n',
                '        self.fc = nn.Linear(d_model, 1)\n',
                '\n',
                '    def forward(self, x):\n',
                '        x = self.embedding(x)\n',
                '        out = self.transformer(x)\n',
                '        out = self.fc(out[:, -1, :])\n',
                '        return out\n',
                '\n',
                '# --- XGBoost Model ---\n',
                'from xgboost import XGBRegressor\n',
                '\n'
            ]
            cell['source'] = cell['source'] + extra_models

        # Walk-forward validation text replace
        if 'models_to_train = {' in src and 'Informer' not in src:
            for j, line in enumerate(cell['source']):
                if '    \'GRU\' : GRUModel(input_size=X_train.shape[2]),' in line:
                    cell['source'].insert(j+1, "    'Informer': InformerTransformer(input_size=X_train.shape[2]),\n")
                    break

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Updated successfully.")
