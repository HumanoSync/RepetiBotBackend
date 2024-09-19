from models import UserRobot

class UserRobotRepository:
    def __init__(self, db):
        self.db = db

    def save(self, user_id, robot_id):
        cursor = self.db.conn.execute(
            'INSERT INTO user_robots (user_id, robot_id) VALUES (?, ?)',
            (user_id, robot_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, user_id, robot_id):
        self.db.conn.execute(
            'UPDATE user_robots SET user_id = ?, robot_id = ? WHERE id = ?',
            (user_id, robot_id, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute('DELETE FROM user_robots WHERE id = ?', (id,))
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute('SELECT id, user_id, robot_id FROM user_robots WHERE id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return UserRobot(id=row[0], user_id=row[1], robot_id=row[2])
        return None

    def findAll(self):
        cursor = self.db.conn.execute('SELECT id, user_id, robot_id FROM user_robots')
        rows = cursor.fetchall()
        return [UserRobot(id=row[0], user_id=row[1], robot_id=row[2]) for row in rows]
    
    def findAllByUserId(self, user_id):
        cursor = self.db.conn.execute('SELECT id, user_id, robot_id FROM user_robots WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        return [UserRobot(id=row[0], user_id=row[1], robot_id=row[2]) for row in rows]
