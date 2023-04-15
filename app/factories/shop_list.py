from fastapi import Depends

from dal.shop_list import ABCShopListDal
from dal.user import ABCUserDal
from dal.friendship import ABCFriendshipDal
from dal.item import ABCItemDal
from dal.user_list import ABCUserListDal
from dal.recipe_list import ABCRecipeListDal
from dal.recipe import ABCRecipeDal
from factories.dal_factories import (
    get_user_dal,
    get_shop_list_dal,
    get_friendship_dal,
    get_item_dal,
    get_user_list_dal,
    get_user_list_dal,
    get_recipe_list_dal,
    get_recipe_dal,
)
from services.shop_list import ABCShopListService, ShopListService


def get_shop_list_service(
    shop_list_dal: ABCShopListDal = Depends(get_shop_list_dal),
    friendship_dal: ABCFriendshipDal = Depends(get_friendship_dal),
    item_dal: ABCItemDal = Depends(get_item_dal),
    user_dal: ABCUserDal = Depends(get_user_dal),
    user_list_dal: ABCUserListDal = Depends(get_user_list_dal),
    recipe_list_dal: ABCRecipeListDal = Depends(get_recipe_list_dal),
    recipe_dal: ABCRecipeDal = Depends(get_recipe_dal),
) -> ABCShopListService:
    client = ShopListService(
        shop_list_dal, friendship_dal, item_dal, user_dal, user_list_dal, recipe_list_dal, recipe_dal
    )
    try:
        yield client
    finally:
        pass
