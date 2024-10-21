from typing import List
from pydantic import BaseModel

class UpdatePositionRequest(BaseModel):
    delay: int
    angles: List[int]
