import json
from sqlalchemy import ARRAY
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from device.domain.model.movement import Movement
    from security.domain.model.user import User

class Robot(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    token: Optional[str] = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    botname: str = Field(nullable=False, sa_column_kwargs={"unique": True, "nullable": False})
    initial_position: str = Field(nullable=False)
    current_position: str = Field(nullable=False)
    is_connected_broker: Optional[bool] = Field(nullable=False, default=False)
    user_id: Optional[int] = Field(foreign_key="user.id", nullable=False)

    user: Optional["User"] = Relationship(back_populates="robots")
    movements: List["Movement"] = Relationship(back_populates="robot")