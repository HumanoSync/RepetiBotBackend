from dataclasses import asdict
import uuid

class RobotService:
    def __init__(self, robotRepository):
        self.repository = robotRepository

    def registerRobot(self, botname):
        if not botname:
            return {"code": -32700, "message": "Botname is required"}
        
        if self.repository.findByName(botname):
            return {"code": -32700, "message": "Robot with this name already exists"}
        
        token = self.generateRobotToken(botname)
        self.repository.save(botname, token)  # Guardamos el bot y su token en la BD
        auth_response = {
            "token": token,
            "robot": asdict(self.validateRobotToken(token))  # Validamos y devolvemos la info del robot
        }
        return auth_response

    def generateRobotToken(self, botname):
        token = str(uuid.uuid4())
        while self.repository.findByToken(token):
            token = str(uuid.uuid4())
        return token


    def validateRobotToken(self, token):
        # Verificamos si el token existe en la base de datos de robots
        robot = self.repository.findByToken(token)
        if robot:
            return robot  # Si el token es válido, devolvemos la info del robot
        else:
            raise ValueError("Invalid or expired token")
        
    def updateRobotById(self, robotId, botname):
        if not robotId or not isinstance(robotId, int):
            return {"code": -32700, "message": "Robot ID is required and must be an integer"}
        
        if not botname:
            return {"code": -32700, "message": "Robot botname is required"}

        if not self.repository.findById(robotId):
            return {"code": -32700, "message": "Robot ID does not exist"}
        
        existingRobot = self.repository.findByName(botname)
        if existingRobot and existingRobot.id != robotId:
            return {"code": -32700, "message": "Robot with this botname already exists"}

        self.repository.updateById(robotId, botname)
        robot = self.repository.findById(robotId)
        return asdict(robot)

    def deleteRobotById(self, robotId):
        if not isinstance(robotId, int):
            return {"code": -32700, "message": "Robot ID is required and must be an integer"}

        if not self.repository.findById(robotId):
            return {"code": -32700, "message": "message": "Robot ID does not exist"}

        self.repository.deleteById(robotId)
        return {"id": robotId}

    def getRobotById(self, robotId):
        if not isinstance(robotId, int):
            return {"code": -32700, "message": "Robot ID is required and must be an integer"}

        robot = self.repository.findById(robotId)
        if robot:
            return asdict(robot)
        else:
            return {"code": -32700, "message": "Robot not found"}

    def getAllRobots(self):
        robots = self.repository.findAll()
        return {
            "total_items": len(robots),
            "content": [asdict(robot) for robot in robots]
        }
