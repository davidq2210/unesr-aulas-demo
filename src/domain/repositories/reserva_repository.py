from abc import ABC, abstractmethod
from datetime import date
from src.domain.entities.reserva import Reserva


class IReservaRepository(ABC):
    @abstractmethod
    def buscar_por_aula_y_fecha(self, aula_id: int, fecha: date) -> list[Reserva]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_docente_y_fecha(self, docente_id: int, fecha: date) -> list[Reserva]:
        raise NotImplementedError

    @abstractmethod
    def guardar(self, reserva: Reserva) -> Reserva:
        raise NotImplementedError

    @abstractmethod
    def obtener_por_id(self, id: int) -> Reserva | None:
        raise NotImplementedError

    @abstractmethod
    def listar_por_fecha(self, fecha: date) -> list[Reserva]:
        raise NotImplementedError
