import sqlite3
from datetime import date, time, timedelta
from src.application.ports.cartelera_query_port import ICarteleraQueryPort
from src.application.dtos.cartelera_dto import ItemCarteleraDTO, ConsultarCarteleraFiltroDTO


class SqliteCarteleraQueryAdapter(ICarteleraQueryPort):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def _rows_to_dtos(self, rows: list[sqlite3.Row]) -> list[ItemCarteleraDTO]:
        items: list[ItemCarteleraDTO] = []
        for row in rows:
            h_ini_p = [int(p) for p in row["hora_inicio"].split(":")]
            h_fin_p = [int(p) for p in row["hora_fin"].split(":")]
            f_p = [int(p) for p in row["fecha"].split("-")]

            items.append(
                ItemCarteleraDTO(
                    reserva_id=row["reserva_id"],
                    aula_id=row["aula_id"],
                    aula_nombre=row["aula_nombre"],
                    pabellon=row["pabellon"],
                    materia_id=row["materia_id"],
                    materia_codigo=row["materia_codigo"],
                    materia_nombre=row["materia_nombre"],
                    carrera_nombre=row["carrera_nombre"],
                    nivel=row["nivel"],
                    docente_nombre=row["docente_nombre"],
                    fecha=date(f_p[0], f_p[1], f_p[2]),
                    hora_inicio=time(h_ini_p[0], h_ini_p[1]),
                    hora_fin=time(h_fin_p[0], h_fin_p[1])
                )
            )
        return items

    def consultar(self, filtro: ConsultarCarteleraFiltroDTO) -> list[ItemCarteleraDTO]:
        query = """
        SELECT 
            r.id AS reserva_id,
            a.id AS aula_id,
            a.nombre AS aula_nombre,
            a.pabellon AS pabellon,
            m.id AS materia_id,
            m.codigo AS materia_codigo,
            m.nombre AS materia_nombre,
            c.nombre AS carrera_nombre,
            c.nivel AS nivel,
            (d.nombres || ' ' || d.apellidos) AS docente_nombre,
            r.fecha,
            r.hora_inicio,
            r.hora_fin
        FROM reservas r
        INNER JOIN aulas a ON r.aula_id = a.id
        INNER JOIN materias m ON r.materia_id = m.id
        INNER JOIN carreras c ON m.carrera_id = c.id
        INNER JOIN docentes d ON r.docente_id = d.id
        WHERE r.fecha = ?
        """
        params: list = [filtro.fecha.isoformat()]

        if filtro.aula_id is not None:
            query += " AND r.aula_id = ?"
            params.append(filtro.aula_id)

        query += " ORDER BY r.hora_inicio ASC, a.nombre ASC;"

        cursor = self._conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()

        return self._rows_to_dtos(rows)

    def consultar_semanal(self, fecha_inicio: date, aula_id: int | None = None) -> list[ItemCarteleraDTO]:
        """
        Consulta la programación semanal (7 días continuos desde fecha_inicio).
        """
        fecha_fin = fecha_inicio + timedelta(days=6)

        query = """
        SELECT 
            r.id AS reserva_id,
            a.id AS aula_id,
            a.nombre AS aula_nombre,
            a.pabellon AS pabellon,
            m.id AS materia_id,
            m.codigo AS materia_codigo,
            m.nombre AS materia_nombre,
            c.nombre AS carrera_nombre,
            c.nivel AS nivel,
            (d.nombres || ' ' || d.apellidos) AS docente_nombre,
            r.fecha,
            r.hora_inicio,
            r.hora_fin
        FROM reservas r
        INNER JOIN aulas a ON r.aula_id = a.id
        INNER JOIN materias m ON r.materia_id = m.id
        INNER JOIN carreras c ON m.carrera_id = c.id
        INNER JOIN docentes d ON r.docente_id = d.id
        WHERE r.fecha >= ? AND r.fecha <= ?
        """
        params: list = [fecha_inicio.isoformat(), fecha_fin.isoformat()]

        if aula_id is not None:
            query += " AND r.aula_id = ?"
            params.append(aula_id)

        query += " ORDER BY r.fecha ASC, r.hora_inicio ASC, a.nombre ASC;"

        cursor = self._conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()

        return self._rows_to_dtos(rows)
