from fastapi import HTTPException
import abc
from pydantic import parse_obj_as

from dal.user import ABCUserDal
from logic.user import hash_password, generate_token
from dto.user import UserSummary, UserSign, UserAuth, UserEdit, User, UserPasswordCheck

from models.user import User as UserModel

from services.user_based_service import UserBasedService

from typing import List


class ABCUserService(UserBasedService):
    @abc.abstractmethod
    def get_all_users(self) -> List[UserAuth]:
        """Returns all users"""

    @abc.abstractmethod
    def save_user(self, user: UserSign) -> UserAuth:
        """Create a user"""

    @abc.abstractmethod
    def log_in_user(self, user: UserSign) -> UserAuth:
        """Logs in the user"""

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> UserSummary:
        """Return user with a given id"""


class UserService(ABCUserService):
    def __init__(
        self,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)

    def construct_user_dto(self, user: UserModel) -> User:
        return User(user_id=user.user_id, username=user.username, email=user.email)

    def get_all_users(self) -> List[UserAuth]:
        return parse_obj_as(List[UserAuth], self.user_dal.get_users())

    def save_user(self, user: UserSign) -> UserAuth:
        current_user = self.user_dal.get_user_by_email(user.email)

        if current_user:
            raise HTTPException(status_code=400, detail="Email is already in use")
        if user.email is None:
            raise HTTPException(status_code=400, detail="Email is necessary")
        if user.username is None:
            raise HTTPException(status_code=400, detail="Username is necessary")

        hashed_password = hash_password(user.password)
        token = generate_token()
        db_user = UserModel(
            email=user.email,
            hashed_password=hashed_password,
            username=user.username,
            token=token,
        )
        saved_user = self.user_dal.create_user(user=db_user)
        return UserAuth.from_orm(saved_user)

    def log_in_user(self, user: UserSign) -> UserAuth:
        current_user = self.user_dal.get_user_by_email(user.email)
        if current_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        hashed_password = hash_password(user.password)
        if hashed_password != current_user.hashed_password:
            raise HTTPException(status_code=403, detail="Wrong password")
        token = generate_token()
        db_user = UserModel(
            user_id=current_user.user_id,
            email=current_user.email,
            hashed_password=current_user.hashed_password,
            username=current_user.username,
            token=token,
        )
        logged_user = self.user_dal.update_user_auth(user=db_user)
        return UserAuth.from_orm(logged_user)

    def get_user_by_id(self, user_id: int) -> UserSummary:
        user = self.user_dal.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return UserSummary.from_orm(user)

    def edit_user(self, user_data: UserEdit) -> User:
        user = self.user_dal.get_user_by_email(user_data.email)
        if hash_password(user_data.old_password) != user.hashed_password:
            raise self.raise_access_denied_error()
        user.username = user_data.username
        user.password = hash_password(user_data.password)

        user = self.user_dal.update_user(user)

        return self.construct_user_dto(user)

    def delete_user(self, token: str, user_data: UserPasswordCheck) -> User:
        user = self.check_user_validity(token)
        if hash_password(user_data.password) != user.hashed_password:
            raise HTTPException(status_code=403, detail="Forbidden")
        self.user_dal.delete_user(user.user_id)
        return self.construct_user_dto(user)
