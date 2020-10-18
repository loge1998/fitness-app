from pydantic.main import BaseModel


class UserResponse(BaseModel):
    user_id: int
    username: str
    height: int
    weight: int
    age: int
    gender: str
