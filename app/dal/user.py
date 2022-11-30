import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.user import User

from typing import List

class ABCUserDal():

    @abc.abstractmethod
    def get_users(self) -> List[User]:
        """Gets all users in database"""

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """Gets the user in database with the given id"""

    def get_user_by_token(self, token: str) -> User:
        """Gets the user in database with the given token"""

    def get_user_by_email(self, email: str) -> User:
        """Gets the user in database with the given email"""

    @abc.abstractmethod
    def create_user(self, user: User) -> User:
        """Creates a new user in database"""

    @abc.abstractmethod
    def update_user_auth(self, user: User) -> User:
        """Login user"""


class UserDal(ABCUserDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_token(self, token: str) -> User:
        return self.db.query(User).filter(User.token == token).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_auth(self, user: User) -> User:
        self.db.query(User).filter(
            User.user_id == user.user_id
        ).\
            update(
                {
                    "token" : user.token
                }
            )
        self.db.commit()
        return self.get_user_by_id(user.user_id)
    
    def update_user(self, user: User) -> User:
        self.db.query(User).filter(
            User.user_id == user.user_id
        ).\
            update(
                {
                    "username" : user.username,
                    "hashed_password" : user.password
                }
            )
        self.db.commit()
        return self.get_user_by_id(user.user_id)

    def delete_user(self, user_id: int) -> User:
        deleted_user = self.get_user_by_id(user_id)

        self.db.query(User).filter(User.user_id == user_id).\
            delete()
       
        self.db.commit()
        return deleted_user