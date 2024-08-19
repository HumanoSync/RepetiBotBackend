import jwt  # Necesitarás instalar esta librería si aún no la tienes
from datetime import datetime, timedelta
from response_handler import ResponseHandler
from dataclasses import asdict

class AuthService(ResponseHandler):
    def __init__(self, robotRepository):
        self.repository = robotRepository
        self.secret_key = "e6e5b0db-4fcc-449c-aa80-10b49b8a156c"

    async def registerRobot(self, data, websocket, requestId):
        robotname = data.get('robotname')
        password = data.get('password')

        if not robotname or not password:
            await self.sendErrorResponse(websocket, {"message": "Robotname and password are required"}, requestId)
            return
        
        if self.repository.findByName(robotname):
            await self.sendErrorResponse(websocket, {"message": "Robot with this name already exists"}, requestId)
            return

        robotId = self.repository.save(robotname, password)
        robot = self.repository.findById(robotId)
        await self.sendResponse(websocket, asdict(robot), requestId)

    async def loginRobot(self, data, websocket, requestId):
        robotname = data.get('robotname')
        password = data.get('password')

        if not robotname or not password:
            await self.sendErrorResponse(websocket, {"message": "Robotname and password are required"}, requestId)
            return

        if self.repository.authenticate(robotname, password):
            token = self.generate_token(robotname)
            payload = {
                "token": token,
                "robot": self.validateToken(token)
            }
            await self.sendResponse(websocket, payload, requestId)
        else:
            await self.sendErrorResponse(websocket, {"message": "Invalid robotname or password"}, requestId)

    def generateToken(self, robotname):
        payload = {
            'robotname': robotname,
            'exp': datetime.utcnow() + timedelta(hours=1)  # El token expira en 1 hora
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def validateToken(self, token):
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return self.repository.findByName(decoded['name'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
