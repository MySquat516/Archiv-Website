CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    original_name TEXT,
    category TEXT NOT NULL,      -- galerie, downloads, medien, historie, produkte
    title TEXT,
    description TEXT,
    upload_date TIMESTAMP DEFAULT NOW(),
    file_path TEXT NOT NULL,     -- relativer Pfad unter /uploads
    file_type TEXT,              -- MIME-Type
    source TEXT DEFAULT 'manual' -- manual, wayback, scan
);
