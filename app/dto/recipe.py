from typing import List
from pydantic import BaseModel

class RecipeCreate(BaseModel):
    name: str
    ingredients: str
    instructions: str


class Recipe(RecipeCreate):
    recipe_id: int

    class Config:
        orm_mode = True

class RecipeSummary(BaseModel):
    recipe_id: int
    name: str

    class Config:
        orm_mode = True