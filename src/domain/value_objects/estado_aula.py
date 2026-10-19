from enum import Enum


class EstadoAula(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    EN_REMODELACION = "EN_REMODELACION"
    INHABILITADA = "INHABILITADA"
