#database SQL

import sqlite3
from pathlib import Path

class Database:
    #simple wrapper around database 

    def __init__(self, path: str | Path = "chatbot.db"):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()


    def create_table(self, name, columns):

        #columns -> list of tuples (column_name, type)

        cols = ", ".join(f"{c[0]} {c[1]}" for c in columns)
        sql = f"CREATE TABLE IF NOT EXISTS {name} ({cols})"
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self, name, rows):

        #rows -> list of tuples

        placeholders = ", ".join("?" * len(rows[0]))
        sql = f"INSERT INTO {name} VALUES ({placeholders})"
        self.cursor.executemany(sql, rows)
        self.conn.commit()

    def select_all(self, name):
        self.cursor.execute(f"SELECT * FROM {name}")
        return self.cursor.fetchall()        