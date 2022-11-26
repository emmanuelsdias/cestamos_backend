import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from app.dal.item import ABCItemDal
from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal

from app.dto.shop_list import Item, ItemEdit


from app.models.user import User as UserModel
from app.models.item import Item as ItemModel
from app.models.user_list import UserList as UserListModel

from app.services.user_based_service import UserBasedService

from typing import List


class ABCItemService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def edit_item(self, token: str, item_data: ItemEdit) -> Item:
        """ Returns invitations from user """

    @abc.abstractmethod
    def delete_item(self, token: str, item_id: int) -> Item:
        """ Deletes item """
    

class ItemService(ABCItemService):

    def __init__(
        self,
        user_dal: ABCUserDal,
        item_dal: ABCItemDal,
        shop_list_dal: ABCShopListDal,
    ):
        super().__init__(user_dal)
        self.dal = item_dal
        self.user_dal = user_dal
        self.shop_list_dal = shop_list_dal


    def construct_item_dto(self, item: ItemModel) -> Item:
        return Item(
            item_id = item.item_id,
            name = item.name,
            quantity = item.quantity,
            was_bought = item.was_bought
        )


    def check_user_list_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.shop_list_dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list is None:
            self.raise_access_denied_error()
        return user_list


    def check_user_list_adm_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.check_user_list_validity(user_id, shop_list_id)
        if not user_list.is_adm:
            self.raise_access_denied_error()
        return user_list


    def edit_item(self, token: str, item_data: ItemEdit) -> Item:
        user = self.check_user_validity(token)
        item = self.dal.get_item_by_id(item_data.item_id)

        if item is None:
            raise HTTPException(
                status_code=404, detail="Item doesn't exist"
            )

        self.check_user_list_validity(user.user_id, item.shop_list_id)

        item.name = item_data.name
        item.quantity = item_data.quantity
        item.was_bought = item_data.was_bought

        item = self.dal.update_item(item)

        return self.construct_item_dto(item)


    def delete_item(self, token: str, item_id: int) -> Item:
        user = self.check_user_validity(token)
        item = self.dal.get_item_by_id(item_id)
        if item is None:
            raise HTTPException(
                status_code=404, detail="Item doesn't exist"
            )
        
        self.check_user_list_adm_validity(user.user_id, item.shop_list_id)
        self.dal.delete_item(item.item_id)
        return self.construct_item_dto(item)

