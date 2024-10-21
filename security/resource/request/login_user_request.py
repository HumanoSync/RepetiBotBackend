from pydantic import BaseModel

class LoginUserRequest(BaseModel):
    username: str
    password: str# Permite que el rol se especifique opcionalmente
