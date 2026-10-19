import unittest
import os
import sqlite3
from datetime import date, time, timedelta

from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.database.schema import init_db_schema
from src.infrastructure.database.unit_of_work_sqlite import SqliteUnitOfWork
from src.infrastructure.persistence.sqlite_aula_repository import SqliteAulaRepository
from src.infrastructure.persistence.sqlite_reserva_repository import SqliteReservaRepository
from src.infrastructure.persistence.sqlite_cartelera_adapter import SqliteCarteleraQueryAdapter
from src.infrastructure.persistence.sqlite_catalogo_repository import SqliteCatalogoRepository
from src.domain.entities.aula import Aula
from src.domain.entities.reserva import Reserva
from src.domain.entities.academico import Docente, Materia
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rango_horario import RangoHorario
from src.application.dtos.cartelera_dto import ConsultarCarteleraFiltroDTO


class TestSqliteRepositories(unittest.TestCase):
    DB_PATH = "test_unesr_aulas.db"

    def setUp(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)
        conn = get_db_connection(self.DB_PATH)
        init_db_schema(conn)
        conn.close()

    def tearDown(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)
        wal = f"{self.DB_PATH}-wal"
        shm = f"{self.DB_PATH}-shm"
        if os.path.exists(wal):
            os.remove(wal)
        if os.path.exists(shm):
            os.remove(shm)

    def test_pragmas_wal_y_timeout(self):
        conn = get_db_connection(self.DB_PATH)
        cur = conn.cursor()
        
        cur.execute("PRAGMA journal_mode;")
        journal = cur.fetchone()[0]
        self.assertEqual(journal.lower(), "wal")

        cur.execute("PRAGMA busy_timeout;")
        timeout = cur.fetchone()[0]
        self.assertEqual(timeout, 5000)

        cur.execute("PRAGMA foreign_keys;")
        fk = cur.fetchone()[0]
        self.assertEqual(fk, 1)

        conn.close()

    def test_aula_repository_guardar_y_obtener(self):
        conn = get_db_connection(self.DB_PATH)
        repo = SqliteAulaRepository(conn)

        aula = Aula(id=None, nombre="Aula 01", capacidad=35, pabellon="Pabellón 1", estado=EstadoAula.DISPONIBLE)
        guardada = repo.guardar(aula)

        self.assertIsNotNone(guardada.id)
        recuperada = repo.obtener_por_id(guardada.id)
        self.assertIsNotNone(recuperada)
        self.assertEqual(recuperada.nombre, "Aula 01")
        self.assertEqual(recuperada.estado, EstadoAula.DISPONIBLE)

        # Actualizar estado
        recuperada.cambiar_estado(EstadoAula.EN_REMODELACION)
        repo.guardar(recuperada)

        actualizada = repo.obtener_por_id(guardada.id)
        self.assertEqual(actualizada.estado, EstadoAula.EN_REMODELACION)
        conn.close()

    def test_reserva_repository_y_unit_of_work(self):
        conn = get_db_connection(self.DB_PATH)
        conn.execute("INSERT INTO carreras (id, codigo, nombre, nivel) VALUES (1, 'INF-01', 'Informática', 'PREGRADO')")
        conn.execute("INSERT INTO materias (id, carrera_id, codigo, nombre) VALUES (1, 1, 'ALG-101', 'Algoritmos')")
        conn.execute("INSERT INTO docentes (id, cedula, nombres, apellidos, email, activo) VALUES (1, 'V-11111', 'Alan', 'Turing', 'aturing@unesr.ve', 1)")
        conn.execute("INSERT INTO usuarios (id, username, email, password_hash, rol) VALUES (1, 'admin', 'admin@unesr.ve', 'hash', 'DIRECTIVO')")
        conn.close()

        uow = SqliteUnitOfWork(self.DB_PATH)
        with uow:
            aula = Aula(id=None, nombre="Aula 02", capacidad=30, pabellon="Pabellón 1", estado=EstadoAula.DISPONIBLE)
            uow.aulas.guardar(aula)
            
            reserva = Reserva(
                id=None,
                aula_id=aula.id,
                docente_id=1,
                materia_id=1,
                fecha=date(2026, 11, 2),
                horario=RangoHorario(time(7, 0), time(9, 0)),
                creado_por_usuario_id=1,
                observaciones="Prueba UoW"
            )
            uow.reservas.guardar(reserva)

        conn2 = get_db_connection(self.DB_PATH)
        reserva_repo = SqliteReservaRepository(conn2)
        reservas_aula = reserva_repo.buscar_por_aula_y_fecha(aula.id, date(2026, 11, 2))
        self.assertEqual(len(reservas_aula), 1)
        self.assertEqual(reservas_aula[0].horario.hora_inicio, time(7, 0))

        cartelera_adapter = SqliteCarteleraQueryAdapter(conn2)
        items = cartelera_adapter.consultar(ConsultarCarteleraFiltroDTO(fecha=date(2026, 11, 2)))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].aula_nombre, "Aula 02")
        self.assertEqual(items[0].materia_codigo, "ALG-101")
        self.assertEqual(items[0].nivel, "PREGRADO")
        self.assertEqual(items[0].materia_nombre, "Algoritmos")
        self.assertEqual(items[0].docente_nombre, "Alan Turing")

        # Probar consulta semanal
        items_semana = cartelera_adapter.consultar_semanal(fecha_inicio=date(2026, 11, 2))
        self.assertEqual(len(items_semana), 1)
        self.assertEqual(items_semana[0].reserva_id, items[0].reserva_id)
        conn2.close()

    def test_catalogo_repository_guardar_docente_y_materia(self):
        conn = get_db_connection(self.DB_PATH)
        conn.execute("INSERT INTO carreras (id, codigo, nombre, nivel) VALUES (1, 'POST-01', 'Maestría en Educación', 'POSTGRADO')")
        catalogo = SqliteCatalogoRepository(conn)

        docente = Docente(id=None, cedula="V-99999", nombres="Luis", apellidos="Beltrán", email="lbeltran@unesr.ve", activo=True)
        docente_guardado = catalogo.guardar_docente(docente)
        self.assertIsNotNone(docente_guardado.id)

        materia = Materia(id=None, carrera_id=1, codigo="MED-101", nombre="Andragogía de Adultos")
        materia_guardada = catalogo.guardar_materia(materia)
        self.assertIsNotNone(materia_guardada.id)

        docentes_db = catalogo.listar_docentes()
        self.assertEqual(len(docentes_db), 1)
        self.assertEqual(docentes_db[0].cedula, "V-99999")

        materias_db = catalogo.listar_materias(carrera_id=1)
        self.assertEqual(len(materias_db), 1)
        self.assertEqual(materias_db[0].codigo, "MED-101")
        conn.close()


if __name__ == "__main__":
    unittest.main()
