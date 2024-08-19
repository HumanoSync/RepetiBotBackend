from dataclasses import asdict
from response_handler import ResponseHandler

class ServoService(ResponseHandler):
    def __init__(self, servoRepository):
        self.repository = servoRepository

    async def createServo(self, robot, data, websocket, requestId):
        angle = data.get('angle')
        robotId = robot['id']

        if not isinstance(angle, int) or not (0 <= angle <= 180):
            await self.sendErrorResponse(websocket, {"message": "Invalid angle: must be an integer between 0 and 180"}, requestId)
            return

        servoId = self.repository.save(angle, robotId)
        servo = self.repository.findById(servoId)
        await self.sendResponse(websocket, asdict(servo), requestId)

    async def updateServoById(self, data, websocket, requestId):
        servoId = data.get('id')
        angle = data.get('angle')

        if not isinstance(servoId, int):
            await self.sendErrorResponse(websocket, {"message": "Servo ID is required and must be an integer"}, requestId)
            return

        if not isinstance(angle, int) or not (0 <= angle <= 180):
            await self.sendErrorResponse(websocket, {"message": "Invalid angle: must be an integer between 0 and 180"}, requestId)
            return

        if not self.repository.findById(servoId):
            await self.sendErrorResponse(websocket, {"message": "Servo ID does not exist"}, requestId)
            return

        self.repository.updateById(servoId, angle)
        servo = self.repository.findById(servoId)
        await self.sendResponse(websocket, asdict(servo), requestId)

    async def deleteServoById(self, data, websocket, requestId):
        servoId = data.get('id')  # Assuming servos are tied to the robot ID

        if not servoId or not isinstance(servoId, int):
            await self.sendErrorResponse(websocket, {"message": "Servo ID is required and must be an integer"}, requestId)
            return
        
        if not self.repository.findById(servoId):
            await self.sendErrorResponse(websocket, {"message": "Servo ID does not exist"}, requestId)
            return

        self.repository.deleteById(servoId)
        await self.sendResponse(websocket, {'id': servoId}, requestId)

    async def getServoById(self, data, websocket, requestId):
        servoId = data.get('id')

        if not isinstance(servoId, int):
            await self.sendErrorResponse(websocket, {"message": "Servo ID is required and must be an integer"}, requestId)
            return

        servo = self.repository.findById(servoId)
        if servo:
            await self.sendResponse(websocket, asdict(servo), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Servo not found"}, requestId)

    async def getAllServosByRobotId(self, robot, websocket, requestId):
        robotId = robot['id']
        servos = self.repository.findAllByRobotId(robotId)
        payload = {
            "total_items": len(servos),
            "content": [asdict(servo) for servo in servos]
        }
        await self.sendResponse(websocket, payload, requestId)
