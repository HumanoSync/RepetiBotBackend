import asyncio
from database import Database

from repositories.robot_repository import RobotRepository
from repositories.button_repository import ButtonRepository
from repositories.servo_repository import ServoRepository
from repositories.movement_repository import MovementRepository
from repositories.position_repository import PositionRepository

from services.auth_service import AuthService
from services.button_service import ButtonService
from services.servo_service import ServoService
from services.movement_service import MovementService
from services.position_service import PositionService

from websocket_handler import WebSocketHandler
import websockets

async def startDataServer(authService, buttonManager, servoService, movementService, positionService):
    websocketHandler = WebSocketHandler(authService, buttonManager, servoService, movementService, positionService)
    startServer = websockets.serve(websocketHandler.handleMessage, '0.0.0.0', 8765, max_size=None)
    await startServer
    print("Servidor WebSocket de datos iniciado en el puerto 8765")
    await asyncio.Future()  # Run forever

async def main():
    db = Database()
    robotRepository = RobotRepository(db)
    buttonRepository = ButtonRepository(db)
    servoRepository = ServoRepository(db)
    movementRepository = MovementRepository(db)
    positionRepository = PositionRepository(db)

    authService = AuthService(robotRepository)
    buttonService = ButtonService(buttonRepository)
    servoService = ServoService(servoRepository)
    movementService = MovementService(movementRepository)
    positionService = PositionService(positionRepository, movementRepository)
    
    dataTask = asyncio.create_task(startDataServer(authService, buttonService, servoService, movementService, positionService))

    await asyncio.gather(dataTask)

if __name__ == "__main__":
    asyncio.run(main())