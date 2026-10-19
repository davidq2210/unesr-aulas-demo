import unittest
from src.infrastructure.security.password_hasher import hash_password, verify_password
from src.infrastructure.security.jwt_service import crear_jwt_token, verificar_jwt_token


class TestSecurity(unittest.TestCase):
    def test_hash_y_verificar_password(self):
        password = "mi_clave_segura_unesr"
        hashed = hash_password(password)

        self.assertNotEqual(password, hashed)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("clave_errada", hashed))

    def test_crear_y_verificar_jwt(self):
        payload = {"sub": "1", "username": "admin", "rol": "DIRECTIVO"}
        token = crear_jwt_token(payload, secreto="secreto_test", expires_in_seconds=3600)

        self.assertIsInstance(token, str)
        datos = verificar_jwt_token(token, secreto="secreto_test")
        self.assertEqual(datos["sub"], "1")
        self.assertEqual(datos["username"], "admin")
        self.assertEqual(datos["rol"], "DIRECTIVO")

    def test_jwt_invalido_o_adulterado(self):
        payload = {"sub": "1", "username": "admin", "rol": "DIRECTIVO"}
        token = crear_jwt_token(payload, secreto="secreto_test", expires_in_seconds=3600)

        # Token con firma errada
        with self.assertRaises(ValueError):
            verificar_jwt_token(token, secreto="secreto_falso")

        # Token corrupto
        partes = token.split(".")
        token_adulterado = f"{partes[0]}.eyJhZG1pbiI6dHJ1ZX0.{partes[2]}"
        with self.assertRaises(ValueError):
            verificar_jwt_token(token_adulterado, secreto="secreto_test")


if __name__ == "__main__":
    unittest.main()
