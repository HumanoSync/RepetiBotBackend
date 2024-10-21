from sqlmodel import Session, select
from device.domain.model.position import Position
from shared.database import getSession

class PositionRepository:
    def findById(self, positionId: int) -> Position:
        with getSession() as session:
            statement = select(Position).where(Position.id == positionId)
            return session.exec(statement).first()
    
    def findAll(self) -> list[Position]:
        with getSession() as session:
            statement = select(Position)
            return session.exec(statement).all()
        
    def findAllByMovementId(self, movement_id: int) -> list[Position]:
        with getSession() as session:
            statement = select(Position).where(Position.movement_id == movement_id).order_by(Position.sequence)
            return session.exec(statement).all()
    
    def save(self, position: Position):
        with getSession() as session:
            session.add(position)
            session.commit()
            session.refresh(position)
            return position
        
    def deleteById(self, positionId: int):
        with getSession() as session:
            position = session.get(Position, positionId)
            if position:
                session.delete(position)
                session.commit()

    def findMaxSequenceByMovementId(self, movement_id: int) -> int:
        with getSession() as session:
            statement = select([Position.sequence]).where(Position.movement_id == movement_id).order_by(Position.sequence.desc()).limit(1)
            max_sequence = session.exec(statement).first()
            return max_sequence if max_sequence else 0

    def decrementSequenceAfter(self, position: Position):
        with getSession() as session:
            statement = select(Position).where(Position.sequence > position.sequence, Position.movement_id == position.movement_id)
            positions = session.exec(statement).all()
            for position in positions:
                position.sequence -= 1
                session.add(position)
            session.commit()

    def increaseSequence(self, position: Position):
        with getSession() as session:
            nextPosition = session.exec(select(Position).where(Position.movement_id == position.movement_id, Position.sequence == position.sequence + 1)).first()
            if nextPosition:
                nextPosition.sequence, position.sequence = position.sequence, nextPosition.sequence
                session.add(position)
                session.add(nextPosition)
                session.commit()
                session.refresh(position)
                session.refresh(nextPosition)
            return position

    def decreaseSequence(self, position: Position):
        with getSession() as session:
            prevPosition = session.exec(select(Position).where(Position.movement_id == position.movement_id, Position.sequence == position.sequence - 1)).first()
            if prevPosition:
                prevPosition.sequence, position.sequence = position.sequence, prevPosition.sequence
                session.add(position)
                session.add(prevPosition)
                session.commit()
                session.refresh(position)
                session.refresh(prevPosition)
            return position
