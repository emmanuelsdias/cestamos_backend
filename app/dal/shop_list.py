import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update, and_

from models.shop_list import ShopList
from models.user_list import UserList
from models.item import Item

from typing import List

class ABCShopListDal():

    @abc.abstractmethod
    def get_shop_lists(self) -> List[ShopList]:
        """Gets all shop_lists in database"""

    @abc.abstractmethod
    def get_shop_lists_from_user(self, user_id) -> List[ShopList]:
        """Gets all shop_lists in database from a user """

    @abc.abstractmethod
    def get_shop_list_by_id(self, shop_list_id: int) -> ShopList:
        """Gets the shop_list in database with the given id"""

    @abc.abstractmethod
    def create_shop_list(self, shop_list: ShopList) -> ShopList:
        """Creates a new shop_list in database"""

    @abc.abstractmethod
    def update_list(self, shop_list: ShopList) -> ShopList:
        """ Updates list """

    @abc.abstractmethod
    def delete_shop_list(self, shop_list_id: int) -> ShopList:
        """Deletes list"""

class ShopListDal(ABCShopListDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_shop_lists(self) -> List[ShopList]:
        return self.db.query(ShopList).all()

    def get_shop_lists_from_user(self, user_id) -> List[ShopList]:
        user_lists = self.db.query(UserList).filter(UserList.user_id == user_id).all()
        shop_list_ids = [user_list.shop_list_id for user_list in user_lists]
        return self.db.query(ShopList).filter(ShopList.shop_list_id.in_(shop_list_ids)).all()

    def get_shop_list_by_id(self, shop_list_id: int) -> ShopList:
        return self.db.query(ShopList).filter(ShopList.shop_list_id == shop_list_id).first()

    def create_shop_list(self, shop_list: ShopList) -> ShopList:
        self.db.add(shop_list)
        self.db.commit()
        self.db.refresh(shop_list)
        return shop_list

    def update_list(self, shop_list: ShopList) -> ShopList:
        self.db.query(ShopList).filter(
            ShopList.shop_list_id == shop_list.shop_list_id
        ).\
            update(
                {
                    "name": shop_list.name,
                }
            )
        self.db.commit()
        return self.get_shop_list_by_id(shop_list.shop_list_id)

    def delete_shop_list(self, shop_list_id: int):
        deleted_shop_list = self.get_shop_list_by_id(shop_list_id)

        self.db.query(Item).filter(Item.shop_list_id == shop_list_id).\
            delete()
        self.db.query(UserList).filter(UserList.shop_list_id == shop_list_id).\
            delete()
        self.db.query(ShopList).filter(ShopList.shop_list_id == shop_list_id).\
            delete()
       
        self.db.commit()
        return deleted_shop_list
