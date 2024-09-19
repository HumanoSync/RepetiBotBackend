import sqlite3

class Database:
    def __init__(self, dbName="robot2024.db"):
        self.conn = sqlite3.connect(dbName)
        self.conn.execute("PRAGMA foreign_keys = 1")  # Habilitar el soporte de claves foráneas
        self.createTables()
        self.insertDefaultRoles()

    def createTables(self):
        with self.conn:
            # Tabla de roles de usuario
            self.conn.execute('''CREATE TABLE IF NOT EXISTS roles (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL UNIQUE
                                )''')

            # Tabla de usuarios
            self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    sid TEXT,
                                    username TEXT NOT NULL UNIQUE,
                                    password TEXT NOT NULL,
                                    role_id INTEGER,
                                    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
                                )''')

            # Tabla de robots
            self.conn.execute('''CREATE TABLE IF NOT EXISTS robots (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    sid TEXT,
                                    token TEXT NOT NULL UNIQUE,
                                    botname TEXT NOT NULL UNIQUE
                                )''')

            # Tabla de acceso de usuarios a robots (antes 'robot_assignments')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS accesses (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    robot_id INTEGER,
                                    is_connected BOOLEAN,
                                    UNIQUE (user_id, robot_id),
                                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')

            # Tabla de posiciones iniciales del robot
            self.conn.execute('''CREATE TABLE IF NOT EXISTS initial_positions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    delay INTEGER NOT NULL,
                                    angles TEXT NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')

            # Tabla de movimientos del robot
            self.conn.execute('''CREATE TABLE IF NOT EXISTS movements (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')

            # Tabla de posiciones dentro de un movimiento
            self.conn.execute('''CREATE TABLE IF NOT EXISTS positions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    sequence INTEGER NOT NULL,
                                    delay INTEGER NOT NULL,
                                    angles TEXT NOT NULL,
                                    movement_id INTEGER,
                                    FOREIGN KEY (movement_id) REFERENCES movements(id) ON DELETE CASCADE
                                )''')

            # Tabla de servos del robot
            self.conn.execute('''CREATE TABLE IF NOT EXISTS servos (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    angle INTEGER NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')

            # Tabla de botones del robot
            self.conn.execute('''CREATE TABLE IF NOT EXISTS buttons (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    state BOOLEAN NOT NULL,
                                    robot_id INTEGER,
                                    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE
                                )''')

    def insertDefaultRoles(self):
        with self.conn:
            roles = ['user', 'admin']
            for role in roles:
                self.conn.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (role,))
            self.conn.commit()
