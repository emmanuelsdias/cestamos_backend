import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update, or_

from app.models.friendship import Friendship

from typing import List

class ABCFriendshipDal():

    @abc.abstractmethod
    def get_friendships(self) -> List[Friendship]:
        """Gets all friendships in database"""

    @abc.abstractmethod
    def get_friendships_from_user(self, user_id) -> List[Friendship]:
        """Gets all friendships in database from a user """

    @abc.abstractmethod
    def get_friendship_by_id(self, friendship_id) -> Friendship:
        """Get frienship with given id"""

    @abc.abstractmethod
    def create_friendship(self, friendship: Friendship) -> Friendship:
        """Creates friendship in database"""

    @abc.abstractmethod
    def delete_friendship(self, friendship_id: int) -> Friendship:
        """ Deletes a friendship in database """


class FriendshipDal(ABCFriendshipDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session


    def get_friendships(self) -> List[Friendship]:
        return self.db.query(Friendship).all()


    def get_friendships_from_user(self, user_id) -> List[Friendship]:
        return self.db.query(Friendship).filter(or_(
            Friendship.user_id1 == user_id,
            Friendship.user_id2 == user_id
            )).all()


    def get_friendship_by_id(self, friendship_id) -> Friendship:
        return self.db.query(Friendship).filter(Friendship.friendship_id == friendship_id).first()


    def create_friendship(self, friendship: Friendship) -> Friendship:
        self.db.add(friendship)
        self.db.commit()
        self.db.refresh(friendship)
        return friendship


    def delete_friendship(self, friendship_id: int) -> Friendship:
        deleted_friendship = self.get_friendship_by_id(friendship_id)

        self.db.query(Friendship).filter(Friendship.friendship_id == friendship_id).\
            delete()
       
        self.db.commit()
        return deleted_friendship