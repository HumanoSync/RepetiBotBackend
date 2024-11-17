from typing import List
from pydantic import BaseModel

class CreateRobotRequest(BaseModel):
    botname: str
    initial_position: List[int]

class UpdateRobotRequest(BaseModel):
    token: str
    botname: str
    
class UpdateInitialPositionRequest(BaseModel):
    initial_position: List[int]

class UpdateCurrentPositionRequest(BaseModel):
    current_position: List[int]

