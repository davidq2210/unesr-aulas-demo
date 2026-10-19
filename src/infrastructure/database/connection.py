import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

def _resolve_path(db_path: str = None) -> str:
    if os.environ.get("VERCEL") == "1":
        return "/tmp/unesr_aulas.db"
    if db_path is None:
        return os.environ.get("DB_PATH", "unesr_aulas.db")
    # Si viene una ruta relativa en Vercel, forzar /tmp
    if os.environ.get("VERCEL") == "1" or not os.path.isabs(db_path):
        if os.environ.get("VERCEL") == "1":
            return "/tmp/unesr_aulas.db"
    return str(Path(db_path).resolve())

class DatabaseManager:
    def __init__(self, db_path: str = None) -> None:
        self.db_path = _resolve_path(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path, timeout=15.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if os.environ.get("VERCEL") == "1":
            cursor.execute("PRAGMA journal_mode=MEMORY;")
        else:
            cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=5000;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        try:
            yield conn
        finally:
            conn.close()

def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    target_path = _resolve_path(db_path)
    Path(target_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target_path, timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if os.environ.get("VERCEL") == "1":
        cursor.execute("PRAGMA journal_mode=MEMORY;")
    else:
        cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    return conn
