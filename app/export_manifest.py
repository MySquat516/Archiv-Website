"""
Exportiert alle Upload-Einträge aus der PostgreSQL-DB in eine
manifest_uploads.json, damit build_archive_index.py sie einbinden kann.

Ausführen im Container:
    docker exec pitbull-flask python export_manifest.py

Oder als Cronjob auf dem Host alle 10 Minuten.
"""

import json
import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]
OUTPUT_PATH = "/site/manifest_uploads.json"  # gemountet auf dein Site-Verzeichnis

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        """SELECT id, filename, original_name, category, title, description,
                  upload_date, file_path, file_type, source
           FROM media ORDER BY upload_date DESC"""
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    entries = []
    for r in rows:
        entries.append({
            "id": r[0],
            "filename": r[1],
            "original_name": r[2],
            "category": r[3],
            "title": r[4],
            "description": r[5],
            "upload_date": r[6].isoformat(),
            "url": f"/uploads/{r[7]}",
            "file_type": r[8],
            "source": r[9],
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"{len(entries)} Einträge exportiert nach {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
