from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class CrearReservaInputDTO:
    aula_id: int
    docente_id: int
    materia_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    usuario_id: int
    observaciones: str = ""


@dataclass(frozen=True)
class ReservaOutputDTO:
    id: int
    aula_id: int
    docente_id: int
    materia_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    observaciones: str
