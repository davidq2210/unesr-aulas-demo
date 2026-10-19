import sqlite3
from src.domain.entities.academico import Carrera, Materia, Docente


class SqliteCatalogoRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def listar_carreras(self, nivel: str | None = None) -> list[Carrera]:
        cursor = self._conn.cursor()
        if nivel:
            cursor.execute("SELECT id, codigo, nombre, nivel FROM carreras WHERE nivel = ? ORDER BY nombre ASC;", (nivel,))
        else:
            cursor.execute("SELECT id, codigo, nombre, nivel FROM carreras ORDER BY nombre ASC;")
        rows = cursor.fetchall()
        cursor.close()
        return [
            Carrera(id=r["id"], codigo=r["codigo"], nombre=r["nombre"], nivel=r["nivel"])
            for r in rows
        ]

    def listar_materias(self, carrera_id: int | None = None) -> list[Materia]:
        cursor = self._conn.cursor()
        if carrera_id:
            cursor.execute(
                "SELECT id, carrera_id, codigo, nombre FROM materias WHERE carrera_id = ? ORDER BY nombre ASC;",
                (carrera_id,)
            )
        else:
            cursor.execute("SELECT id, carrera_id, codigo, nombre FROM materias ORDER BY nombre ASC;")
        rows = cursor.fetchall()
        cursor.close()
        return [
            Materia(id=r["id"], carrera_id=r["carrera_id"], codigo=r["codigo"], nombre=r["nombre"])
            for r in rows
        ]

    def listar_docentes(self, solo_activos: bool = True) -> list[Docente]:
        cursor = self._conn.cursor()
        query = "SELECT id, cedula, nombres, apellidos, email, activo FROM docentes"
        if solo_activos:
            query += " WHERE activo = 1"
        query += " ORDER BY apellidos ASC, nombres ASC;"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [
            Docente(
                id=r["id"],
                cedula=r["cedula"],
                nombres=r["nombres"],
                apellidos=r["apellidos"],
                email=r["email"],
                activo=bool(r["activo"])
            )
            for r in rows
        ]

    def guardar_docente(self, docente: Docente) -> Docente:
        cursor = self._conn.cursor()
        if docente.id is None:
            cursor.execute(
                "INSERT INTO docentes (cedula, nombres, apellidos, email, activo) VALUES (?, ?, ?, ?, ?);",
                (docente.cedula, docente.nombres, docente.apellidos, docente.email, 1 if docente.activo else 0)
            )
            docente.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE docentes SET cedula = ?, nombres = ?, apellidos = ?, email = ?, activo = ? WHERE id = ?;",
                (docente.cedula, docente.nombres, docente.apellidos, docente.email, 1 if docente.activo else 0, docente.id)
            )
        cursor.close()
        return docente

    def guardar_materia(self, materia: Materia) -> Materia:
        cursor = self._conn.cursor()
        if materia.id is None:
            cursor.execute(
                "INSERT INTO materias (carrera_id, codigo, nombre) VALUES (?, ?, ?);",
                (materia.carrera_id, materia.codigo, materia.nombre)
            )
            materia.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE materias SET carrera_id = ?, codigo = ?, nombre = ? WHERE id = ?;",
                (materia.carrera_id, materia.codigo, materia.nombre, materia.id)
            )
        cursor.close()
        return materia
