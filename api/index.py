import os
import sys

# Forzar inclusión del directorio raíz en sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Vercel Serverless solo permite escribir en /tmp
db_file = "/tmp/unesr_aulas.db"
os.environ["DB_PATH"] = db_file
os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"

# Sembrar base de datos si no existe en /tmp
try:
    from src.infrastructure.database.seeder import seed_database
    if not os.path.exists(db_file):
        seed_database(db_file)
except Exception as err:
    print(f"Aviso de inicialización Seeder: {err}")

# Importar aplicación FastAPI
from src.presentation.main import app
