from typing import List, Optional
from pydantic import BaseModel

class RobotResponse(BaseModel):
    id: int
    botname: str
    current_position: List[int]
    initial_position: List[int]
    is_connected_broker: bool

class RobotResponseWithToken(BaseModel):
    id: int
    token: str
    botname: str
    current_position: List[int]
    initial_position: List[int]
    is_connected_broker: bool

class RobotResponseWithoutPositions(BaseModel):
    id: int
    botname: str
    is_connected_broker: bool