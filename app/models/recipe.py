from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from dal.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    name = Column(String(50))
    description = Column(String)
    ingredients = Column(String)
    people_served = Column(Integer)
    instructions = Column(String)
    prep_time = Column(String(100))
    cooking_time = Column(String(100))
    resting_time = Column(String(100))
    is_public = Column(Boolean, default=False)


class RecipeList(Base):
    __tablename__ = "recipe_lists"

    recipe_list_id = Column(Integer, primary_key=True, index=True)

    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    shop_list_id = Column(Integer, ForeignKey("shop_lists.shop_list_id"))
