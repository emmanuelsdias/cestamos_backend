from fastapi import Depends
from sqlalchemy.orm import Session

from app.dal.recipe import RecipeDal, ABCRecipeDal

from app.factories.config import get_settings
from app.factories.db_session import get_db

from app.services.recipe import ABCRecipeService, RecipeService
from app.utils.settings import Settings


def get_recipe_dal(
    db: Session = Depends(get_db)
) -> ABCRecipeDal:
    dal = RecipeDal(db)
    try:
        yield dal
    finally:
        pass


def get_recipe_service(
    recipe_dal: ABCRecipeDal = Depends(get_recipe_dal)
) -> ABCRecipeService:
    client = RecipeService(recipe_dal)
    try:
        yield client
    finally:
        pass