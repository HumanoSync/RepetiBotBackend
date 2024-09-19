from dataclasses import asdict


class AccessService:
    def __init__(self, accessRepository, robotRepository, userRepository):
        self.repository = accessRepository
        self.robotRepository = robotRepository
        self.userRepository = userRepository

    def connect(self, userId, robotId):
        if not isinstance(userId, int) or not isinstance(robotId, int):
            return {"code": -32602, "message": "User ID and Robot ID are required and must be integers"}
        
        # Verificar si la relación usuario-robot existe en la tabla access
        access = self.repository.findAccess(userId, robotId)
        if not access:
            return {"code": -32602, "message": "Access relation between user and robot not found"}

        # Actualizar el estado de conexión
        if access.is_connected:
            return {"code": -32603, "message": "User is already connected to this robot"}

        self.accessRepository.updateConnectionStatus(userId, robotId, True)
        return {"message": "User connected to robot successfully"}

    def disconnect(self, userId, robotId):
        if not isinstance(userId, int) or not isinstance(robotId, int):
            return {"code": -32602, "message": "user_id and robot_id are required"}
        
        # Verificar si la relación usuario-robot existe en la tabla access
        access = self.repository.findAccess(userId, robotId)
        if not access:
            return {"code": -32602, "message": "Access relation between user and robot not found"}

        # Actualizar el estado de desconexión
        if not access.is_connected:
            return {"code": -32603, "message": "User is not connected to this robot"}

        self.repository.updateConnectionStatus(userId, robotId, False)
        return {"message": "User disconnected from robot successfully"}
    
    def createAccess(self, userId, robotId):
        if not isinstance(userId, int) or not isinstance(robotId, int):
            return {"code": -32602, "message": "user_id and robot_id are required"}
            
        # Verificar si el usuario y el robot existen
        if not self.userRepository.findById(userId):
            return {"code": -32602, "message": "User not found"}
        
        if not self.robotRepository.findById(robotId):
            return {"code": -32602, "message": "Robot not found"}

        # Verificar si ya existe la relación
        if self.repository.findByUserIdAndRobotId(userId, robotId):
            return {"code": -32604, "message": "Access already exists between user and robot"}

        # Crear nuevo acceso
        accessId = self.repository.createAccess(userId, robotId)
        access = self.repository.findById(accessId)
        return asdict(access)

    def deleteAccess(self, userId, robotId):
        if not isinstance(userId, int) or not isinstance(robotId, int):
            return {"code": -32602, "message": "user_id and robot_id are required"}
        
        # Verificar si el acceso existe
        access = self.repository.findByUserIdAndRobotId(userId, robotId)
        if not access:
            return {"code": -32602, "message": "Access relation between user and robot not found"}

        # Eliminar acceso
        accessId = self.repository.deleteById(access.id)
        return {'id': accessId}
    
    async def getAllRobotsByUserId(self, userId):
        if not isinstance(userId, int):
            return {"code": -32602, "message": "user_id are required"}
        
        robots = self.repository.findAllRobotsByUserId(userId)
        return {
            "total_items": len(robots),
            "content": [asdict(robot) for robot in robots]
        }
