import unittest
from datetime import date, time

from src.application.dtos.reserva_dto import CrearReservaInputDTO
from src.application.use_cases.crear_reserva import CrearReservaUseCase
from src.domain.entities.aula import Aula
from src.domain.entities.reserva import Reserva
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.repositories.aula_repository import IAulaRepository
from src.domain.repositories.reserva_repository import IReservaRepository
from src.domain.exceptions import (
    AulaNoDisponibleError,
    ColisionAulaError,
    ColisionDocenteError,
    EntidadNoEncontradaError
)
from src.application.ports.unit_of_work import IUnitOfWork


class InMemoryAulaRepository(IAulaRepository):
    def __init__(self):
        self.aulas: dict[int, Aula] = {}

    def obtener_por_id(self, id: int) -> Aula | None:
        return self.aulas.get(id)

    def listar_todas(self) -> list[Aula]:
        return list(self.aulas.values())

    def guardar(self, aula: Aula) -> Aula:
        if aula.id is None:
            aula.id = len(self.aulas) + 1
        self.aulas[aula.id] = aula
        return aula


class InMemoryReservaRepository(IReservaRepository):
    def __init__(self):
        self.reservas: list[Reserva] = []

    def buscar_por_aula_y_fecha(self, aula_id: int, fecha: date) -> list[Reserva]:
        return [r for r in self.reservas if r.aula_id == aula_id and r.fecha == fecha]

    def buscar_por_docente_y_fecha(self, docente_id: int, fecha: date) -> list[Reserva]:
        return [r for r in self.reservas if r.docente_id == docente_id and r.fecha == fecha]

    def guardar(self, reserva: Reserva) -> Reserva:
        if reserva.id is None:
            reserva.id = len(self.reservas) + 1
        self.reservas.append(reserva)
        return reserva

    def obtener_por_id(self, id: int) -> Reserva | None:
        for r in self.reservas:
            if r.id == id:
                return r
        return None

    def listar_por_fecha(self, fecha: date) -> list[Reserva]:
        return [r for r in self.reservas if r.fecha == fecha]


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self, aula_repo: IAulaRepository, reserva_repo: IReservaRepository):
        self.aulas = aula_repo
        self.reservas = reserva_repo
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


class TestCrearReservaUseCase(unittest.TestCase):
    def setUp(self):
        self.aula_repo = InMemoryAulaRepository()
        self.reserva_repo = InMemoryReservaRepository()
        self.uow = FakeUnitOfWork(self.aula_repo, self.reserva_repo)
        self.use_case = CrearReservaUseCase(self.uow)

        # Crear un aula disponible
        self.aula = Aula(
            id=1,
            nombre="Aula 101",
            capacidad=30,
            pabellon="A",
            estado=EstadoAula.DISPONIBLE
        )
        self.aula_repo.guardar(self.aula)

    def test_crear_reserva_exitosamente(self):
        dto = CrearReservaInputDTO(
            aula_id=1,
            docente_id=10,
            materia_id=100,
            fecha=date(2026, 11, 2),
            hora_inicio=time(7, 0),
            hora_fin=time(9, 0),
            usuario_id=1,
            observaciones="Clase inaugural"
        )
        resultado = self.use_case.ejecutar(dto)

        self.assertIsNotNone(resultado.id)
        self.assertEqual(resultado.aula_id, 1)
        self.assertEqual(resultado.docente_id, 10)
        self.assertTrue(self.uow.committed)
        self.assertEqual(len(self.reserva_repo.reservas), 1)

    def test_crear_reserva_falla_si_aula_no_existe(self):
        dto = CrearReservaInputDTO(
            aula_id=999,
            docente_id=10,
            materia_id=100,
            fecha=date(2026, 11, 2),
            hora_inicio=time(7, 0),
            hora_fin=time(9, 0),
            usuario_id=1
        )
        with self.assertRaises(EntidadNoEncontradaError):
            self.use_case.ejecutar(dto)

    def test_crear_reserva_falla_por_aula_en_remodelacion(self):
        self.aula.estado = EstadoAula.EN_REMODELACION
        self.aula_repo.guardar(self.aula)

        dto = CrearReservaInputDTO(
            aula_id=1,
            docente_id=10,
            materia_id=100,
            fecha=date(2026, 11, 2),
            hora_inicio=time(7, 0),
            hora_fin=time(9, 0),
            usuario_id=1
        )
        with self.assertRaises(AulaNoDisponibleError):
            self.use_case.ejecutar(dto)

    def test_crear_reserva_falla_por_colision_de_aula(self):
        # Primera reserva
        dto1 = CrearReservaInputDTO(
            aula_id=1,
            docente_id=10,
            materia_id=100,
            fecha=date(2026, 11, 2),
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            usuario_id=1
        )
        self.use_case.ejecutar(dto1)

        # Segunda reserva que se solapa (09:00 a 11:00) en la misma aula
        dto2 = CrearReservaInputDTO(
            aula_id=1,
            docente_id=20,
            materia_id=101,
            fecha=date(2026, 11, 2),
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
            usuario_id=2
        )
        with self.assertRaises(ColisionAulaError):
            self.use_case.ejecutar(dto2)

    def test_crear_reserva_falla_por_colision_de_docente(self):
        # Crear segunda aula
        aula2 = Aula(id=2, nombre="Aula 102", capacidad=30, pabellon="A", estado=EstadoAula.DISPONIBLE)
        self.aula_repo.guardar(aula2)

        # Docente 10 reserva Aula 1 de 08:00 a 10:00
        dto1 = CrearReservaInputDTO(
            aula_id=1,
            docente_id=10,
            materia_id=100,
            fecha=date(2026, 11, 2),
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            usuario_id=1
        )
        self.use_case.ejecutar(dto1)

        # Mismo Docente 10 intenta reservar Aula 2 de 09:00 a 11:00
        dto2 = CrearReservaInputDTO(
            aula_id=2,
            docente_id=10,
            materia_id=102,
            fecha=date(2026, 11, 2),
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
            usuario_id=1
        )
        with self.assertRaises(ColisionDocenteError):
            self.use_case.ejecutar(dto2)


if __name__ == "__main__":
    unittest.main()
