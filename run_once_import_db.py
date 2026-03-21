# run_once_import_db.py
# Run this script ONCE from the project root to populate tech.db
# Usage: python run_once_import_db.py

import sqlite3
from datetime import date, timedelta

DB_PATH = "tech.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Schedule (
        ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
        date       TEXT NOT NULL,
        time       TEXT NOT NULL,
        position   TEXT NOT NULL,
        available  INTEGER NOT NULL
    )
""")

# Clear existing data
cursor.execute("DELETE FROM Schedule")

# Config
positions = ["Python Dev", "Sql Dev", "Analyst", "ML"]
times     = ["09:00", "10:00", "11:00", "12:00", "13:00",
             "14:00", "15:00", "16:00", "17:00"]
skip_days = {5, 0}  # Saturday=5, Monday=0

start   = date.today()
end     = date(start.year + 1, start.month, start.day)
current = start

count = 0
while current <= end:
    if current.weekday() not in skip_days:
        for t in times:
            for pos in positions:
                cursor.execute(
                    "INSERT INTO Schedule (date, time, position, available) VALUES (?, ?, ?, ?)",
                    (current.isoformat(), t, pos, 1)
                )
                count += 1
    current += timedelta(days=1)

conn.commit()
conn.close()
print(f"Done. {count} slots inserted into {DB_PATH}")
