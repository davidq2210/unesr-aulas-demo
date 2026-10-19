import unittest
import os
import sys

# Asegurar acceso a .packages para FastAPI y dependencias
packages_path = os.path.abspath(".packages")
if packages_path not in sys.path:
    sys.path.insert(0, packages_path)

from starlette.testclient import TestClient
from datetime import date

from src.presentation.main import app, DB_FILE_PATH
from src.infrastructure.database.schema import init_db_schema
from src.infrastructure.database.seeder import seed_database
from src.infrastructure.database.connection import get_db_connection


class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_api_unesr.db"
        cls._limpiar(cls.test_db)
        seed_database(cls.test_db)
        app.state.db_path = cls.test_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        cls._limpiar(cls.test_db)

    @classmethod
    def _limpiar(cls, db_path):
        for ext in ["", "-wal", "-shm"]:
            f = f"{db_path}{ext}"
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError:
                    pass

    def test_01_login_exitoso_directivo(self):
        resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["rol"], "DIRECTIVO")

    def test_02_login_fallido_credenciales_invalidas(self):
        resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "clave_falsa"})
        self.assertEqual(resp.status_code, 401)

    def test_03_consultar_cartelera_publica_incluye_codigo_y_nivel(self):
        hoy = date.today().isoformat()
        resp = self.client.get(f"/api/v1/cartelera?fecha={hoy}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]["aula_nombre"], "Aula 01")
        self.assertEqual(data[0]["materia_codigo"], "INF-101")
        self.assertEqual(data[0]["nivel"], "PREGRADO")

    def test_04_consultar_cartelera_semanal(self):
        hoy = date.today().isoformat()
        resp = self.client.get(f"/api/v1/cartelera/semanal?fecha_inicio={hoy}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_05_listar_aulas(self):
        resp = self.client.get("/api/v1/aulas")
        self.assertEqual(resp.status_code, 200)
        aulas = resp.json()
        self.assertEqual(len(aulas), 12)

    def test_06_cambiar_estado_aula_como_directivo(self):
        auth_resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        resp = self.client.patch("/api/v1/aulas/1/estado", json={"nuevo_estado": "EN_REMODELACION"}, headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["estado"], "EN_REMODELACION")

        resp2 = self.client.patch("/api/v1/aulas/1/estado", json={"nuevo_estado": "DISPONIBLE"}, headers=headers)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json()["estado"], "DISPONIBLE")

    def test_07_colision_de_aula_retorna_http_409(self):
        auth_resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        hoy = date.today().isoformat()
        payload = {
            "aula_id": 1,
            "docente_id": 2,
            "materia_id": 2,
            "fecha": hoy,
            "hora_inicio": "08:00",
            "hora_fin": "10:00",
            "observaciones": "Intento de solapamiento"
        }
        resp = self.client.post("/api/v1/reservas", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 409)
        self.assertIn("ya posee una reserva", resp.json()["detail"])

    def test_08_reserva_aula_no_disponible_retorna_http_409(self):
        auth_resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        hoy = date.today().isoformat()
        payload = {
            "aula_id": 9,
            "docente_id": 2,
            "materia_id": 2,
            "fecha": hoy,
            "hora_inicio": "10:00",
            "hora_fin": "12:00"
        }
        resp = self.client.post("/api/v1/reservas", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 409)
        self.assertIn("no está disponible para asignación", resp.json()["detail"])

    def test_09_crear_y_eliminar_reserva_exitosa(self):
        auth_resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        hoy = date.today().isoformat()
        payload = {
            "aula_id": 2,
            "docente_id": 2,
            "materia_id": 2,
            "fecha": hoy,
            "hora_inicio": "14:00",
            "hora_fin": "16:00",
            "observaciones": "Reserva de prueba E2E"
        }
        resp = self.client.post("/api/v1/reservas", json=payload, headers=headers)
        self.assertEqual(resp.status_code, 201)
        reserva_id = resp.json()["id"]

        del_resp = self.client.delete(f"/api/v1/reservas/{reserva_id}", headers=headers)
        self.assertEqual(del_resp.status_code, 200)
        self.assertTrue(del_resp.json()["ok"])

    def test_10_agregar_docente_y_materia_dinamicos(self):
        auth_resp = self.client.post("/api/v1/auth/login", json={"username": "admin", "password": "unesr2026"})
        token = auth_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Registrar docente
        doc_resp = self.client.post(
            "/api/v1/catalogo/docentes",
            json={"cedula": "V-20111222", "nombres": "Elena", "apellidos": "Torres", "email": "etorres@unesr.ve"},
            headers=headers
        )
        self.assertEqual(doc_resp.status_code, 201)
        self.assertEqual(doc_resp.json()["nombres"], "Elena")

        # Registrar materia
        mat_resp = self.client.post(
            "/api/v1/catalogo/materias",
            json={"carrera_id": 1, "codigo": "INF-305", "nombre": "Inteligencia Artificial y Aprendizaje"},
            headers=headers
        )
        self.assertEqual(mat_resp.status_code, 201)
        self.assertEqual(mat_resp.json()["codigo"], "INF-305")

    def test_11_frontend_rutas_accesibles(self):
        resp_home = self.client.get("/")
        self.assertEqual(resp_home.status_code, 200)
        self.assertIn("text/html", resp_home.headers["content-type"])
        self.assertIn("UNESR", resp_home.text)

        resp_login = self.client.get("/login")
        self.assertEqual(resp_login.status_code, 200)
        self.assertIn("text/html", resp_login.headers["content-type"])

        resp_panel = self.client.get("/panel")
        self.assertEqual(resp_panel.status_code, 200)
        self.assertIn("text/html", resp_panel.headers["content-type"])


if __name__ == "__main__":
    unittest.main()
