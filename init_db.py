import sqlite3

DB_FILE = "revenue_recovery.db"
SCHEMA_FILE = "db/schema.sql"

connection = sqlite3.connect(DB_FILE)
with open(SCHEMA_FILE, "r") as f:
    connection.executescript(f.read())
connection.commit()
connection.close()

print(f"Database created: {DB_FILE}")