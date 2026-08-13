"""SQLite storage layer -- see .jarvis/decisions.md D-0010.

Phase 1 only needs two tables: permission grants and an audit log. Later
phases add tables behind this same get_connection() entry point rather
than each subsystem opening its own database file.
"""

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS permission_grants (
    capability TEXT PRIMARY KEY,
    granted INTEGER NOT NULL DEFAULT 0,
    tier TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    detail TEXT NOT NULL
);
"""


def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
