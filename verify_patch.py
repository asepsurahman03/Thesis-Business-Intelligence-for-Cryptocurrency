#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open(r"e:\Nusa Putra\S2\Tesis\Analisis Bit Coin\05_Reports\Manuscript_IEEE_FINAL_2026.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = [
    ("SHOULD EXIST",   "Theoretical Justification for GRU Superiority"),
    ("SHOULD EXIST",   "Benchmarking Against Published Studies"),
    ("SHOULD EXIST",   "Operational Power BI Prototype and Practical Implications"),
    ("SHOULD EXIST",   "Zerveas"),
    ("SHOULD EXIST",   "Nie et al."),
    ("SHOULD EXIST",   "Broadly speaking"),
    ("SHOULD EXIST",   "broader deployment in live trading"),
    ("SHOULD NOT EXIST", "institutional-level"),
    ("SHOULD NOT EXIST", "tokenization difficulties"),
    ("SHOULD NOT EXIST", "recurrent structures consistently captured rapid modifications"),
]

print("=" * 70)
for expected, keyword in checks:
    found = keyword.lower() in html.lower()
    if expected == "SHOULD EXIST":
        status = "OK  " if found else "FAIL"
    else:
        status = "OK  " if not found else "FAIL"
    print(f"[{status}] {expected}: '{keyword[:55]}'")

print("=" * 70)
print(f"Total HTML size: {len(html):,} bytes")
