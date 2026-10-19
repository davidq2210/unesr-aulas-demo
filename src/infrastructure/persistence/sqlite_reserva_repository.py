import sqlite3
from datetime import date, time
from src.domain.repositories.reserva_repository import IReservaRepository
from src.domain.entities.reserva import Reserva
from src.domain.value_objects.rango_horario import RangoHorario


class SqliteReservaRepository(IReservaRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def _row_to_entity(self, row: sqlite3.Row) -> Reserva:
        h_inicio_str = row["hora_inicio"]
        h_fin_str = row["hora_fin"]

        h_ini_parts = [int(p) for p in h_inicio_str.split(":")]
        h_fin_parts = [int(p) for p in h_fin_str.split(":")]

        horario = RangoHorario(
            hora_inicio=time(h_ini_parts[0], h_ini_parts[1]),
            hora_fin=time(h_fin_parts[0], h_fin_parts[1])
        )

        fecha_parts = [int(p) for p in row["fecha"].split("-")]
        fecha_obj = date(fecha_parts[0], fecha_parts[1], fecha_parts[2])

        return Reserva(
            id=row["id"],
            aula_id=row["aula_id"],
            docente_id=row["docente_id"],
            materia_id=row["materia_id"],
            fecha=fecha_obj,
            horario=horario,
            creado_por_usuario_id=row["creado_por_usuario_id"],
            observaciones=row["observaciones"] or ""
        )

    def buscar_por_aula_y_fecha(self, aula_id: int, fecha: date) -> list[Reserva]:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, "
            "creado_por_usuario_id, observaciones FROM reservas WHERE aula_id = ? AND fecha = ?;",
            (aula_id, fecha.isoformat())
        )
        rows = cursor.fetchall()
        cursor.close()
        return [self._row_to_entity(r) for r in rows]

    def buscar_por_docente_y_fecha(self, docente_id: int, fecha: date) -> list[Reserva]:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, "
            "creado_por_usuario_id, observaciones FROM reservas WHERE docente_id = ? AND fecha = ?;",
            (docente_id, fecha.isoformat())
        )
        rows = cursor.fetchall()
        cursor.close()
        return [self._row_to_entity(r) for r in rows]

    def obtener_por_id(self, id: int) -> Reserva | None:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, "
            "creado_por_usuario_id, observaciones FROM reservas WHERE id = ?;",
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return self._row_to_entity(row)

    def listar_por_fecha(self, fecha: date) -> list[Reserva]:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, "
            "creado_por_usuario_id, observaciones FROM reservas WHERE fecha = ? "
            "ORDER BY hora_inicio ASC;",
            (fecha.isoformat(),)
        )
        rows = cursor.fetchall()
        cursor.close()
        return [self._row_to_entity(r) for r in rows]

    def guardar(self, reserva: Reserva) -> Reserva:
        cursor = self._conn.cursor()
        h_inicio_str = reserva.horario.hora_inicio.strftime("%H:%M")
        h_fin_str = reserva.horario.hora_fin.strftime("%H:%M")
        fecha_str = reserva.fecha.isoformat()

        if reserva.id is None:
            cursor.execute(
                """
                INSERT INTO reservas (aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, creado_por_usuario_id, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    reserva.aula_id,
                    reserva.docente_id,
                    reserva.materia_id,
                    fecha_str,
                    h_inicio_str,
                    h_fin_str,
                    reserva.creado_por_usuario_id,
                    reserva.observaciones
                )
            )
            reserva.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE reservas SET aula_id = ?, docente_id = ?, materia_id = ?, fecha = ?, hora_inicio = ?, hora_fin = ?, observaciones = ?
                WHERE id = ?;
                """,
                (
                    reserva.aula_id,
                    reserva.docente_id,
                    reserva.materia_id,
                    fecha_str,
                    h_inicio_str,
                    h_fin_str,
                    reserva.observaciones,
                    reserva.id
                )
            )
        cursor.close()
        return reserva

    def eliminar(self, id: int) -> bool:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = ?;", (id,))
        filas = cursor.rowcount
        cursor.close()
        return filas > 0
