from models import Movement

class MovementRepository:
    def __init__(self, db):
        self.db = db

    def save(self, name, robot_id):
        cursor = self.db.conn.execute(
            "INSERT INTO movements (name, robot_id) VALUES (?, ?)", 
            (name, robot_id)
        )
        self.db.conn.commit()
        return cursor.lastrowid

    def updateById(self, id, name):
        self.db.conn.execute(
            "UPDATE movements SET name = ? WHERE id = ?",
            (name, id)
        )
        self.db.conn.commit()

    def deleteById(self, id):
        self.db.conn.execute(
            "DELETE FROM movements WHERE id = ?",
            (id,)
        )
        self.db.conn.commit()

    def findById(self, id):
        cursor = self.db.conn.execute(
            "SELECT id, name FROM movements WHERE id = ?",
            (id)
        )
        row = cursor.fetchone()
        if row:
            return Movement(id=row[0], name=row[1])
        return None

    def findByNameAndRobotId(self, name, robot_id):
        cursor = self.db.conn.execute(
            "SELECT id, name FROM movements WHERE name = ? AND robot_id = ?",
            (name, robot_id)
        )
        row = cursor.fetchone()
        if row:
            return Movement(id=row[0], name=row[1])
        return None

    def findAllByRobotId(self, robot_id):
        cursor = self.db.conn.execute(
            "SELECT id, name FROM movements WHERE robot_id = ?",
            (robot_id,)
        )
        rows = cursor.fetchall()
        return [Movement(id=row[0], name=row[1]) for row in rows]
