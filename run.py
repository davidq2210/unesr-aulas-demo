import sys
import os

packages_path = os.path.abspath(".packages")
if packages_path not in sys.path:
    sys.path.insert(0, packages_path)

import uvicorn
from src.presentation.main import app

if __name__ == "__main__":
    print("Iniciando Servidor UNESR Los Teques (Gestión y Reserva de Aulas)...")
    print("URL Local: http://127.0.0.1:8000")
    print("Cartelera Pública: http://127.0.0.1:8000/")
    print("Acceso / Login: http://127.0.0.1:8000/login")
    print("Panel de Gestión: http://127.0.0.1:8000/panel")
    uvicorn.run("src.presentation.main:app", host="0.0.0.0", port=8000, reload=True)
