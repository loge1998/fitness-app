from app.dto.user_input import UserInput
from app.dto.user_response import UserResponse
from app.dto.user_update import UserUpdate
from app.core.auth import *
from app.services.users import *
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/user", tags=["user"], response_model=UserResponse)
def get_user_details(current_user=Depends(get_current_user)):
    return current_user


@router.post("/user/signup", tags=["user"], response_model=UserResponse, status_code=201)
def create_user(user: UserInput):
    if check_if_username_present(user.username):
        response = {
            "error": "auth-0001",
            "message": "Username already exist"
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response
        )
    return signup_user(**vars(user))


@router.put("/user", tags=["user"], response_model=UserResponse, status_code=201)
def update_user(user: UserUpdate, current_user=Depends(get_current_user)):
    db_user_details = current_user
    if not db_user_details:
        response = {
            "error": "auth-0002",
            "message": "Username does not exist"
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response
        )

    return update_user_details(db_user_details['user_id'], **vars(user))





