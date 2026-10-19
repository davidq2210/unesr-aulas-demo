from dataclasses import dataclass
from src.domain.value_objects.rol_usuario import RolUsuario


@dataclass(frozen=True)
class CambiarEstadoAulaInputDTO:
    aula_id: int
    nuevo_estado: str
    usuario_rol: RolUsuario


@dataclass(frozen=True)
class AulaOutputDTO:
    id: int
    nombre: str
    capacidad: int
    pabellon: str
    estado: str
