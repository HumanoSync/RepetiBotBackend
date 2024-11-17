import json
from fastapi import HTTPException, status
from device.domain.model.position import Position
from device.domain.persistence.position_repository import PositionRepository

class PositionService:
    def __init__(self, positionRepository: PositionRepository):
        self.repository = positionRepository

    def create(self, position: Position):
        if any(angle < 0 or angle > 180 for angle in json.loads(position.angles)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Each angle must be between 0 and 180")
        
        max_sequence = self.repository.findMaxSequenceByMovementId(position.movement_id)
        position.sequence = max_sequence + 1
        return self.repository.save(position)
    
    def getById(self, positionId: int):
        position = self.repository.findById(positionId)
        if not position:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
        return position
    
    def getAllByMovementId(self, movementId: int):
        return self.repository.findAllByMovementId(movementId)
    
    def updateById(self, positionId: int, newDelay: int, newAngles: str):
        positionToUpdate = self.getById(positionId)

        if any(angle < 0 or angle > 180 for angle in json.loads(newAngles)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Each angle must be between 0 and 180")

        positionToUpdate.delay = newDelay
        positionToUpdate.angles = newAngles
        return self.repository.save(positionToUpdate)
    
    def increaseSequenceById(self, positionId: int):
        positionToIncrease = self.getById(positionId)
        max_sequence = self.repository.findMaxSequenceByMovementId(positionToIncrease.movement_id)

        if positionToIncrease.sequence < max_sequence:
            return self.repository.increaseSequence(positionToIncrease)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the maximum sequence")
    
    def decreaseSequenceById(self, positionId: int):
        positionToDecrease = self.getById(positionId)

        if positionToDecrease.sequence > 1:  # La secuencia mínima es 1
            return self.repository.decreaseSequence(positionToDecrease)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position is already at the minimum sequence")
    
    def deleteById(self, positionId: int):
        positionToDelete = self.getById(positionId)
        self.repository.deleteById(positionToDelete.id)
        self.repository.decrementSequenceAfter(positionToDelete)
        return True