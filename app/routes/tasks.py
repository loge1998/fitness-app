from app.dto.task import Task
from fastapi import APIRouter

from app.dto.task_response import TaskResponse
from app.services.tasks import add_task, get_task_by_id

router = APIRouter()


@router.post("/tasks", tags=["task"], response_model=TaskResponse)
def create_user(payload: Task) -> TaskResponse:
    task = add_task(**vars(payload))
    return TaskResponse(**task)


@router.get("/tasks/{task_id}", tags=["task"], response_model=TaskResponse)
def create_user(task_id: int) -> TaskResponse:
    task = get_task_by_id(task_id)
    return TaskResponse(**task)



