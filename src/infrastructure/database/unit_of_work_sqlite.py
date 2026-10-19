import sqlite3
from typing import Any
from src.application.ports.unit_of_work import IUnitOfWork
from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.persistence.sqlite_aula_repository import SqliteAulaRepository
from src.infrastructure.persistence.sqlite_reserva_repository import SqliteReservaRepository


class SqliteUnitOfWork(IUnitOfWork):
    """
    Implementación concreta de Unit of Work compatible tanto con SQLite local
    como con el PostgresConnectionWrapper (Supabase).
    Garantiza aislamiento y atomicidad de transacciones.
    """

    def __init__(self, db_path: str = "unesr_aulas.db"):
        self._db_path = db_path
        self._conn: Any = None
        self._in_transaction: bool = False
        self.aulas: SqliteAulaRepository | None = None
        self.reservas: SqliteReservaRepository | None = None

    def __enter__(self) -> "SqliteUnitOfWork":
        self._conn = get_db_connection(self._db_path)
        
        # En SQLite usamos BEGIN IMMEDIATE para prevenir bloqueos de carrera.
        # En PostgreSQL (Supabase) iniciamos transacción estándar o dejamos que el driver la maneje.
        try:
            if isinstance(self._conn, sqlite3.Connection):
                self._conn.execute("BEGIN IMMEDIATE;")
            else:
                self._conn.execute("BEGIN;")
        except Exception:
            pass

        self._in_transaction = True
        self.aulas = SqliteAulaRepository(self._conn)
        self.reservas = SqliteReservaRepository(self._conn)
        return self

    def commit(self) -> None:
        if self._conn and self._in_transaction:
            self._in_transaction = False
            try:
                self._conn.commit()
            except Exception:
                pass

    def rollback(self) -> None:
        if self._conn and self._in_transaction:
            self._in_transaction = False
            try:
                self._conn.rollback()
            except Exception:
                pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                self.rollback()
            else:
                self.commit()
        finally:
            if self._conn:
                try:
                    self._conn.close()
                except Exception:
                    pass
                self._conn = None
