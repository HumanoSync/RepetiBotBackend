import json
from device.domain.model.robot import Robot
from device.resource.request.robot_request import CreateRobotRequest, UpdateRobotRequest
from device.resource.response.robot_response import RobotResponse, RobotResponseWithToken, RobotResponseWithoutPositions

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
                             is_connected_broker=robot.is_connected_broker)
    
    @staticmethod
    def modelToResponseWithToken(robot: Robot) -> RobotResponseWithToken:
        return RobotResponseWithToken(id=robot.id, 
                                      token=robot.token,
                                      botname=robot.botname, 
                                      current_position=json.loads(robot.current_position), 
                                      initial_position=json.loads(robot.initial_position), 
                                      is_connected_broker=robot.is_connected_broker)
    
    @staticmethod
    def modelToResponseWithoutPositions(robot: Robot) -> RobotResponse:
        return RobotResponseWithoutPositions(id=robot.id, 
                                             botname=robot.botname,
                                             is_connected_broker=robot.is_connected_broker)