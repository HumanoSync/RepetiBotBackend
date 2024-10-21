from typing import List
from pydantic import BaseModel

class CreateRobotRequest(BaseModel):
    botname: str
    initial_position: List[int]
