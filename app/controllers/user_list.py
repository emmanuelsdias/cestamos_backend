from fastapi import APIRouter
from fastapi import Depends

from services.user_list import ABCUserListService
from factories.user_list import get_user_list_service

from dto.shop_list import UserList, UserListStatus

router = APIRouter()


@router.put("/{user_list_id}", response_model=UserList)
async def change_user_status(
    user_list_id: int,
    user_list_status: UserListStatus,
    token: str = None,
    user_list_service: ABCUserListService = Depends(get_user_list_service)
):
    return user_list_service.change_user_status(user_list_id, user_list_status, token)


@router.delete("/{user_list_id}")
async def delete_user_list(
    user_list_id: int,
    token: str = None,
    user_list_service: ABCUserListService = Depends(get_user_list_service)
):
    return user_list_service.delete_user_list(user_list_id, token)
