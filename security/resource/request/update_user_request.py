from pydantic import BaseModel

from security.domain.model.user import Role

class UpdateUserRequest(BaseModel):
    username: str
    password: str
    phone: str
    role: Role
