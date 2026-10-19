import sys
import os

packages_path = os.path.abspath(".packages")
if packages_path not in sys.path:
    sys.path.insert(0, packages_path)

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infrastructure.security.jwt_service import verificar_jwt_token
from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.persistence.sqlite_usuario_repository import SqliteUsuarioRepository
from src.domain.entities.usuario import Usuario

SECRET_KEY = "unesr_los_teques_secret_key_2026"
security_bearer = HTTPBearer(auto_error=False)


def get_db_path(request: Request) -> str:
    """Extrae la ruta de base de datos activa (soporta inyección en tests)."""
    return getattr(request.app.state, "db_path", "unesr_aulas.db")


def get_current_user_optional(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer)
) -> Usuario | None:
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = verificar_jwt_token(token, SECRET_KEY)
        username = payload.get("username")
        if not username:
            return None
        db_path = get_db_path(request)
        conn = get_db_connection(db_path)
        repo = SqliteUsuarioRepository(conn)
        user = repo.obtener_por_username(username)
        conn.close()
        return user
    except Exception:
        return None


def get_current_user(
    user: Usuario | None = Depends(get_current_user_optional)
) -> Usuario:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de acceso inválidas o token expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_role(roles_permitidos: list[str]):
    def rol_checker(user: Usuario = Depends(get_current_user)) -> Usuario:
        if user.rol.value not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso denegado: El rol '{user.rol.value}' no tiene autorización para esta operación."
            )
        return user
    return rol_checker
