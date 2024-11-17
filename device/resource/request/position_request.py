from typing import List
from pydantic import BaseModel

class CreatePositionRequest(BaseModel):
    delay: int
    angles: List[int]
    movement_id: int

class UpdatePositionRequest(BaseModel):
    delay: int
    angles: List[int]
