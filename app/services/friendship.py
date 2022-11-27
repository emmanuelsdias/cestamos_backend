import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from app.dal.friendship import ABCFriendshipDal
from app.dal.user import ABCUserDal

from app.dto.friendship import Friendship

from app.models.friendship import Friendship as FriendshipModel
from app.models.user import User as UserModel

from app.services.user_based_service import UserBasedService


from typing import List

class ABCFriendshipService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_friendships(self, token) -> List[Friendship]:
        """ Returns friendships from user """

    @abc.abstractmethod
    def delete_friendship(self, friendship_id: int, token: str) -> Friendship:
        """ Delete a friendship """


class FriendshipService(ABCFriendshipService):

    def __init__(
        self,
        friendship_dal: ABCFriendshipDal,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)
        self.dal = friendship_dal

    
    def construct_friendship_dto(self, user: UserModel, friendship: FriendshipModel) -> Friendship:
        if user.user_id == friendship.user_id1:
            user_friend = self.user_dal.get_user_by_id(friendship.user_id2)
        else:
            user_friend = self.user_dal.get_user_by_id(friendship.user_id1)
        
        friendship_dto = Friendship(
            friendship_id = friendship.friendship_id,
            user_id = user_friend.user_id,
            username = user_friend.username,
        )
        return friendship_dto


    def get_friendships(self, token) -> List[Friendship]:
        user = self.check_user_validity(token)
        friendships = self.dal.get_friendships_from_user(user.user_id)
        friendships_res = [self.construct_friendship_dto(user, friendship) for friendship in friendships]
        return friendships_res


    def delete_friendship(self, friendship_id: int, token: str) -> Friendship:
        user = self.check_user_validity(token)
        current_friendship = self.dal.get_friendship_by_id(friendship_id)
        if current_friendship is None:
            raise HTTPException(
                status_code=400, detail="Friendship doesn't exist"
            )
        if user.user_id not in [current_friendship.user_id1, current_friendship.user_id2]:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        deleted_friendship = self.dal.delete_friendship(friendship_id)
        
        return self.construct_friendship_dto(user, deleted_friendship)