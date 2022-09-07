from fastapi import APIRouter
from fastapi import Depends

from app.services.recipe import ABCRecipeService
from app.factories.recipe import get_recipe_service

from app.dto.recipe import Recipe, RecipeCreate, RecipeSummary
from typing import List


router = APIRouter()

@router.get("/", response_model=List[RecipeSummary])
async def get_all_recipes(
    recipe_service: ABCRecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_all_recipes()

@router.post("/", response_model=Recipe)
async def create_recipe(
    recipe: RecipeCreate,
    recipe_service: ABCRecipeService = Depends(get_recipe_service)
):
    return recipe_service.create_recipe(recipe)

@router.get("/:recipe_id", response_model=Recipe)
async def get_recipe_by_id(
    recipe_id: int,
    recipe_service: ABCRecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_recipe_by_id()


@router.put("/:recipe_id", response_model=Recipe)
async def get_recipe_by_id(
    recipe_id: int,
    recipe: RecipeCreate,
    recipe_service: ABCRecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_recipe_by_id()