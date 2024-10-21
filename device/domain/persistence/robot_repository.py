from sqlmodel import Session, select
from device.domain.model.robot import Robot
from shared.database import getSession

class RobotRepository:
    def __init__(self):
        pass  # No necesitas inyectar la sesión directamente

    def findByBotname(self, botname: str) -> Robot:
        with getSession() as session:
            query = select(Robot).where(Robot.botname == botname)
            return session.exec(query).first()
        
    def findByToken(self, robotToken: str) -> Robot:
        with getSession() as session:
            query = select(Robot).where(Robot.token == robotToken)
            return session.exec(query).first()

    def findById(self, RobotId: int) -> Robot:
        with getSession() as session:
            query = select(Robot).where(Robot.id == RobotId)
            return session.exec(query).first()

    def findAll(self) -> list[Robot]:
        with getSession() as session:
            query = select(Robot)
            return session.exec(query).all()
        
    def findAllByUserId(self, userId: int) -> list[Robot]:
        with getSession() as session:
            query = select(Robot).where(Robot.user_id == userId)
            return session.exec(query).all()
        
    def save(self, robot: Robot):
        with getSession() as session:
            session.add(robot)
            session.commit()
            session.refresh(robot)
            return robot
        
    def deleteById(self, robotId: int):
        with getSession() as session:
            robot = session.get(Robot, robotId)
            if robot:
                session.delete(robot)
                session.commit()
