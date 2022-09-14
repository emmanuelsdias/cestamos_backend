import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal
from app.dal.friendship import ABCFriendshipDal

from app.dto.shop_list import ShopList, ShopListCreate, ShopListSummary, UserList

from app.models.shop_list import ShopList as ShopListModel
from app.models.user_list import UserList as UserListModel
from app.models.user import User as UserModel

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



class ShopListService(ABCShopListService):

    def __init__(
        self,
        shop_list_dal: ABCShopListDal,
        friendship_dal: ABCFriendshipDal,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)
        self.friendship_dal = friendship_dal
        self.dal = shop_list_dal


    def construct_user_list_dto(self, user_id, shop_list_id):
        user = self.user_dal.get_user_by_id(user_id)
        user_list = self.dal.get_user_list_by_user_id(shop_list_id, user_id)
        user_list_dto = UserList(
            user_id = user_id,
            username = user.username,
            is_adm = user_list.is_adm,
            is_nutritionist = user_list.is_nutritionist
        )
        return user_list_dto


    def construct_shop_list_summary_dto(self, shop_list: ShopListModel) -> ShopListSummary:
        user_lists = self.dal.get_user_lists_by_shop_list_id(shop_list.shop_list_id)
        user_lists_dto = [
            UserList(
                user_id = user_list.user_id,
                username = self.user_dal.get_user_by_id(user_list.user_id).username,
                is_adm = user_list.is_adm,
                is_nutritionist = user_list.is_nutritionist
            ) for user_list in user_lists
        ]

        shop_list_summary = ShopListSummary(
            shop_list_id = shop_list.shop_list_id,
            name = shop_list.name,
            user_lists = user_lists_dto
        )

        return shop_list_summary


    def get_shop_lists(self, token) -> List[ShopListSummary]:
        user = self.check_user_validity(token)
        shop_lists = self.dal.get_shop_lists_from_user(user.user_id)
        shop_lists_dto = [self.construct_shop_list_summary_dto(shop_list) for shop_list in shop_lists]
        return shop_lists_dto


    def get_shop_list_by_id(self, shop_list_id: int, token: str) -> ShopList:
        user = self.check_user_validity(token)

        shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if user.user_id != shop_list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        return parse_obj_as(ShopList, self.dal.get_shop_list_by_id(shop_list_id))

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
            self.dal.create_user_list(shop_list_id, user_list_db)

        user_list_db = UserListModel(
            user_id = user.user_id,
            shop_list_id = shop_list_id,
            is_adm = True
        )
        self.dal.create_user_list(shop_list_id, user_list_db)  
        
        created_shop_list_dto = self.construct_shop_list_summary_dto(created_shop_list)
        return created_shop_list_dto
    


    def update_shop_list(self, shop_list_id: int, shop_list: ShopListCreate, token: str) -> ShopList:
        user = self.check_user_validity(token)
        current_shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if current_shop_list is None:
            raise HTTPException(
                status_code=400, detail="ShopList doesn't exist"
            )
        if user.user_id != current_shop_list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        db_shop_list = ShopListModel(
            shop_list_id=shop_list_id,
            name = shop_list.name,
            ingredients=shop_list.ingredients,
            instructions=shop_list.instructions,
        )
        saved_shop_list = self.dal.update_shop_list(db_shop_list)
        return ShopList.from_orm(saved_shop_list)

    def delete_shop_list(self, shop_list_id: int, token: str) -> ShopList:
        user = self.check_user_validity(token)
        current_shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if current_shop_list is None:
            raise HTTPException(
                status_code=400, detail="ShopList doesn't exist"
            )
        if user.user_id != current_shop_list.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        deleted_shop_list = self.dal.delete_shop_list(shop_list_id)
        return ShopList.from_orm(deleted_shop_list)