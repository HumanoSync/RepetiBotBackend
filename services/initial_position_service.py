from response_builder import ResponseHandler
from dataclasses import asdict

class InitialPositionService(ResponseHandler):
    def __init__(self, initiaPositionRepository):
        self.repository = initiaPositionRepository

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

    async def createInitialPosition(self, data, websocket, requestId):
        robotId = data.get('robot_Id')
        angles = data.get('angles')
        time = data.get('time')

        if not self.validateAngles(angles):
            await self.sendErrorResponse(websocket, {"message": "Invalid angles format: angles must be a list of dictionaries with integer id and angle between 0 and 180"}, requestId)
            return

        if not isinstance(time, int) or time < 0:
            await self.sendErrorResponse(websocket, {"message": "Invalid time format: time must be a non-negative integer"}, requestId)
            return
        
        # Verifica si el usuario ya tiene una posición inicial
        existingPosition = self.repository.findByRobotId(robotId)
        if existingPosition:
            await self.sendErrorResponse(websocket, {"message": "User already has an initial position"}, requestId)
            return

        initialPositionId = self.repository.save(time, angles, robotId)
        initialPosition = self.repository.findById(initialPositionId)
        await self.sendResponse(websocket, asdict(initialPosition), requestId)

    async def updateInitialPositionById(self, data, websocket, requestId):
        initialPositionId = data.get('id')
        time = data.get('time')
        angles = data.get('angles')

        if not isinstance(initialPositionId, int):
            await self.sendErrorResponse(websocket, {"message": "Initial Position ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(initialPositionId):
            await self.sendErrorResponse(websocket, {"message": "Initial Position ID does not exist"}, requestId)
            return

        if not self.validateAngles(angles):
            await self.sendErrorResponse(websocket, {"message": "Invalid angles format: angles must be a list of dictionaries with integer id and angle between 0 and 180"}, requestId)
            return

        if not isinstance(time, int) or time < 0:
            await self.sendErrorResponse(websocket, {"message": "Invalid time format: time must be a non-negative integer"}, requestId)
            return

        self.repository.updateById(initialPositionId, time, angles)
        initialPosition = self.repository.findById(initialPositionId)
        await self.sendResponse(websocket, asdict(initialPosition), requestId)

    async def deleteInitialPositionById(self, data, websocket, requestId):
        initialPositionId = data.get('id')

        if not isinstance(initialPositionId, int):
            await self.sendErrorResponse(websocket, {"message": "Initial Position ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(initialPositionId):
            await self.sendErrorResponse(websocket, {"message": "Initial Position ID does not exist"}, requestId)
            return

        self.repository.deleteById(initialPositionId)
        await self.sendResponse(websocket, {'id': initialPositionId}, requestId)

    async def getInitialPositionById(self, data, websocket, requestId):
        initialPositionId = data.get('id')
        
        if not isinstance(initialPositionId, int):
            await self.sendErrorResponse(websocket, {"message": "Initial Position ID is required and must be an integer"}, requestId)
            return

        initialPosition = self.repository.findById(initialPositionId)
        if initialPosition:
            await self.sendResponse(websocket, asdict(initialPosition), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Initial Position not found"}, requestId)
