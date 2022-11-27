import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal
from app.dal.friendship import ABCFriendshipDal
from app.dal.item import ABCItemDal
from app.dal.user_list import ABCUserListDal

from app.dto.shop_list import ShopList, ShopListCreate, ShopListSummary, ShopListEdit
from app.dto.shop_list import UserList, UserListCreate
from app.dto.shop_list import Item, ItemCreate

from app.models.shop_list import ShopList as ShopListModel
from app.models.user_list import UserList as UserListModel
from app.models.user import User as UserModel
from app.models.item import Item as ItemModel

from app.services.user_based_service import UserBasedService


from typing import List

class ABCShopListService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_shop_lists(self, token) -> List[ShopListSummary]:
        """ Returns shop lists from user """
    
    @abc.abstractmethod
    def get_shop_list_by_id(self, shop_list_id) -> ShopList:
        """ Return the shop list with given id """

    @abc.abstractmethod
    def create_shop_list(self, shop_list: ShopListCreate, token: str) -> ShopList:
        """ Create a shop list """

    @abc.abstractmethod
    def add_users_to_list(self, shop_list_id: int, user_lists: List[UserListCreate], token: str) -> List[UserList]:
        """ Adds users to list """

    @abc.abstractmethod
    def change_user_status(shop_list_id: int, user_id: int, user_list_status, token: str) -> UserList:
        """ Set user to adm or to nutritionist """
    
    @abc.abstractmethod
    def add_item_to_list(self, shop_list_id: int, item: ItemCreate, token: str) -> ShopList:
        """ Adds item to list and return the resulting list """

    @abc.abstractmethod
    def rename_list(self, shop_list_id: int, new_name: str, token: str) -> ShopList:
        """ Renames list """

    @abc.abstractmethod
    def delete_list(self, shop_list_id: int, token: str) -> ShopListSummary:
        """ Deletes list """



class ShopListService(ABCShopListService):

    def __init__(
        self,
        shop_list_dal: ABCShopListDal,
        friendship_dal: ABCFriendshipDal,
        item_dal: ABCItemDal,
        user_dal: ABCUserDal,
        user_list_dal: ABCUserListDal
    ):
        super().__init__(user_dal)
        self.friendship_dal = friendship_dal
        self.item_dal = item_dal
        self.user_list_dal = user_list_dal
        self.dal = shop_list_dal


    def construct_user_list_dto(self, user_list: UserListModel) -> UserList:
        user = self.user_dal.get_user_by_id(user_list.user_id)
        user_list_dto = UserList(
            user_id = user.user_id,
            username = user.username,
            is_adm = user_list.is_adm,
            is_nutritionist = user_list.is_nutritionist
        )
        return user_list_dto


    def construct_shop_list_summary_dto(self, shop_list: ShopListModel) -> ShopListSummary:
        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list.shop_list_id)
        user_lists_dto = [
            self.construct_user_list_dto(user_list) for user_list in user_lists
        ]

        shop_list_summary = ShopListSummary(
            shop_list_id = shop_list.shop_list_id,
            name = shop_list.name,
            user_lists = user_lists_dto
        )

        return shop_list_summary


    def construct_shop_list_dto(self, shop_list: ShopListModel) -> ShopList:
        shop_list_summary = self.construct_shop_list_summary_dto(shop_list)

        items = self.item_dal.get_items_from_list(shop_list.shop_list_id)

        items_dto = [
            Item(
                item_id = item.item_id,
                name = item.name,
                quantity = item.quantity,
                was_bought = item.was_bought
            )
            for item in items
        ]

        shop_list_dto = ShopList(
            shop_list_id = shop_list.shop_list_id,
            name = shop_list_summary.name,
            user_lists = shop_list_summary.user_lists,
            items = items_dto
        )

        return shop_list_dto



    def check_user_list_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.user_list_dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list is None:
            self.raise_access_denied_error()
        return user_list

    def check_user_list_adm_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.check_user_list_validity(user_id, shop_list_id)
        if not user_list.is_adm:
            self.raise_access_denied_error()
        return user_list


    def get_shop_lists(self, token) -> List[ShopListSummary]:
        user = self.check_user_validity(token)
        shop_lists = self.dal.get_shop_lists_from_user(user.user_id)
        shop_lists_dto = [self.construct_shop_list_summary_dto(shop_list) for shop_list in shop_lists]
        return shop_lists_dto


    def get_shop_list_by_id(self, shop_list_id: int, token: str) -> ShopList:
        user = self.check_user_validity(token)

        shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list_id)

        if not (user.user_id in [u.user_id for u in user_lists]):
            self.raise_access_denied_error()

        items = self.item_dal.get_items_from_list(shop_list_id)
        items_dto = parse_obj_as(List[Item], items)
        shop_list_dto = ShopList(
            shop_list_id = shop_list_id,
            name = shop_list.name,
            user_lists = [self.construct_user_list_dto(user_list) for user_list in user_lists],
            items = items_dto
        )
        
        return shop_list_dto


    def create_shop_list(self, shop_list: ShopListCreate, token: str) -> ShopList:
        user = self.check_user_validity(token)
        
        db_shop_list = ShopListModel(
            name = shop_list.name,
            is_template = shop_list.is_template,
        )
        invited_user_ids = [id for id in shop_list.user_ids if id != user.user_id]
        
        for invited_user_id in invited_user_ids:
            friendship = self.friendship_dal.get_friendship_from_user_pair(user.user_id, invited_user_id)
            if friendship is None:
                raise HTTPException(
                    status_code=400, detail="Friendship necessary"
                )

        created_shop_list = self.dal.create_shop_list(shop_list=db_shop_list)

        shop_list_id = created_shop_list.shop_list_id
        for user_id in invited_user_ids:
            user_list_db = UserListModel(
                user_id = user_id,
                shop_list_id = shop_list_id
            )
            self.dal.create_user_list(user_list_db)

        user_list_db = UserListModel(
            user_id = user.user_id,
            shop_list_id = shop_list_id,
            is_adm = True
        )
        self.dal.create_user_list(user_list_db)  
        
        created_shop_list_dto = self.construct_shop_list_summary_dto(created_shop_list)
        return created_shop_list_dto
    

    def add_users_to_list(self, shop_list_id: int, user_lists: List[UserListCreate], token: str) -> List[UserList]:
        user = self.check_user_validity(token)
        self.check_user_list_adm_validity(user.user_id, shop_list_id)
        current_user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list_id)
        current_user_list_ids = [u.user_id for u in current_user_lists]

        for user_list in user_lists:
            if not self.friendship_dal.get_friendship_from_user_pair(user.user_id, user_list.user_id):
                continue
            if user_list.user_id in current_user_list_ids:
                continue
            user_list_db = UserListModel(
                user_id = user_list.user_id,
                shop_list_id = shop_list_id,
                is_nutritionist = user_list.is_nutritionist
            )
            self.dal.create_user_list(user_list_db)
        
        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list_id)

        user_lists_dto = [
            self.construct_user_list_dto(user_list) for user_list in user_lists
        ]

        return user_lists_dto

    
    def change_user_status(self, shop_list_id: int, user_id: int, user_list_status, token: str) -> UserList:
        user = self.check_user_validity(token)
        request_user_list = self.check_user_list_adm_validity(user.user_id, shop_list_id)

        user_list = self.user_list_dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list_status.is_adm is not None:
            if request_user_list.user_id != user_list.user_id:
                user_list.is_adm = user_list_status.is_adm
        if user_list_status.is_nutritionist is not None:
            user_list.is_nutritionist = user_list_status.is_nutritionist

        updated_user_list = self.dal.update_user_list(user_list)
        return self.construct_user_list_dto(updated_user_list)


    def add_item_to_list(self, shop_list_id: int, item: ItemCreate, token: str) -> ShopList:
        user = self.check_user_validity(token)
        self.check_user_list_adm_validity(user.user_id, shop_list_id)
        item_db = ItemModel(
            shop_list_id = shop_list_id,
            name = item.name,
            quantity = item.quantity
        )
        self.item_dal.create_item(item_db)
        
        return self.get_shop_list_by_id(shop_list_id, token)

    def delete_shop_list(self, shop_list_id: int, token: str) -> ShopList:
        user = self.check_user_validity(token)
        current_shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if current_shop_list is None:
            raise HTTPException(
                status_code=400, detail="ShopList doesn't exist"
            )
        if user.user_id != current_shop_list.user_id:
            self.raise_access_denied_error()
        deleted_shop_list = self.dal.delete_shop_list(shop_list_id)
        return ShopList.from_orm(deleted_shop_list)

    def rename_list(self, shop_list_id: int, shop_list_data: ShopListEdit, token: str) -> ShopListSummary:
        user = self.check_user_validity(token)
        shop_list = self.dal.get_shop_list_by_id(shop_list_id)

        if shop_list is None:
            raise HTTPException(
                status_code=404, detail="ShopList doesn't exist"
            )

        self.check_user_list_validity(user.user_id, shop_list_id)
        
        shop_list.name = shop_list_data.name
        shop_list = self.dal.update_list(shop_list)

        return self.construct_shop_list_summary_dto(shop_list)


    def delete_list(self, shop_list_id: int, token: str) -> ShopListSummary:
        user = self.check_user_validity(token)
        shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if shop_list is None:
            raise HTTPException(
                status_code=404, detail="ShopList doesn't exist"
            )
        
        self.check_user_list_adm_validity(user.user_id, shop_list_id)

        # TODO: Deletar todos os itens que pertencem à lista
        # TODO: Deletar todos os user_lists que pertencem à lista
        # TODO: Deletar a lista

        return self.construct_shop_list_summary_dto(shop_list)

