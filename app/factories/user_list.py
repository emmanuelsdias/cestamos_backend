from fastapi import Depends

from dal.shop_list import ABCShopListDal
from dal.user import ABCUserDal
from dal.user_list import ABCUserListDal
from factories.dal_factories import get_user_dal, get_shop_list_dal, get_user_list_dal
from services.user_list import ABCUserListService, UserListService


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
