from models import Robot

class RobotRepository:
    def __init__(self, db):
        self.db = db

    def save(self, name):
        cursor = self.db.conn.execute(
            'INSERT INTO robots (name) VALUES (?)',
            (name,)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, name):
        self.db.conn.execute(
            'UPDATE robots SET name = ? WHERE id = ?',
            (name, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute('DELETE FROM robots WHERE id = ?', (id,))
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, name FROM robots WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Robot(id=row[0], name=row[1])
        return None
    
    def findByName(self, name):
        cursor = self.db.conn.execute('SELECT id, name FROM robots WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return Robot(id=row[0], name=row[1])
        return None

    def findAll(self):
        cursor = self.db.conn.execute('SELECT id, name FROM robots')
        rows = cursor.fetchall()
        return [Robot(id=row[0], name=row[1]) for row in rows]
