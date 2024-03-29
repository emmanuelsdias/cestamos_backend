from fastapi import APIRouter
from fastapi import Depends

from services.user import ABCUserService
from factories.user import get_user_service

from dto.user import User, UserSign, UserAuth, UserEdit, UserPasswordCheck
from typing import List


router = APIRouter()


@router.get("/", response_model=List[UserAuth])
async def get_all_users(user_service: ABCUserService = Depends(get_user_service)):
    return user_service.get_all_users()


@router.post("/", response_model=UserAuth)
async def sign_user(
    user: UserSign, user_service: ABCUserService = Depends(get_user_service)
):
    return (
        user_service.save_user(user) if user.new_user else user_service.log_in_user(user)
    )


@router.put("/", response_model=User)
async def edit_user(
    user_data: UserEdit,
    user_service: ABCUserService = Depends(get_user_service),
):
    return user_service.edit_user(user_data)


@router.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: int,
    user_data: UserPasswordCheck,
    token: str = None,
    user_service: ABCUserService = Depends(get_user_service),
):
    return user_service.delete_user(user_id, token, user_data)
