from pydantic import BaseModel

class UpdateRobotRequest(BaseModel):
    token: str
    botname: str
