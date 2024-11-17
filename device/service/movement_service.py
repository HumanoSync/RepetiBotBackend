from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from device.domain.persistence.movement_repository import MovementRepository
from device.service.position_service import PositionService

class MovementService:
    def __init__(self, movementRepository: MovementRepository, positionService: PositionService):
        self.repository = movementRepository
        self.positionService = positionService
    
    def create(self, movement: Movement):
        if self.repository.findByNameAndRobotId(movement.name, movement.robot_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        return self.repository.save(movement)
        
    def getById(self, movement_id: int):
        movement = self.repository.findById(movement_id)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        return movement
    
    def getAllByRobotId(self, robotId: int):        
        return self.repository.findAllByRobotId(robotId)
    
    def updateById(self, movementId: str, newName: str):
        movementToUpdate = self.getById(movementId)
        movementToUpdate.name = newName
        return self.repository.save(movementToUpdate)
    
    def deleteById(self, movementId: int):
        movementToDelete = self.getById(movementId)
        self.repository.deleteById(movementToDelete.id)
        return True