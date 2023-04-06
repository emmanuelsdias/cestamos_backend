from fastapi import Depends

from dal.friendship import ABCFriendshipDal
from dal.user import ABCUserDal
from factories.dal_factories import get_user_dal, get_friendship_dal
from services.friendship import ABCFriendshipService, FriendshipService


def get_friendship_service(
    friendship_dal: ABCFriendshipDal = Depends(get_friendship_dal),
    user_dal: ABCUserDal = Depends(get_user_dal),
) -> ABCFriendshipService:
    client = FriendshipService(friendship_dal, user_dal)
    try:
        yield client
    finally:
        pass
