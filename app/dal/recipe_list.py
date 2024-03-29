import abc
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.recipe import RecipeList

from typing import List


class ABCRecipeListDal:
    @abc.abstractmethod
    def get_recipe_list_by_id(self, recipe_list_id: int) -> RecipeList:
        """Gets recipe_list given id"""

    @abc.abstractmethod
    def create_recipe_list(self, recipe_list: RecipeList) -> RecipeList:
        """Adds recipe to list"""

    @abc.abstractmethod
    def get_recipe_lists_by_shop_list_id(self, shop_list_id: int) -> List[RecipeList]:
        """Gets all recipe_lists from list"""

    @abc.abstractmethod
    def get_recipe_list_by_shop_list_id_and_recipe_id(
        self, shop_list_id: int, recipe_id: int
    ) -> RecipeList:
        """Gets recipe_list from list and recipe ids"""

    @abc.abstractmethod
    def get_recipe_lists_by_shop_list_id(self, shop_list_id: int) -> List[RecipeList]:
        """Gets all recipe_lists from list"""

    @abc.abstractmethod
    def delete_recipe_list(self, recipe_list: RecipeList) -> RecipeList:
        """Delete recipe_list given id"""

    @abc.abstractmethod
    def delete_recipe_lists_by_shop_list_id(self, shop_list_id: int) -> None:
        """Delete recipe_lists given shop list id"""


class RecipeListDal(ABCRecipeListDal):
    def __init__(self, db_session: Session):
        self.db: Session = db_session

    def get_recipe_list_by_id(self, recipe_list_id: int) -> RecipeList:
        return (
            self.db.query(RecipeList)
            .filter(RecipeList.recipe_list_id == recipe_list_id)
            .first()
        )

    def create_recipe_list(self, recipe_list: RecipeList) -> RecipeList:
        self.db.add(recipe_list)
        self.db.commit()
        self.db.refresh(recipe_list)
        return recipe_list

    def get_recipe_list_by_shop_list_id_and_recipe_id(
        self, shop_list_id: int, recipe_id: int
    ) -> RecipeList:
        return (
            self.db.query(RecipeList)
            .filter(
                and_(
                    RecipeList.shop_list_id == shop_list_id,
                    RecipeList.recipe_id == recipe_id,
                )
            )
            .first()
        )

    def get_recipe_lists_by_shop_list_id(self, shop_list_id: int) -> List[RecipeList]:
        return (
            self.db.query(RecipeList)
            .filter(RecipeList.shop_list_id == shop_list_id)
            .all()
        )

    def delete_recipe_list(self, recipe_list: RecipeList) -> RecipeList:
        deleted_recipe_list = self.get_recipe_list_by_id(recipe_list.recipe_list_id)
        self.db.query(RecipeList).filter(
            RecipeList.recipe_list_id == recipe_list.recipe_list_id
        ).delete()
        self.db.commit()
        return deleted_recipe_list

    def delete_recipe_lists_by_shop_list_id(self, shop_list_id: int) -> None:
        self.db.query(RecipeList).filter(RecipeList.shop_list_id == shop_list_id).delete()
        self.db.commit()
