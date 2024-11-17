from typing import Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    enabled: Optional[bool]
    role: Optional[str]

