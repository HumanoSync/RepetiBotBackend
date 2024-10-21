from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: Optional[int]
    username: Optional[str]
    phone: Optional[str]
    role: Optional[str]
