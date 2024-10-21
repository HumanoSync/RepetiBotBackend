from pydantic import BaseModel

class CreateMovementRequest(BaseModel):
    name: str
    robot_id: int
