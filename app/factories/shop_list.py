from fastapi import Depends

from app.dal.shop_list import ABCShopListDal
from app.dal.user import ABCUserDal
from app.dal.friendship import ABCFriendshipDal
from app.dal.item import ABCItemDal
from app.factories.dal_factories import get_user_dal, get_shop_list_dal, get_friendship_dal, get_item_dal
from app.services.shop_list import ABCShopListService, ShopListService


def get_shop_list_service(
    shop_list_dal: ABCShopListDal = Depends(get_shop_list_dal),
    friendship_dal: ABCFriendshipDal = Depends(get_friendship_dal),
    item_dal: ABCItemDal = Depends(get_item_dal),
    user_dal: ABCUserDal = Depends(get_user_dal),
) -> ABCShopListService:
    client = ShopListService(shop_list_dal, friendship_dal, item_dal, user_dal)
    try:
        yield client
    finally:
        pass