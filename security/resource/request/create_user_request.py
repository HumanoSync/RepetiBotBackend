from pydantic import BaseModel

from security.domain.model.user import Role

class CreateUserRequest(BaseModel):
    username: str
    password: str
    phone: str
    role: Role
