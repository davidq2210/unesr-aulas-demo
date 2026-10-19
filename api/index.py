import sys
import os

# Añadir raíz del proyecto al path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Vercel Serverless solo permite escritura en /tmp
db_path = "/tmp/unesr_aulas.db"

try:
    from src.infrastructure.database.seeder import seed_database
    seed_database(db_path)
except Exception as e:
    print(f"Aviso Seeder: {e}")

# Indicar a la aplicación qué base de datos usar
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
os.environ["DB_PATH"] = db_path

from src.presentation.main import app
