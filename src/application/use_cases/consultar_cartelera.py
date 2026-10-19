from datetime import date
from src.application.ports.cartelera_query_port import ICarteleraQueryPort
from src.application.dtos.cartelera_dto import ConsultarCarteleraFiltroDTO, ItemCarteleraDTO


class ConsultarCarteleraUseCase:
    """
    Caso de Uso: Consultar Cartelera de Aulas.
    Permite la lectura pública o estudiantil del cronograma de clases y asignación de aulas
    para una fecha determinada o para la semana completa (Lunes a Sábado).
    """

    def __init__(self, query_port: ICarteleraQueryPort):
        self._query_port = query_port

    def ejecutar(self, filtro: ConsultarCarteleraFiltroDTO) -> list[ItemCarteleraDTO]:
        return self._query_port.consultar(filtro)

    def ejecutar_semanal(self, fecha_inicio: date, aula_id: int | None = None) -> list[ItemCarteleraDTO]:
        return self._query_port.consultar_semanal(fecha_inicio, aula_id)
