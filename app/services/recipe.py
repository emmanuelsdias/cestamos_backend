import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from dal.recipe import ABCRecipeDal
from dal.user import ABCUserDal
from dal.friendship import ABCFriendshipDal

from dto.recipe import Recipe, RecipeCreate, RecipeSummary

from models.recipe import Recipe as RecipeModel
from models.user import User as UserModel

from services.user_based_service import UserBasedService


from typing import List


class ABCRecipeService(UserBasedService):
    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_recipes(self, token: str, get_feed: bool) -> List[RecipeSummary]:
        """Returns recipes from user"""

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id) -> Recipe:
        """Return the recipe with given id"""

    @abc.abstractmethod
    def create_recipe(self, recipe: RecipeCreate, token: str) -> Recipe:
        """Create a recipe"""

    @abc.abstractmethod
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate, token: str) -> Recipe:
        """Edit a recipe"""

    @abc.abstractmethod
    def delete_recipe(self, recipe_id: int, token: str) -> Recipe:
        """Delete a recipe"""


class RecipeService(ABCRecipeService):
    def __init__(
        self,
        recipe_dal: ABCRecipeDal,
        user_dal: ABCUserDal,
        friendship_dal: ABCFriendshipDal,
    ):
        super().__init__(user_dal)
        self.dal = recipe_dal
        self.friendship_dal = friendship_dal

    def construct_recipe_dto(self, recipe: RecipeModel) -> Recipe:
        author = self.user_dal.get_user_by_id(recipe.user_id)
        recipe_dto = Recipe(
            recipe_id=recipe.recipe_id,
            author_user_id=author.user_id,
            author_user_name=author.username,
            name=recipe.name,
            description=recipe.description,
            ingredients=recipe.ingredients,
            people_served=recipe.people_served,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            cooking_time=recipe.cooking_time,
            resting_time=recipe.resting_time,
            is_public=recipe.is_public,
        )
        return recipe_dto

    def construct_recipe_summary_dto(self, recipe: RecipeModel) -> RecipeSummary:
        author = self.user_dal.get_user_by_id(recipe.user_id)
        recipe_summary_dto = RecipeSummary(
            recipe_id=recipe.recipe_id,
            name=recipe.name,
            description=recipe.description,
            prep_time=recipe.prep_time,
            cooking_time=recipe.cooking_time,
            resting_time=recipe.resting_time,
            author_user_id=author.user_id,
            author_user_name=author.username,
        )
        return recipe_summary_dto

    def get_recipes(self, token: str, get_feed: bool) -> List[RecipeSummary]:
        user = self.check_user_validity(token)
        recipes = []
        if not get_feed:
            recipes = self.dal.get_recipes_from_user(user.user_id)
        else:
            friendships = self.friendship_dal.get_friendships_from_user(user.user_id)
            friends_ids = []
            for friendship in friendships:
                if friendship.user_id1 == user.user_id:
                    friends_ids.append(friendship.user_id2)
                else:
                    friends_ids.append(friendship.user_id1)

            for friend_id in friends_ids:
                recipes += self.dal.get_recipes_from_user(friend_id)
            # filter out private recipes
            recipes = [recipe for recipe in recipes if recipe.is_public]
        recipes_dtos = [self.construct_recipe_summary_dto(recipe) for recipe in recipes]
        return recipes_dtos

    def get_recipe_by_id(self, recipe_id: int, token: str) -> Recipe:
        user = self.check_user_validity(token)
        recipe = self.dal.get_recipe_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        if user.user_id != recipe.user_id:
            if not recipe.is_public:
                self.raise_access_denied_error()
            friendship = self.friendship_dal.get_friendship_from_user_pair(
                user.user_id, recipe.user_id
            )
            if not friendship:
                self.raise_access_denied_error()
        return self.construct_recipe_dto(recipe)

    def create_recipe(self, recipe: RecipeCreate, token: str) -> Recipe:
        user = self.check_user_validity(token)

        db_recipe = RecipeModel(
            user_id=user.user_id,
            name=recipe.name,
            description=recipe.description,
            ingredients=recipe.ingredients,
            people_served=recipe.people_served,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            cooking_time=recipe.cooking_time,
            resting_time=recipe.resting_time,
            is_public=recipe.is_public,
        )

        created_recipe = self.dal.create_recipe(recipe=db_recipe)
        return self.construct_recipe_dto(created_recipe)

    def update_recipe(self, recipe_id: int, recipe: RecipeCreate, token: str) -> Recipe:
        user = self.check_user_validity(token)
        current_recipe = self.dal.get_recipe_by_id(recipe_id)
        if current_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe doesn't exist")
        if user.user_id != current_recipe.user_id:
            self.raise_access_denied_error()
        db_recipe = RecipeModel(
            recipe_id=recipe_id,
            name=recipe.name,
            description=recipe.description,
            ingredients=recipe.ingredients,
            people_served=recipe.people_served,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            cooking_time=recipe.cooking_time,
            resting_time=recipe.resting_time,
            is_public=recipe.is_public,
        )
        saved_recipe = self.dal.update_recipe(db_recipe)
        return self.construct_recipe_dto(saved_recipe)

    def delete_recipe(self, recipe_id: int, token: str) -> Recipe:
        user = self.check_user_validity(token)
        current_recipe = self.dal.get_recipe_by_id(recipe_id)
        if current_recipe is None:
            raise HTTPException(status_code=400, detail="Recipe doesn't exist")
        if user.user_id != current_recipe.user_id:
            self.raise_access_denied_error()
        deleted_recipe = self.dal.delete_recipe(recipe_id)
        return self.construct_recipe_dto(deleted_recipe)
