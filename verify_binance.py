import pandas as pd

csv = r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\01_Data\btc_5year_hourly_bigdata.csv'
df = pd.read_csv(csv)
df['Open_Time'] = pd.to_datetime(df['Open_Time'])
days = (df['Open_Time'].max() - df['Open_Time'].min()).days

result = []
result.append("=== VERIFIKASI DATA BINANCE ===")
result.append("Source : Binance API (data-api.binance.vision)")
result.append("Rows   : {:,}".format(len(df)))
result.append("Cols   : {}".format(list(df.columns)))
result.append("Start  : {}".format(df['Open_Time'].min()))
result.append("End    : {}".format(df['Open_Time'].max()))
result.append("Cover  : {} hari ({:.2f} tahun)".format(days, days/365.25))
result.append("")
result.append("Sample 3 baris pertama:")
result.append(df.head(3).to_string())
result.append("")
result.append("Sample 3 baris terakhir:")
result.append(df.tail(3).to_string())

out = "\n".join(result)
print(out)
with open(r'e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\verify_result.txt', 'w', encoding='utf-8') as f:
    f.write(out)
