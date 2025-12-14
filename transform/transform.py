import os
import pandas as pd
import time

start_time = time.time()

# Pobierz nazwę pliku z ENV
DATA_FILE = os.getenv("DATA_FILE", "chunk_1.csv")

print(f"🚀 Start przetwarzania {DATA_FILE}")

# Wczytaj dane
df = pd.read_csv(DATA_FILE)

# 🔄 Przykładowa transformacja — zsumuj sprzedaż według kategorii
if "Sale (Dollars)" in df.columns:
    df["Sale (Dollars)"] = df["Sale (Dollars)"].replace('[\$,]', '', regex=True).astype(float)
    summary = df.groupby("Category Name")["Sale (Dollars)"].sum().reset_index()
else:
    summary = df.copy()

# Zapisz wynik
output_file = f"processed_{os.path.basename(DATA_FILE)}"
summary.to_csv(output_file, index=False)

elapsed = time.time() - start_time
print(f"✅ Zakończono przetwarzanie {DATA_FILE} w {elapsed:.2f}s")
