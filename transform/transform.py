import os
import pandas as pd

# Pobierz nazwę pliku z ENV (domyślnie chunk_1.csv)
DATA_FILE = os.getenv("DATA_FILE", "chunk_1.csv")

print(f"📥 Extracting data from {DATA_FILE}...")
df = pd.read_csv(DATA_FILE)

print("🔄 Transforming data...")
# Dla przykładu — policz sumę sprzedaży per kategoria (zależnie od kolumn)
if "Sale (Dollars)" in df.columns:
    df["Sale (Dollars)"] = df["Sale (Dollars)"].replace('[\$,]', '', regex=True).astype(float)
    summary = df.groupby("Category Name")["Sale (Dollars)"].sum().reset_index()
else:
    df["processed_value"] = df[df.columns[0]] * 2
    summary = df

output_file = f"processed_{os.path.basename(DATA_FILE)}"
print(f"💾 Saving processed data to {output_file}...")
summary.to_csv(output_file, index=False)

print(f"✅ Finished processing {DATA_FILE}")
