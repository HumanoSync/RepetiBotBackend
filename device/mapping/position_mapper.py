import json
from device.domain.model.position import Position
from device.resource.request.create_position_request import CreatePositionRequest
from device.resource.request.update_position_request import UpdatePositionRequest
from device.resource.response.position_response import PositionResponse

class PositionMapper:
    @staticmethod
    def createRequestToModel(request: CreatePositionRequest) -> Position:
        return Position(delay=request.delay, 
                        angles=json.dumps(request.angles), 
                        movement_id=request.movement_id)
    
    @staticmethod
    def updateRequestToModel(request: UpdatePositionRequest) -> Position:
        return Position(delay=request.delay, 
                        angles=json.dumps(request.angles))
    
    @staticmethod
    def ModelToResponse(position: Position) -> PositionResponse:
        return PositionResponse(id=position.id, 
                                sequence=position.sequence, 
                                delay=position.delay, 
                                angles=json.loads(position.angles), 
                                movement_id=position.movement_id)
