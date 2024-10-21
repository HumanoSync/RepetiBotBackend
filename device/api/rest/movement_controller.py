from fastapi import APIRouter, Depends
from device.mapping.movement_mapper import MovementMapper
from device.resource.request.update_movement_request import UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse
from device.resource.request.create_movement_request import CreateMovementRequest
from security.domain.model.user import Role
from security.service.authorize import authorize_roles
from shared.container import Container

# Inyectar el contenedor
container = Container()
movementService = container.movementService()

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/movement",
    tags=["movement"]
)

# Crear movimiento
@router.post("/create", response_model=MovementResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
async def createMovement(request: CreateMovementRequest):
    movement = movementService.create(MovementMapper.createRequestToModel(request))
    return MovementMapper.modelToResponse(movement)

# Obtener todos los movimientos por ID de robot
@router.get("/all-by-robot/{robotId}", response_model=list[MovementResponse], dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
async def getAllMovementsByRobotId(robotId: int):
    movements = movementService.getAllByRobotId(robotId)
    return [MovementMapper.modelToResponse(movement) for movement in movements]

# Actualizar movimiento por ID
@router.put("/update/{movementId}", response_model=MovementResponse, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
async def updateMovementById(movementId: int, request: UpdateMovementRequest):
    movement = movementService.updateById(movementId, MovementMapper.updateRequestToModel(request))
    return MovementMapper.modelToResponse(movement)

# Eliminar movimiento por ID
@router.delete("/delete/{movementId}", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
async def deleteMovementById(movementId: int):
    isDeleted = movementService.deleteById(movementId)
    return {"is_deleted": isDeleted}

# Ejecutar movimiento por ID y token de robot
@router.post("/execute/{movementId}/{robotToken}", response_model=dict, dependencies=[Depends(authorize_roles([Role.USER, Role.ADMIN]))])
async def executeMovementByIdAndRobotToken(movementId: int, robotToken: str):
    message = movementService.executeByIdAndRobotToken(movementId, robotToken)
    return {"message": message}