from response_handler import ResponseHandler
from repositories.movement_repository import MovementRepository
from dataclasses import asdict

class MovementService(ResponseHandler):
    def __init__(self, movementRepository):
        self.repository = movementRepository

    async def createMovement(self, robot, data, websocket, requestId):
        robotId = robot['id']
        name = data.get('name')
        
        if not name:
            await self.sendErrorResponse(websocket, {"message": "Movement name is required"}, requestId)
            return

        if self.repository.findByNameAndRobotId(name, robotId):
            await self.sendErrorResponse(websocket, {"message": "Movement with this name already exists"}, requestId)
            return

        movementId = self.repository.save(name, robotId)
        movement = self.repository.findById(movementId)
        await self.sendResponse(websocket, asdict(movement), requestId)

    async def updateMovementById(self, robot, data, websocket, requestId):
        robotId = robot['id']
        movementId = data.get('id')
        name = data.get('name')

        if not movementId or not isinstance(movementId, int):
            await self.sendErrorResponse(websocket, {"message": "Movement ID is required and must be an integer"}, requestId)
            return

        if not name:
            await self.sendErrorResponse(websocket, {"message": "Movement name is required"}, requestId)
            return

        if not self.repository.findById(movementId):
            await self.sendErrorResponse(websocket, {"message": "Movement ID does not exist"}, requestId)
            return

        existingMovement = self.repository.findByNameAndRobotId(name, robotId)
        if existingMovement and existingMovement.id != movementId:
            await self.sendErrorResponse(websocket, {"message": "Movement with this name already exists"}, requestId)
            return

        self.repository.updateById(movementId, name)
        movement = self.repository.findById(movementId)
        await self.sendResponse(websocket, asdict(movement), requestId)

    async def deleteMovementById(self, data, websocket, requestId):
        movementId = data.get('id')

        if not movementId or not isinstance(movementId, int):
            await self.sendErrorResponse(websocket, {"message": "Movement ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(movementId):
            await self.sendErrorResponse(websocket, {"message": "Movement ID does not exist for this robot"}, requestId)
            return

        self.repository.deleteById(movementId)
        await self.sendResponse(websocket, {'id': movementId}, requestId)

    async def getMovementById(self, data, websocket, requestId):
        movementId = data.get('id')

        if not movementId or not isinstance(movementId, int):
            await self.sendErrorResponse(websocket, {"message": "Movement ID is required and must be an integer"}, requestId)
            return

        movement = self.repository.findById(movementId)
        if movement:
            await self.sendResponse(websocket, asdict(movement), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Movement not found for this robot"}, requestId)

    async def getAllMovementsByRobotId(self, robot, websocket, requestId):
        robotId = robot['id']
        movements = self.repository.findAllByRobotId(robotId)
        payload = {
            "total_items": len(movements),
            "content": [asdict(movement) for movement in movements]
        }
        await self.sendResponse(websocket, payload, requestId)
