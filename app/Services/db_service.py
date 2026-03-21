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
        """Create the Schedule table if it doesn't exist."""
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
        self.conn.commit()

    def get_available_slots(self, limit: int = 3) -> list[dict]:
        """Return the next N available Python Dev slots from today onward."""
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
        """Mark a slot as unavailable once confirmed."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Schedule
            SET available = 0
            WHERE date = ? AND time = ? AND available = 1
        """, (slot_date, slot_time))
        self.conn.commit()
        return cursor.rowcount > 0