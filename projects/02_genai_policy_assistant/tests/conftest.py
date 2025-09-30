# Make `from app import app` work by adding the api/ dir to sys.path
import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parents[1] / "api"
API_DIR_STR = str(API_DIR)
if API_DIR_STR not in sys.path:
    sys.path.insert(0, API_DIR_STR)
