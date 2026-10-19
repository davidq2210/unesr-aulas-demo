import unittest
import os
from datetime import date, time
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.database.schema import init_db_schema
from src.infrastructure.database.unit_of_work_sqlite import SqliteUnitOfWork
from src.application.use_cases.crear_reserva import CrearReservaUseCase
from src.application.dtos.reserva_dto import CrearReservaInputDTO
from src.domain.entities.aula import Aula
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.exceptions import ColisionAulaError


class TestConcurrenciaSqlite(unittest.TestCase):
    DB_PATH = "test_concurrencia.db"

    def setUp(self):
        self._limpiar_archivos()
        conn = get_db_connection(self.DB_PATH)
        init_db_schema(conn)

        # Crear datos iniciales requeridos
        conn.execute("INSERT INTO carreras (id, codigo, nombre, nivel) VALUES (1, 'ADM-01', 'Administración', 'PREGRADO');")
        conn.execute("INSERT INTO materias (id, carrera_id, codigo, nombre) VALUES (1, 1, 'MAT-01', 'Matemática');")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (1, 'V-100', 'Docente', 'Uno', 'd1@unesr.ve', 1);")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (2, 'V-200', 'Docente', 'Dos', 'd2@unesr.ve', 1);")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (3, 'V-300', 'Docente', 'Tres', 'd3@unesr.ve', 1);")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (4, 'V-400', 'Docente', 'Cuatro', 'd4@unesr.ve', 1);")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (5, 'V-500', 'Docente', 'Cinco', 'd5@unesr.ve', 1);")
        conn.execute("INSERT INTO usuarios (id, username, email, password_hash, rol) VALUES (1, 'admin', 'admin@unesr.ve', 'hash', 'DIRECTIVO');")
        conn.execute("INSERT INTO aulas (id, nombre, capacidad, pabellon, estado) VALUES (1, 'Aula Magna', 100, 'Pabellón Central', 'DISPONIBLE');")
        conn.close()

    def tearDown(self):
        self._limpiar_archivos()

    def _limpiar_archivos(self):
        for ext in ["", "-wal", "-shm"]:
            f = f"{self.DB_PATH}{ext}"
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError:
                    pass

    def test_carrera_de_reservas_simultaneas_en_misma_aula(self):
        """
        Simula 5 coordinadores intentando reservar exactamente la misma aula física,
        fecha y bloque horario en el mismo instante.
        Con BEGIN IMMEDIATE + busy_timeout=5000:
        - 1 transacción debe tener éxito.
        - Las otras 4 deben detectar la colisión y lanzar ColisionAulaError.
        - El total de reservas en la base de datos debe ser exactamente 1.
        """
        num_hilos = 5
        fecha_reserva = date(2026, 11, 2)
        hora_ini = time(8, 0)
        hora_fin = time(10, 0)

        def intentar_reserva(docente_id: int):
            # Cada hilo tiene su propio Unit of Work / conexión hacia la misma base de datos SQLite WAL
            uow = SqliteUnitOfWork(self.DB_PATH)
            use_case = CrearReservaUseCase(uow)
            dto = CrearReservaInputDTO(
                aula_id=1,
                docente_id=docente_id,
                materia_id=1,
                fecha=fecha_reserva,
                hora_inicio=hora_ini,
                hora_fin=hora_fin,
                usuario_id=1,
                observaciones=f"Reserva por hilo con docente {docente_id}"
            )
            return use_case.ejecutar(dto)

        exitos = []
        colisiones = []
        otros_errores = []

        with ThreadPoolExecutor(max_workers=num_hilos) as executor:
            futuros = {executor.submit(intentar_reserva, i + 1): i + 1 for i in range(num_hilos)}
            for futuro in as_completed(futuros):
                try:
                    res = futuro.result()
                    exitos.append(res)
                except ColisionAulaError as e:
                    colisiones.append(e)
                except Exception as e:
                    otros_errores.append(e)

        self.assertEqual(len(otros_errores), 0, f"Hubo errores inesperados: {otros_errores}")
        self.assertEqual(len(exitos), 1, f"Se esperaba exactamente 1 éxito, pero hubo {len(exitos)}")
        self.assertEqual(len(colisiones), num_hilos - 1, f"Se esperaban {num_hilos - 1} colisiones")

        # Comprobar en base de datos física
        conn = get_db_connection(self.DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reservas WHERE aula_id = 1 AND fecha = ?;", (fecha_reserva.isoformat(),))
        total_reservas = cur.fetchone()[0]
        conn.close()

        self.assertEqual(total_reservas, 1)


if __name__ == "__main__":
    unittest.main()
