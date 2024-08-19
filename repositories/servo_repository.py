import json
from models import Servo

class ServoRepository:
    def __init__(self, db):
        self.db = db

    def save(self, angle, robot_id):
        cursor = self.db.conn.execute(
            'INSERT INTO servos (angle, robot_id) VALUES (?, ?)',
            (angle, robot_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, angle):
        self.db.conn.execute(
            'UPDATE servos SET angle = ? WHERE id = ?',
            (angle, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute('DELETE FROM servos WHERE id = ?', (id,))
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, angle, robot_id FROM servos WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Servo(id=row[0], angle=row[1], robot_id=row[2])
        return None

    def findAllByRobotId(self, robot_id):
        cursor = self.db.conn.execute('SELECT id, angle, robot_id FROM servos WHERE robot_id = ?', (robot_id,))
        rows = cursor.fetchall()
        return [Servo(id=row[0], angle=row[1], robot_id=row[2]) for row in rows]
