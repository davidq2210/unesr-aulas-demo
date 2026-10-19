import sqlite3
from src.domain.entities.usuario import Usuario
from src.domain.value_objects.rol_usuario import RolUsuario


class SqliteUsuarioRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def obtener_por_username(self, username: str) -> Usuario | None:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash, rol, docente_id, activo FROM usuarios WHERE username = ?;",
            (username,)
        )
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        return Usuario(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            rol=RolUsuario(row["rol"]),
            docente_id=row["docente_id"],
            activo=bool(row["activo"])
        )

    def guardar(self, usuario: Usuario) -> Usuario:
        cursor = self._conn.cursor()
        if usuario.id is None:
            cursor.execute(
                """
                INSERT INTO usuarios (username, email, password_hash, rol, docente_id, activo)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    usuario.username,
                    usuario.email,
                    usuario.password_hash,
                    usuario.rol.value,
                    usuario.docente_id,
                    1 if usuario.activo else 0
                )
            )
            usuario.id = cursor.lastrowid
        else:
            cursor.execute(
                """
                UPDATE usuarios SET username = ?, email = ?, password_hash = ?, rol = ?, docente_id = ?, activo = ?
                WHERE id = ?;
                """,
                (
                    usuario.username,
                    usuario.email,
                    usuario.password_hash,
                    usuario.rol.value,
                    usuario.docente_id,
                    1 if usuario.activo else 0,
                    usuario.id
                )
            )
        cursor.close()
        return usuario
