from fastapi import Depends
from sqlalchemy.orm import Session

from app.dal.user import UserDal, ABCUserDal

from app.factories.config import get_settings
from app.factories.db_session import get_db

from app.services.user import ABCUserService, UserService
from app.utils.settings import Settings


def get_user_dal(
    db: Session = Depends(get_db)
) -> ABCUserDal:
    dal = UserDal(db)
    try:
        yield dal
    finally:
        pass


def get_user_service(
    user_dal: ABCUserDal = Depends(get_user_dal)
) -> ABCUserService:
    client = UserService(user_dal)
    try:
        yield client
    finally:
        pass