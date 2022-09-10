import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.models.user import User

from typing import List

class ABCUserDal():

    @abc.abstractmethod
    def get_all_users(self) -> List[User]:
        """Gets all users in database"""

    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """Gets the user in database with the given id"""

    @abc.abstractmethod
    def create_user(self, user: User) -> User:
        """Creates a new user in database"""


class UserDal(ABCUserDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user