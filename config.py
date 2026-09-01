import os
import sqlite3
import shutil
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(BASE_DIR, "revenue_recovery.db")

def get_db_path():
    if os.environ.get("VERCEL"):
        db_file = "/tmp/revenue_recovery.db"
        if not os.path.exists(db_file) and os.path.exists(DEFAULT_DB):
            try:
                shutil.copyfile(DEFAULT_DB, db_file)
            except Exception:
                pass
        return db_file
    return DEFAULT_DB

def get_connection():
    db_path = get_db_path()
    return sqlite3.connect(db_path)