from pydantic.main import BaseModel


class TaskResponse(BaseModel):
    task_id: int
    title: str
    due_date: str
    is_completed: bool
