import sys
import os

packages_path = os.path.abspath(".packages")
if packages_path not in sys.path:
    sys.path.insert(0, packages_path)

from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    rol: str
    docente_id: Optional[int] = None


class CambiarEstadoRequest(BaseModel):
    nuevo_estado: str = Field(..., pattern="^(DISPONIBLE|EN_REMODELACION|INHABILITADA)$")


class CrearAulaRequest(BaseModel):
    nombre: str
    capacidad: int = Field(gt=0)
    pabellon: str
    estado: str = "DISPONIBLE"


class CrearReservaRequest(BaseModel):
    aula_id: int
    docente_id: int
    materia_id: int
    fecha: str  # YYYY-MM-DD
    hora_inicio: str  # HH:MM
    hora_fin: str  # HH:MM
    observaciones: Optional[str] = ""


class CrearDocenteRequest(BaseModel):
    cedula: str
    nombres: str
    apellidos: str
    email: str


class CrearMateriaRequest(BaseModel):
    carrera_id: int
    codigo: str
    nombre: str
