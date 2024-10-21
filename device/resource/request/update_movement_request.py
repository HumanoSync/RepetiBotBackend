from pydantic import BaseModel

class UpdateMovementRequest(BaseModel):
    name: str

