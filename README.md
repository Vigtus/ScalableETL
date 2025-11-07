# ScalableETL

🧩 Ogólna koncepcja projektu

Celem projektu jest zaprojektowanie i przetestowanie skalowalnej architektury procesu ETL (Extract – Transform – Load) działającej w środowisku chmurowym.
Nie skupia się on na przetwarzaniu konkretnego typu danych, lecz na inżynierii i wydajności całego pipeline’u – jego odporności, elastyczności i możliwości automatycznego skalowania.

🎯 Założenia projektu

Projekt ma pokazać, jak nowoczesne narzędzia chmurowe (takie jak Docker, Kubernetes, Azure Data Factory czy Apache Airflow) mogą współpracować w celu budowy skalowalnego systemu przetwarzania danych.

🔍 Zakres badań i testów

W ramach realizacji projektu analizowane są następujące aspekty działania systemu:

Skalowalność – jak pipeline reaguje na zwiększenie ilości danych wejściowych (np. wzrost rozmiaru plików CSV lub liczby rekordów).

Równoległość zadań – testy zachowania systemu przy jednoczesnym uruchamianiu wielu procesów ETL.

Automatyczne skalowanie (Auto-Scaling) – w jaki sposób Kubernetes (Horizontal Pod Autoscaler) zwiększa liczbę replik kontenerów przy wzroście obciążenia i jak szybko reaguje na zmiany.

Monitorowanie i metryki – implementacja systemu obserwowalności z wykorzystaniem Prometheus i Grafana do pomiaru wydajności, obciążenia CPU/RAM oraz czasu przetwarzania danych.

🧠 Kluczowy cel

Projekt ma charakter badawczo-inżynierski – jego głównym rezultatem jest:

praktyczna demonstracja działania skalowalnego procesu ETL w środowisku konteneryzowanym,

analiza wpływu konfiguracji i parametrów klastra na efektywność przetwarzania,

dokumentacja wyników i rekomendacji dotyczących optymalizacji pipeline’ów danych.
