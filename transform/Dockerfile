# 🧱 1. Bazowy obraz z Pythonem
FROM python:3.11-slim

# 📂 2. Ustaw katalog roboczy
WORKDIR /app

# 🔧 3. Zainstaluj systemowe zależności (w tym ODBC)
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 📦 4. Skopiuj plik z zależnościami Pythona
COPY requirements.txt .

# 🐍 5. Zainstaluj paczki Pythona
RUN pip install --no-cache-dir -r requirements.txt

# 💾 6. Skopiuj kod aplikacji
COPY transform.py .

# ▶️ 7. Ustal komendę startową
CMD ["python", "transform.py"]
