import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from app.dal.item import ABCItemDal
from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal

from app.dto.shop_list import Item, ItemEdit


from app.models.user import User as UserModel

from app.services.user_based_service import UserBasedService

from typing import List


class ABCItemService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def edit_item(self, token: str, item_data: ItemEdit) -> Item:
        """ Returns invitations from user """
    

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


    def edit_item(self, token: str, item_data: ItemEdit) -> Item:
        user = self.check_user_validity(token)

        return Item(
            item_id = 123,
            name = "aaaaa",
            quantity = "2 kg",
            was_bought = False,
        )
