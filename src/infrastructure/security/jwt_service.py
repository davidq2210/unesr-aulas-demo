import hmac
import hashlib
import json
import base64
import time


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def crear_jwt_token(payload: dict, secreto: str, expires_in_seconds: int = 86400) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())

    full_payload = payload.copy()
    full_payload["iat"] = now
    full_payload["exp"] = now + expires_in_seconds

    encoded_header = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _base64url_encode(json.dumps(full_payload, separators=(",", ":")).encode("utf-8"))

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(secreto.encode("utf-8"), signing_input, hashlib.sha256).digest()
    encoded_signature = _base64url_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def verificar_jwt_token(token: str, secreto: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token JWT malformado.")

    encoded_header, encoded_payload, encoded_signature = parts
    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")

    expected_signature = hmac.new(secreto.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_signature = _base64url_decode(encoded_signature)

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise ValueError("Firma del token inválida.")

    payload_bytes = _base64url_decode(encoded_payload)
    payload = json.loads(payload_bytes.decode("utf-8"))

    now = int(time.time())
    if "exp" in payload and payload["exp"] < now:
        raise ValueError("Token expirado.")

    return payload
