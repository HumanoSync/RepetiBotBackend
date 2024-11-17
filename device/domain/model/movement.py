from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Relationship

if TYPE_CHECKING:
    from device.domain.model.robot import Robot
    from device.domain.model.position import Position

class Movement(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    robot_id: Optional[int] = Field(foreign_key="robot.id", nullable=False)
    
    robot: Optional["Robot"] = Relationship(back_populates="movements")
    positions: List["Position"] = Relationship(back_populates="movement")