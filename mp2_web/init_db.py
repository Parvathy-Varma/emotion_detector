# init_db.py
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'app.db')
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT
);

CREATE TABLE IF NOT EXISTS detections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  emotion TEXT,
  confidence REAL,
  detected_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  detection_id INTEGER,
  mood TEXT,
  game_id TEXT,
  picked_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  detection_id INTEGER,
  mood TEXT,
  video_id TEXT,
  video_title TEXT,
  picked_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS survey (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  detection_id INTEGER,
  rating INTEGER,
  comments TEXT,
  submitted_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    for stmt in SCHEMA.strip().split(';'):
        if stmt.strip():
            cur.execute(stmt)
    conn.commit()
    conn.close()
    print("DB initialized at", DB)

if __name__ == "__main__":
    init_db()
