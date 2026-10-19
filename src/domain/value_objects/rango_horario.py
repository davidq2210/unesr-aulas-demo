from dataclasses import dataclass
from datetime import time
from src.domain.exceptions import RangoHorarioInvalidoError


@dataclass(frozen=True)
class RangoHorario:
    hora_inicio: time
    hora_fin: time

    def __post_init__(self):
        if self.hora_inicio >= self.hora_fin:
            raise RangoHorarioInvalidoError(
                f"La hora de inicio ({self.hora_inicio}) debe ser anterior a la hora de fin ({self.hora_fin})."
            )

        limite_apertura = time(7, 0)
        limite_cierre = time(19, 0)

        if self.hora_inicio < limite_apertura or self.hora_fin > limite_cierre:
            raise RangoHorarioInvalidoError(
                "El horario debe estar comprendido dentro de la jornada operativa UNESR (07:00 a 19:00)."
            )

    def se_solapa_con(self, otro: "RangoHorario") -> bool:
        """
        Determina si dos intervalos semi-abiertos [inicio, fin) se intersectan.
        Dos rangos se solapan si y solo si: max(inicio_1, inicio_2) < min(fin_1, fin_2).
        Si fin_1 == inicio_2, el resultado es False (clases contiguas no colisionan).
        """
        return max(self.hora_inicio, otro.hora_inicio) < min(self.hora_fin, otro.hora_fin)
