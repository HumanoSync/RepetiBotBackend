from dataclasses import asdict
from response_builder import ResponseHandler

class UserRobotService(ResponseHandler):
    def __init__(self, userRobotRepository):
        self.repository = userRobotRepository

    async def createUserRobot(self, data, websocket, requestId):
        userId = data.get('user_id')
        robotId = data.get('robot_id')

        if not isinstance(userId, int) or not isinstance(robotId, int):
            await self.sendErrorResponse(websocket, {"message": "User ID and Robot ID are required and must be integers"}, requestId)
            return

        userRobotId = self.repository.save(userId, robotId)
        userRobot = self.repository.findById(userRobotId)
        await self.sendResponse(websocket, asdict(userRobot), requestId)

    async def updateUserRobotById(self, data, websocket, requestId):
        userRobotId = data.get('id')
        userId = data.get('user_id')
        robotId = data.get('robot_id')

        if not isinstance(userRobotId, int):
            await self.sendErrorResponse(websocket, {"message": "UserRobot ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(userRobotId):
            await self.sendErrorResponse(websocket, {"message": "UserRobot ID does not exist"}, requestId)
            return

        self.repository.updateById(userRobotId, userId, robotId)
        userRobot = self.repository.findById(userRobotId)
        await self.sendResponse(websocket, asdict(userRobot), requestId)

    async def deleteUserRobotById(self, data, websocket, requestId):
        userRobotId = data.get('id')

        if not isinstance(userRobotId, int):
            await self.sendErrorResponse(websocket, {"message": "UserRobot ID is required and must be an integer"}, requestId)
            return

        if not self.repository.findById(userRobotId):
            await self.sendErrorResponse(websocket, {"message": "UserRobot ID does not exist"}, requestId)
            return

        self.repository.deleteById(userRobotId)
        await self.sendResponse(websocket, {'id': userRobotId}, requestId)

    async def getUserRobotById(self, data, websocket, requestId):
        userRobotId = data.get('id')

        if not isinstance(userRobotId, int):
            await self.sendErrorResponse(websocket, {"message": "UserRobot ID is required and must be an integer"}, requestId)
            return

        userRobot = self.repository.findById(userRobotId)
        if userRobot:
            await self.sendResponse(websocket, asdict(userRobot), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "UserRobot not found"}, requestId)

    async def getAllUserRobotsByUserId(self, data, websocket, requestId):
        userId = data.get('user_id')
        userRobots = self.repository.findAllByUserId(userId)
        payload = {
            "total_items": len(userRobots),
            "content": [asdict(userRobot) for userRobot in userRobots]
        }
        await self.sendResponse(websocket, payload, requestId)
    async def getAllUserRobots(self, websocket, requestId):
        userRobots = self.repository.findAll()
        payload = {
            "total_items": len(userRobots),
            "content": [asdict(userRobot) for userRobot in userRobots]
        }
        await self.sendResponse(websocket, payload, requestId)
