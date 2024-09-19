from response_builder import ResponseHandler
from dataclasses import asdict

class PositionService(ResponseHandler):
    def __init__(self, positionRepository, movementRepository):
        self.repository = positionRepository
        self.movementRepository = movementRepository

    def validateAngles(self, angles):
        if not isinstance(angles, list):
            return False
        for angle in angles:
            if not isinstance(angle, dict):
                return False
            if 'id' not in angle or 'angle' not in angle:
                return False
            if not isinstance(angle['id'], int) or not isinstance(angle['angle'], int):
                return False
            if not (0 <= angle['angle'] <= 180):
                return False
        return True

    async def createPosition(self, data, websocket, requestId):
        movementId = data.get('movement_id')
        angles = data.get('angles')
        time = data.get('time')

        if not isinstance(movementId, int):
            await self.sendErrorResponse(websocket, {"message": "Movement ID is required and must be an integer"}, requestId)
            return

        if not self.movementRepository.findById(movementId):
            await self.sendErrorResponse(websocket, {"message": "Movement ID does not exist"}, requestId)
            return

        if not self.validateAngles(angles):
            await self.sendErrorResponse(websocket, {"message": "Invalid angles format: angles must be a list of dictionaries with integer id and angle between 0 and 180"}, requestId)
            return

        if not isinstance(time, int) or time < 0:
            await self.sendErrorResponse(websocket, {"message": "Invalid time format: time must be a non-negative integer"}, requestId)
            return

        positions = self.repository.findAllByMovementId(movementId)
        order = len(positions) + 1

        positionId = self.repository.save(order, time, angles, movementId)
        position = self.repository.findById(positionId)
        await self.sendResponse(websocket, asdict(position), requestId)

    async def updatePositionById(self, data, websocket, requestId):
        positionId = data.get('id')
        time = data.get('time')
        angles = data.get('angles')

        if not isinstance(positionId, int):
            await self.sendErrorResponse(websocket, {"message": "Position ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(positionId):
            await self.sendErrorResponse(websocket, {"message": "Position ID does not exist"}, requestId)
            return

        if not self.validateAngles(angles):
            await self.sendErrorResponse(websocket, {"message": "Invalid angles format: angles must be a list of dictionaries with integer id and angle between 0 and 180"}, requestId)
            return

        if not isinstance(time, int) or time < 0:
            await self.sendErrorResponse(websocket, {"message": "Invalid time format: time must be a non-negative integer"}, requestId)
            return

        self.repository.updateById(positionId, time, angles)
        position = self.repository.findById(positionId)
        await self.sendResponse(websocket, asdict(position), requestId)

    async def deletePositionById(self, data, websocket, requestId):
        positionId = data.get('id')

        if not isinstance(positionId, int):
            await self.sendErrorResponse(websocket, {"message": "Position ID is required and must be an integer"}, requestId)
            return

        position = self.repository.findById(positionId)
        if not position:
            await self.sendErrorResponse(websocket, {"message": "Position ID does not exist"}, requestId)
            return

        self.repository.deleteById(positionId)
        self.repository.decrementOrder(position.order, position.movement_id)
        await self.sendResponse(websocket, {'id': positionId}, requestId)

    async def getPositionById(self, data, websocket, requestId):
        positionId = data.get('id')
        
        if not isinstance(positionId, int):
            await self.sendErrorResponse(websocket, {"message": "Position ID is required and must be an integer"}, requestId)
            return

        position = self.repository.findById(positionId)
        if position:
            await self.sendResponse(websocket, asdict(position), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Position not found"}, requestId)

    async def getAllPositionsByMovementId(self, data, websocket, requestId):
        movementId = data.get('movement_id')

        if not isinstance(movementId, int):
            await self.sendErrorResponse(websocket, {"message": "Movement ID is required and must be an integer"}, requestId)
            return

        if not self.movementRepository.findById(movementId):
            await self.sendErrorResponse(websocket, {"message": "Movement ID does not exist"}, requestId)
            return

        positions = self.repository.findAllByMovementId(movementId)
        payload = {
            "total_items": len(positions),
            "content": [asdict(position) for position in positions]
        }
        await self.sendResponse(websocket, payload, requestId)

    async def movePositionUpById(self, data, websocket, requestId):
        positionId = data.get('id')

        if not isinstance(positionId, int):
            await self.sendErrorResponse(websocket, {"message": "Position ID is required and must be an integer"}, requestId)
            return

        position = self.repository.findById(positionId)
        if not position:
            await self.sendErrorResponse(websocket, {"message": "Position ID does not exist"}, requestId)
            return

        if position.order > 1:  # Verificar si no es la primera posición
            self.repository.swapWithPrevious(position.id, position.order, position.movement_id)
            await self.sendResponse(websocket, {'id': positionId, 'status': 'moved up'}, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Position is already at the top"}, requestId)

    async def movePositionDownById(self, data, websocket, requestId):
        positionId = data.get('id')

        if not isinstance(positionId, int):
            await self.sendErrorResponse(websocket, {"message": "Position ID is required and must be an integer"}, requestId)
            return

        position = self.repository.findById(positionId)
        if not position:
            await self.sendErrorResponse(websocket, {"message": "Position ID does not exist"}, requestId)
            return

        max_order = self.repository.findMaxOrder(position.movement_id)  # Obtener el orden máximo
        if position.order < max_order:  # Verificar si no es la última posición
            self.repository.swapWithNext(position.id, position.order, position.movement_id)
            await self.sendResponse(websocket, {'id': positionId, 'status': 'moved down'}, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Position is already at the bottom"}, requestId)

