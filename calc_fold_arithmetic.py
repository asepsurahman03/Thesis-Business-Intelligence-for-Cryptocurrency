from datetime import datetime, timedelta

start = datetime(2021, 3, 1, 0, 0, 0)

def candle_to_dt(n):
    return start + timedelta(hours=n-1)

def fmt(dt):
    return dt.strftime("%Y-%m-%d")

print("=== Formula saat ini (stride=168, berurutan) ===")
print("Fold k test = candle [720+(k-1)*168+1] to [720+k*168]")
print()
for k in [1, 6, 10, 24]:
    c_start = 720 + (k-1)*168 + 1
    c_end   = 720 + k*168
    print(f"Fold {k:2d}: candles {c_start}--{c_end} => {fmt(candle_to_dt(c_start))} to {fmt(candle_to_dt(c_end))}")
print(f"Fold 24 akhir = candle {720+24*168}")
print(f"Cakupan: {720+24*168} dari 43786 candle = {(720+24*168)/43786*100:.1f}%")
print()

# Terra-Luna: 9 May 2022
terra_luna = datetime(2022, 5, 9)
delta_hours = (terra_luna - start).days * 24
print(f"Terra-Luna 9 May 2022 = candle ~{delta_hours}")

# FTX: 8 Nov 2022
ftx = datetime(2022, 11, 8)
delta_ftx = (ftx - start).days * 24
print(f"FTX 8 Nov 2022 = candle ~{delta_ftx}")

print()
print("=== Jika fold tersebar di 5 tahun (stride besar) ===")
# Untuk fold 24 test berakhir di candle 43,786:
# last test end = 43786
# last test start = 43786 - 168 + 1 = 43619
# Fold 1 test start = 721 (setelah 720 training)
# stride = (43619 - 721) / (24-1) = 42898 / 23 = 1865
stride = (43786 - 168 + 1 - 721) // (24-1)
print(f"Stride agar fold 24 mencapai akhir data: {stride} candles = {stride/24:.0f} hari = {stride/24/30:.1f} bulan")
print()
for k in [1, 6, 10, 24]:
    c_start = 721 + (k-1)*stride
    c_end   = c_start + 167
    train_s = c_start - 720
    train_e = c_start - 1
    print(f"Fold {k:2d}: train [{train_s}--{train_e}] test [{c_start}--{c_end}] => {fmt(candle_to_dt(c_start))} to {fmt(candle_to_dt(c_end))}")

print()
print("Dengan stride=1865, apakah fold 6 mencakup Terra-Luna?")
for k in [1, 6, 10, 24]:
    c_start = 721 + (k-1)*stride
    c_end   = c_start + 167
    print(f"Fold {k:2d}: {fmt(candle_to_dt(c_start))} to {fmt(candle_to_dt(c_end))}")
