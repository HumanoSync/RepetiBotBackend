import json
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from device.domain.model.movement import Movement

class Position(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    sequence: Optional[int] = Field(nullable=False)
    delay: int = Field(nullable=False)
    angles: str = Field(nullable=False)
    movement_id: Optional[int] = Field(foreign_key="movement.id", nullable=False)

    movement: Optional["Movement"] = Relationship(back_populates="positions")