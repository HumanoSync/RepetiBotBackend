from typing import Optional
from pydantic import BaseModel

class PositionResponse(BaseModel):
    id: Optional[int]
    sequence: Optional[int]
    delay: Optional[int]
    angles: Optional[str]
    movement_id: Optional[int]
