from fastapi import Depends

from app.dal.user import ABCUserDal
from app.factories.dal_factories import get_user_dal
from app.services.user import ABCUserService, UserService


def get_user_service(
    user_dal: ABCUserDal = Depends(get_user_dal)
) -> ABCUserService:
    client = UserService(user_dal)
    try:
        yield client
    finally:
        pass