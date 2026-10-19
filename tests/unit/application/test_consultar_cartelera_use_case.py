import unittest
from datetime import date, time, timedelta

from src.application.dtos.cartelera_dto import ItemCarteleraDTO, ConsultarCarteleraFiltroDTO
from src.application.use_cases.consultar_cartelera import ConsultarCarteleraUseCase
from src.application.ports.cartelera_query_port import ICarteleraQueryPort


class FakeCarteleraQueryPort(ICarteleraQueryPort):
    def __init__(self):
        self.datos: list[ItemCarteleraDTO] = []

    def consultar(self, filtro: ConsultarCarteleraFiltroDTO) -> list[ItemCarteleraDTO]:
        res = [item for item in self.datos if item.fecha == filtro.fecha]
        if filtro.aula_id is not None:
            res = [item for item in res if item.aula_id == filtro.aula_id]
        return sorted(res, key=lambda x: (x.hora_inicio, x.aula_nombre))

    def consultar_semanal(self, fecha_inicio: date, aula_id: int | None = None) -> list[ItemCarteleraDTO]:
        fecha_fin = fecha_inicio + timedelta(days=5)  # Lunes a Sábado
        res = [item for item in self.datos if fecha_inicio <= item.fecha <= fecha_fin]
        if aula_id is not None:
            res = [item for item in res if item.aula_id == aula_id]
        return sorted(res, key=lambda x: (x.fecha, x.hora_inicio, x.aula_nombre))


class TestConsultarCarteleraUseCase(unittest.TestCase):
    def setUp(self):
        self.query_port = FakeCarteleraQueryPort()
        self.use_case = ConsultarCarteleraUseCase(self.query_port)
        self.lunes = date(2026, 11, 2)  # Supongamos lunes

        # Cargar datos ficticios con materia_codigo y nivel
        self.query_port.datos = [
            ItemCarteleraDTO(
                reserva_id=1,
                aula_id=1,
                aula_nombre="Aula 01",
                pabellon="Pabellón A",
                materia_id=10,
                materia_codigo="RMF-201",
                materia_nombre="Presupuesto y Finanzas",
                carrera_nombre="Lic. en Administración mención RMF",
                nivel="PREGRADO",
                docente_nombre="Prof. Simón Rodríguez",
                fecha=self.lunes,
                hora_inicio=time(7, 0),
                hora_fin=time(9, 0)
            ),
            ItemCarteleraDTO(
                reserva_id=2,
                aula_id=2,
                aula_nombre="Aula 02",
                pabellon="Pabellón A",
                materia_id=20,
                materia_codigo="MCE-101",
                materia_nombre="Metodología Andragógica Avanzada",
                carrera_nombre="Maestría en Ciencias de la Educación",
                nivel="POSTGRADO",
                docente_nombre="Prof. Andrés Bello",
                fecha=self.lunes,
                hora_inicio=time(9, 0),
                hora_fin=time(11, 0)
            ),
            ItemCarteleraDTO(
                reserva_id=3,
                aula_id=1,
                aula_nombre="Aula 01",
                pabellon="Pabellón A",
                materia_id=30,
                materia_codigo="DOC-01",
                materia_nombre="Seminario de Tesis Doctoral",
                carrera_nombre="Doctorado en Ciencias de la Educación",
                nivel="DOCTORADO",
                docente_nombre="Prof. José Martí",
                fecha=self.lunes + timedelta(days=2),  # Miércoles
                hora_inicio=time(7, 0),
                hora_fin=time(9, 0)
            )
        ]

    def test_consultar_cartelera_por_fecha_incluye_codigo_y_nivel(self):
        filtro = ConsultarCarteleraFiltroDTO(fecha=self.lunes)
        cartelera = self.use_case.ejecutar(filtro)

        self.assertEqual(len(cartelera), 2)
        self.assertEqual(cartelera[0].materia_codigo, "RMF-201")
        self.assertEqual(cartelera[0].nivel, "PREGRADO")
        self.assertEqual(cartelera[1].materia_codigo, "MCE-101")
        self.assertEqual(cartelera[1].nivel, "POSTGRADO")

    def test_consultar_cartelera_semanal_completa(self):
        cartelera_semana = self.use_case.ejecutar_semanal(fecha_inicio=self.lunes)

        self.assertEqual(len(cartelera_semana), 3)
        self.assertEqual(cartelera_semana[0].fecha, self.lunes)
        self.assertEqual(cartelera_semana[2].fecha, self.lunes + timedelta(days=2))
        self.assertEqual(cartelera_semana[2].nivel, "DOCTORADO")

    def test_consultar_cartelera_semanal_filtrada_por_aula(self):
        cartelera_aula_1 = self.use_case.ejecutar_semanal(fecha_inicio=self.lunes, aula_id=1)

        self.assertEqual(len(cartelera_aula_1), 2)
        for c in cartelera_aula_1:
            self.assertEqual(c.aula_id, 1)


if __name__ == "__main__":
    unittest.main()
