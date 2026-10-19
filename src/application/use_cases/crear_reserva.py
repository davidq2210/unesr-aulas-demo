from src.application.ports.unit_of_work import IUnitOfWork
from src.application.dtos.reserva_dto import CrearReservaInputDTO, ReservaOutputDTO
from src.domain.entities.reserva import Reserva
from src.domain.value_objects.rango_horario import RangoHorario
from src.domain.services.motor_anti_colision import MotorAntiColision
from src.domain.exceptions import EntidadNoEncontradaError


class CrearReservaUseCase:
    """
    Caso de Uso: Crear Reserva de Aula.
    Orquesta la validación de existencia del aula física, verificación de disponibilidad
    operativa y el motor anti-colisión bajo una transacción atómica del Unit of Work.
    """

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    def ejecutar(self, dto: CrearReservaInputDTO) -> ReservaOutputDTO:
        with self._uow as uow:
            aula = uow.aulas.obtener_por_id(dto.aula_id)
            if aula is None:
                raise EntidadNoEncontradaError(f"No existe el aula física con ID {dto.aula_id}.")

            horario = RangoHorario(hora_inicio=dto.hora_inicio, hora_fin=dto.hora_fin)

            # Instanciar el servicio de dominio con el repositorio dentro de la transacción
            motor = MotorAntiColision(reserva_repo=uow.reservas)
            motor.validar_reserva(
                aula=aula,
                docente_id=dto.docente_id,
                fecha=dto.fecha,
                horario=horario
            )

            reserva = Reserva(
                id=None,
                aula_id=aula.id,
                docente_id=dto.docente_id,
                materia_id=dto.materia_id,
                fecha=dto.fecha,
                horario=horario,
                creado_por_usuario_id=dto.usuario_id,
                observaciones=dto.observaciones
            )

            reserva_guardada = uow.reservas.guardar(reserva)

        return ReservaOutputDTO(
            id=reserva_guardada.id,
            aula_id=reserva_guardada.aula_id,
            docente_id=reserva_guardada.docente_id,
            materia_id=reserva_guardada.materia_id,
            fecha=reserva_guardada.fecha,
            hora_inicio=reserva_guardada.horario.hora_inicio,
            hora_fin=reserva_guardada.horario.hora_fin,
            observaciones=reserva_guardada.observaciones
        )
