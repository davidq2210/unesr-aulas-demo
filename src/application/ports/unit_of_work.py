from typing import Protocol
from src.domain.repositories.aula_repository import IAulaRepository
from src.domain.repositories.reserva_repository import IReservaRepository


class IUnitOfWork(Protocol):
    """
    Puerto Unit of Work: encapsula los límites transaccionales de la aplicación.
    Garantiza que las operaciones sobre repositorios compartan la misma transacción atómica.
    """
    aulas: IAulaRepository
    reservas: IReservaRepository

    def __enter__(self) -> "IUnitOfWork":
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...
