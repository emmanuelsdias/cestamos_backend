from models.recipe import Recipe as RecipeModel
from models.recipe import RecipeList as RecipeListModel
from models.user import User

from dto.recipe import Recipe, RecipeSummary


def construct_recipe_summary_dto(recipe: RecipeModel, user: User) -> RecipeSummary:
    return RecipeSummary(
        recipe_id=recipe.recipe_id,
        name=recipe.name,
        description=recipe.description,
        prep_time=recipe.prep_time,
        cooking_time=recipe.cooking_time,
        resting_time=recipe.resting_time,
        author_user_id=user.user_id,
        author_user_name=user.username,
    )


def construct_recipe_dto(recipe: RecipeModel, user: User) -> Recipe:
    return Recipe(
        recipe_id=recipe.recipe_id,
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        people_served=recipe.people_served,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cooking_time=recipe.cooking_time,
        resting_time=recipe.resting_time,
        is_public=recipe.is_public,
        author_user_id=user.user_id,
        author_user_name=user.username,
    )
