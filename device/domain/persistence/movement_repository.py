from sqlmodel import select
from device.domain.model.movement import Movement
from shared.database import getSession

class MovementRepository:
    def findById(self, movementId: int) -> Movement:
        with getSession() as session:
            statement = select(Movement).where(Movement.id == movementId)
            return session.exec(statement).first()
        
    def findByNameAndRobotId(self, movementName: str, robotId: int) -> Movement:
        with getSession() as session:
            statement = select(Movement).where((Movement.name == movementName) & (Movement.robot_id == robotId))
            return session.exec(statement).first()
        
    def findAll(self) -> list[Movement]:
        with getSession() as session:
            statement = select(Movement)
            return session.exec(statement).all()
    
    def findAllByRobotId(self, robotId: int) -> list[Movement]:
        with getSession() as session:
            statement = select(Movement).where(Movement.robot_id == robotId)
            return session.exec(statement).all()
        
    def save(self, movement: Movement):
        with getSession() as session:
            session.add(movement)
            session.commit()
            session.refresh(movement)
            return movement
        
    def deleteById(self, movementId: int):
        with getSession() as session:
            movement = session.get(Movement, movementId)
            if movement:
                session.delete(movement)
                session.commit()