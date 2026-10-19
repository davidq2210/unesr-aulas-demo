from abc import ABC, abstractmethod
from src.domain.entities.aula import Aula


class IAulaRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Aula | None:
        raise NotImplementedError

    @abstractmethod
    def listar_todas(self) -> list[Aula]:
        raise NotImplementedError

    @abstractmethod
    def guardar(self, aula: Aula) -> Aula:
        raise NotImplementedError
