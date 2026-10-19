from enum import Enum


class RolUsuario(str, Enum):
    DIRECTIVO = "DIRECTIVO"
    COORDINADOR = "COORDINADOR"
    PROFESOR = "PROFESOR"
    ESTUDIANTE = "ESTUDIANTE"
