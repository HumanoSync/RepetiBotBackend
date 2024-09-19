from models import User

class UserRepository:
    def __init__(self, db):
        self.db = db

    def save(self, name, password, role_id):
        cursor = self.db.conn.execute(
            'INSERT INTO users (name, password, role_id) VALUES (?, ?, ?)', 
            (name, password, role_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    # def updateById(self, id, name, password, role_id):
    #     self.db.conn.execute(
    #         'UPDATE users SET name = ?, password = ?, role_id = ? WHERE id = ?', 
    #         (name, password, role_id, id)
    #     )
    #     self.db.conn.commit()

    # def deleteById(self, id):
    #     self.db.conn.execute('DELETE FROM users WHERE id = ?', (id,))
    #     self.db.conn.commit()

    # def findById(self, id):
    #     cursor = self.db.conn.execute('SELECT id, name, role_id FROM users WHERE id = ?', (id,))
    #     row = cursor.fetchone()
    #     if row:
    #         return User(id=row[0], name=row[1], role_id=row[2])
    #     return None

    def findByName(self, name):
        cursor = self.db.conn.execute('SELECT id, name, role_id FROM users WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], name=row[1], role_id=row[2])
        return None

    def findAll(self):
        cursor = self.db.conn.execute('SELECT id, name, role_id FROM users')
        rows = cursor.fetchall()
        return [User(id=row[0], name=row[1], role_id=row[2]) for row in rows]

    def authenticate(self, name, password):
        cursor = self.db.conn.execute('SELECT id FROM users WHERE name = ? AND password = ?', (name, password))
        row = cursor.fetchone()
        return row is not None
