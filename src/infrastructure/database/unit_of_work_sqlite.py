import sqlite3
from src.application.ports.unit_of_work import IUnitOfWork
from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.persistence.sqlite_aula_repository import SqliteAulaRepository
from src.infrastructure.persistence.sqlite_reserva_repository import SqliteReservaRepository


class SqliteUnitOfWork(IUnitOfWork):
    """
    Implementación concreta de Unit of Work para SQLite.
    Garantiza aislamiento y atomicidad de transacciones mediante 'BEGIN IMMEDIATE'.
    """

    def __init__(self, db_path: str = "unesr_aulas.db"):
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None
        self._in_transaction: bool = False
        self.aulas: SqliteAulaRepository | None = None
        self.reservas: SqliteReservaRepository | None = None

    def __enter__(self) -> "SqliteUnitOfWork":
        self._conn = get_db_connection(self._db_path)
        # Adquiere bloqueo de escritura antes de leer, previniendo carreras en la verificación
        self._conn.execute("BEGIN IMMEDIATE;")
        self._in_transaction = True
        self.aulas = SqliteAulaRepository(self._conn)
        self.reservas = SqliteReservaRepository(self._conn)
        return self

    def commit(self) -> None:
        if self._conn and self._in_transaction:
            self._in_transaction = False
            try:
                self._conn.execute("COMMIT;")
            except sqlite3.OperationalError:
                pass

    def rollback(self) -> None:
        if self._conn and self._in_transaction:
            self._in_transaction = False
            try:
                self._conn.execute("ROLLBACK;")
            except sqlite3.OperationalError:
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
