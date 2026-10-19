from datetime import date
from src.domain.entities.aula import Aula
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.repositories.reserva_repository import IReservaRepository
from src.domain.exceptions import ColisionAulaError, ColisionDocenteError


class MotorAntiColision:
    """
    Servicio de Dominio encargado de hacer cumplir el invariante de exclusión mutua
    y disponibilidad operativa para las reservas de aulas de la UNESR Los Teques.
    """

    def __init__(self, reserva_repo: IReservaRepository):
        self._reserva_repo = reserva_repo

    def validar_reserva(
        self,
        aula: Aula,
        docente_id: int,
        fecha: date,
        horario: RangoHorario,
        reserva_id_excluir: int | None = None
    ) -> None:
        # Regla 1: Disponibilidad operativa del aula física
        aula.validar_disponibilidad_operativa()

        # Regla 2: Motor Anti-Colisión de Espacio (No doble reserva en la misma aula y fecha)
        if aula.id is not None:
            reservas_existentes_aula = self._reserva_repo.buscar_por_aula_y_fecha(aula.id, fecha)
            for r in reservas_existentes_aula:
                if reserva_id_excluir is not None and r.id == reserva_id_excluir:
                    continue
                if r.horario.se_solapa_con(horario):
                    raise ColisionAulaError(
                        f"Conflicto de asignación: El aula '{aula.nombre}' ya posee una reserva "
                        f"de {r.horario.hora_inicio.strftime('%H:%M')} a {r.horario.hora_fin.strftime('%H:%M')} "
                        f"para la fecha {fecha.isoformat()}."
                    )

        # Regla 3: Motor Anti-Colisión de Docente (Un profesor no puede duplicarse)
        reservas_existentes_docente = self._reserva_repo.buscar_por_docente_y_fecha(docente_id, fecha)
        for r in reservas_existentes_docente:
            if reserva_id_excluir is not None and r.id == reserva_id_excluir:
                continue
            if r.horario.se_solapa_con(horario):
                raise ColisionDocenteError(
                    f"Conflicto de disponibilidad: El docente (ID {docente_id}) ya está asignado "
                    f"a otra aula en el horario {r.horario.hora_inicio.strftime('%H:%M')} a "
                    f"{r.horario.hora_fin.strftime('%H:%M')} para la fecha {fecha.isoformat()}."
                )
