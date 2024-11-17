from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
