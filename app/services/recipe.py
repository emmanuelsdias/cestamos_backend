from fastapi import HTTPException
import abc
from pydantic import parse_obj_as

from app.dal.recipe import ABCRecipeDal
from app.dto.recipe import Recipe, RecipeCreate, RecipeSummary

from app.models.recipe import Recipe as RecipeModel

from app.utils.settings import Settings

from typing import List

class ABCRecipeService():
    @abc.abstractmethod
    def get_all_recipes(self) -> List[Recipe]:
        """ Returns all recipes """
    
    @abc.abstractmethod
    def create_recipe(self, recipe) -> Recipe:
        """ Create a recipe """

    def get_recipe_by_id(self, recipe_id) -> Recipe:
        """ Return the recipe with given id """


class RecipeService(ABCRecipeService):

    def __init__(
        self,
        recipe_dal: ABCRecipeDal,
    ):
        self.dal = recipe_dal

    def get_all_recipes(self, limit: int = 100) -> List[RecipeSummary]:
        return parse_obj_as(List[RecipeSummary], self.dal.get_all_recipes(limit))

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return parse_obj_as(Recipe, self.dal.get_recipe_by_id(recipe_id))

    def create_recipe(self, recipe: RecipeCreate) -> Recipe:
        db_recipe = RecipeModel(
            user_id=1, # TODO: get user_id from auth token.
            ingredients=hashed_password,
            instructions=recipe.recipename,
        )
        created_recipe = self.dal.create_recipe(recipe=db_recipe)
        return Recipe.from_orm(created_recipe)