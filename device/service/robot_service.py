import json
from typing import List
import uuid
from fastapi import HTTPException, status
from device.domain.persistence.robot_repository import RobotRepository
from device.domain.model.robot import Robot
from security.service.user_service import UserService
from shared.mqtt_client import mqttClient

class RobotService:
    def __init__(self, robotRepository: RobotRepository, userService: UserService):
        self.repository = robotRepository
        self.userService = userService
    
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
        robot = self.repository.findAll()
        return robot
    
    def getAllByUserId(self, userId: int):
        self.userService.getById(userId)
        robot = self.repository.findAllByUserId(userId)
        return robot
    
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
        robot.is_connected_broker = isConnected or robot.is_connected_broker
        return self.repository.save(robot)
    
    def moveToInitialPositionByToken(self, robotToken: str):
        # Verificar si el robot está conectado
        robot = self.getByToken(robotToken)

        # Preparar el comando para mover a la posición inicial
        initialPosition = robot.initial_position  # Obtener la posición inicial desde la base de datos

        # Publicar el mensaje con la posición inicial
        topic = f"robot/{robot.token}/access/movement"
        message = {
            "movement": [{"angles": initialPosition, "delay": 500}]  # Duración estimada para alcanzar la posición inicial
        }
        mqttClient.publish(topic, json.dumps(message))
        print(topic)
        
        # Actualizar la posición actual del robot en la base de datos
        robot.current_position = initialPosition
        self.repository.save(robot)

        return "Robot moved to initial position"
    
    def moveToCurrentPositionByToken(self, robotToken: str):
        # Verificar si el robot está conectado
        robot = self.getByToken(robotToken)
        
        currentPosition = robot.current_position

        # Publicar el mensaje con la nueva posición
        topic = f"robot/{robot.token}/access/movement"
        message = {
            "movement": [{"angles": currentPosition, "delay": 500}]
        }
        mqttClient.publish(topic, json.dumps(message))
        print(topic)

        return "Current position updated and sent to robot"