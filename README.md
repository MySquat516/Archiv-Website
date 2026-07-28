# Archiv-Website

Statische Website mit Upload-Funktion. Dateien werden über ein Formular auf der Startseite hochgeladen und erscheinen automatisch auf der Downloads-Seite.

## Stack

- **Nginx** – liefert die statischen Seiten aus, leitet `/upload` und `/manifest.json` an die App weiter
- **Flask** (Python) – Upload-Verarbeitung, Datenbank-Anbindung
- **PostgreSQL** – speichert Metadaten zu den hochgeladenen Dateien

## Setup

1. `.env` anlegen (siehe `.env.example`):
   ```
   DB_NAME=erstewebsite
   DB_USER=erstewebsite
   DB_PASSWORD=dein-passwort
   ```

2. Starten:
   ```bash
   docker compose up -d --build
   ```

3. Website erreichbar unter `http://localhost:8090`

## Struktur

```
site/           Statische HTML-Seiten, CSS
app/            Flask-Anwendung (Upload-Logik)
nginx.conf      Nginx-Konfiguration
docker-compose.yml
```

## Kategorien bearbeiten

Kategorien sind an zwei Stellen definiert und müssen synchron gehalten werden:
- `app/app.py` → `CATEGORIES`-Liste
- `site/index.html` → Dropdown im Upload-Formular

## Uploads verwalten / löschen

Admin-Übersicht unter `/upload` – zeigt die letzten 20 Uploads mit Lösch-Button.