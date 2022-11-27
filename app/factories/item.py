from fastapi import Depends

from app.dal.user import ABCUserDal
from app.dal.item import ABCItemDal
from app.dal.shop_list import ABCShopListDal
from app.factories.dal_factories import get_user_dal, get_item_dal, get_shop_list_dal
from app.services.item import ABCItemService, ItemService


def get_item_service(
    user_dal: ABCUserDal = Depends(get_user_dal),
    item_dal: ABCItemDal = Depends(get_item_dal),
    shop_list_dal: ABCShopListDal = Depends(get_shop_list_dal),
) -> ABCItemService:
    client = ItemService(user_dal, item_dal, shop_list_dal)
    try:
        yield client
    finally:
        pass