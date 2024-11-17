from pydantic import BaseModel

from security.domain.model.user import Role

class UpdateUserRequest(BaseModel):
    full_name: str
