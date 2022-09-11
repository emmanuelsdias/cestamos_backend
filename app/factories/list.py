from fastapi import Depends

from app.dal.list import ABCListDal
from app.dal.user import ABCUserDal
from app.factories.dal_factories import get_user_dal, get_list_dal
from app.services.list import ABCListService, ListService


def get_list_service(
    list_dal: ABCListDal = Depends(get_list_dal),
    user_dal: ABCUserDal = Depends(get_user_dal)
) -> ABCListService:
    client = ListService(list_dal, user_dal)
    try:
        yield client
    finally:
        pass