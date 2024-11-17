from typing import Optional, List
from sqlmodel import select
from device.domain.model.movement import Movement
from core.database import getSession
from core.base_repository import BaseRepository  # Asegúrate de importar el BaseRepository

class MovementRepository(BaseRepository[Movement]):
    def __init__(self):
        super().__init__(Movement)  # Pasa el modelo Movement al BaseRepository

    def findByNameAndRobotId(self, movementName: str, robotId: int) -> Optional[Movement]:
        with getSession() as session:
            statement = select(Movement).where((Movement.name == movementName) & (Movement.robot_id == robotId))
            return session.exec(statement).first()

    def findAllByRobotId(self, robotId: int) -> List[Movement]:
        with getSession() as session:
            statement = select(Movement).where(Movement.robot_id == robotId)
            return session.exec(statement).all()
