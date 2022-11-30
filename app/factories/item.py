from fastapi import Depends

from app.dal.user import ABCUserDal
from app.dal.item import ABCItemDal
from app.dal.shop_list import ABCShopListDal
from app.dal.user_list import ABCUserListDal
from app.factories.dal_factories import get_user_dal, get_item_dal, get_shop_list_dal, get_user_list_dal
from app.services.item import ABCItemService, ItemService


def get_item_service(
    user_dal: ABCUserDal = Depends(get_user_dal),
    item_dal: ABCItemDal = Depends(get_item_dal),
    shop_list_dal: ABCShopListDal = Depends(get_shop_list_dal),
    user_list_dal: ABCUserListDal = Depends(get_user_list_dal),
) -> ABCItemService:
    client = ItemService(user_dal, item_dal, shop_list_dal, user_list_dal)
    try:
        yield client
    finally:
        pass