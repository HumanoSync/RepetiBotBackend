import json
from device.domain.model.robot import Robot
from device.resource.request.create_robot_request import CreateRobotRequest
from device.resource.request.update_robot_request import UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse

class RobotMapper:
    @staticmethod
    def createRequestToModel(request: CreateRobotRequest, currentUserId: int) -> Robot:
        return Robot(botname=request.botname, 
                     current_position=json.dumps(request.initial_position), 
                     initial_position=json.dumps(request.initial_position), 
                     user_id=currentUserId)

    @staticmethod
    def modelToResponse(robot: Robot) -> RobotResponse:
        return RobotResponse(id=robot.id, 
                             botname=robot.botname, 
                             current_position=json.loads(robot.current_position), 
                             initial_position=json.loads(robot.initial_position), 
                             is_connected_broker=robot.is_connected_broker, 
                             user_id=robot.id)
    
    @staticmethod
    def modelToResponseWithToken(robot: Robot) -> RobotResponse:
        return RobotResponse(id=robot.id, 
                             botname=robot.botname, 
                             token=robot.token,
                             current_position=json.loads(robot.current_position), 
                             initial_position=json.loads(robot.initial_position), 
                             is_connected_broker=robot.is_connected_broker, 
                             user_id=robot.id)
    
    @staticmethod
    def modelToResponseWithoutPositions(robot: Robot) -> RobotResponse:
        return RobotResponse(id=robot.id, 
                             botname=robot.botname,
                             is_connected_broker=robot.is_connected_broker, 
                             user_id=robot.id)