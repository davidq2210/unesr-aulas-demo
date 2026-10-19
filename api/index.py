import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

db_path = "/tmp/unesr_aulas.db"
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
os.environ["DB_PATH"] = db_path

try:
    from src.infrastructure.database.seeder import seed_database
    seed_database(db_path)
except Exception as e:
    print(f"Seeder notice: {e}")

from src.presentation.main import app
