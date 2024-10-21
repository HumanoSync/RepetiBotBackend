from dependency_injector import containers, providers
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.service.movement_service import MovementService
from device.service.position_service import PositionService
from security.domain.persistence.user_repository import UserRepository
from device.domain.persistence.robot_repository import RobotRepository
from security.service.jwt_service import JwtService
from security.service.user_service import UserService
from device.service.robot_service import RobotService

class Container(containers.DeclarativeContainer):
    # Repositories
    userRepository = providers.Factory(UserRepository)
    robotRepository = providers.Factory(RobotRepository)
    movementRepository = providers.Factory(MovementRepository)
    positionRepository = providers.Factory(PositionRepository)

    # Services
    userService = providers.Factory(UserService, userRepository=userRepository)
    jwtService = providers.Factory(JwtService, userService=userService)
    robotService  = providers.Factory(RobotService, robotRepository=robotRepository, userService=userService)
    positionService = providers.Factory(PositionService, positionRepository=positionRepository)
    movementService = providers.Factory(MovementService, movementRepository=movementRepository, robotService=robotService, positionService=positionService)