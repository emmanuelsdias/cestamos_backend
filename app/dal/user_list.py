import abc
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.user_list import UserList

from typing import List

class ABCUserListDal():

    @abc.abstractmethod
    def get_user_list_by_user_id(self, shop_list_id: int, user_id: int) -> UserList:
        """Gets the user_list in database with the given id"""

    @abc.abstractmethod
    def get_user_list_by_user_list_id(self, user_list_id: int) -> UserList:
        """Gets the user_list in database with the given id"""

    @abc.abstractmethod
    def get_user_lists_by_shop_list_id(self, shop_list_id: int) -> List[UserList]:
        """ Get users from list """

    @abc.abstractmethod
    def update_user_list(self, user_list: UserList) -> UserList:
        """ Updates user list """

    @abc.abstractmethod
    def delete_user_list(self, user_list_id: int) -> UserList:
        """ Deletes user list """


class UserListDal(ABCUserListDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_user_list_by_user_id(self, shop_list_id: int, user_id: int) -> UserList:
        user_list = self.db.query(UserList).filter(
            and_(
                UserList.shop_list_id == shop_list_id,
                UserList.user_id == user_id
            )
        ).first()
        return user_list

    def get_user_list_by_user_list_id(self, user_list_id: int) -> UserList:
        user_list = self.db.query(UserList).filter(
            UserList.user_list_id == user_list_id
        ).first()
        return user_list

    def get_user_lists_by_shop_list_id(self, shop_list_id: int) -> List[UserList]:
        user_lists = self.db.query(UserList).filter(
            UserList.shop_list_id == shop_list_id
        ).all()
        return user_lists

    def update_user_list(self, user_list: UserList) -> UserList:
        self.db.query(UserList).filter(
            UserList.user_list_id == user_list.user_list_id
        ).\
            update(
                {
                    "is_adm" : user_list.is_adm,
                    "is_nutritionist" : user_list.is_nutritionist
                }
            )
        self.db.commit()
        return self.get_user_list_by_user_list_id(user_list.user_list_id)

    def delete_user_list(self, user_list_id: int) -> UserList:
        deleted_user_list = self.get_user_list_by_user_list_id(user_list_id)

        self.db.query(UserList).filter(UserList.user_list_id == user_list_id).\
            delete()
       
        self.db.commit()
        return deleted_user_list
