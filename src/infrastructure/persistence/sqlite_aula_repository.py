import sqlite3
from src.domain.repositories.aula_repository import IAulaRepository
from src.domain.entities.aula import Aula
from src.domain.value_objects.estado_aula import EstadoAula


class SqliteAulaRepository(IAulaRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def obtener_por_id(self, id: int) -> Aula | None:
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, nombre, capacidad, pabellon, estado FROM aulas WHERE id = ?;", (id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Aula(
            id=row["id"],
            nombre=row["nombre"],
            capacidad=row["capacidad"],
            pabellon=row["pabellon"],
            estado=EstadoAula(row["estado"])
        )

    def listar_todas(self) -> list[Aula]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, nombre, capacidad, pabellon, estado FROM aulas ORDER BY id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        return [
            Aula(
                id=r["id"],
                nombre=r["nombre"],
                capacidad=r["capacidad"],
                pabellon=r["pabellon"],
                estado=EstadoAula(r["estado"])
            )
            for r in rows
        ]

    def guardar(self, aula: Aula) -> Aula:
        cursor = self._conn.cursor()
        if aula.id is None:
            cursor.execute(
                "INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);",
                (aula.nombre, aula.capacidad, aula.pabellon, aula.estado.value)
            )
            aula.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE aulas SET nombre = ?, capacidad = ?, pabellon = ?, estado = ? WHERE id = ?;",
                (aula.nombre, aula.capacidad, aula.pabellon, aula.estado.value, aula.id)
            )
        cursor.close()
        return aula
