import os
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

try:
    import psycopg2
    from psycopg2.extras import DictCursor
    HAS_PSYCOPG2 = True
except Exception as err:
    HAS_PSYCOPG2 = False


class PostgresCursorWrapper:
    def __init__(self, cursor: Any) -> None:
        self._cursor = cursor
        self._lastrowid: Any = None

    def execute(self, query: str, vars: Any = None) -> Any:
        pg_query = re.sub(r"\?", "%s", query)
        stripped = pg_query.strip().rstrip(";")
        es_insert = stripped.lstrip().upper().startswith("INSERT INTO")
        tiene_returning = "RETURNING" in stripped.upper()

        if es_insert and not tiene_returning:
            modified_query = f"{stripped} RETURNING id;"
            try:
                res = self._cursor.execute(modified_query, vars)
                row = self._cursor.fetchone()
                if row:
                    self._lastrowid = row[0] if isinstance(row, (tuple, list)) else row.get("id", row[0])
                return res
            except Exception:
                self._cursor.connection.rollback()
                self._lastrowid = None
                return self._cursor.execute(pg_query, vars)

        self._lastrowid = None
        return self._cursor.execute(pg_query, vars)

    def executemany(self, query: str, vars_list: Any) -> Any:
        pg_query = re.sub(r"\?", "%s", query)
        self._lastrowid = None
        return self._cursor.executemany(pg_query, vars_list)

    def fetchone(self) -> Any:
        return self._cursor.fetchone()

    def fetchall(self) -> list[Any]:
        return self._cursor.fetchall()

    def fetchmany(self, size: int = None) -> list[Any]:
        if size is None:
            return self._cursor.fetchmany()
        return self._cursor.fetchmany(size)

    def close(self) -> None:
        self._cursor.close()

    @property
    def lastrowid(self) -> Any:
        return self._lastrowid

    @property
    def rowcount(self) -> int:
        return self._cursor.rowcount

    def __iter__(self):
        return iter(self._cursor)


class PostgresConnectionWrapper:
    def __init__(self, conn: Any) -> None:
        self._conn = conn

    def cursor(self) -> PostgresCursorWrapper:
        return PostgresCursorWrapper(self._conn.cursor(cursor_factory=DictCursor))

    def execute(self, query: str, vars: Any = None) -> PostgresCursorWrapper:
        cur = self.cursor()
        cur.execute(query, vars)
        return cur

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def close(self) -> None:
        self._conn.close()


def get_target_db_path(db_path: str = None) -> str:
    if os.environ.get("VERCEL") == "1":
        return "/tmp/unesr_aulas.db"
    if db_path:
        return db_path
    return os.environ.get("DB_PATH", "unesr_aulas.db")


def get_db_connection(db_path: str = None) -> Any:
    database_url = os.environ.get("DATABASE_URL")
    es_test = db_path is not None and ("test_" in db_path or db_path == ":memory:")

    # En producción Vercel o con DATABASE_URL, Supabase tiene prioridad absoluta
    if database_url and not es_test:
        clean_url = database_url.strip('"').strip("'")
        if "sslmode=" not in clean_url:
            clean_url += ("&" if "?" in clean_url else "?") + "sslmode=require"
        try:
            raw_conn = psycopg2.connect(clean_url)
            return PostgresConnectionWrapper(raw_conn)
        except Exception as e:
            print(f"[MOTOR DB] ❌ ERROR CONEXION SUPABASE: {type(e).__name__} -> {e}")

    # Fallback SQLite solo para pruebas locales
    target = get_target_db_path(db_path)
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


class DatabaseManager:
    def __init__(self, db_path: str = None) -> None:
        self.db_path = db_path

    @contextmanager
    def get_connection(self) -> Generator[Any, None, None]:
        conn = get_db_connection(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
