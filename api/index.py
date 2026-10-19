import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

os.environ["VERCEL"] = "1"
os.environ["DB_PATH"] = "/tmp/unesr_aulas.db"

# Importen laeng ti app a saan a mangpataray iti dadduma a makadadael a setup
from src.presentation.main import app
