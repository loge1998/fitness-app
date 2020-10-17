from pydantic.main import BaseModel


class Task(BaseModel):
    title: str
    due_date: str
    is_completed: bool = False
