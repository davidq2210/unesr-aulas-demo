import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
sys.path.insert(0, ROOT_DIR)

os.environ["VERCEL"] = "1"
db_file = "/tmp/unesr_aulas.db"
os.environ["DB_PATH"] = db_file

try:
from src.infrastructure.database.seeder import seed_database
seed_database(db_file)
except Exception as err:
print(f"Error seeding /tmp db: {err}")

from src.presentation.main import app
