import json
from fastapi import HTTPException, status
from device.domain.model.movement import Movement
from device.domain.persistence.movement_repository import MovementRepository
import paho.mqtt.client as mqtt

from device.service.position_service import PositionService
from device.service.robot_service import RobotService

class MovementService:
    def __init__(self, movementRepository: MovementRepository, robotService: RobotService, positionService: PositionService):
        self.repository = movementRepository
        self.robotService = robotService
        self.positionService = positionService
    
    def create(self, movement: Movement):
        if self.repository.findByNameAndRobotId(movement.name, movement.robot_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The movememnt already exists for this robot")
        return self.repository.save(movement)
        
    def getById(self, movement_id: int):
        movement = self.repository.findById(movement_id)
        if not movement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
        return movement
    
    def getAllByRobotId(self, robotId: int):        
        return self.repository.findAllByRobotId(robotId)
    
    def updateById(self, movementId: str, newName: str):
        movementToUpdate = self.getById(movementId)
        movementToUpdate.name = newName
        return self.repository.save(movementToUpdate)
    
    def deleteById(self, movementId: int):
        movementToDelete = self.getById(movementId)
        self.repository.deleteById(movementToDelete)
        return True

    def executeByIdAndRobotToken(self, movementId: int, robotToken: str):
        movement = self.getById(movementId)
        robot = self.robotService.getByToken(robotToken)

        if movement.robot.token != robot.token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The robot not exists for this movement")


        positions = self.positionService.getAllByMovementId(movement.id)  

        if not positions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No positions found for this movement")
                      
        # Inicializar cliente MQTT para enviar comandos al robot
        mqtt_client = mqtt.Client(client_id=f"client_for_{robot.token}")
        mqtt_client.username_pw_set("your_mqtt_username", "your_mqtt_password")
        mqtt_client.connect("broker.hivemq.com", 1883, 60)
        mqtt_client.loop_start()

        # Enviar todas las posiciones del movimiento al robot en un solo mensaje
        topic = f"robot/{robot.token}/access/movement"
        message = {
            "movement": [{"angles": position.angles, "delay": position.delay} for position in positions]
        }
        mqtt_client.publish(topic, json.dumps(message))

        mqtt_client.loop_stop()
        mqtt_client.disconnect()


        # Actualizar la posición actual en la base de datos con los últimos ángulos enviados
        self.robotService.updateCurrentPositionByToken(robot.token, positions[-1].angles)
        return "Movement executed successfully"