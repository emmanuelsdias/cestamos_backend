import abc
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.models.recipe import Recipe

from typing import List

class ABCRecipeDal():

    @abc.abstractmethod
    def get_all_recipes(self, limit: int = 100) -> List[Recipe]:
        """Gets all recipes in database"""

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        """Gets the recipe in database with the given id"""

    @abc.abstractmethod
    def create_recipe(self, recipe: Recipe) -> Recipe:
        """Creates a new recipe in database"""


class RecipeDal(ABCRecipeDal):

    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_all_recipes(self, limit: int = 100) -> List[Recipe]:
        return self.db.query(Recipe).limit(limit).all()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()

    def create_recipe(self, recipe: Recipe) -> Recipe:
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe