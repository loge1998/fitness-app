from typing import Dict, List
from app.db.user_goals import get_all_goals, add_goals
from fastapi import APIRouter, Depends
from app.dto.goal_input import goalInput
from app.services.users import get_all_goals_for_username
from app.core.auth import get_current_user
router = APIRouter()


@router.get("/goals", tags=["goals"])
async def get_goals() -> List:
    return get_all_goals()


@router.post("/goals", tags=["goals"])
def set_goals(payload: goalInput):
    return add_goals(payload.goal)


@router.get("/user-goals", tags=["goals"])
def get_goals_of_an_user(current_user=Depends(get_current_user)):
    return get_all_goals_for_username(current_user['username'])