from dependency_injector import containers, providers
from device.domain.persistence.movement_repository import MovementRepository
from device.domain.persistence.position_repository import PositionRepository
from device.service.movement_service import MovementService
from device.service.position_service import PositionService
from security.domain.persistence.user_repository import UserRepository
from device.domain.persistence.robot_repository import RobotRepository
from security.service.auth_service import AuthService
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
    authService = providers.Factory(AuthService, userRepository=userRepository)

    positionService = providers.Factory(PositionService, positionRepository=positionRepository)
    movementService = providers.Factory(MovementService, movementRepository=movementRepository, positionService=positionService)
    robotService  = providers.Factory(RobotService, robotRepository=robotRepository, movementService=movementService, positionService=positionService)
    
    # robotService  = providers.Factory(RobotService, robotRepository=robotRepository)
    # movementService = providers.Factory(MovementService, movementRepository=movementRepository, robotService=robotService)
    # positionService = providers.Factory(PositionService, positionRepository=positionRepository, robotService=robotService, movementService=movementService)
    

    # robotService  = providers.Factory(RobotService, robotRepository=robotRepository, movementService=providers.Dependency(), positionService=providers.Dependency())
    # movementService = providers.Factory(MovementService, movementRepository=movementRepository, robotService=robotService, positionService=providers.Dependency())
    # positionService = providers.Factory(PositionService, positionRepository=positionRepository)

    # robotService.provided.kwargs['movementService'] = movementService
    # robotService.provided.kwargs['positionService'] = positionService
    # movementService.provided.kwargs['positionService'] = positionService