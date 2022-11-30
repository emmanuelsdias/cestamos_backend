import abc
from fastapi import HTTPException

from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal
from app.dal.user_list import ABCUserListDal

from app.dto.shop_list import UserList, UserListStatus

from app.models.user_list import UserList as UserListModel

from app.services.user_based_service import UserBasedService


from typing import List

class ABCUserListService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def change_user_status(self, user_list_id: int, user_list_status: UserListStatus, token: str) -> UserList:
        """ Changes user's status in list """

    @abc.abstractmethod
    def delete_user_list(self, user_list_id: int, token: str) -> UserList:
        """ Deletes user from list """



class UserListService(ABCUserListService):

    def __init__(
        self,
        shop_list_dal: ABCShopListDal,
        user_list_dal: ABCUserListDal,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)
        self.user_dal = user_dal
        self.shop_list_dal = shop_list_dal
        self.dal = user_list_dal

    def construct_user_list_dto(self, user_list: UserListModel) -> UserList:
        user = self.user_dal.get_user_by_id(user_list.user_id)
        user_list_dto = UserList(
            user_id = user.user_id,
            username = user.username,
            is_adm = user_list.is_adm,
            is_nutritionist = user_list.is_nutritionist,
            user_list_id = user_list.user_list_id,
        )
        return user_list_dto

    def check_user_list_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list is None:
            self.raise_access_denied_error()
        return user_list

    def check_user_list_adm_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.check_user_list_validity(user_id, shop_list_id)
        if not user_list.is_adm:
            self.raise_access_denied_error()
        return user_list

    def change_user_status(self, user_list_id: int, user_list_status: UserListStatus, token: str) -> UserList:
        user = self.check_user_validity(token)
        user_list = self.dal.get_user_list_by_user_list_id(user_list_id)
        if user_list is None:
            raise HTTPException(
                status_code=404, detail="User List doesn't exist"
            )
        self.check_user_list_adm_validity(user.user_id, user_list.shop_list_id)
        if user_list_status.is_adm is not None:
            if user.user_id != user_list.user_id:
                user_list.is_adm = user_list_status.is_adm
        if user_list_status.is_nutritionist is not None:
            user_list.is_nutritionist = user_list_status.is_nutritionist
        updated_user_list = self.dal.update_user_list(user_list)
        return self.construct_user_list_dto(updated_user_list)

    def delete_user_list(self, user_list_id: int, token: str) -> UserList:
        user = self.check_user_validity(token)
        user_list = self.dal.get_user_list_by_user_list_id(user_list_id)
        if user_list is None:
            raise HTTPException(
                status_code=404, detail="User List doesn't exist"
            )
        if user.user_id == user_list.user_id:
            users_from_same_list = self.dal.get_user_lists_by_shop_list_id(user_list.shop_list_id)
            if len(users_from_same_list) == 1:
                self.shop_list_dal.delete_shop_list(user_list.shop_list_id)
        else:
            self.check_user_list_adm_validity(user.user_id, user_list.shop_list_id)
            self.dal.delete_user_list(user_list.user_list_id)
        return self.construct_user_list_dto(user_list)
