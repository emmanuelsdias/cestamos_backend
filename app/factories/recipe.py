from fastapi import Depends

from dal.recipe import ABCRecipeDal
from dal.user import ABCUserDal
from dal.friendship import ABCFriendshipDal
from factories.dal_factories import get_user_dal, get_recipe_dal, get_friendship_dal
from services.recipe import ABCRecipeService, RecipeService


def get_recipe_service(
    recipe_dal: ABCRecipeDal = Depends(get_recipe_dal),
    user_dal: ABCUserDal = Depends(get_user_dal),
    friendship_dal: ABCFriendshipDal = Depends(get_friendship_dal),
) -> ABCRecipeService:
    client = RecipeService(recipe_dal, user_dal, friendship_dal)
    try:
        yield client
    finally:
        pass
