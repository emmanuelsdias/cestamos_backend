from fastapi import APIRouter
from fastapi import Depends

from app.services.user import ABCUserService
from app.factories.user import get_user_service

from app.dto.user import User, UserCreate, UserAuth
from typing import List


router = APIRouter()

@router.get("/", response_model=List[UserAuth])
async def get_all_users(
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.get_all_users()

@router.post("/", response_model=UserAuth)
async def get_all_users(
    user: UserCreate,
    user_service: ABCUserService = Depends(get_user_service)
):
    return user_service.create_user(user)
