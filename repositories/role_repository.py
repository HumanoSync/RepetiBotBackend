from models import Role

class RoleRepository:
    def __init__(self, db):
        self.db = db

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, name FROM roles WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Role(id=row[0], name=row[1])
        return None

    def findByName(self, name):
        cursor = self.db.conn.execute('SELECT id, name FROM roles WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return Role(id=row[0], name=row[1])
        return None
