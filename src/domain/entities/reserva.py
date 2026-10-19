from dataclasses import dataclass
from datetime import date
from src.domain.value_objects.rango_horario import RangoHorario


@dataclass
class Reserva:
    id: int | None
    aula_id: int
    docente_id: int
    materia_id: int
    fecha: date
    horario: RangoHorario
    creado_por_usuario_id: int
    observaciones: str = ""
