import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

def get_db_path() -> str:
    if os.environ.get("VERCEL") == "1":
        return "/tmp/unesr_aulas.db"
    return os.environ.get("DB_PATH", "unesr_aulas.db")

class DatabaseManager:
    def __init__(self, db_path: str = None) -> None:
        self.db_path = get_db_path() if db_path is None else db_path
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
    target = get_db_path() if db_path is None else db_path
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if os.environ.get("VERCEL") == "1":
        cursor.execute("PRAGMA journal_mode=MEMORY;")
    else:
        cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    return conn
