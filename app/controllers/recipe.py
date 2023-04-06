from fastapi import APIRouter
from fastapi import Depends

from services.recipe import ABCRecipeService
from factories.recipe import get_recipe_service

from dto.recipe import Recipe, RecipeCreate, RecipeSummary
from typing import List


router = APIRouter()


@router.get("/", response_model=List[RecipeSummary])
async def get_recipes(
    token: str = None, recipe_service: ABCRecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_recipes(token)


@router.post("/", response_model=Recipe)
async def create_recipe(
    recipe: RecipeCreate,
    token: str = None,
    recipe_service: ABCRecipeService = Depends(get_recipe_service),
):
    return recipe_service.create_recipe(recipe, token)


@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe_by_id(
    recipe_id: int,
    token: str = None,
    recipe_service: ABCRecipeService = Depends(get_recipe_service),
):
    return recipe_service.get_recipe_by_id(recipe_id, token)


@router.put("/{recipe_id}", response_model=Recipe)
async def edit_recipe(
    recipe_id: int,
    recipe: RecipeCreate,
    token: str = None,
    recipe_service: ABCRecipeService = Depends(get_recipe_service),
):
    return recipe_service.update_recipe(recipe_id, recipe, token)


@router.delete("/{recipe_id}", response_model=Recipe)
async def delete_recipe(
    recipe_id: int,
    token: str = None,
    recipe_service: ABCRecipeService = Depends(get_recipe_service),
):
    return recipe_service.delete_recipe(recipe_id, token)
