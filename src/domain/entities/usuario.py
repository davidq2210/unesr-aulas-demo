from dataclasses import dataclass
from src.domain.value_objects.rol_usuario import RolUsuario


@dataclass
class Usuario:
    id: int | None
    username: str
    email: str
    password_hash: str
    rol: RolUsuario
    docente_id: int | None = None
    activo: bool = True

    def es_gestion_academica(self) -> bool:
        """Determina si el usuario tiene privilegios de DIRECTIVO o COORDINADOR."""
        return self.rol in (RolUsuario.DIRECTIVO, RolUsuario.COORDINADOR)
