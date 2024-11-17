from typing import Optional
from pydantic import BaseModel

class MovementResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]
