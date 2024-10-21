from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from device.domain.model.robot import Robot

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    password: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    role: Role = Field(default=Role.USER)

    robots: List["Robot"] = Relationship(back_populates="user")

    