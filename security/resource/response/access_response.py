from typing import Optional
from pydantic import BaseModel

from device.domain.model.robot import Robot
from security.domain.model.user import User

class AccessResponse(BaseModel):
    id: Optional[int]
    is_connected: Optional[bool]
    user_id: Optional[int]
    robot_id: Optional[int]
    
    user: Optional[User]
    robot: Optional[Robot]
