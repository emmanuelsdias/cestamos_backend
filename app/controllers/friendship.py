from fastapi import APIRouter
from fastapi import Depends

from services.friendship import ABCFriendshipService
from factories.friendship import get_friendship_service

from dto.friendship import Friendship
from typing import List


router = APIRouter()


@router.get("/", response_model=List[Friendship])
async def get_friendships(
    token: str = None,
    friendship_service: ABCFriendshipService = Depends(get_friendship_service),
):
    return friendship_service.get_friendships(token)


@router.delete("/{friendship_id}", response_model=Friendship)
async def delete_friendship(
    friendship_id: int,
    token: str = None,
    friendship_service: ABCFriendshipService = Depends(get_friendship_service),
):
    return friendship_service.delete_friendship(friendship_id, token)
