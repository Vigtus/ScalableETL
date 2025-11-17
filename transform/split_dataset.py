import pandas as pd
import numpy as np
import os

# Nazwa oryginalnego dużego pliku
SOURCE_FILE = "sample_data.csv"

# Liczba części, na które chcesz podzielić dane
NUM_PARTS = 4

# Sprawdź, czy plik istnieje
if not os.path.exists(SOURCE_FILE):
    raise FileNotFoundError(f"Plik {SOURCE_FILE} nie istnieje w katalogu.")

print("📦 Wczytywanie danych...")
df = pd.read_csv(SOURCE_FILE)

# Liczba wszystkich rekordów
total_rows = len(df)
rows_per_part = total_rows // NUM_PARTS

print(f"🔪 Dzielimy {total_rows:,} rekordów na {NUM_PARTS} części po ok. {rows_per_part:,} wierszy każda...")

# Dzielimy DataFrame na N równych części
for i, chunk in enumerate(np.array_split(df, NUM_PARTS), start=1):
    file_name = f"chunk_{i}.csv"
    chunk.to_csv(file_name, index=False)
    print(f"✅ Zapisano {file_name} ({len(chunk):,} rekordów)")

print("🎉 Podział danych zakończony pomyślnie!")
