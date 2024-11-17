from fastapi import APIRouter, Depends
from device.mapping.movement_mapper import MovementMapper
from device.resource.request.movement_request import CreateMovementRequest, UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse
from security.domain.model.user import Role
from crosscutting.authorization import authorizeRoles
from core.container import Container

# Inyectar el contenedor
container = Container()
movementService = container.movementService()

# Definir el router con prefijo y etiqueta
router = APIRouter(
    prefix="/api/v1/movement",
    tags=["movement"]
)

# Crear movimiento
@router.post("/create", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def createMovement(request: CreateMovementRequest):
    movement = movementService.create(MovementMapper.createRequestToModel(request))
    return MovementMapper.modelToResponse(movement)

# Obtener todos los movimientos por ID de robot
@router.get("/all-by-robot/{robotId}", response_model=list[MovementResponse], dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def getAllMovementsByRobotId(robotId: int):
    movements = movementService.getAllByRobotId(robotId)
    return [MovementMapper.modelToResponse(movement) for movement in movements]

# Actualizar movimiento por ID
@router.put("/update/{movementId}", response_model=MovementResponse, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def updateMovementById(movementId: int, request: UpdateMovementRequest):
    movement = movementService.updateById(movementId, request.name)
    return MovementMapper.modelToResponse(movement)

# Eliminar movimiento por ID
@router.delete("/delete/{movementId}", response_model=bool, dependencies=[Depends(authorizeRoles([Role.USER, Role.ADMIN]))])
async def deleteMovementById(movementId: int):
    return movementService.deleteById(movementId)