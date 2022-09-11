from fastapi import Depends

from app.dal.recipe import ABCRecipeDal
from app.dal.user import ABCUserDal
from app.factories.dal_factories import get_user_dal, get_recipe_dal
from app.services.recipe import ABCRecipeService, RecipeService


def get_recipe_service(
    recipe_dal: ABCRecipeDal = Depends(get_recipe_dal),
    user_dal: ABCUserDal = Depends(get_user_dal)
) -> ABCRecipeService:
    client = RecipeService(recipe_dal, user_dal)
    try:
        yield client
    finally:
        pass