import json
import uuid
from fastapi import HTTPException, status
from device.domain.persistence.robot_repository import RobotRepository
from device.domain.model.robot import Robot
from crosscutting.mqtt_client import mqttClient
from device.service.movement_service import MovementService
from device.service.position_service import PositionService

class RobotService:
    def __init__(self, robotRepository: RobotRepository, movementService: MovementService, positionService: PositionService):
        self.repository = robotRepository
        self.movementService = movementService
        self.positionService = positionService
    
    def create(self, robot: Robot):
        if any(angle < 0 or angle > 180 for angle in json.loads(robot.initial_position)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Each angle must be between 0 and 180")
        
        if self.repository.findByBotname(robot.botname):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot already exists")
        
        # Generar un token único para el robot
        token = str(uuid.uuid4())
        while self.repository.findByToken(token):
            token = str(uuid.uuid4())
        
        robot.token = token
        return self.repository.save(robot)
    
    def getById(self, robotId: int):
        robot = self.repository.findById(robotId)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
        return robot
    
    def getByBotname(self, botname: str):
        robot = self.repository.findByBotname(botname)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found")
        return robot
    
    def getByToken(self, robotToken: str):
        robot = self.repository.findByToken(robotToken)
        if not robot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found by token")
        return robot
    
    def getAll(self):
        robots = self.repository.findAll()
        return robots
    
    def getAllByUserId(self, userId: int):
        robots = self.repository.findAllByUserId(userId)
        return robots
    
    def updateByToken(self, robotToken: str, newToken: str, newBotname: str):
        robotToUpdate = self.getByToken(robotToken)

        robotToUpdate.token = newToken or robotToUpdate.token
        robotToUpdate.botname = newBotname or robotToUpdate.botname    
        return self.repository.save(robotToUpdate)
    
    def updateInitialPositionByToken(self, robotToken: str, newInitialPosition: str):
        robotToUpdate = self.getByToken(robotToken)
        
        if any(angle < 0 or angle > 180 for angle in json.loads(newInitialPosition)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Each angle must be between 0 and 180")

        robotToUpdate.initial_position = newInitialPosition
        return self.repository.save(robotToUpdate)

    def updateCurrentPositionByToken(self, robotToken: str, newCurrentPosition: str):
        robotToUpdate = self.getByToken(robotToken)
        
        if any(angle < 0 or angle > 180 for angle in json.loads(newCurrentPosition)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Each angle must be between 0 and 180")

        robotToUpdate.current_position = newCurrentPosition
        return self.repository.save(robotToUpdate)
    
    def deleteByToken(self, robotToken: str):
        robotToDelete = self.getByToken(robotToken)
        self.repository.deleteById(robotToDelete.id)
        return True
    
    def updateConnectionStatus(self, robotToken: str, isConnected: bool):
        robot = self.getByToken(robotToken)
        robot.is_connected_broker = isConnected
        return self.repository.save(robot)
    
    def moveToInitialPosition(self, robotToken: str):
        # Verificar si el robot está conectado
        robot = self.getByToken(robotToken)

        # Publicar el mensaje con la posición inicial
        topic = f"robot/{robotToken}/access/movement"
        message = {
            "movement": [{"delay": 500, "angles": json.loads(robot.initial_position)}]  # Duración estimada para alcanzar la posición inicial
        }
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")
        
        # Actualizar la posición actual del robot en la base de datos
        robot.current_position = robot.initial_position
        self.repository.save(robot)

        return "Robot moved to initial position"
    
    def moveToCurrentPosition(self, robotToken: str):
        # Verificar si el robot está conectado
        robot = self.getByToken(robotToken)

        if robot.token != robot.token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The robot not exists for this movement")

        # Publicar el mensaje con la nueva posición
        topic = f"robot/{robotToken}/access/movement"
        message = {
            "movement": [{"delay": 500, "angles": json.loads(robot.current_position)}]
        }
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return "Robot moved to current position"
    
    def executeMovement(self, movementId: int, robotToken: str):
        movement = self.movementService.getById(movementId)

        if self.getById(movement.robot_id).token != robotToken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Robot not found or the token is invalid for this movement")


        positions = self.positionService.getAllByMovementId(movement.id)  

        message = {
            "movement": [{"delay": position.delay, "angles": json.loads(position.angles)} for position in positions]
        }

        # Enviar todas las posiciones del movimiento al robot en un solo mensaje
        topic = f"robot/{robotToken}/access/movement"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        # Actualizar la posición actual en la base de datos con los últimos ángulos enviados
        self.updateCurrentPositionByToken(robotToken, positions[-1].angles)
        return "Movement executed successfully"
    
    #{60, 150, 30, 30, 120, 30, 150, 150, 90, 90, 0, 90, 90, 180, 90, 90}
    def saveDataLocally(self, robotToken: str):
        # Verificar si el robot existe y está conectado
        robot = self.getByToken(robotToken)
        movements = self.movementService.getAllByRobotId(robot.id)

        # Construir la estructura de datos para los movimientos y posiciones
        movements_data = []
        for movement in movements:
            positions = self.positionService.getAllByMovementId(movement.id)

            positions_data = [
                {"delay": position.delay, "angles": json.loads(position.angles)}  # Convertir angles a lista
                for position in positions
            ]
            movements_data.append({"name": movement.name, "positions": positions_data})

        # Crear el mensaje JSON con los datos adicionales del robot
        message = {
            "robot_id": robot.id,
            "botname": robot.botname,
            "initial_position": json.loads(robot.initial_position),
            "movements": movements_data
        }

        # Publicar el mensaje a través de MQTT
        topic = f"robot/{robotToken}/access/save"
        mqttClient.publish(topic, json.dumps(message))
        print(f"Data sent to topic {topic}")

        return "Robot data saved locally for offline usage"
    
# robot -> movement -> position
# position -> movement -> robot
