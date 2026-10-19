import unittest

from src.application.dtos.aula_dto import CambiarEstadoAulaInputDTO
from src.application.use_cases.cambiar_estado_aula import CambiarEstadoAulaUseCase
from src.domain.entities.aula import Aula
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rol_usuario import RolUsuario
from src.domain.repositories.aula_repository import IAulaRepository
from src.domain.repositories.reserva_repository import IReservaRepository
from src.domain.exceptions import EntidadNoEncontradaError
from src.application.exceptions import PermisoDenegadoError
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


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self, aula_repo: IAulaRepository):
        self.aulas = aula_repo
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


class TestCambiarEstadoAulaUseCase(unittest.TestCase):
    def setUp(self):
        self.aula_repo = InMemoryAulaRepository()
        self.uow = FakeUnitOfWork(self.aula_repo)
        self.use_case = CambiarEstadoAulaUseCase(self.uow)

        self.aula = Aula(
            id=1,
            nombre="Aula 101",
            capacidad=35,
            pabellon="A",
            estado=EstadoAula.DISPONIBLE
        )
        self.aula_repo.guardar(self.aula)

    def test_directivo_puede_cambiar_estado_a_remodelacion(self):
        dto = CambiarEstadoAulaInputDTO(
            aula_id=1,
            nuevo_estado="EN_REMODELACION",
            usuario_rol=RolUsuario.DIRECTIVO
        )
        resultado = self.use_case.ejecutar(dto)

        self.assertEqual(resultado.estado, "EN_REMODELACION")
        self.assertTrue(self.uow.committed)
        self.assertEqual(self.aula_repo.obtener_por_id(1).estado, EstadoAula.EN_REMODELACION)

    def test_coordinador_puede_inhabilitar_aula(self):
        dto = CambiarEstadoAulaInputDTO(
            aula_id=1,
            nuevo_estado="INHABILITADA",
            usuario_rol=RolUsuario.COORDINADOR
        )
        resultado = self.use_case.ejecutar(dto)

        self.assertEqual(resultado.estado, "INHABILITADA")
        self.assertEqual(self.aula_repo.obtener_por_id(1).estado, EstadoAula.INHABILITADA)

    def test_profesor_o_estudiante_no_tienen_permiso(self):
        dto = CambiarEstadoAulaInputDTO(
            aula_id=1,
            nuevo_estado="EN_REMODELACION",
            usuario_rol=RolUsuario.PROFESOR
        )
        with self.assertRaises(PermisoDenegadoError):
            self.use_case.ejecutar(dto)

    def test_aula_inexistente_lanza_error(self):
        dto = CambiarEstadoAulaInputDTO(
            aula_id=999,
            nuevo_estado="DISPONIBLE",
            usuario_rol=RolUsuario.DIRECTIVO
        )
        with self.assertRaises(EntidadNoEncontradaError):
            self.use_case.ejecutar(dto)


if __name__ == "__main__":
    unittest.main()
