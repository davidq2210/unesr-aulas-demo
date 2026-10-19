import unittest
from datetime import date, time

from src.domain.entities.aula import Aula
from src.domain.entities.reserva import Reserva
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.services.motor_anti_colision import MotorAntiColision
from src.domain.repositories.reserva_repository import IReservaRepository
from src.domain.exceptions import (
    AulaNoDisponibleError,
    ColisionAulaError,
    ColisionDocenteError
)


class FakeReservaRepository(IReservaRepository):
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


class TestMotorAntiColision(unittest.TestCase):
    def setUp(self):
        self.repo = FakeReservaRepository()
        self.motor = MotorAntiColision(reserva_repo=self.repo)
        self.aula_disponible = Aula(
            id=1,
            nombre="Aula 101",
            capacidad=30,
            pabellon="A",
            estado=EstadoAula.DISPONIBLE
        )
        self.fecha = date(2026, 11, 2)

    def test_rechaza_reserva_si_aula_no_esta_disponible(self):
        aula_remodelacion = Aula(
            id=2,
            nombre="Aula 102",
            capacidad=30,
            pabellon="A",
            estado=EstadoAula.EN_REMODELACION
        )
        horario = RangoHorario(time(8, 0), time(10, 0))

        with self.assertRaises(AulaNoDisponibleError):
            self.motor.validar_reserva(
                aula=aula_remodelacion,
                docente_id=1,
                fecha=self.fecha,
                horario=horario
            )

    def test_rechaza_si_existe_colision_en_la_misma_aula(self):
        # Reserva existente: 08:00 a 10:00
        self.repo.guardar(
            Reserva(
                id=1,
                aula_id=self.aula_disponible.id,
                docente_id=10,
                materia_id=1,
                fecha=self.fecha,
                horario=RangoHorario(time(8, 0), time(10, 0)),
                creado_por_usuario_id=1
            )
        )

        # Intento de reserva solapada: 09:00 a 11:00
        horario_solapado = RangoHorario(time(9, 0), time(11, 0))
        with self.assertRaises(ColisionAulaError) as ctx:
            self.motor.validar_reserva(
                aula=self.aula_disponible,
                docente_id=20,  # Otro docente, pero la misma aula ocupada
                fecha=self.fecha,
                horario=horario_solapado
            )
        self.assertIn("Aula 101", str(ctx.exception))

    def test_permite_reserva_en_clases_contiguas_misma_aula(self):
        # Reserva existente: 08:00 a 10:00
        self.repo.guardar(
            Reserva(
                id=1,
                aula_id=self.aula_disponible.id,
                docente_id=10,
                materia_id=1,
                fecha=self.fecha,
                horario=RangoHorario(time(8, 0), time(10, 0)),
                creado_por_usuario_id=1
            )
        )

        # Nueva reserva contigua: 10:00 a 12:00 -> Válida (no colisiona)
        horario_contiguo = RangoHorario(time(10, 0), time(12, 0))
        try:
            self.motor.validar_reserva(
                aula=self.aula_disponible,
                docente_id=20,
                fecha=self.fecha,
                horario=horario_contiguo
            )
        except (ColisionAulaError, ColisionDocenteError):
            self.fail("No debió lanzar ColisionAulaError en clases contiguas.")

    def test_permite_reserva_en_misma_aula_pero_distinta_fecha(self):
        # Reserva existente: 08:00 a 10:00 el 2026-11-02
        self.repo.guardar(
            Reserva(
                id=1,
                aula_id=self.aula_disponible.id,
                docente_id=10,
                materia_id=1,
                fecha=self.fecha,
                horario=RangoHorario(time(8, 0), time(10, 0)),
                creado_por_usuario_id=1
            )
        )

        # Misma aula y misma hora el 2026-11-03 -> Válida
        otra_fecha = date(2026, 11, 3)
        horario = RangoHorario(time(8, 0), time(10, 0))
        self.motor.validar_reserva(
            aula=self.aula_disponible,
            docente_id=20,
            fecha=otra_fecha,
            horario=horario
        )

    def test_rechaza_si_docente_esta_asignado_a_otra_aula_al_mismo_tiempo(self):
        # Docente 10 ya tiene clase en Aula 999 de 08:00 a 10:00
        self.repo.guardar(
            Reserva(
                id=1,
                aula_id=999,
                docente_id=10,
                materia_id=1,
                fecha=self.fecha,
                horario=RangoHorario(time(8, 0), time(10, 0)),
                creado_por_usuario_id=1
            )
        )

        # Se intenta asignar al Docente 10 en Aula 101 de 09:00 a 11:00
        horario_solapado = RangoHorario(time(9, 0), time(11, 0))
        with self.assertRaises(ColisionDocenteError) as ctx:
            self.motor.validar_reserva(
                aula=self.aula_disponible,
                docente_id=10,
                fecha=self.fecha,
                horario=horario_solapado
            )
        self.assertIn("10", str(ctx.exception))

    def test_permite_actualizacion_excluyendo_propia_reserva(self):
        # Reserva existente: ID 1
        reserva = Reserva(
            id=1,
            aula_id=self.aula_disponible.id,
            docente_id=10,
            materia_id=1,
            fecha=self.fecha,
            horario=RangoHorario(time(8, 0), time(10, 0)),
            creado_por_usuario_id=1
        )
        self.repo.guardar(reserva)

        # Actualizar la reserva 1 con el mismo horario no debe colisionar consigo misma
        self.motor.validar_reserva(
            aula=self.aula_disponible,
            docente_id=10,
            fecha=self.fecha,
            horario=RangoHorario(time(8, 0), time(10, 0)),
            reserva_id_excluir=1
        )


if __name__ == "__main__":
    unittest.main()
