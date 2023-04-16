import abc
from fastapi import HTTPException

from dal.shop_list import ABCShopListDal
from dal.user import ABCUserDal
from dal.recipe_list import ABCRecipeListDal
from dal.user_list import ABCUserListDal

from dto.shop_list import UserList, UserListStatus

from models.user_list import UserList as UserListModel

from services.user_based_service import UserBasedService


from typing import List


class ABCUserListService(UserBasedService):
    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def change_user_status(
        self, user_list_id: int, new_user_list_status: UserListStatus, token: str
    ) -> UserList:
        """Changes user's status in list"""

    @abc.abstractmethod
    def delete_user_list(self, user_list_id: int, token: str) -> UserList:
        """Deletes user from list"""


class UserListService(ABCUserListService):
    def __init__(
        self,
        shop_list_dal: ABCShopListDal,
        user_list_dal: ABCUserListDal,
        user_dal: ABCUserDal,
        recipe_list_dal: ABCRecipeListDal,
    ):
        super().__init__(user_dal)
        self.user_dal = user_dal
        self.shop_list_dal = shop_list_dal
        self.recipe_list_dal = recipe_list_dal
        self.dal = user_list_dal

    def construct_user_list_dto(self, user_list: UserListModel) -> UserList:
        user = self.user_dal.get_user_by_id(user_list.user_id)
        user_list_dto = UserList(
            user_id=user.user_id,
            username=user.username,
            is_adm=user_list.is_adm,
            is_nutritionist=user_list.is_nutritionist,
            user_list_id=user_list.user_list_id,
        )
        return user_list_dto

    def check_user_list_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list is None:
            self.raise_access_denied_error()
        return user_list

    def check_user_list_adm_validity(
        self, user_id: int, shop_list_id: int
    ) -> UserListModel:
        user_list = self.check_user_list_validity(user_id, shop_list_id)
        if not user_list.is_adm:
            self.raise_access_denied_error()
        return user_list

    def change_user_status(
        self, user_list_id: int, new_user_list_status: UserListStatus, token: str
    ) -> UserList:
        user = self.check_user_validity(token)
        target_user_list = self.dal.get_user_list_by_user_list_id(user_list_id)
        if target_user_list is None:
            raise HTTPException(status_code=404, detail="User List doesn't exist")

        self.check_user_list_adm_validity(user.user_id, target_user_list.shop_list_id)

        if new_user_list_status.is_adm is not None:
            target_user_list.is_adm = new_user_list_status.is_adm

        if new_user_list_status.is_nutritionist is not None:
            if new_user_list_status.is_nutritionist:
                # check if there is nutritionist
                there_is_nutritionist = False
                current_user_lists = self.dal.get_user_lists_by_shop_list_id(
                    target_user_list.shop_list_id
                )
                for current_user_list in current_user_lists:
                    if (
                        current_user_list.is_nutritionist
                        and current_user_list.user_id != target_user_list.user_id
                    ):
                        there_is_nutritionist = True
                        break
                if there_is_nutritionist:
                    raise HTTPException(
                        status_code=400, detail="There is already a nutritionist"
                    )
            elif target_user_list.is_nutritionist:
                # delete all recipes from list
                self.recipe_list_dal.delete_recipe_lists_by_shop_list_id(
                    target_user_list.shop_list_id
                )

            target_user_list.is_nutritionist = new_user_list_status.is_nutritionist
        updated_user_list = self.dal.update_user_list(target_user_list)
        return self.construct_user_list_dto(updated_user_list)

    def delete_user_list(self, user_list_id: int, token: str) -> UserList:
        user = self.check_user_validity(token)
        user_list = self.dal.get_user_list_by_user_list_id(user_list_id)
        if user_list is None:
            raise HTTPException(status_code=404, detail="User List doesn't exist")
        if user.user_id == user_list.user_id:
            users_from_same_list = self.dal.get_user_lists_by_shop_list_id(
                user_list.shop_list_id
            )
            if len(users_from_same_list) == 1:
                self.shop_list_dal.delete_shop_list(user_list.shop_list_id)
            else:
                self.dal.delete_user_list(user_list.user_list_id)
        else:
            self.check_user_list_adm_validity(user.user_id, user_list.shop_list_id)
            self.dal.delete_user_list(user_list.user_list_id)
        return self.construct_user_list_dto(user_list)
