import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy import update

from models.recipe import Recipe

from typing import List


class ABCRecipeDal:
    @abc.abstractmethod
    def get_recipes(self) -> List[Recipe]:
        """Gets all recipes in database"""

    @abc.abstractmethod
    def get_recipes_from_user(self, user_id) -> List[Recipe]:
        """Gets all recipes in database from a user"""

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        """Gets the recipe in database with the given id"""

    @abc.abstractmethod
    def create_recipe(self, recipe: Recipe) -> Recipe:
        """Creates a new recipe in database"""

    @abc.abstractmethod
    def update_recipe(self, recipe: Recipe) -> Recipe:
        """Updates recipe in database"""

    @abc.abstractmethod
    def delete_recipe(self, recipe_id: int) -> Recipe:
        """Deletes a recipe in database"""


class RecipeDal(ABCRecipeDal):
    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_recipes(self) -> List[Recipe]:
        return self.db.query(Recipe).all()

    def get_recipes_from_user(self, user_id) -> List[Recipe]:
        return self.db.query(Recipe).filter(Recipe.user_id == user_id).all()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()

    def create_recipe(self, recipe: Recipe) -> Recipe:
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def update_recipe(self, recipe: Recipe) -> Recipe:
        self.db.query(Recipe).filter(Recipe.recipe_id == recipe.recipe_id).update(
            {
                "name": recipe.name,
                "ingredients": recipe.ingredients,
                "instructions": recipe.instructions,
            }
        )

        self.db.commit()
        return self.get_recipe_by_id(recipe.recipe_id)

    def delete_recipe(self, recipe_id: int) -> Recipe:
        deleted_recipe = self.get_recipe_by_id(recipe_id)

        self.db.query(Recipe).filter(Recipe.recipe_id == recipe_id).delete()

        self.db.commit()
        return deleted_recipe
