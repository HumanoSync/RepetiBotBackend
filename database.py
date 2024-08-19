import sqlite3

class Database:
    def __init__(self, dbName="robot2024.db"):
        self.conn = sqlite3.connect(dbName)
        self.conn.execute("PRAGMA foreign_keys = 1")  # Habilitar el soporte de claves foráneas
        self.createTables()

    def createTables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS robots (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS initial_positions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    angles TEXT NOT NULL,
                                    robot_id INTEGER UNIQUE,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS movements (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS positions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    "order" INTEGER NOT NULL,
                                    time INTEGER NOT NULL,
                                    angles TEXT NOT NULL,
                                    movement_id INTEGER,
                                    FOREIGN KEY (movement_id) REFERENCES movements(id) ON DELETE CASCADE
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS servos (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    angle INTEGER NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS buttons (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    state BOOLEAN NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')