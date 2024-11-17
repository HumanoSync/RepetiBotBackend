from typing import Optional
from sqlmodel import Session, select
from core.base_repository import BaseRepository
from device.domain.model.robot import Robot
from core.database import getSession

class RobotRepository(BaseRepository[Robot]):
    def __init__(self):
        super().__init__(Robot)  # Pasa el modelo Robot al BaseRepository

    def findByBotname(self, botname: str) -> Optional[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.botname == botname)
            return session.exec(statement).first()
        
    def findByToken(self, robotToken: str) -> Optional[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.token == robotToken)
            return session.exec(statement).first()
        
    def findAllByUserId(self, userId: int) -> list[Robot]:
        with getSession() as session:
            statement = select(Robot).where(Robot.user_id == userId)
            return session.exec(statement).all()