from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class ItemCarteleraDTO:
    reserva_id: int
    aula_id: int
    aula_nombre: str
    pabellon: str
    materia_id: int
    materia_codigo: str
    materia_nombre: str
    carrera_nombre: str
    nivel: str  # PREGRADO | POSTGRADO | DOCTORADO | TALLER
    docente_nombre: str
    fecha: date
    hora_inicio: time
    hora_fin: time


@dataclass(frozen=True)
class ConsultarCarteleraFiltroDTO:
    fecha: date
    aula_id: int | None = None
