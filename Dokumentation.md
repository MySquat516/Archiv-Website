# Dokumentation: Erste-Website (Port 8090)

Statische Website mit Upload-Funktion, läuft auf dem ZimaOS-Server (`192.168.178.51:8090`).

---

## 1. Architektur

```
Nginx (Webserver)
  ├── liefert statische HTML/CSS-Dateien aus
  ├── /uploads/  → liefert hochgeladene Dateien direkt aus
  ├── /upload    → leitet an Flask-App weiter
  └── /manifest.json → leitet an Flask-App weiter (dynamische Datei-Liste)

Flask-App (Python)
  ├── Formular-Verarbeitung für Uploads
  ├── speichert Dateien auf die Festplatte (Volume)
  └── speichert Metadaten in PostgreSQL

PostgreSQL
  └── Tabelle "media": id, filename, category, title, description, upload_date, file_path, file_type
```

**Wichtiges Prinzip:** Dateien werden **nicht** in der Datenbank gespeichert, sondern nur auf der Festplatte. Die Datenbank enthält nur die Metadaten (Pfad, Titel, Kategorie etc.).

---

## 2. Ordnerstruktur (Server: `/DATA/AppData/erste-website/`)

```
erste-website/
├── .env                  (Zugangsdaten, NICHT in Git)
├── .env.example          (Vorlage für Git)
├── .gitignore
├── README.md
├── docker-compose.yml
├── nginx.conf
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init_db.sql
│   ├── app.py
│   └── templates/upload.html
└── site/
    ├── index.html         (Startseite mit Upload-Formular)
    ├── ueber-uns.html
    ├── projekte.html
    ├── galerie.html       (zeigt Kategorie "Bilder")
    ├── downloads.html     (zeigt Kategorien "Downloads" + "Dokumente")
    ├── kontakt.html
    ├── style.css           (gemeinsames Stylesheet aller Seiten)
    └── manifest.json       (nicht mehr aktiv genutzt, ersetzt durch /manifest.json-Endpunkt in Flask)
```

---

## 3. Volumes

- `/DATA/AppData/erste-website/site` → statische Website-Dateien
- `/DATA/AppData/erste-website/uploads` → hochgeladene Dateien
- `/DATA/AppData/erste-website/db-data` → PostgreSQL-Datenbankdateien

---

## 4. Container-Namen

`erste-website-nginx`, `erste-website-app`, `erste-website-db`

---

## 5. Umgebungsvariablen (`.env` auf dem Server, nicht in Git)

```
DB_NAME=erstewebsite
DB_USER=erstewebsite
DB_PASSWORD=<echtes Passwort>
```

---

## 6. Kategorien

Aktuell definiert in `app/app.py` (`CATEGORIES`) und im Dropdown in `site/index.html`:

| Kategorie (Wert) | Anzeige-Seite |
|---|---|
| `dokumente` | `downloads.html` |
| `downloads` | `downloads.html` |
| `bilder` | `galerie.html` |
| `videos` | *(noch keine eigene Seite)* |

**Wichtig:** Kategorien müssen an zwei Stellen synchron gehalten werden — `app/app.py` (`CATEGORIES`-Liste) und `site/index.html` (Dropdown-Optionen). Änderungen an `app.py` erfordern einen Rebuild (`docker compose up -d --build`), Änderungen an HTML-Dateien wirken sofort.

---

## 7. Admin-Bereich

Unter `/upload` (GET) gibt es eine einfache Übersicht der letzten 20 Uploads mit Lösch-Funktion. Aktuell **nicht passwortgeschützt**, nur über die (nicht verlinkte) URL erreichbar.

---

## 8. Häufige Befehle

### Container starten / neu starten

```bash
cd /DATA/AppData/erste-website
docker compose up -d --build      # nach Code-Änderungen (app.py, Dockerfile)
docker compose up -d              # nach Config-Änderungen (docker-compose.yml, nginx.conf)
docker compose restart            # einfacher Neustart ohne Neubau
```

### Container-Reste entfernen (bei Namenskonflikten)

```bash
docker rm -f <container-name>
```

### Logs prüfen

```bash
docker logs erste-website-app
```

### manifest.json manuell prüfen

```bash
curl http://localhost:8090/manifest.json
```

---

## 9. Bekannte offene Punkte / Ideen für später

- **Video-Kategorie** hat noch keine eigene Anzeige-Seite
- **`/upload`-Adminbereich** ist nicht passwortgeschützt (nur "security by obscurity" über unverlinkte URL)
- Alte Kategorien aus einer früheren Version (`galerie`, `medien`, `historie`, `produkte`) könnten noch als "verwaiste" Einträge in der Datenbank liegen, falls vor der Umstellung schon Dateien hochgeladen wurden

---

## 10. Git / GitHub

Das Projekt liegt unter `https://github.com/MySquat516/Archiv-Website.git`.

### Was NICHT ins Repo gehört (`.gitignore`)

```
.env
db-data/
uploads/
site/uploads/
__pycache__/
*.pyc
```

### Typischer Workflow in VS Code

```bash
git add .
git commit -m "Beschreibung der Änderung"
git push
```