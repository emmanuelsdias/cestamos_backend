from fastapi import APIRouter
from fastapi import Depends

from services.shop_list import ABCShopListService
from factories.shop_list import get_shop_list_service

from dto.shop_list import ShopList, ShopListCreate, ShopListSummary, ShopListEdit
from dto.shop_list import UserList, UserListCreate
from dto.shop_list import ItemCreate
from dto.recipe import RecipeSummary, Recipe
from typing import List


router = APIRouter()


@router.get("/", response_model=List[ShopListSummary])
async def get_shop_lists(
    token: str = None,
    return_templates: bool = False,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.get_shop_lists(token, return_templates)


@router.post("/", response_model=ShopListSummary)
async def create_shop_list(
    shop_list: ShopListCreate,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.create_shop_list(shop_list, token)


@router.get("/{shop_list_id}", response_model=ShopList)
async def get_shop_list_by_id(
    shop_list_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.get_shop_list_by_id(shop_list_id, token)


@router.put("/{shop_list_id}", response_model=ShopListSummary)
async def rename_list(
    shop_list_id: int,
    shop_list_data: ShopListEdit,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.rename_list(shop_list_id, shop_list_data, token)


@router.delete("/{shop_list_id}")
async def delete_list(
    shop_list_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.delete_list(shop_list_id, token)


@router.post("/{shop_list_id}/user", response_model=List[UserList])
async def add_users_to_list(
    shop_list_id: int,
    user_lists: List[UserListCreate],
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.add_users_to_list(shop_list_id, user_lists, token)


@router.post("/{shop_list_id}/item", response_model=ShopList)
async def add_items_to_list(
    shop_list_id: int,
    items: List[ItemCreate],
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.add_items_to_list(shop_list_id, items, token)


@router.get("/{shop_list_id}/recipe", response_model=List[RecipeSummary])
async def get_recipes_from_list(
    shop_list_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.get_recipes_from_list(shop_list_id, token)


@router.get("/{shop_list_id}/recipe/{recipe_id}", response_model=Recipe)
async def get_recipe_from_list(
    shop_list_id: int,
    recipe_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.get_recipe_from_list(shop_list_id, recipe_id, token)


@router.post("/{shop_list_id}/recipe/{recipe_id}", response_model=RecipeSummary)
async def add_recipe_to_list(
    shop_list_id: int,
    recipe_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.add_recipe_to_list(shop_list_id, recipe_id, token)


@router.delete("/{shop_list_id}/recipe/{recipe_id}", response_model=RecipeSummary)
async def remove_recipe_from_list(
    shop_list_id: int,
    recipe_id: int,
    token: str = None,
    shop_list_service: ABCShopListService = Depends(get_shop_list_service),
):
    return shop_list_service.remove_recipe_from_list(shop_list_id, recipe_id, token)
