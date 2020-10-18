from pydantic.main import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    age: Optional[int]
    gender: Optional[str]
