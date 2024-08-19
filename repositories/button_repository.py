from models import Button

class ButtonRepository:
    def __init__(self, db):
        self.db = db

    def save(self, state, robot_id):
        cursor = self.db.conn.execute(
            'INSERT INTO buttons (state, robot_id) VALUES (?, ?)',
            (state, robot_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, state):
        self.db.conn.execute(
            'UPDATE buttons SET state = ? WHERE id = ?',
            (state, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute('DELETE FROM buttons WHERE id = ?', (id,))
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, state, robot_id FROM buttons WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Button(id=row[0], state=row[1], robot_id=row[2])
        return None

    def findAllByRobotId(self, robot_id):
        cursor = self.db.conn.execute('SELECT id, state, robot_id FROM buttons WHERE robot_id = ?', (robot_id,))
        rows = cursor.fetchall()
        return [Button(id=row[0], state=row[1], robot_id=row[2]) for row in rows]
