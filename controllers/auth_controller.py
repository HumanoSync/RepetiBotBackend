import json
from response_builder import JSONRPCResponseBuilder

class AuthController:
    def __init__(self, userService, robotService):
        self.userService = userService
        self.robotService = robotService

    async def handleRequest(self, method, params, websocket, request_id):
        if method == "auth.register":
            await self.registerUser(params, websocket, request_id)
        elif method == "auth.login":
            await self.loginUser(params, websocket, request_id)
        else:
            await self.sendErrorResponse(websocket, -32601, "Method not found", request_id)

    async def registerUser(self, params, websocket, request_id):
        result = self.userService.registerUser(params.get("username"), params.get("password"), params.get("role_name"))
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def loginUser(self, params, websocket, request_id):
        result = self.userService.loginUser(params.get("username"), params.get("password"))
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def registerRobot(self, params, websocket, request_id):
        result = self.robotService.registerRobot(params.get("botname"))
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def sendErrorResponse(self, websocket, code, message, request_id):
        # Usar JSONRPCResponseBuilder para construir la respuesta de error
        error_response = JSONRPCResponseBuilder().set_error(code, message).set_id(request_id).build()
        await websocket.send(json.dumps(error_response))

    async def sendSuccessResponse(self, websocket, result, request_id):
        # Usar JSONRPCResponseBuilder para construir la respuesta exitosa
        success_response = JSONRPCResponseBuilder().set_result(result).set_id(request_id).build()
        await websocket.send(json.dumps(success_response))
