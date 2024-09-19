from models import InitialPosition
import json

class InitialPositionRepository:
    def __init__(self, db):
        self.db = db

    def save(self, time, angles, user_id):
        angles_json = json.dumps(angles)
        cursor = self.db.conn.execute(
            'INSERT INTO initial_positions (time, angles, user_id) VALUES (?, ?, ?)',
            (time, angles_json, user_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, time, angles):
        angles_json = json.dumps(angles)
        self.db.conn.execute(
            'UPDATE initial_positions SET time = ?, angles = ? WHERE id = ?',
            (time, angles_json, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute('DELETE FROM initial_positions WHERE id = ?', (id,))
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, time, angles, user_id FROM initial_positions WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return InitialPosition(id=row[0], time=row[1], angles=json.loads(row[2]), user_id=row[3])
        return None
    
    def findByUserId(self, user_id):
        cursor = self.db.conn.execute('SELECT id, time, angles, user_id FROM initial_positions WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return InitialPosition(id=row[0], time=row[1], angles=json.loads(row[2]), user_id=row[3])
        return None
