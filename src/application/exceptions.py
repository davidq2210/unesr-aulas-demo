class AplicacionError(Exception):
    """Clase base para errores de la capa de aplicación."""
    pass


class PermisoDenegadoError(AplicacionError):
    """Se lanza cuando un usuario no cuenta con los privilegios requeridos para la acción."""
    pass
