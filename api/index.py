import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ["VERCEL"] = "1"
os.environ["DB_PATH"] = "/tmp/unesr_aulas.db"

try:
    from src.infrastructure.database.seeder import seed_database
    if not os.path.exists("/tmp/unesr_aulas.db"):
        seed_database("/tmp/unesr_aulas.db")
except Exception as e:
    print(f"Aviso Seeder: {e}")

from src.presentation.main import app
