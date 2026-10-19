from typing import Protocol
from datetime import date
from src.application.dtos.cartelera_dto import ItemCarteleraDTO, ConsultarCarteleraFiltroDTO


class ICarteleraQueryPort(Protocol):
    """
    Puerto de lectura optimizado para la cartelera estudiantil / pública.
    Desacopla las consultas de alta lectura de los agregados de escritura.
    """
    def consultar(self, filtro: ConsultarCarteleraFiltroDTO) -> list[ItemCarteleraDTO]:
        ...

    def consultar_semanal(self, fecha_inicio: date, aula_id: int | None = None) -> list[ItemCarteleraDTO]:
        ...
