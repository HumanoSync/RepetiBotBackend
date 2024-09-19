import json
from response_builder import JSONRPCResponseBuilder

class AccessController:
    def __init__(self, accessService):
        self.accessService = accessService

    async def handleRequest(self, method, params, websocket, request_id):
        if method == "access.connect":
            await self.registerUser(params, websocket, request_id)
        elif method == "access.disconnect":
            await self.loginUser(params, websocket, request_id)
        elif method == "access.create":
            await self.createAccess(params, websocket, request_id)
        elif method == "access.delete":
            await self.deleteAccess(params, websocket, request_id)
        else:
            await self.sendErrorResponse(websocket, -32601, "Method not found", request_id)

    async def connect(self, params, websocket, request_id):
        result = self.accessService.connect(params.get("robot_id"))
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def disconnect(self, params, websocket, request_id):
        result = self.accessService.disconnect()
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def createAccess(self, params, websocket, request_id):
        result = self.accessService.createAccess(params.get("user_id"), params.get("robot_id"))
        if "code" in result and "message" in result:
            await self.sendErrorResponse(websocket, result["code"], result["message"], request_id)
        else:
            await self.sendSuccessResponse(websocket, result, request_id)

    async def deleteAccess(self, params, websocket, request_id):
        result = self.accessService.deleteAccess(params.get("user_id"), params.get("robot_id"))
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
