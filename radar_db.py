import sqlite3
from config import *

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS radar (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        car_number TEXT,
        car_tezlik INTEGER,
        car_jarima INTEGER,
        vaqt TEXT

        )""")
        self.conn.commit()

    def add_radar(self, car_number, car_tezlik, car_jarima, vaqt):
        self.cursor.execute("INSERT INTO radar (car_number,car_tezlik,car_jarima,vaqt) VALUES (?,?,?,?)",
                            (car_number, car_tezlik, car_jarima, vaqt))
        self.conn.commit()

    def get_car_number(self, car_number):
        self.cursor.execute(
            "SELECT id, car_number, car_tezlik, car_jarima, vaqt FROM radar WHERE car_number=? and car_jarima>0",
            (car_number,))
        rows = self.cursor.fetchall()
        return rows

    def pay_by_id(self, jarima_id):
        self.cursor.execute("SELECT * FROM radar WHERE id=? and car_jarima>0", (jarima_id,))
        row = self.cursor.fetchone()
        return row

    def set_jarima(self, jarima_id, jarima):
        self.cursor.execute("UPDATE radar SET car_jarima=? WHERE id=? ", (jarima, jarima_id))
        self.conn.commit()

    def get_all_jarima(self):
        self.cursor.execute("SELECT * FROM radar WHERE car_jarima>0")
        rows = self.cursor.fetchall()
        return rows


db=Database(DB_NAME)