import unittest
from datetime import date, time

from src.domain.entities.aula import Aula
from src.domain.entities.academico import Carrera, Materia, Docente
from src.domain.entities.usuario import Usuario
from src.domain.entities.reserva import Reserva
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rol_usuario import RolUsuario
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.exceptions import AulaNoDisponibleError


class TestEntities(unittest.TestCase):
    def test_aula_disponibilidad_operativa_ok(self):
        aula = Aula(
            id=1,
            nombre="Aula 01",
            capacidad=35,
            pabellon="Pabellón 1",
            estado=EstadoAula.DISPONIBLE
        )
        # No debe lanzar excepción
        aula.validar_disponibilidad_operativa()
        self.assertEqual(aula.estado, EstadoAula.DISPONIBLE)

    def test_aula_no_disponible_en_remodelacion_lanza_error(self):
        aula = Aula(
            id=2,
            nombre="Aula 02",
            capacidad=40,
            pabellon="Pabellón 1",
            estado=EstadoAula.EN_REMODELACION
        )
        with self.assertRaises(AulaNoDisponibleError) as ctx:
            aula.validar_disponibilidad_operativa()
        self.assertIn("EN_REMODELACION", str(ctx.exception))

    def test_aula_no_disponible_inhabilitada_lanza_error(self):
        aula = Aula(
            id=3,
            nombre="Aula 03",
            capacidad=30,
            pabellon="Pabellón 2",
            estado=EstadoAula.INHABILITADA
        )
        with self.assertRaises(AulaNoDisponibleError) as ctx:
            aula.validar_disponibilidad_operativa()
        self.assertIn("INHABILITADA", str(ctx.exception))

    def test_aula_cambiar_estado(self):
        aula = Aula(
            id=1,
            nombre="Aula 01",
            capacidad=35,
            pabellon="Pabellón 1",
            estado=EstadoAula.DISPONIBLE
        )
        aula.cambiar_estado(EstadoAula.EN_REMODELACION)
        self.assertEqual(aula.estado, EstadoAula.EN_REMODELACION)

    def test_entidades_academicas_creacion(self):
        carrera = Carrera(id=1, codigo="ADM-01", nombre="Administración de Recursos Materiales", nivel="PREGRADO")
        self.assertEqual(carrera.codigo, "ADM-01")

        materia = Materia(id=10, carrera_id=1, codigo="PRE-101", nombre="Presupuesto y Finanzas")
        self.assertEqual(materia.carrera_id, 1)

        docente = Docente(
            id=100,
            cedula="V-12345678",
            nombres="Simón",
            apellidos="Rodríguez",
            email="srodriguez@unesr.edu.ve",
            activo=True
        )
        self.assertEqual(docente.nombre_completo, "Simón Rodríguez")

    def test_usuario_roles_y_permisos(self):
        coord = Usuario(
            id=1,
            username="coordinador1",
            email="coord@unesr.edu.ve",
            password_hash="hash_secreto",
            rol=RolUsuario.COORDINADOR
        )
        self.assertTrue(coord.es_gestion_academica())

        prof = Usuario(
            id=2,
            username="profesor1",
            email="prof@unesr.edu.ve",
            password_hash="hash_secreto",
            rol=RolUsuario.PROFESOR,
            docente_id=100
        )
        self.assertFalse(prof.es_gestion_academica())
        self.assertEqual(prof.docente_id, 100)

    def test_reserva_creacion(self):
        horario = RangoHorario(time(8, 0), time(10, 0))
        reserva = Reserva(
            id=1,
            aula_id=1,
            docente_id=100,
            materia_id=10,
            fecha=date(2026, 11, 2),
            horario=horario,
            creado_por_usuario_id=2,
            observaciones="Clase presencial quincenal"
        )
        self.assertEqual(reserva.aula_id, 1)
        self.assertEqual(reserva.fecha, date(2026, 11, 2))
        self.assertEqual(reserva.horario, horario)


if __name__ == "__main__":
    unittest.main()
