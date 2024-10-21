import json
from typing import List
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from device.mapping.robot_mapper import RobotMapper
from device.resource.request.create_robot_request import CreateRobotRequest
from device.resource.request.update_robot_request import UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse
from device.service.robot_service import RobotService
from security.domain.model.user import Role, User
from security.service.authorize import authorize_roles, get_current_user
from shared.container import Container

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/robot",
    tags=["robot"]
)

# Crear robot
@router.post("/create", response_model=RobotResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def createRobot(request: CreateRobotRequest, currentUser: User = Depends(get_current_user), robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.create(RobotMapper.createRequestToModel(request, currentUser.id))
    return RobotMapper.modelToResponseWithToken(robot)

# obtener todos mis robots
@router.get("/all-by-my", response_model=list[RobotResponse], dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def getAllRobotsByMy(currentUser: User = Depends(get_current_user), robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAllByUserId(currentUser.id)
    return [RobotMapper.modelToResponseWithToken(robot) for robot in robots]

# Obtener robot por token
@router.get("/by-token/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def getRobotByToken(robotToken: str, robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.getByToken(robotToken)
    return RobotMapper.modelToResponse(robot)

# Actualizar robot por token
@router.put("/update/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def updateRobotByToken(robotToken: str, request: UpdateRobotRequest, robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateByToken(robotToken, request.token, request.botname)
    return RobotMapper.modelToResponse(robot)

# Actualizar posición inicial por token
@router.put("/update-initial-position/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def updateInitialPositionByToken(robotToken: str, newPosition: List[int], robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateInitialPositionByToken(robotToken, json.dump(newPosition))
    return RobotMapper.modelToResponse(robot)

# Actualizar posición actual por token
@router.put("/update-current-position/{robotToken}", response_model=RobotResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def updateCurrentPositionByToken(robotToken: str, newPosition: List[int], robotService: RobotService = Depends(Provide[Container.robotService])):
    robot = robotService.updateCurrentPositionByToken(robotToken, json.dump(newPosition))
    return RobotMapper.modelToResponse(robot)

# Eliminar robot por token
@router.delete("/delete/{robotToken}", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def deleteRobotByToken(robotToken: str, robotService: RobotService = Depends(Provide[Container.robotService])):
    isDeleted = robotService.deleteByToken(robotToken)
    return {"is_deleted": isDeleted}

# Mover a la posición inicial por token
@router.post("/move-initial-position/{robotToken}", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def moveToInitialPositionByToken(robotToken: str, robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.moveToInitialPositionByToken(robotToken)
    return {"message": message}

# Mover a la posición actual por token
@router.post("/move-current-position/{robotToken}", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
@inject
async def moveToCurrentPositionByToken(robotToken: str, robotService: RobotService = Depends(Provide[Container.robotService])):
    message = robotService.moveToCurrentPositionByToken(robotToken)
    return {"message": message}

# ADMIN*************************************************************************************************************
# Obtener todos los robots con sus tokens
@router.get("/all", response_model=list[RobotResponse], dependencies=[Depends(authorize_roles([Role.ADMIN]))])
@inject
async def getAllRobots(robotService: RobotService = Depends(Provide[Container.robotService])):
    robots = robotService.getAll()
    return [RobotMapper.modelToResponseWithToken(robot) for robot in robots]