class DominioError(Exception):
    """Clase base para todos los errores semánticos del dominio."""
    pass


class RangoHorarioInvalidoError(DominioError):
    """Se lanza cuando un rango horario viola la coherencia o la jornada operativa."""
    pass


class AulaNoDisponibleError(DominioError):
    """Se lanza cuando un aula no se encuentra en estado operativo DISPONIBLE."""
    pass


class ColisionAulaError(DominioError):
    """Se lanza cuando se intenta reservar un aula ya ocupada en el mismo rango/fecha."""
    pass


class ColisionDocenteError(DominioError):
    """Se lanza cuando un docente ya se encuentra asignado a otra aula en el mismo horario."""
    pass


class EntidadNoEncontradaError(DominioError):
    """Se lanza cuando una entidad requerida no existe en el repositorio."""
    pass
