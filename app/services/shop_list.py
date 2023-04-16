import abc
from pydantic import parse_obj_as
from fastapi import HTTPException

from dal.shop_list import ABCShopListDal
from dal.user import ABCUserDal
from dal.friendship import ABCFriendshipDal
from dal.item import ABCItemDal
from dal.user_list import ABCUserListDal
from dal.recipe_list import ABCRecipeListDal
from dal.recipe import ABCRecipeDal

from dto.shop_list import ShopList, ShopListCreate, ShopListSummary, ShopListEdit
from dto.shop_list import UserList, UserListCreate
from dto.shop_list import Item, ItemCreate
from dto.recipe import RecipeSummary, Recipe

from dto_converter.recipe import construct_recipe_summary_dto, construct_recipe_dto

from models.shop_list import ShopList as ShopListModel
from models.user_list import UserList as UserListModel
from models.item import Item as ItemModel
from models.recipe import RecipeList as RecipeListModel

from services.user_based_service import UserBasedService


from typing import List


class ABCShopListService(UserBasedService):
    def __init__(self, user_dal: ABCUserDal):
        super().__init__(user_dal)

    @abc.abstractmethod
    def get_shop_lists(self, token: str, return_templates: bool) -> List[ShopListSummary]:
        """Returns shop lists from user"""

    @abc.abstractmethod
    def get_shop_list_by_id(self, shop_list_id) -> ShopList:
        """Return the shop list with given id"""

    @abc.abstractmethod
    def create_shop_list(self, shop_list: ShopListCreate, token: str) -> ShopList:
        """Create a shop list"""

    @abc.abstractmethod
    def add_users_to_list(
        self, shop_list_id: int, new_user_lists: List[UserListCreate], token: str
    ) -> List[UserList]:
        """Adds users to list"""

    @abc.abstractmethod
    def add_item_to_list(
        self, shop_list_id: int, item: ItemCreate, token: str
    ) -> ShopList:
        """Adds item to list and return the resulting list"""

    @abc.abstractmethod
    def add_recipe_to_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> RecipeSummary:
        """Adds a recipe to a list and return the summary of the recipe"""

    @abc.abstractmethod
    def remove_recipe_from_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> RecipeSummary:
        """Removes a recipe from a list and return the summary of the recipe"""

    @abc.abstractmethod
    def rename_list(self, shop_list_id: int, new_name: str, token: str) -> ShopList:
        """Renames list"""

    @abc.abstractmethod
    def delete_list(self, shop_list_id: int, token: str) -> ShopListSummary:
        """Deletes list"""

    @abc.abstractmethod
    def get_recipes_from_list(self, shop_list_id: int, token: str) -> List[RecipeSummary]:
        """Returns all recipes from list"""

    @abc.abstractmethod
    def get_recipe_from_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> Recipe:
        """Returns specific recipe from list"""


class ShopListService(ABCShopListService):
    def __init__(
        self,
        shop_list_dal: ABCShopListDal,
        friendship_dal: ABCFriendshipDal,
        item_dal: ABCItemDal,
        user_dal: ABCUserDal,
        user_list_dal: ABCUserListDal,
        recipe_list_dal: ABCRecipeListDal,
        recipe_dal: ABCRecipeDal,
    ):
        super().__init__(user_dal)
        self.friendship_dal = friendship_dal
        self.item_dal = item_dal
        self.user_list_dal = user_list_dal
        self.recipe_list_dal = recipe_list_dal
        self.recipe_dal = recipe_dal
        self.dal = shop_list_dal

    def construct_user_list_dto(self, user_list: UserListModel) -> UserList:
        user = self.user_dal.get_user_by_id(user_list.user_id)
        user_list_dto = UserList(
            user_id=user.user_id,
            username=user.username,
            is_adm=user_list.is_adm,
            is_nutritionist=user_list.is_nutritionist,
            user_list_id=user_list.user_list_id,
        )
        return user_list_dto

    def construct_shop_list_summary_dto(
        self, shop_list: ShopListModel
    ) -> ShopListSummary:
        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(
            shop_list.shop_list_id
        )
        user_lists_dto = [
            self.construct_user_list_dto(user_list) for user_list in user_lists
        ]

        shop_list_summary = ShopListSummary(
            shop_list_id=shop_list.shop_list_id,
            name=shop_list.name,
            user_lists=user_lists_dto,
        )

        return shop_list_summary

    def construct_shop_list_dto(self, shop_list: ShopListModel) -> ShopList:
        shop_list_summary = self.construct_shop_list_summary_dto(shop_list)

        items = self.item_dal.get_items_from_list(shop_list.shop_list_id)

        items_dto = [
            Item(
                item_id=item.item_id,
                name=item.name,
                quantity=item.quantity,
                was_bought=item.was_bought,
            )
            for item in items
        ]

        shop_list_dto = ShopList(
            shop_list_id=shop_list.shop_list_id,
            name=shop_list_summary.name,
            user_lists=shop_list_summary.user_lists,
            items=items_dto,
        )

        return shop_list_dto

    def check_user_list_validity(self, user_id: int, shop_list_id: int) -> UserListModel:
        user_list = self.user_list_dal.get_user_list_by_user_id(shop_list_id, user_id)
        if user_list is None:
            self.raise_access_denied_error()
        return user_list

    def check_user_list_adm_validity(
        self, user_id: int, shop_list_id: int
    ) -> UserListModel:
        user_list = self.check_user_list_validity(user_id, shop_list_id)
        if not user_list.is_adm:
            self.raise_access_denied_error()
        return user_list

    def get_shop_lists(self, token: str, return_templates: bool) -> List[ShopListSummary]:
        user = self.check_user_validity(token)
        shop_lists = self.dal.get_shop_lists_from_user(user.user_id)
        filtered_shop_lists = [
            shop_list
            for shop_list in shop_lists
            if shop_list.is_template == return_templates
        ]
        shop_lists_dto = [
            self.construct_shop_list_summary_dto(shop_list)
            for shop_list in filtered_shop_lists
        ]
        return shop_lists_dto

    def get_shop_list_by_id(self, shop_list_id: int, token: str) -> ShopList:
        user = self.check_user_validity(token)

        shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list_id)

        user_list = self.check_user_list_validity(user.user_id, shop_list_id)
        if (not user_list.is_adm) and (user_list.is_nutritionist):
            self.raise_access_denied_error()

        items = self.item_dal.get_items_from_list(shop_list_id)
        items_dto = parse_obj_as(List[Item], items)
        shop_list_dto = ShopList(
            shop_list_id=shop_list_id,
            name=shop_list.name,
            user_lists=[
                self.construct_user_list_dto(user_list) for user_list in user_lists
            ],
            items=items_dto,
        )

        return shop_list_dto

    def create_shop_list(self, shop_list: ShopListCreate, token: str) -> ShopList:
        user = self.check_user_validity(token)

        db_shop_list = ShopListModel(
            name=shop_list.name,
            is_template=shop_list.is_template,
        )
        invited_user_ids = [id for id in shop_list.user_ids if id != user.user_id]
        # remove duplicates
        invited_user_ids = list(dict.fromkeys(invited_user_ids))

        for invited_user_id in invited_user_ids:
            friendship = self.friendship_dal.get_friendship_from_user_pair(
                user.user_id, invited_user_id
            )
            if friendship is None:
                raise HTTPException(status_code=400, detail="Friendship necessary")

        created_shop_list = self.dal.create_shop_list(shop_list=db_shop_list)

        shop_list_id = created_shop_list.shop_list_id
        for user_id in invited_user_ids:
            user_list_db = UserListModel(user_id=user_id, shop_list_id=shop_list_id)
            self.user_list_dal.create_user_list(user_list_db)

        user_list_db = UserListModel(
            user_id=user.user_id, shop_list_id=shop_list_id, is_adm=True
        )
        self.user_list_dal.create_user_list(user_list_db)

        created_shop_list_dto = self.construct_shop_list_summary_dto(created_shop_list)
        return created_shop_list_dto

    def add_users_to_list(
        self, shop_list_id: int, new_user_lists: List[UserListCreate], token: str
    ) -> List[UserList]:
        user = self.check_user_validity(token)
        self.check_user_list_adm_validity(user.user_id, shop_list_id)
        current_user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(
            shop_list_id
        )
        current_user_list_ids = [u.user_id for u in current_user_lists]

        there_is_nutritionist_in_list = False
        for ul in current_user_lists:
            if ul.is_nutritionist:
                there_is_nutritionist_in_list = True
                break

        for ul in new_user_lists:
            if ul.is_nutritionist:
                if there_is_nutritionist_in_list:
                    raise HTTPException(
                        status_code=400,
                        detail="The list will get more than one nutritionist.",
                    )
                there_is_nutritionist_in_list = True

        for user_list in new_user_lists:
            if not self.friendship_dal.get_friendship_from_user_pair(
                user.user_id, user_list.user_id
            ):
                continue
            if user_list.user_id in current_user_list_ids:
                continue
            user_list_db = UserListModel(
                user_id=user_list.user_id,
                shop_list_id=shop_list_id,
                is_nutritionist=user_list.is_nutritionist,
            )
            self.user_list_dal.create_user_list(user_list_db)

        user_lists = self.user_list_dal.get_user_lists_by_shop_list_id(shop_list_id)

        user_lists_dto = [
            self.construct_user_list_dto(user_list) for user_list in user_lists
        ]

        return user_lists_dto

    def add_item_to_list(
        self, shop_list_id: int, item: ItemCreate, token: str
    ) -> ShopList:
        user = self.check_user_validity(token)
        user_list = self.check_user_list_validity(user.user_id, shop_list_id)
        if user_list.is_nutritionist:
            self.raise_access_denied_error()
        item_db = ItemModel(
            shop_list_id=shop_list_id, name=item.name, quantity=item.quantity
        )
        self.item_dal.create_item(item_db)

        return self.get_shop_list_by_id(shop_list_id, token)

    def rename_list(
        self, shop_list_id: int, shop_list_data: ShopListEdit, token: str
    ) -> ShopListSummary:
        user = self.check_user_validity(token)
        shop_list = self.dal.get_shop_list_by_id(shop_list_id)

        if shop_list is None:
            raise HTTPException(status_code=404, detail="ShopList doesn't exist")

        self.check_user_list_validity(user.user_id, shop_list_id)

        shop_list.name = shop_list_data.name
        shop_list = self.dal.update_list(shop_list)

        return self.construct_shop_list_summary_dto(shop_list)

    def delete_list(self, shop_list_id: int, token: str) -> ShopListSummary:
        user = self.check_user_validity(token)
        shop_list = self.dal.get_shop_list_by_id(shop_list_id)
        if shop_list is None:
            raise HTTPException(status_code=404, detail="ShopList doesn't exist")

        self.check_user_list_adm_validity(user.user_id, shop_list_id)
        self.dal.delete_shop_list(shop_list.shop_list_id)
        return self.construct_shop_list_summary_dto(shop_list)

    def get_recipes_from_list(self, shop_list_id: int, token: str) -> List[RecipeSummary]:
        user = self.check_user_validity(token)
        self.check_user_list_validity(user.user_id, shop_list_id)
        recipe_lists = self.recipe_list_dal.get_recipe_lists_by_shop_list_id(shop_list_id)
        recipe_ids = [r.recipe_id for r in recipe_lists]
        recipes = [
            self.recipe_dal.get_recipe_by_id(recipe_id) for recipe_id in recipe_ids
        ]
        recipes_dto = [construct_recipe_summary_dto(recipe, user) for recipe in recipes]
        return recipes_dto

    def get_recipe_from_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> Recipe:
        user = self.check_user_validity(token)
        self.check_user_list_validity(user.user_id, shop_list_id)
        recipe = self.recipe_dal.get_recipe_by_id(recipe_id)
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe doesn't exist")
        recipe_list = self.recipe_list_dal.get_recipe_list_by_shop_list_id_and_recipe_id(
            shop_list_id, recipe_id
        )
        if recipe_list is None:
            self.raise_access_denied_error()
        recipe_dto = construct_recipe_dto(recipe, user)
        return recipe_dto

    def add_recipe_to_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> RecipeSummary:
        user = self.check_user_validity(token)
        user_list = self.check_user_list_validity(user.user_id, shop_list_id)
        if not user_list.is_nutritionist:
            self.raise_access_denied_error()
        recipe_list = self.recipe_list_dal.get_recipe_list_by_shop_list_id_and_recipe_id(
            shop_list_id, recipe_id
        )
        if recipe_list is not None:
            raise HTTPException(status_code=400, detail="Recipe already in list")
        recipe_list = RecipeListModel(
            shop_list_id=shop_list_id,
            recipe_id=recipe_id,
        )
        self.recipe_list_dal.create_recipe_list(recipe_list)
        recipe = self.recipe_dal.get_recipe_by_id(recipe_id)
        recipe_summary = construct_recipe_summary_dto(recipe, user)
        return recipe_summary

    def remove_recipe_from_list(
        self, shop_list_id: int, recipe_id: int, token: str
    ) -> RecipeSummary:
        user = self.check_user_validity(token)
        user_list = self.check_user_list_validity(user.user_id, shop_list_id)
        if not user_list.is_nutritionist:
            self.raise_access_denied_error()
        recipe_list = self.recipe_list_dal.get_recipe_list_by_shop_list_id_and_recipe_id(
            shop_list_id, recipe_id
        )
        if recipe_list is None:
            raise HTTPException(status_code=404, detail="Recipe not in list")
        self.recipe_list_dal.delete_recipe_list(recipe_list)
        recipe = self.recipe_dal.get_recipe_by_id(recipe_id)
        recipe_summary = construct_recipe_summary_dto(recipe, user)
        return recipe_summary
