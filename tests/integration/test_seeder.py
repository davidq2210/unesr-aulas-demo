import unittest
import os
from datetime import date, time

from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.database.schema import init_db_schema
from src.infrastructure.database.seeder import seed_database
from src.infrastructure.persistence.sqlite_aula_repository import SqliteAulaRepository
from src.infrastructure.persistence.sqlite_reserva_repository import SqliteReservaRepository
from src.domain.value_objects.estado_aula import EstadoAula


class TestSeeder(unittest.TestCase):
    DB_PATH = "test_seeder.db"

    def setUp(self):
        self._limpiar()
        conn = get_db_connection(self.DB_PATH)
        init_db_schema(conn)
        conn.close()

    def tearDown(self):
        self._limpiar()

    def _limpiar(self):
        for ext in ["", "-wal", "-shm"]:
            f = f"{self.DB_PATH}{ext}"
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError:
                    pass

    def test_seeder_puebla_datos_iniciales_idempotente(self):
        # Primera ejecución
        seed_database(self.DB_PATH)

        conn = get_db_connection(self.DB_PATH)
        aula_repo = SqliteAulaRepository(conn)
        aulas = aula_repo.listar_todas()

        self.assertEqual(len(aulas), 12)
        # Primeras 8 disponibles
        for a in aulas[:8]:
            self.assertEqual(a.estado, EstadoAula.DISPONIBLE)
        # 9 y 10 en remodelación
        self.assertEqual(aulas[8].estado, EstadoAula.EN_REMODELACION)
        self.assertEqual(aulas[9].estado, EstadoAula.EN_REMODELACION)
        # 11 y 12 inhabilitadas
        self.assertEqual(aulas[10].estado, EstadoAula.INHABILITADA)
        self.assertEqual(aulas[11].estado, EstadoAula.INHABILITADA)

        # Reserva inicial de hoy
        reserva_repo = SqliteReservaRepository(conn)
        hoy = date.today()
        reservas_hoy = reserva_repo.buscar_por_aula_y_fecha(aulas[0].id, hoy)
        self.assertEqual(len(reservas_hoy), 1)
        self.assertEqual(reservas_hoy[0].horario.hora_inicio, time(7, 0))
        self.assertEqual(reservas_hoy[0].horario.hora_fin, time(9, 0))

        conn.close()

        # Segunda ejecución no duplica registros
        seed_database(self.DB_PATH)
        conn2 = get_db_connection(self.DB_PATH)
        aulas2 = SqliteAulaRepository(conn2).listar_todas()
        self.assertEqual(len(aulas2), 12)
        conn2.close()


if __name__ == "__main__":
    unittest.main()
