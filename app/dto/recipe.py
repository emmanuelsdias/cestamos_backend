from pydantic import BaseModel


class RecipeCreate(BaseModel):
    name: str
    description: str
    ingredients: str
    people_served: int
    instructions: str
    prep_time: str
    cooking_time: str
    resting_time: str
    is_public: bool


class Recipe(RecipeCreate):
    recipe_id: int
    author_user_id: int
    author_user_name: str

    class Config:
        orm_mode = True


class RecipeSummary(BaseModel):
    recipe_id: int
    name: str
    description: str
    prep_time: str
    cooking_time: str
    resting_time: str
    author_user_id: int
    author_user_name: str

    class Config:
        orm_mode = True
