from __future__ import annotations
import os
import sqlite3
from typing import Dict, Any
from datetime import datetime
from app.config import settings

DB_PATH = os.path.join(settings.app_data_dir, "memory.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  category TEXT,
  priority INTEGER,
  planned_start TEXT,
  planned_end TEXT,
  status TEXT
);

CREATE TABLE IF NOT EXISTS activity_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  intent TEXT,
  text TEXT,
  duration_min INTEGER,
  label TEXT  -- focus, admin, personal, wasted
);

CREATE TABLE IF NOT EXISTS habits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  days_of_week TEXT,
  time_window TEXT,
  strict INTEGER,
  streak INTEGER
);

CREATE TABLE IF NOT EXISTS preferences (
  key TEXT PRIMARY KEY,
  value TEXT
);
"""

_conn = None

def get_conn():
    global _conn
    if _conn is None:
        os.makedirs(settings.app_data_dir, exist_ok=True)
        _conn = sqlite3.connect(DB_PATH)
        _conn.execute("PRAGMA journal_mode=WAL;")
        _conn.executescript(SCHEMA_SQL)
    return _conn


def log_activity(intent: str, text: str, duration_min: int = 0, label: str = "focus") -> None:
    conn = get_conn()
    conn.execute(
        "INSERT INTO activity_log(timestamp, intent, text, duration_min, label) VALUES(?,?,?,?,?)",
        (datetime.now().isoformat(), intent, text, duration_min, label),
    )
    conn.commit()


def set_pref(key: str, value: str) -> None:
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO preferences(key, value) VALUES(?,?)", (key, value))
    conn.commit()


def get_pref(key: str, default: str = "") -> str:
    conn = get_conn()
    cur = conn.execute("SELECT value FROM preferences WHERE key=?", (key,))
    row = cur.fetchone()
    return row[0] if row else default