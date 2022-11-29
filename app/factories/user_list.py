from fastapi import Depends

from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal
from app.dal.user_list import ABCUserListDal
from app.factories.dal_factories import get_user_dal, get_shop_list_dal, get_user_list_dal
from app.services.user_list import ABCUserListService, UserListService


def get_user_list_service(
    shop_list_dal: ABCShopListDal = Depends(get_shop_list_dal),
    user_list_dal: ABCUserListDal = Depends(get_user_list_dal),
    user_dal: ABCUserDal = Depends(get_user_dal),
) -> ABCUserListService:
    client = UserListService(shop_list_dal, user_list_dal, user_dal)
    try:
        yield client
    finally:
        pass
