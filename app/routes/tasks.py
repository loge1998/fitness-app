from app.dto.task import Task
from fastapi import APIRouter

from app.dto.task_response import TaskResponse
from app.services.tasks import add_task, get_task_by_id, get_all_tasks_for_user
from typing import List

router = APIRouter()


@router.post("/tasks", tags=["task"], response_model=TaskResponse)
def create_user(payload: Task) -> TaskResponse:
    username = ''  # This has to be passed from token
    task = add_task(**vars(payload), username=username)
    return TaskResponse(**task)


@router.get("/tasks", tags=["task"], response_model=List[TaskResponse])
def create_user() -> List[TaskResponse]:
    username = '' # This has to be passed from token
    tasks = get_all_tasks_for_user(username)
    return [TaskResponse(**task) for task in tasks]


@router.get("/tasks/{task_id}", tags=["task"], response_model=TaskResponse)
def create_user(task_id: int) -> TaskResponse:
    task = get_task_by_id(task_id)
    return TaskResponse(**task)



