import os
import uuid

import psycopg2
from flask import Flask, request, redirect, render_template, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]
DATABASE_URL = os.environ["DATABASE_URL"]

ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp",
    "pdf", "zip", "docx", "xlsx", "txt", "mp3", "mp4"
}
CATEGORIES = ["galerie", "downloads", "medien", "historie", "produkte"]


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET"])
def upload_form():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, original_name, category, title, upload_date FROM media ORDER BY upload_date DESC LIMIT 20")
    recent = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("upload.html", categories=CATEGORIES, recent=recent)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Keine Datei ausgewählt", 400

    file = request.files["file"]
    category = request.form.get("category", "").strip()
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if file.filename == "" or not allowed_file(file.filename):
        return "Ungültige Datei oder kein Dateiname", 400
    if category not in CATEGORIES:
        return "Ungültige Kategorie", 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    stored_name = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, stored_name)
    file.save(filepath)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO media (filename, original_name, category, title, description, file_path, file_type, source)
           VALUES (%s, %s, %s, %s, %s, %s, %s, 'manual')""",
        (stored_name, secure_filename(file.filename), category, title, description, stored_name, file.mimetype),
    )
    conn.commit()
    cur.close()
    conn.close()

    # Ajax-Request von der Startseite (index.html) erwartet direkt eine Antwort
    if request.form.get("ajax") == "1":
        return jsonify({"status": "ok"})

    return redirect(url_for("upload_form"))


@app.route("/upload/delete/<int:media_id>", methods=["POST"])
def delete_media(media_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT file_path FROM media WHERE id = %s", (media_id,))
    row = cur.fetchone()
    if row:
        full_path = os.path.join(UPLOAD_FOLDER, row[0])
        if os.path.exists(full_path):
            os.remove(full_path)
        cur.execute("DELETE FROM media WHERE id = %s", (media_id,))
        conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("upload_form"))


@app.route("/manifest.json", methods=["GET"])
def manifest_json():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, original_name, category, title, description,
                  upload_date, file_path, file_type
           FROM media ORDER BY upload_date DESC"""
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    items = [
        {
            "id": r[0],
            "original_name": r[1],
            "category": r[2],
            "title": r[3],
            "description": r[4],
            "upload_date": r[5].isoformat(),
            "url": f"/uploads/{r[6]}",
            "file_type": r[7],
        }
        for r in rows
    ]
    return jsonify(items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
