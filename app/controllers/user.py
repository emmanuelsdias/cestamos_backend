from fastapi import APIRouter
from fastapi import Depends

from app.services.user import ABCUserService
from app.factories.user import get_user_service

from app.dto.user import User, UserCreate, UserAuth, UserEdit, UserPasswordCheck
from typing import List


router = APIRouter()

@router.get("/", response_model=List[UserAuth])
async def get_all_users(
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.get_all_users()

@router.post("/", response_model=UserAuth)
async def save_user(
    user: UserCreate,
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.save_user(user)

@router.put("/", response_model = User)
async def edit_user(
    user_data: UserEdit,
    token: str = None,
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.edit_user(token, user_data)

@router.delete("/", response_model = User)
async def delete_user(
    user_data: UserPasswordCheck,
    token: str = None,
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.delete_user(token, user_data)