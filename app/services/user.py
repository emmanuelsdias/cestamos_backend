from fastapi import HTTPException
import abc
from pydantic import parse_obj_as

from app.dal.user import ABCUserDal
from app.logic.user import hash_password, generate_token
from app.dto.user import UserCreate, UserAuth

from app.models.user import User as UserModel

from app.utils.settings import Settings

from typing import List

class ABCUserService():
    @abc.abstractmethod
    def get_all_users(self) -> List[UserAuth]:
        """ Returns all users """
    
    @abc.abstractmethod
    def create_user(self, user) -> UserAuth:
        """ Create a user """


class UserService(ABCUserService):

    def __init__(
        self,
        user_dal: ABCUserDal,
    ):
        self.dal = user_dal

    def get_all_users(self) -> List[UserAuth]:
        return parse_obj_as(List[UserAuth], self.dal.get_users())

    def create_user(self, user: UserCreate) -> UserAuth:
        current_user = self.dal.get_user_by_email(user.email)
        if current_user:
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )
        hashed_password = hash_password(user.password)
        token = generate_token()
        db_user = UserModel(
            email=user.email, 
            hashed_password=hashed_password,
            username=user.username,
            token=token,
        )
        created_user = self.dal.create_user(user=db_user)
        return UserAuth.from_orm(created_user)