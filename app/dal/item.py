import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.item import Item

from typing import List

class ABCItemDal():

    @abc.abstractmethod
    def get_items(self) -> List[Item]:
        """Gets all items in database"""

    @abc.abstractmethod
    def get_items_from_list(self, shop_list_id: int) -> List[Item]:
        """Gets all items in database from a user """

    # @abc.abstractmethod
    # def get_item_by_id(self, item_id: int) -> Item:
    #     """Gets the item in database with the given id"""

    # @abc.abstractmethod
    # def create_item(self, item: Item) -> Item:
    #     """Creates a new item in database"""

    # @abc.abstractmethod
    # def update_item(self, item: Item) -> Item:
    #     """ Updates item in database """

    # @abc.abstractmethod
    # def delete_item(self, item_id: int) -> Item:
    #     """ Deletes a item in database """


class ItemDal(ABCItemDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_items(self) -> List[Item]:
        return self.db.query(Item).all()

    def get_items_from_list(self, shop_list_id: int) -> List[Item]:
        return self.db.query(Item).filter(Item.shop_list_id == shop_list_id).all()

    # def get_item_by_id(self, item_id: int) -> Item:
    #     return self.db.query(Item).filter(Item.item_id == item_id).first()

    