from fastapi import HTTPException
import abc
from pydantic import parse_obj_as

from app.dal.user import ABCUserDal
from app.logic.user import hash_password
from app.dto.user import User, UserCreate

from app.models.user import User as UserModel

from app.utils.settings import Settings

from typing import List

class ABCUserService():
    @abc.abstractmethod
    def get_all_users(self) -> List[User]:
        """ Returns all users """
    
    @abc.abstractmethod
    def create_user(self, user) -> User:
        """ Create a user """


class UserService(ABCUserService):

    def __init__(
        self,
        user_dal: ABCUserDal,
    ):
        self.dal = user_dal

    def get_all_users(self, limit: int = 100) -> List[User]:
        return parse_obj_as(List[User], self.dal.get_users(limit))

    def create_user(self, user: UserCreate) -> User:
        current_user = self.dal.get_user_by_email(user.email)
        if current_user:
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )
        hashed_password = hash_password(user.password)
        db_user = UserModel(
            email=user.email, 
            hashed_password=hashed_password,
            username=user.username,
        )
        created_user = self.dal.create_user(user=db_user)
        return User.from_orm(created_user)