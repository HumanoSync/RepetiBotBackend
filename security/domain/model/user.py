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
    email: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})  # Email único e indexado
    full_name: str = Field(nullable=False)  # Nombre completo
    hashed_password: str = Field(nullable=False)  # Contraseña hasheada
    enabled: Optional[bool] = Field(default=False)  # Estado de deshabilitado
    role: Optional[Role] = Field(default=Role.USER)

    robots: List["Robot"] = Relationship(back_populates="user")