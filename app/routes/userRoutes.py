from typing import Dict
from app.apis.user.crud import *
from app.apis.api_b.mainmod import main_func as main_func_b
from app.dto.userInput import UserInput
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/user/{userid}", tags=["user"], response_model=UserInput)
async def get_user(userid: int) -> Dict[str, int]:
    return


@router.post("/user", tags=["user"], response_model=UserInput)
def create_user(payload: UserInput) -> UserInput:
    return insert_user_to_db(payload)


@router.put("/user/{userid}", tags=["user"], response_model=UserInput)
def update_user(payload: UserInput) -> UserInput:
    pass


