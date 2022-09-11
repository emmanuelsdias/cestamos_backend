import abc
from pydantic import parse_obj_as

from app.dal.recipe import ABCRecipeDal
from app.dal.user import ABCUserDal

from app.dto.recipe import Recipe, RecipeCreate, RecipeSummary

from app.models.recipe import Recipe as RecipeModel
from app.models.user import User as UserModel

from app.services.user_based_service import UserBasedService


from typing import List

class ABCRecipeService(UserBasedService):

    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_recipes(self, token) -> List[RecipeSummary]:
        """ Returns recipes from user """
    
    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id) -> Recipe:
        """ Return the recipe with given id """

    @abc.abstractmethod
    def create_recipe(self, recipe: RecipeCreate, token: str) -> Recipe:
        """ Create a recipe """

    @abc.abstractmethod
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate, token: str) -> Recipe:
        """ Edit a recipe """

    @abc.abstractmethod
    def delete_recipe(self, recipe_id: int, token: str) -> Recipe:
        """ Delete a recipe """


class RecipeService(ABCRecipeService):

    def __init__(
        self,
        recipe_dal: ABCRecipeDal,
        user_dal: ABCUserDal,
    ):
        super().__init__(user_dal)
        self.dal = recipe_dal


    def get_recipes(self, token) -> List[RecipeSummary]:
        user = self.check_user_validity(token)
        recipes = self.dal.get_recipes_from_user(user.user_id)
        print(recipes)
        return parse_obj_as(List[RecipeSummary], recipes)

    def get_recipe_by_id(self, recipe_id: int, token: str) -> Recipe:
        user = self.check_user_validity(token)

        recipe = self.dal.get_recipe_by_id(recipe_id)
        if user.user_id != recipe.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        return parse_obj_as(Recipe, recipe)

    def create_recipe(self, recipe: RecipeCreate, token: str) -> Recipe:
        user = self.check_user_validity(token)
        
        db_recipe = RecipeModel(
            user_id=user.user_id,
            name = recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
        )
        created_recipe = self.dal.create_recipe(recipe=db_recipe)
        return Recipe.from_orm(created_recipe)
    
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate, token: str) -> Recipe:
        user = self.check_user_validity(token)
        current_recipe = self.dal.get_recipe_by_id(recipe_id)
        if current_recipe is None:
            raise HTTPException(
                status_code=400, detail="Recipe doesn't exist"
            )
        if user.user_id != current_recipe.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        db_recipe = RecipeModel(
            recipe_id=recipe_id,
            name = recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
        )
        saved_recipe = self.dal.update_recipe(db_recipe)
        return Recipe.from_orm(saved_recipe)

    def delete_recipe(self, recipe_id: int, token: str) -> Recipe:
        user = self.check_user_validity(token)
        current_recipe = self.dal.get_recipe_by_id(recipe_id)
        if current_recipe is None:
            raise HTTPException(
                status_code=400, detail="Recipe doesn't exist"
            )
        if user.user_id != current_recipe.user_id:
            raise HTTPException(
                status_code=403, detail="Access Denied"
            )
        deleted_recipe = self.dal.delete_recipe(recipe_id)
        return Recipe.from_orm(deleted_recipe)