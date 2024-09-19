import json
from container import Container

from controllers.auth_controller import AuthController
from controllers.robot_controller import RobotController
from controllers.access_controller import AccessController

from response_builder import JSONRPCResponseBuilder
from request_builder import JSONRPCRequestBuilder

class WebSocketHandler:
    def __init__(self):
        self.container = Container()

        # Extrae las dependencias desde el contenedor
        self.authService = self.container.auth_service()
        self.accessService = self.container.access_service()
        self.robotService = self.container.robot_service()

        # Controladores inicializados con los servicios necesarios
        self.authController = AuthController(self.authService)
        self.robotController = RobotController(self.authService)
        self.accessController = AccessController(self.authService)

    async def handleMessage(self, websocket):
        async for message in websocket:
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                print('Error al decodificar el mensaje JSON')
                await self.sendErrorResponse(websocket, -32700, "Invalid JSON", None)
                continue
            
            # Usamos el JSONRPCRequestBuilder para construir la solicitud y luego extraer la información
            try:
                request = JSONRPCRequestBuilder() \
                    .set_method(data.get('method')) \
                    .set_params(data.get('params', {})) \
                    .set_id(data.get('id')) \
                    .build()
            except ValueError as e:
                await self.sendErrorResponse(websocket, -32600, str(e), None)
                continue

            method = request["method"]
            params = request["params"]  # Parámetros de la solicitud
            request_id = request["id"]
            token = params.get("token")  # Extraer el token de los parámetros

            if not method:
                await self.sendErrorResponse(websocket, -32600, "Invalid Request", request_id)
                continue

            # Primero, manejar rutas de autenticación
            if method.startswith("auth"):
                await self.authController.handleRequest(method, params, websocket, request_id)
            else:
                # Primero, intentar validar como un robot
                robot = self.authService.validateRobotToken(token)
                if robot:
                    role_name = "robot"
                else:
                # Si no es robot, intentamos como usuario
                    user = self.authService.validateUserToken(token)
                    if not user:
                        await self.sendErrorResponse(websocket, -32000, "Unauthorized", request_id)
                        continue
                    role = self.authService.getRoleById(user.role_id)
                    role_name = role.name

                # Verificar permisos para el endpoint
                if not self.hasPermission(method, role_name):
                    await self.sendErrorResponse(websocket, -32000, "Forbidden", request_id)
                    continue

                # Rutas para Robots
                if method.startswith("robot"):
                    await self.robotController.handleRequest(method, params, websocket, request_id)
                # Rutas para Access
                elif method.startswith("access"):
                    await self.accessController.handleRequest(method, params, websocket, request_id)
                else:
                    await self.sendErrorResponse(websocket, -32601, "Method not found", request_id)

    async def sendErrorResponse(self, websocket, code, message, request_id):
        # Usar JSONRPCResponseBuilder para construir la respuesta de error
        error_response = JSONRPCResponseBuilder().set_error(code, message).set_id(request_id).build()
        await websocket.send(json.dumps(error_response))

    async def sendSuccessResponse(self, websocket, result, request_id):
        # Usar JSONRPCResponseBuilder para construir la respuesta exitosa
        success_response = JSONRPCResponseBuilder().set_result(result).set_id(request_id).build()
        await websocket.send(json.dumps(success_response))

    def hasPermission(self, method, role_name):
        # Define role-based access control for "admin" and "user"
        permissions = {
            # Permisos para los robots
            "robots.create": ["admin", "user", "robot"],
            "robots.update": ["admin", "user", "robot"],
            "robots.delete": ["admin", "user", "robot"],
            "robots.get": ["admin", "user", "robot"],
            "robots.getAll": ["admin", "user", "robot"],

            # Permisos para las posiciones iniciales
            "initial-positions.create": ["admin", "user", "robot"],
            "initial-positions.update": ["admin", "user", "robot"],
            "initial-positions.delete": ["admin", "user", "robot"],
            "initial-positions.get": ["admin", "user", "robot"],
            "initial-positions.getAll": ["admin", "user", "robot"],

            # Permisos para los botones
            "buttons.create": ["admin", "user", "robot"],
            "buttons.update": ["admin", "user", "robot"],
            "buttons.delete": ["admin", "user", "robot"],
            "buttons.get": ["admin", "user", "robot"],
            "buttons.getAll": ["admin", "user", "robot"],

            # Permisos para los servos
            "servos.create": ["admin", "user", "robot"],
            "servos.update": ["admin", "user", "robot"],
            "servos.delete": ["admin", "user", "robot"],
            "servos.get": ["admin", "user", "robot"],
            "servos.getAll": ["admin", "user", "robot"],

            # Permisos para los movimientos
            "movements.create": ["admin", "user", "robot"],
            "movements.update": ["admin", "user", "robot"],
            "movements.delete": ["admin", "user", "robot"],
            "movements.get": ["admin", "user", "robot"],
            "movements.getAll": ["admin", "user", "robot"],

            # Permisos para las posiciones
            "positions.create": ["admin", "user", "robot"],
            "positions.update": ["admin", "user", "robot"],
            "positions.delete": ["admin", "user", "robot"],
            "positions.get": ["admin", "user", "robot"],
            "positions.getAll": ["admin", "user", "robot"],
            "positions.moveUp": ["admin", "user", "robot"],
            "positions.moveDown": ["admin", "user", "robot"],
        }

        return role_name in permissions.get(method, [])
