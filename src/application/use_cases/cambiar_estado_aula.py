from src.application.ports.unit_of_work import IUnitOfWork
from src.application.dtos.aula_dto import CambiarEstadoAulaInputDTO, AulaOutputDTO
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.value_objects.rol_usuario import RolUsuario
from src.domain.exceptions import EntidadNoEncontradaError
from src.application.exceptions import PermisoDenegadoError


class CambiarEstadoAulaUseCase:
    """
    Caso de Uso: Cambiar Estado Operativo de un Aula.
    Aplica RBAC estricto: solo roles directivos y de coordinación académica
    pueden modificar el estado operativo de los recursos físicos.
    """

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    def ejecutar(self, dto: CambiarEstadoAulaInputDTO) -> AulaOutputDTO:
        # Validación de seguridad RBAC
        if dto.usuario_rol not in (RolUsuario.DIRECTIVO, RolUsuario.COORDINADOR):
            raise PermisoDenegadoError(
                f"El rol '{dto.usuario_rol}' no tiene autorización para modificar el estado del aula."
            )

        with self._uow as uow:
            aula = uow.aulas.obtener_por_id(dto.aula_id)
            if aula is None:
                raise EntidadNoEncontradaError(f"No existe el aula física con ID {dto.aula_id}.")

            nuevo_estado = EstadoAula(dto.nuevo_estado)
            aula.cambiar_estado(nuevo_estado)
            aula_actualizada = uow.aulas.guardar(aula)

        return AulaOutputDTO(
            id=aula_actualizada.id,
            nombre=aula_actualizada.nombre,
            capacidad=aula_actualizada.capacidad,
            pabellon=aula_actualizada.pabellon,
            estado=aula_actualizada.estado.value
        )
