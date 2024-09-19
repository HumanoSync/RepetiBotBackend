from dataclasses import asdict
from response_builder import ResponseHandler

class ButtonService(ResponseHandler):
    def __init__(self, buttonRepository):
        self.repository = buttonRepository

    async def createButton(self, data, websocket, requestId):
        state = data.get('state')
        robotId = data.get('robot_id')

        if not isinstance(state, bool):
            await self.sendErrorResponse(websocket, {"message": "Invalid state: must be a boolean"}, requestId)
            return

        buttonId = self.repository.save(state, robotId)
        button = self.repository.findById(buttonId)
        await self.sendResponse(websocket, asdict(button), requestId)

    async def updateButtonById(self, data, websocket, requestId):
        buttonId = data.get('id')
        state = data.get('state')

        if not isinstance(buttonId, int):
            await self.sendErrorResponse(websocket, {"message": "Button ID is required and must be an integer"}, requestId)
            return

        if not isinstance(state, bool):
            await self.sendErrorResponse(websocket, {"message": "Invalid state: must be a boolean"}, requestId)
            return

        if not self.repository.findById(buttonId):
            await self.sendErrorResponse(websocket, {"message": "Button ID does not exist"}, requestId)
            return

        self.repository.updateById(buttonId, state)
        button = self.repository.findById(buttonId)
        await self.sendResponse(websocket, asdict(button), requestId)

    async def deleteButton(self, data, websocket, requestId):
        buttonId = data.get('id')  # Assuming buttons are tied to the user ID

        if not buttonId or not isinstance(buttonId, int):
            await self.sendErrorResponse(websocket, {"message": "Servo ID is required and must be an integer"}, requestId)
            return
        
        if not self.repository.findById(buttonId):
            await self.sendErrorResponse(websocket, {"message": "Button ID does not exist"}, requestId)
            return

        self.repository.deleteById(buttonId)
        await self.sendResponse(websocket, {'id': buttonId}, requestId)

    async def getButtonById(self, data, websocket, requestId):
        buttonId = data.get('id')

        if not isinstance(buttonId, int):
            await self.sendErrorResponse(websocket, {"message": "Button ID is required and must be an integer"}, requestId)
            return

        button = self.repository.findById(buttonId)
        if button:
            await self.sendResponse(websocket, asdict(button), requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Button not found"}, requestId)

    async def getAllButtonsByRobotId(self, data, websocket, requestId):
        robotId = data.get('robot_id')
        buttons = self.repository.findAllByRobotId(robotId)
        payload = {
            "total_items": len(buttons),
            "content": [asdict(button) for button in buttons]
        }
        await self.sendResponse(websocket, payload, requestId)
