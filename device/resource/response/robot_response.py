from typing import List, Optional
from pydantic import BaseModel

class RobotResponse(BaseModel):
    id: Optional[int]
    token: Optional[str]
    botname: Optional[str]
    current_position: Optional[List[int]]
    initial_position: Optional[List[int]]
    is_connected_broker: Optional[bool]
