import sqlite3
import os

class DatabaseSession:
    def init(self):
        self.conn = None

    def init(self):
        db_path = "backend/database/predprof.db"
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_id INTEGER,
                tile_index INTEGER,
                data TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_id INTEGER,
                x INTEGER,
                y INTEGER,
                type TEXT,  -- 'cuper' or 'engel'
                price REAL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map_id INTEGER,
                x INTEGER,
                y INTEGER,
                name TEXT
            )
        """)
        self.conn.commit()

    def get_connection(self):
        return self.conn

db_session = DatabaseSession()