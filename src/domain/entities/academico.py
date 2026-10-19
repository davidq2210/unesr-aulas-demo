from dataclasses import dataclass


@dataclass
class Carrera:
    id: int | None
    codigo: str
    nombre: str
    nivel: str  # "PREGRADO" | "POSTGRADO"


@dataclass
class Materia:
    id: int | None
    carrera_id: int
    codigo: str
    nombre: str


@dataclass
class Docente:
    id: int | None
    cedula: str
    nombres: str
    apellidos: str
    email: str
    activo: bool = True

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"
