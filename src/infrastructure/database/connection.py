import sqlite3
from typing import Optional


def get_db_connection(db_path: str = "unesr_aulas.db") -> sqlite3.Connection:
    """
    Retorna una conexión a SQLite configurada con los pragmas de alto rendimiento y concurrencia:
    - journal_mode=WAL: Permite múltiples lectores simultáneos sin bloqueo de escritores.
    - busy_timeout=5000: Espera hasta 5 segundos si existe una transacción de escritura activa.
    - foreign_keys=ON: Garantiza integridad referencial relacional.
    - isolation_level=None: Habilita el control manual explícito de transacciones atómicas (BEGIN IMMEDIATE / COMMIT / ROLLBACK).
    """
    conn = sqlite3.connect(
        database=db_path,
        timeout=5.0,
        check_same_thread=False,
        isolation_level=None
    )
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

    return conn
