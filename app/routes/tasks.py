from app.dto.task import Task
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.dto.task_response import TaskResponse
from app.services.tasks import add_task, get_task_by_id, get_all_tasks_for_user
from typing import List

router = APIRouter()


@router.post("/tasks", tags=["task"], response_model=TaskResponse)
def add_task_to_db(payload: Task, current_user=Depends(get_current_user)) -> TaskResponse:
    username = current_user['username']  # This has to be passed from token
    task = add_task(**vars(payload), username=username)
    return TaskResponse(**task)


@router.get("/tasks", tags=["task"], response_model=List[TaskResponse])
def create_user(current_user=Depends(get_current_user)) -> List[TaskResponse]:
    username = current_user['username']  # This has to be passed from token
    tasks = get_all_tasks_for_user(username)
    return [TaskResponse(**task) for task in tasks]


@router.get("/tasks/{task_id}", tags=["task"], response_model=TaskResponse)
def create_user(task_id: int) -> TaskResponse:
    task = get_task_by_id(task_id)
    return TaskResponse(**task)



