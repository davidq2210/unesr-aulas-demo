import unittest
from datetime import time
from dataclasses import FrozenInstanceError

from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rol_usuario import RolUsuario
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.exceptions import RangoHorarioInvalidoError


class TestValueObjects(unittest.TestCase):
    def test_estado_aula_valores_permitidos(self):
        self.assertEqual(EstadoAula.DISPONIBLE.value, "DISPONIBLE")
        self.assertEqual(EstadoAula.EN_REMODELACION.value, "EN_REMODELACION")
        self.assertEqual(EstadoAula.INHABILITADA.value, "INHABILITADA")

    def test_rol_usuario_valores_permitidos(self):
        self.assertEqual(RolUsuario.DIRECTIVO.value, "DIRECTIVO")
        self.assertEqual(RolUsuario.COORDINADOR.value, "COORDINADOR")
        self.assertEqual(RolUsuario.PROFESOR.value, "PROFESOR")
        self.assertEqual(RolUsuario.ESTUDIANTE.value, "ESTUDIANTE")

    def test_rango_horario_creacion_valida(self):
        rango = RangoHorario(hora_inicio=time(7, 0), hora_fin=time(9, 0))
        self.assertEqual(rango.hora_inicio, time(7, 0))
        self.assertEqual(rango.hora_fin, time(9, 0))

    def test_rango_horario_invalido_inicio_igual_o_mayor_a_fin(self):
        with self.assertRaises(RangoHorarioInvalidoError):
            RangoHorario(hora_inicio=time(9, 0), hora_fin=time(9, 0))

        with self.assertRaises(RangoHorarioInvalidoError):
            RangoHorario(hora_inicio=time(10, 0), hora_fin=time(8, 0))

    def test_rango_horario_fuera_de_jornada_unesr(self):
        # Jornada operativa UNESR: 07:00 a 19:00
        with self.assertRaises(RangoHorarioInvalidoError):
            RangoHorario(hora_inicio=time(6, 59), hora_fin=time(8, 0))

        with self.assertRaises(RangoHorarioInvalidoError):
            RangoHorario(hora_inicio=time(18, 0), hora_fin=time(19, 1))

    def test_rango_horario_inmutable(self):
        rango = RangoHorario(hora_inicio=time(7, 0), hora_fin=time(9, 0))
        with self.assertRaises(FrozenInstanceError):
            rango.hora_inicio = time(8, 0)  # type: ignore

    def test_solapamiento_mismo_rango(self):
        r1 = RangoHorario(time(8, 0), time(10, 0))
        r2 = RangoHorario(time(8, 0), time(10, 0))
        self.assertTrue(r1.se_solapa_con(r2))
        self.assertTrue(r2.se_solapa_con(r1))

    def test_solapamiento_parcial_cruzado(self):
        r1 = RangoHorario(time(7, 0), time(9, 0))
        r2 = RangoHorario(time(8, 0), time(10, 0))
        self.assertTrue(r1.se_solapa_con(r2))
        self.assertTrue(r2.se_solapa_con(r1))

    def test_solapamiento_uno_contiene_al_otro(self):
        r_contenedor = RangoHorario(time(7, 0), time(12, 0))
        r_contenido = RangoHorario(time(8, 30), time(10, 30))
        self.assertTrue(r_contenedor.se_solapa_con(r_contenido))
        self.assertTrue(r_contenido.se_solapa_con(r_contenedor))

    def test_no_solapamiento_clases_contiguas(self):
        # Intervalos semi-abiertos [07:00, 09:00) y [09:00, 11:00) NO colisionan
        r1 = RangoHorario(time(7, 0), time(9, 0))
        r2 = RangoHorario(time(9, 0), time(11, 0))
        self.assertFalse(r1.se_solapa_con(r2))
        self.assertFalse(r2.se_solapa_con(r1))

    def test_no_solapamiento_rangos_disjuntos(self):
        r1 = RangoHorario(time(7, 0), time(9, 0))
        r2 = RangoHorario(time(11, 0), time(13, 0))
        self.assertFalse(r1.se_solapa_con(r2))
        self.assertFalse(r2.se_solapa_con(r1))


if __name__ == "__main__":
    unittest.main()
