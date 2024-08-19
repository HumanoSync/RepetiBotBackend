import json

class WebSocketHandler:
    def __init__(self, authService, buttonService, servoService, movementService, positionService):
        self.authService = authService
        self.buttonService = buttonService
        self.servoService = servoService
        self.movementService = movementService
        self.positionService = positionService
        #self.videoControl = videoControl

    async def handleMessage(self, websocket, path):
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print('Error al decodificar el mensaje JSON')
                await self.sendErrorResponse(websocket, {"message": "Invalid JSON"}, None)
                continue
            
            endpoint = data.get('endpoint')
            method = data.get('method')
            payload = data.get('payload', {})
            requestId = data.get('request_id')
            token = data.get('token')

            if not endpoint or not method:
                await self.sendErrorResponse(websocket, {"message": "Invalid request"}, requestId)
                continue

            # Primero, manejar rutas de autenticación
            if endpoint.startswith("/auth"):
                await self.handleAuthRequests(endpoint, method, payload, websocket, requestId)

            # Verificar autenticación para otros endpoints
            robot = self.authService.validateToken(token)
            if not robot:
                await self.sendErrorResponse(websocket, {"message": "Unauthorized"}, requestId)
                continue

            # Rutas para Button
            if endpoint.startswith("/app/buttons"):
                await self.handleButtonRequests(endpoint, method, robot, payload, websocket, requestId)
            # Rutas para Servo
            elif endpoint.startswith("/app/servos"):
                await self.handleServoRequests(endpoint, method, robot, payload, websocket, requestId)
            # Rutas para Movements
            elif endpoint.startswith("/app/movements"):
                await self.handleMovementRequests(endpoint, method, robot, payload, websocket, requestId)
            # Rutas para Positions
            elif endpoint.startswith("/app/positions"):
                await self.handlePositionRequests(endpoint, method, payload, websocket, requestId)
            else:
                await self.sendErrorResponse(websocket, {"message": "Invalid endpoint"}, requestId)

    async def handleAuthRequests(self, endpoint, method, payload, websocket, requestId):
        if endpoint == "/auth/register" and method == "POST":
            await self.authService.registerRobot(payload, websocket, requestId)
        elif endpoint == "/auth/login" and method == "POST":
            await self.authService.loginRobot(payload, websocket, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid authentication request"}, requestId)

    async def handleButtonRequests(self, endpoint, method, robot, payload, websocket, requestId):
        if endpoint == "/app/buttons/create" and method == "POST":
            await self.buttonService.createButton(robot, payload, websocket, requestId)
        elif endpoint == "/app/buttons/update" and method == "POST":
            await self.buttonService.updateButtonById(payload, websocket, requestId)
        elif endpoint == "/app/buttons/delete" and method == "POST":
            await self.buttonService.deleteButtonById(payload, websocket, requestId)
        elif endpoint == "/app/buttons/get" and method == "GET":
            await self.buttonService.getButtonById(payload, websocket, requestId)
        elif endpoint == "/app/buttons/getAll" and method == "GET":
            await self.buttonService.getAllButtonsByRobotId(robot, websocket, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid button request"}, requestId)

    async def handleServoRequests(self, endpoint, method, robot, payload, websocket, requestId):
        if endpoint == "/app/servos/create" and method == "POST":
            await self.servoService.createServo(robot, payload, websocket, requestId)
        elif endpoint == "/app/servos/update" and method == "POST":
            await self.servoService.updateServoById(payload, websocket, requestId)
        elif endpoint == "/app/servos/delete" and method == "POST":
            await self.servoService.deleteServoById(payload, websocket, requestId)
        elif endpoint == "/app/servos/get" and method == "GET":
            await self.servoService.getServoById(payload, websocket, requestId)
        elif endpoint == "/app/servos/getAll" and method == "GET":
            await self.servoService.getAllServosByRobotId(robot, websocket, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid servo request"}, requestId)

    async def handleMovementRequests(self, endpoint, method, robot, payload, websocket, requestId):
        if endpoint == "/app/movements/create" and method == "POST":
            await self.movementService.createMovement(robot, payload, websocket, requestId)
        elif endpoint == "/app/movements/update" and method == "POST":
            await self.movementService.updateMovementById(robot, payload, websocket, requestId)
        elif endpoint == "/app/movements/delete" and method == "POST":
            await self.movementService.deleteMovementById(payload, websocket, requestId)
        elif endpoint == "/app/movements/get" and method == "GET":
            await self.movementService.getMovementById(payload, websocket, requestId)
        elif endpoint == "/app/movements/getAll" and method == "GET":
            await self.movementService.getAllMovementsByRobotId(robot, websocket, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid movement request"}, requestId)

    async def handlePositionRequests(self, endpoint, method, payload, websocket, requestId):
        if endpoint == "/app/positions/create" and method == "POST":
            await self.positionService.createPosition(payload, websocket, requestId)
        elif endpoint == "/app/positions/update" and method == "POST":
            await self.positionService.updatePositionById(payload, websocket, requestId)
        elif endpoint == "/app/positions/delete" and method == "POST":
            await self.positionService.deletePositionById(payload, websocket, requestId)
        elif endpoint == "/app/positions/get" and method == "GET":
            await self.positionService.getPositionById(payload, websocket, requestId)
        elif endpoint == "/app/positions/getAll" and method == "GET":
            await self.positionService.getAllPositionsByMovementId(payload, websocket, requestId)
        elif endpoint == "/app/positions/moveUp" and method == "POST":
            await self.positionService.movePositionUpById(payload, websocket, requestId)
        elif endpoint == "/app/positions/moveDown" and method == "POST":
            await self.positionService.movePositionDownById(payload, websocket, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid position request"}, requestId)

    async def sendErrorResponse(self, websocket, errorMessage, requestId):
        response = {
            'request_id': requestId,
            'error': errorMessage
        }
        await websocket.send(json.dumps(response))
