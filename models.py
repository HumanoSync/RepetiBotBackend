from dataclasses import dataclass

@dataclass
class Role:
    id: int
    name: str
@dataclass
class User:
    id: int
    name: str
    role_id: int

@dataclass
class UserRobot:
    id: int
    user_id: int
    robot_id: int

@dataclass
class Robot:
    id: int
    name: str

@dataclass
class InitialPosition:
    id: int
    time: int
    angles: list
    robot_id: int

@dataclass
class Movement:
    id: int
    name: str
    robot_id: int

@dataclass
class Position:
    id: int
    order:int
    time: int
    angles: list
    movement_id: int

@dataclass
class Button:
    id: int
    state: bool
    robot_id: int

@dataclass
class Servo:
    id: int
    angle: int
    robot_id: int