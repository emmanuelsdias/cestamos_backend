from fastapi import HTTPException
import abc
from pydantic import parse_obj_as

from app.dal.user import ABCUserDal
from app.logic.user import hash_password, generate_token
from app.dto.user import UserSummary, UserCreate, UserAuth

from app.models.user import User as UserModel

from typing import List


class ABCUserService():
    @abc.abstractmethod
    def get_all_users(self) -> List[UserAuth]:
        """ Returns all users """
    
    @abc.abstractmethod
    def save_user(self, user) -> UserAuth:
        """ Create a user or logs in the user """
    
    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> UserSummary:
        """ Return user with a given id """


class UserService(ABCUserService):

    def __init__(
        self,
        user_dal: ABCUserDal,
    ):
        self.dal = user_dal

    def get_all_users(self) -> List[UserAuth]:
        return parse_obj_as(List[UserAuth], self.dal.get_users())

    def save_user(self, user: UserCreate) -> UserAuth:
        current_user = self.dal.get_user_by_email(user.email)
        hashed_password = hash_password(user.password)
        token = generate_token()
        
        if current_user:
            if current_user.hashed_password != hashed_password:
                raise HTTPException(
                    status_code=403, detail="Wrong password"
                )
            db_user = current_user
            db_user.token = token
            saved_user = self.dal.update_user_auth(db_user)
            return UserAuth.from_orm(saved_user)

        if user.username is None:
            raise HTTPException(
                status_code=400, detail="Username is necessary"
            )
        db_user = UserModel(
            email=user.email, 
            hashed_password=hashed_password,
            username=user.username,
            token=token,
        )
        saved_user = self.dal.create_user(user=db_user)
        return UserAuth.from_orm(saved_user)

    def get_user_by_id(self, user_id: int) -> UserSummary:
        user = self.dal.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        return UserSummary.from_orm(user)
