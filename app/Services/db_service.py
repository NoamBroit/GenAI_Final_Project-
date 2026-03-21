# app/Services/db_service.py

import os
import sqlite3
from datetime import date


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tech.db")


class DBService:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        """Create and seed the Schedule table if it doesn't exist."""
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Schedule (
                ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
                date       TEXT NOT NULL,
                time       TEXT NOT NULL,
                position   TEXT NOT NULL,
                available  INTEGER NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) FROM Schedule")
        if cursor.fetchone()[0] == 0:
            self._seed(cursor)

        self.conn.commit()

    def _seed(self, cursor):
        import random
        from datetime import timedelta

        positions = ["Python Dev", "Sql Dev", "Analyst", "ML"]
        times     = ["09:00", "10:00", "11:00", "12:00", "13:00",
                     "14:00", "15:00", "16:00", "17:00"]
        skip_days = {5, 0}  # Saturday=5, Monday=0

        start   = date.today()
        end     = date(start.year + 1, start.month, start.day)
        current = start

        while current <= end:
            if current.weekday() not in skip_days:
                for t in times:
                    for pos in positions:
                        available = 1 if random.random() >= 0.5 else 0
                        cursor.execute(
                            "INSERT INTO Schedule (date, time, position, available) VALUES (?, ?, ?, ?)",
                            (current.isoformat(), t, pos, available)
                        )
            current += timedelta(days=1)

    def get_available_slots(self, limit: int = 3) -> list[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT date, time, position
            FROM Schedule
            WHERE available = 1
              AND date >= ?
              AND position = 'Python Dev'         
            ORDER BY date, time
            LIMIT ?
        """, (date.today().isoformat(), limit))

        return [
            {"date": row[0], "time": row[1], "position": row[2]}
            for row in cursor.fetchall()
        ]

    def confirm_slot(self, slot_date: str, slot_time: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Schedule
            SET available = 0
            WHERE date = ? AND time = ? AND available = 1
        """, (slot_date, slot_time))
        self.conn.commit()
        return cursor.rowcount > 0
