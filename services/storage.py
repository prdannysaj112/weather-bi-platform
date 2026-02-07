import sqlite3
from typing import Optional

class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._conn() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS weather_obs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                captured_at TEXT NOT NULL,
                city TEXT NOT NULL,
                temp_f REAL,
                humidity INTEGER,
                wind_mph REAL,
                condition TEXT
            )
            """)
            c.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                city TEXT NOT NULL,
                sales REAL NOT NULL
            )
            """)
            c.commit()

    def insert_weather(self, captured_at: str, city: str, temp_f: float, humidity: int, wind_mph: float, condition: str):
        with self._conn() as c:
            c.execute("""
                INSERT INTO weather_obs (captured_at, city, temp_f, humidity, wind_mph, condition)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (captured_at, city, temp_f, humidity, wind_mph, condition))
            c.commit()

    def insert_sales(self, date: str, city: str, sales: float):
        with self._conn() as c:
            c.execute("""
                INSERT INTO sales (date, city, sales)
                VALUES (?, ?, ?)
            """, (date, city, sales))
            c.commit()

    def recent_weather(self, city: str, limit: int = 30):
        with self._conn() as c:
            cur = c.execute("""
                SELECT captured_at, temp_f, humidity, wind_mph, condition
                FROM weather_obs
                WHERE city = ?
                ORDER BY captured_at DESC
                LIMIT ?
            """, (city, limit))
            rows = cur.fetchall()
        return rows

    def recent_sales(self, city: str, limit: int = 30):
        with self._conn() as c:
            cur = c.execute("""
                SELECT date, sales
                FROM sales
                WHERE city = ?
                ORDER BY date DESC
                LIMIT ?
            """, (city, limit))
            rows = cur.fetchall()
        return rows
