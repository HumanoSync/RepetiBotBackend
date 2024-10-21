from device.domain.model.movement import Movement
from device.resource.request.create_movement_request import CreateMovementRequest
from device.resource.request.update_movement_request import UpdateMovementRequest
from device.resource.response.movement_response import MovementResponse

class MovementMapper:
    @staticmethod
    def createRequestToModel(request: CreateMovementRequest) -> Movement:
        return Movement(name=request.name, robot_id=request.robot_id)
    
    @staticmethod
    def updateRequestToModel(request: UpdateMovementRequest) -> Movement:
        return Movement(name=request.name)
    
    @staticmethod
    def modelToResponse(request: Movement) -> MovementResponse:
        return Movement(id=request.id, name=request.name, robot_id=request.robot_id)
