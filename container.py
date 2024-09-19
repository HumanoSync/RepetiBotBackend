from dependency_injector import containers, providers
from database import Database
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from repositories.access_repository import AccessRepository
from repositories.robot_repository import RobotRepository
from repositories.initial_position_repository import InitialPositionRepository
from repositories.button_repository import ButtonRepository
from repositories.servo_repository import ServoRepository
from repositories.movement_repository import MovementRepository
from repositories.position_repository import PositionRepository
from services.user_service import AuthService
from services.access_service import AccessService
from services.robot_service import RobotService
from services.initial_position_service import InitialPositionService
from services.button_service import ButtonService
from services.servo_service import ServoService
from services.movement_service import MovementService
from services.position_service import PositionService

class Container(containers.DeclarativeContainer):

    # Database
    database = providers.Singleton(Database)
    
    # Repositories
    role_repository = providers.Factory(RoleRepository, db=database)
    user_repository = providers.Factory(UserRepository, db=database)
    access_repository = providers.Factory(AccessRepository, db=database)
    robot_repository = providers.Factory(RobotRepository, db=database)
    initial_position_repository = providers.Factory(InitialPositionRepository, db=database)
    button_repository = providers.Factory(ButtonRepository, db=database)
    servo_repository = providers.Factory(ServoRepository, db=database)
    movement_repository = providers.Factory(MovementRepository, db=database)
    position_repository = providers.Factory(PositionRepository, db=database)
    
    # Services
    auth_service = providers.Factory(AuthService, userRepository=user_repository, roleRepository=role_repository)
    access_service = providers.Factory(AccessService, accessRepository=access_repository)
    robot_service = providers.Factory(RobotService, robotRepository=robot_repository)
    initial_position_service = providers.Factory(InitialPositionService, initialPositionRepository=initial_position_repository)
    button_service = providers.Factory(ButtonService, buttonRepository=button_repository)
    servo_service = providers.Factory(ServoService, servoRepository=servo_repository)
    movement_service = providers.Factory(MovementService, movementRepository=movement_repository)
    position_service = providers.Factory(PositionService, positionRepository=position_repository, movementRepository=movement_repository)