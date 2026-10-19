import hashlib
import os
import secrets


def hash_password(password: str) -> str:
    """
    Genera un hash seguro utilizando PBKDF2-HMAC-SHA256 con salt criptográfico de 16 bytes.
    Formato retornado: <salt_hex>$<iterations>$<hash_hex>
    """
    salt = secrets.token_bytes(16)
    iterations = 100_000
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{salt.hex()}${iterations}${derived.hex()}"


def verify_password(password: str, hashed_value: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash almacenado.
    Utiliza hmac.compare_digest para prevenir ataques de temporización.
    """
    try:
        salt_hex, iterations_str, expected_hash_hex = hashed_value.split("$")
        salt = bytes.fromhex(salt_hex)
        iterations = int(iterations_str)
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return secrets.compare_digest(derived.hex(), expected_hash_hex)
    except Exception:
        return False
