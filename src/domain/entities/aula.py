from dataclasses import dataclass
from src.domain.value_objects.estado_aula import EstadoAula
from src.domain.exceptions import AulaNoDisponibleError


@dataclass
class Aula:
    id: int | None
    nombre: str
    capacidad: int
    pabellon: str
    estado: EstadoAula

    def validar_disponibilidad_operativa(self) -> None:
        """
        Garantiza la regla crítica de negocio 1:
        Un aula no puede reservarse si su estado no es DISPONIBLE.
        """
        if self.estado != EstadoAula.DISPONIBLE:
            raise AulaNoDisponibleError(
                f"El aula '{self.nombre}' no está disponible para asignación (Estado operativo: {self.estado.value})."
            )

    def cambiar_estado(self, nuevo_estado: EstadoAula) -> None:
        self.estado = nuevo_estado
