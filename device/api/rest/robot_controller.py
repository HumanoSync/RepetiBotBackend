import json
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.robot_mapper import RobotMapper
from device.resource.request.robot_request import CreateRobotRequest, UpdateCurrentPositionRequest, UpdateInitialPositionRequest, UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseWithToken, RobotResponseWithoutPositions
from device.service.robot_service import RobotService
from security.domain.model.user import Role, User
from crosscutting.authorization import authorizeRoles, getAuthenticatedUser
from core.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/robot",
    tags=["robot"]
)

# Crear robot
@router.post("/create", response_model=RobotResponseWithToken, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def createRobot(request: CreateRobotRequest, 
                      authenticatedUser: User = Depends(getAuthenticatedUser), 
                      robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.create(RobotMapper.createRequestToModel(request, authenticatedUser.id))
    return RobotMapper.modelToResponseWithToken(robot)

@router.get("/all", response_model=list[RobotResponseWithoutPositions], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobots(robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAll()
    return [RobotMapper.modelToResponseWithoutPositions(robot) for robot in robots]

# obtener todos mis robots
@router.get("/all-by-my", response_model=list[RobotResponseWithToken], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsByMy(authenticatedUser: User = Depends(getAuthenticatedUser), 
                           robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAllByUserId(authenticatedUser.id)
    return [RobotMapper.modelToResponseWithToken(robot) for robot in robots]

# Obtener robot por token
@router.get("/by-token/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotByToken(robotToken: str, 
                          robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.getByToken(robotToken)
    return RobotMapper.modelToResponse(robot)

# Actualizar robot por token
@router.put("/update/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateRobotByToken(robotToken: str, 
                             request: UpdateRobotRequest, 
                             robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateByToken(robotToken, request.token, request.botname)
    return RobotMapper.modelToResponse(robot)

# Actualizar posición inicial por token
@router.put("/update-initial-position/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateInitialPositionByToken(robotToken: str, 
                                       newPosition: UpdateInitialPositionRequest, 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateInitialPositionByToken(robotToken, json.dumps(newPosition.initial_position))
    return RobotMapper.modelToResponse(robot)

# Actualizar posición actual por token
@router.put("/update-current-position/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def updateCurrentPositionByToken(robotToken: str, 
                                       newPosition: UpdateCurrentPositionRequest, 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateCurrentPositionByToken(robotToken, json.dumps(newPosition.current_position))
    return RobotMapper.modelToResponse(robot)

# Eliminar robot por token
@router.delete("/delete/{robotToken}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def deleteRobotByToken(robotToken: str, 
                             robotService: RobotService = Depends(Provide[Container.robotService])):
    isDeleted = robotService.deleteByToken(robotToken)
    return {"is_deleted": isDeleted}

# Mover a la posición inicial por token
@router.post("/move-initial-position/{robotToken}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToInitialPositionByToken(robotToken: str, 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.moveToInitialPosition(robotToken)
    return {"message": message}

# Mover a la posición actual por token
@router.post("/move-current-position/{robotToken}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToCurrentPositionByToken(robotToken: str, 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.moveToCurrentPosition(robotToken)
    return {"message": message}

# Ejecutar movimiento por ID y token de robot
@router.post("/execute-movement/{movementId}/{robotToken}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def executeMovementByIdAndRobotToken(movementId: int, 
                                           robotToken: str, 
                                           robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.executeMovement(movementId, robotToken)
    return {"message": message}

# Guardar data en el robot para su uso local
@router.post("/save-data-locally/{robotToken}", response_model=dict, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
@inject
async def moveToCurrentPositionByToken(robotToken: str, 
                                       robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.saveDataLocally(robotToken)
    return {"message": message}

# ADMIN*************************************************************************************************************
# Obtener todos los robots con sus tokens
@router.get("/all-with-token", response_model=list[RobotResponseWithToken], dependencies=[Depends(authorizeRoles([Role.ADMIN]))])
@inject
async def getAllRobots(robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAll()
    return [RobotMapper.modelToResponseWithToken(robot) for robot in robots]