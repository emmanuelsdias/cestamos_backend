import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.list import List
from app.models.user_list import UserList

from typing import List

class ABCListDal():

    @abc.abstractmethod
    def get_lists(self) -> List[List]:
        """Gets all lists in database"""

    @abc.abstractmethod
    def get_lists_from_user(self, user_id) -> List[List]:
        """Gets all lists in database from a user """

    @abc.abstractmethod
    def get_list_by_id(self, list_id: int) -> List:
        """Gets the list in database with the given id"""

    @abc.abstractmethod
    def create_list(self, list: List) -> List:
        """Creates a new list in database"""


class ListDal(ABCListDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_lists(self) -> List[List]:
        return self.db.query(List).all()

    def get_lists_from_user(self, user_id) -> List[List]:
        user_lists = self.db.query(UserList).filter(UserList.user_id == user_id)
        list_ids = [user_list.list_id for userlist in user_lists]
        return self.db.query(List).filter(List.list_id in list_ids).all()

    def get_list_by_id(self, list_id: int) -> List:
        return self.db.query(List).filter(List.list_id == list_id).first()

    def create_list(self, list: List) -> List:
        self.db.add(list)
        self.db.commit()
        self.db.refresh(list)
        return list

    