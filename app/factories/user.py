from fastapi import Depends

from dal.user import ABCUserDal
from factories.dal_factories import get_user_dal
from services.user import ABCUserService, UserService


def get_user_service(user_dal: ABCUserDal = Depends(get_user_dal)) -> ABCUserService:
    client = UserService(user_dal)
    try:
        yield client
    finally:
        pass
