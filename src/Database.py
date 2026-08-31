import sqlite3
from datetime import datetime, timedelta

DB_NAME = "Movies.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER NOT NULL,
            media_type TEXT NOT NULL,
            title TEXT NOT NULL,
            poster_url TEXT,
            overview TEXT,
            release_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(tmdb_id, media_type)
        )
    """)
    conn.commit()
    conn.close()

def save_or_update_media(tmdb_id, media_type, title, poster_url=None, overview=None, release_date=None):
    conn = connect_db()
    conn.execute("""
        INSERT INTO media (tmdb_id, media_type, title, poster_url, overview, release_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(tmdb_id, media_type)
        DO UPDATE SET
            title = excluded.title,
            poster_url = excluded.poster_url,
            overview = excluded.overview,
            release_date = excluded.release_date
    """, (tmdb_id, media_type, title, poster_url, overview, release_date))
    conn.commit()
    conn.close()

def get_explore_media(limit=20):
    conn = connect_db()
    rows = conn.execute("""
        SELECT tmdb_id, media_type, title, poster_url, overview, release_date
        FROM media
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_old_media(days=30, keep_latest=100):
    conn = connect_db()

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "DELETE FROM media WHERE created_at < ?",
        (cutoff,)
    )

    conn.execute("""
        DELETE FROM media
        WHERE id NOT IN (
            SELECT id
            FROM media
            ORDER BY id DESC
            LIMIT ?
        )
    """, (keep_latest,))

    conn.commit()
    conn.close()