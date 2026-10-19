import os
import sys

# Forzar directorio raiz en el sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Entorno Vercel
os.environ["VERCEL"] = "1"
os.environ["DB_PATH"] = "/tmp/unesr_aulas.db"

from src.presentation.main import app
