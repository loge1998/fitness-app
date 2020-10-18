from typing import Dict
from pydantic.main import BaseModel


class UserInput(BaseModel):
    username: str
    password: str
    height: int
    weight: int
    age: int
    gender: str
    goals: Dict[int, int]
