import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ["VERCEL"] = "1"
os.environ["DB_PATH"] = "/tmp/unesr_aulas.db"

# Inicializar la base de datos de aulas en /tmp si no existe
try:
    from src.infrastructure.database.seeder import seed_database
    if not os.path.exists("/tmp/unesr_aulas.db"):
        seed_database("/tmp/unesr_aulas.db")
except Exception as exc:
    print(f"[Seeder Notice] {exc}")

from src.presentation.main import app
